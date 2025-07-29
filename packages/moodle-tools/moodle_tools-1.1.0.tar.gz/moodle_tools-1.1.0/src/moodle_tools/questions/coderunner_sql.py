"""This module implements SQL questions in Moodle CodeRunner."""

import io
import json
import random
import re
import shutil
import string
import tempfile
from base64 import b64encode
from collections.abc import Generator, Iterable
from contextlib import contextmanager, redirect_stdout
from pathlib import Path

import duckdb
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger

from moodle_tools.questions.coderunner import CoderunnerQuestion, Testcase
from moodle_tools.utils import ParsingError, preprocess_text

DB_CONNECTION_ERROR = (
    "Question parsing requested a database connection but `database_connection` is False. In this "
    "case, you must provide a result for each test case since we cannot automatically fetch the "
    "result from the database."
)

JinjaEnv = Environment(
    loader=PackageLoader("moodle_tools.questions"),
    lstrip_blocks=True,
    trim_blocks=True,
    autoescape=select_autoescape(),
)


@contextmanager
def open_tmp_db_connection(path: str | Path) -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Open a connection to a temporary copy of a provided database.

    Args:
        path: Path to the database file.

    Yields:
        duckdb.DuckDBPyConnection: A connection to the database.
    """
    with tempfile.NamedTemporaryFile("wb") as tmp_db:
        shutil.copy2(path, tmp_db.name)
        con = duckdb.connect(tmp_db.name, config={"threads": 1})
        try:
            yield con
        finally:
            con.close()


class CoderunnerSQLQuestion(CoderunnerQuestion):
    """Template for a SQL question in Moodle CodeRunner."""

    ACE_LANG = "sql"
    MAX_ROWS = 50
    MAX_WIDTH = 500

    def __init__(
        self,
        *,
        question: str,
        title: str,
        answer: str,
        testcases: list[Testcase],
        database_path: str,
        category: str | None = None,
        grade: float = 1.0,
        general_feedback: str = "",
        answer_preload: str = "",
        all_or_nothing: bool = True,
        check_results: bool = False,
        parser: str | None = None,
        internal_copy: bool = False,
        database_connection: bool = True,
        **flags: bool,
    ) -> None:
        """Create a new SQL question.

        Args:
            question: The question text displayed to students.
            title: Title of the question.
            answer: The piece of code that, when executed, leads to the correct result.
            testcases: List of testcases for checking the student answer.
            database_path: Path to the DuckDB database (e.g., "./eshop.db").
            category: The category of the question.
            grade: The total number of points of the question.
            general_feedback: Feedback that is displayed once the quiz has closed.
            answer_preload: Text that is preloaded into the answer box.
            all_or_nothing: If True, the student must pass all test cases to receive any
                points. If False, the student gets partial credit for each test case passed.
            check_results: If testcase_results are provided, run the reference solution and check
                if the results match.
            parser: Code parser for formatting the correct answer and testcases.
            internal_copy: Flag to create an internal copy for debugging purposes.
            database_connection: If True, connect to the provided database to fetch the expected
                result. If False, use the provided result.
            flags: Additional flags that can be used to control the behavior of the
                question.
        """
        self.inmemory_db = database_path == ":memory:"

        if self.inmemory_db:
            self.database_path = Path(
                f"db-{''.join(random.choices(string.digits, k=12))}.db"  # noqa: S311
            ).absolute()
            duckdb.connect(self.database_path, config={"threads": 1}).close()

        else:
            self.database_path = Path(database_path).absolute()
            if not self.database_path.exists():
                raise FileNotFoundError(
                    f"Provided database path does not exist: {self.database_path}"
                )

        self.database_connection = database_connection

        answer = answer.strip()

        if answer[-1] != ";":
            raise ParsingError(
                f"SQL queries must end with a ';' symbol. But the last symbol was: {answer[-1]}"
            )

        super().__init__(
            question=question,
            title=title,
            answer=answer,
            testcases=testcases,
            category=category,
            grade=grade,
            general_feedback=general_feedback,
            answer_preload=answer_preload,
            all_or_nothing=all_or_nothing,
            check_results=check_results,
            parser=parser,
            internal_copy=internal_copy,
            **flags,
        )

    @property
    def files(self) -> list[dict[str, str]]:
        if self.inmemory_db:
            # If the database is in memory, we don't need to send it
            return []
        with self.database_path.open("rb") as file:
            files = {
                "name": self.database_path.name,
                "encoding": b64encode(file.read()).decode("utf-8"),
            }

        return [files]

    def cleanup(self) -> None:
        logger.debug("Cleaning up {}.", self.__class__.__name__)

        if self.inmemory_db:
            logger.debug("Removing temporary DB file.")
            self.database_path.unlink()


class CoderunnerDDLQuestion(CoderunnerSQLQuestion):
    """Template for a SQL DDL/DML question in Moodle CodeRunner."""

    CODERUNNER_TYPE = "python3"
    RESULT_COLUMNS_DEFAULT = """[["Testfall", "extra"], ["Bewertung", "awarded"]]"""
    RESULT_COLUMNS_DEBUG = (
        """[["Beschreibung", "extra"], """
        """["Test", "testcode"], ["Erhalten", "got"], """
        """["Erwartet", "expected"], ["Bewertung", "awarded"]]"""
    )
    TEST_TEMPLATE = "testlogic_ddl.py.j2"

    def __init__(
        self,
        *,
        question: str,
        title: str,
        answer: str,
        testcases: list[Testcase],
        database_path: str,
        category: str | None = None,
        grade: float = 1,
        general_feedback: str = "",
        answer_preload: str = "",
        all_or_nothing: bool = False,
        check_results: bool = False,
        parser: str | None = None,
        internal_copy: bool = False,
        database_connection: bool = True,
        **flags: bool,
    ) -> None:
        super().__init__(
            question=question,
            title=title,
            answer=answer,
            testcases=self.render_test_templates(testcases),
            database_path=database_path,
            category=category,
            grade=grade,
            general_feedback=general_feedback,
            answer_preload=answer_preload,
            all_or_nothing=all_or_nothing,
            check_results=check_results,
            parser=parser,
            internal_copy=internal_copy,
            database_connection=database_connection,
            **flags,
        )

        if check_results:
            self.check_results()

    @staticmethod
    def render_test_templates(testcases: list[Testcase]) -> list[Testcase]:
        """Replace test templates with the respective Jinja templates and render them.

        The tests are modified in-place. The function returns the same list it received.

        Args:
            testcases: List of testcases.

        Returns:
            list[Testcase]: List of testcases with rendered templated.
        """
        for testcase in testcases:
            rendered_statements = []

            test_statements = [t.strip() for t in testcase["code"].split(";") if t.strip()]
            for statement in test_statements:
                match statement.split(" "):
                    case ["MT_testtablecorrectness", table_name, *tests]:
                        extra = testcase.get("extra", {})

                        flex_datatypes: dict[str, list[str]] = {}
                        if not isinstance(extra, dict):
                            logger.warning("`extra` is not a dictionary. Ignoring.")
                        elif "flex_datatypes" in extra and isinstance(
                            extra["flex_datatypes"], dict
                        ):
                            flex_datatypes = extra["flex_datatypes"]

                        templates: Iterable[Path] = [
                            Path(template)
                            for template in JinjaEnv.list_templates(
                                filter_func=lambda n: n.startswith("ddl_check_tablecorrectness/")
                            )
                        ]

                        # If tests are provided, filter the templates to only include those
                        if tests:
                            templates = filter(
                                lambda t: t.name.split(".")[0].split("-")[1] in tests, templates
                            )

                        rendered_statements.append(
                            "\n\n----------\n\n".join(
                                [
                                    JinjaEnv.get_template(str(template)).render(
                                        tablename=table_name,
                                        flex_datatypes=json.dumps(flex_datatypes)
                                        .replace("'", "''")
                                        .replace('"', "'"),
                                    )
                                    for template in templates
                                ]
                            )
                        )

                    case _:
                        if statement.startswith("MT_"):
                            logger.warning(
                                "Test code {} does not match any known template.", testcase["code"]
                            )
                        else:
                            rendered_statements.append(statement + ";")

            testcase["code"] = "\n\n".join(rendered_statements)

        return testcases

    def fetch_expected_result(self, test_code: str) -> str:
        if not self.database_connection:
            raise ParsingError(DB_CONNECTION_ERROR)

        # A DDL/DML test might include multiple statements, so we need to split them
        statements = [code for code in test_code.split(";") if code.strip()]
        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture), open_tmp_db_connection(self.database_path) as con:
            con.sql(self.answer)
            for statement in statements:
                try:
                    res = con.sql(statement)
                    if res:
                        res.show(max_width=self.MAX_WIDTH, max_rows=self.MAX_ROWS)
                    else:
                        print(res)
                except duckdb.ConstraintException as e:
                    # DuckDB prints the individual constraint implementation in the error message
                    # so we have to filter it out.
                    match = re.search(
                        r"^Constraint Error: CHECK constraint failed on table (.+?) .*$", str(e)
                    )
                    if match:
                        print(f"CHECK constraint failed on table {match.group(1)}")
                    else:
                        print(e)
                except duckdb.Error as e:
                    print(e)

        return stdout_capture.getvalue()

    def validate_query(self, testcase: Testcase) -> None:
        if "## non_viable_flex_type ##" in testcase["result"]:
            logger.warning(
                "Non-viable flex type detected in test case {}. "
                "Please check that the set of possible types matches the sample solution.",
                testcase.get("description", "Untitled test"),
            )


class CoderunnerDQLQuestion(CoderunnerSQLQuestion):
    """Template for a SQL DQL question in Moodle CodeRunner."""

    CODERUNNER_TYPE = "python3"
    RESULT_COLUMNS_DEFAULT = ""  # TODO
    RESULT_COLUMNS_DEBUG = ""  # TODO
    TEST_TEMPLATE = "testlogic_dql.py.j2"

    def __init__(
        self,
        *,
        question: str,
        title: str,
        answer: str,
        testcases: list[Testcase],
        database_path: str,
        category: str | None = None,
        grade: float = 1,
        general_feedback: str = "",
        answer_preload: str = "",
        all_or_nothing: bool = True,
        check_results: bool = False,
        parser: str | None = None,
        internal_copy: bool = False,
        database_connection: bool = True,
        **flags: bool,
    ) -> None:
        super().__init__(
            question=question,
            title=title,
            answer=answer,
            testcases=testcases,
            database_path=database_path,
            category=category,
            grade=grade,
            general_feedback=general_feedback,
            answer_preload=answer_preload,
            all_or_nothing=all_or_nothing,
            check_results=check_results,
            parser=parser,
            internal_copy=internal_copy,
            database_connection=database_connection,
            **flags,
        )

        if database_connection:
            self.question += preprocess_text(self.extract_expected_output_schema(answer), **flags)

        # We use standardized test names and hide all tests but the first for this type of question
        for i, testcase in enumerate(self.testcases):
            testcase["description"] = f"Testfall {i + 1}"
            if i > 0 and "hidden" not in testcase:
                testcase["show"] = "HIDE"

        if check_results:
            self.check_results()

    def fetch_expected_result(self, test_code: str) -> str:
        if not self.database_connection:
            raise ParsingError(DB_CONNECTION_ERROR)

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture), open_tmp_db_connection(self.database_path) as con:
            con.sql(test_code)
            res = con.sql(self.answer)
            if res:
                res.show(max_width=self.MAX_WIDTH, max_rows=self.MAX_ROWS)
            else:
                print(res)

        return stdout_capture.getvalue()

    def extract_expected_output_schema(self, query: str) -> str:
        """Extract the output schema of a query from its operators and its result.

        Args:
            query: The SQL query to parse.

        Returns:
            str: The output schema of the query.
        """
        if not self.database_connection:
            raise ParsingError(DB_CONNECTION_ERROR)

        with open_tmp_db_connection(self.database_path) as con:
            # Run the query, so that we can then get the schema output
            result = con.sql(query)
            result_schema = result.description

        # Grab the ORDER BY statement so that we can get sorting information
        match = re.search(".*ORDER BY (.*);?", query, flags=re.IGNORECASE)
        column_orderings = {}
        if match:
            # Splitting the order on "," and on " " to get the column name and the order modifier
            order_by_statements = match.group(1).replace(";", "").split(",")
            for item in order_by_statements:
                item_split = item.strip().split(" ")
                if len(item_split) == 1:
                    item_split.append("ASC")
                column_orderings.update({item_split[0]: item_split[1]})
        else:
            logger.warning(
                "No ORDER BY statement found in the query. Please ensure that this was intended. "
                "CodeRunner only performs string comparisons between solutions so usually an "
                "ordering is necessary to ensure solution robustness."
            )

        # Creating the output schema string, appending it to the question_text, and return it
        asc_desc_map = {"asc": "↑", "desc": "↓"}
        output_elements: list[str] = []
        for column in result_schema:
            column_name = column[0]
            found_column = False
            for column_order, order_statement in column_orderings.items():
                if column_name in column_order:
                    output_elements.append(
                        f"{column_name} ({asc_desc_map[order_statement.lower()]})"
                    )
                    found_column = True
                    break

            if not found_column:
                output_elements.append(column_name)

        return "\nErgebnisschema:\n\n" + ", ".join(output_elements)
