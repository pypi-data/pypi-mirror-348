import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from llama_api_bench.core.criterias.criterias import get_criteria
from llama_api_bench.core.interface import ProviderConfig
from llama_api_bench.data.data import ALL_TEST_CASES
from llama_api_bench.data.export import save_to_csv, save_to_jsonl, to_dataframe
from llama_api_bench.data.types import CriteriaTestCase, CriteriaTestResult
from llama_api_bench.models.llamaapi import LLAMA_API_MODELS


def run_one(args: tuple[CriteriaTestCase, ProviderConfig, str, bool]) -> CriteriaTestResult:
    tc, provider_config, model, stream = args
    criteria_func = get_criteria(tc.criteria)
    return criteria_func(test_case=tc, model=model, stream=stream, provider_config=provider_config)


def get_results(
    test_cases: dict[str, CriteriaTestCase],
    models: dict[str, list[str]],
    provider_configs: list[ProviderConfig],
    parallel: bool = True,
) -> list[CriteriaTestResult]:
    results = []
    # Flatten all combinations to a list
    combinations = [
        (tc, provider_config, model, stream)
        for tc in test_cases.values()
        for provider_config in provider_configs
        for model, unsupported_test_cases in models.items()
        for stream in [True, False]
        if tc.criteria not in unsupported_test_cases
    ]

    if parallel:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_one, combo) for combo in combinations]
            for f in tqdm(as_completed(futures), total=len(futures), desc="Running test cases (parallel)"):
                results.append(f.result())
    else:
        for tc, provider_config, model, stream in tqdm(combinations, desc="Running test cases"):
            criteria_func = get_criteria(tc.criteria)
            r = criteria_func(test_case=tc, model=model, stream=stream, provider_config=provider_config)
            results.append(r)

    return results


def _rich_display_dataframe(df, title="Dataframe"):
    """Display a Pandas DataFrame as a rich table."""
    console = Console()
    table = Table(title=title)

    for col in df.columns:
        table.add_column(str(col))

    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row.values])

    console.print(table)


def aggregate_metrics(results: list[CriteriaTestResult], print_result: bool = False) -> pd.DataFrame:
    """
    Return aggregated metrics from results in a for visualization.
    """
    df = to_dataframe(results)
    df["pass"] = df["result"].apply(lambda x: x["pass"])
    df = (
        df.groupby(["model", "criteria", "provider", "stream"])
        .agg(num_pass=("pass", "sum"), num_total=("pass", "count"), pass_rate=("pass", "mean"))
        .reset_index()
    )

    if print_result:
        _rich_display_dataframe(df, title="Aggregated Results")

    return df


def get_all_provider_configs() -> list[ProviderConfig]:
    return [
        ProviderConfig(
            provider="llamaapi-openai-compat",
            provider_params={"base_url": "https://api.llama.com/compat/v1/", "api_key": os.getenv("LLAMA_API_KEY")},
        ),
        ProviderConfig(provider="llamaapi", provider_params={"api_key": os.getenv("LLAMA_API_KEY")}),
    ]


def run_all_test_cases(verbose: bool = True):
    """
    Run all test cases and print the results.
    """
    results = get_results(
        ALL_TEST_CASES,
        LLAMA_API_MODELS,
        get_all_provider_configs(),
    )

    save_to_jsonl(results, "results.jsonl")
    save_to_csv(results, "results.csv")
    aggregate_metrics(results, print_result=verbose)


def run_test_case(test_case: str):
    """
    Run a specific test case and print the results.
    """
    tc = ALL_TEST_CASES[test_case]
    results = get_results({test_case: tc}, LLAMA_API_MODELS, get_all_provider_configs())
    aggregate_metrics(results, print_result=True)


def run_criteria(criteria: str):
    """
    Run a specific criteria and print the results.
    """
    filtered_test_cases = {k: v for k, v in ALL_TEST_CASES.items() if v.criteria == criteria}
    results = get_results(filtered_test_cases, LLAMA_API_MODELS, get_all_provider_configs())
    aggregate_metrics(results, print_result=True)
