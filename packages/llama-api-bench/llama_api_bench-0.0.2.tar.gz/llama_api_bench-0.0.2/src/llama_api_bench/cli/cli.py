import typer
from typing_extensions import Annotated

from llama_api_bench.data.data import ALL_TEST_CASES

app = typer.Typer(
    name="llama-api-bench",
    help="A CLI for interacting with llama-api-bench.",
    add_completion=True,
    no_args_is_help=True,
)


@app.command()
def run_all(verbose: Annotated[bool, typer.Option(help="Print a more verbose output.")] = True):
    """
    Run All Test Cases
    """
    if verbose:
        typer.echo("Running all test cases...")

    from llama_api_bench.core.run import run_all_test_cases

    run_all_test_cases(verbose=verbose)


@app.command()
def run_test_case(
    test_case: Annotated[str, typer.Option(help="The name of the test case to run.")],
):
    """
    Run a specific test case
    """
    from llama_api_bench.core.run import run_test_case

    if test_case is not None and test_case not in ALL_TEST_CASES:
        raise typer.BadParameter(
            f"Invalid test case: {test_case}. Please choose from: {', '.join(ALL_TEST_CASES.keys())}"
        )

    run_test_case(test_case=test_case)


@app.command()
def run_criteria(
    criteria: Annotated[str, typer.Option(help="The name of the criteria to run.")],
):
    """
    Run a specific criteria
    """
    from llama_api_bench.core.run import run_criteria

    all_criterias = set([x.criteria for x in ALL_TEST_CASES.values()])

    if criteria not in all_criterias:
        raise typer.BadParameter(f"Invalid criteria: {criteria}. Please choose from: {', '.join(all_criterias)}")

    run_criteria(criteria=criteria)


if __name__ == "__main__":
    app()
