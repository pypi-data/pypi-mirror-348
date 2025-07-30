from prometheus_client import CollectorRegistry, Gauge, Counter, Summary, Histogram, push_to_gateway
from datetime import datetime
import pytest
import time

PUSH_GW_URL = "localhost:9091"
JOB_NAME = "pytest_execution_result_job"

run_id = "Test_Run_"+datetime.now().strftime("%Y%m%d-%H%M%S")

registry = CollectorRegistry()
REGISTERED_METRICS = {}

test_status = Gauge(
    "pytest_test_status",
    "Test pass=1 / fail=0",
    ["test_name", "run_id", "test_duration"],
    registry=registry
)

test_counter = Counter(
    "pytest_test_counter",
    "Counts how many times a test case was run",
    ["test_name", "run_id"],
    registry=registry
)

test_duration_summary = Summary(
    "pytest_test_duration_summary",
    "Summary of test durations",
    ["test_name", "run_id"],
    registry=registry
)

test_duration_histogram = Histogram(
    "pytest_test_duration_histogram",
    "Histogram of test durations",
    ["test_name", "run_id"],
    registry=registry
)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global PUSH_GW_URL
    global JOB_NAME

    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':
        test_name = item.nodeid.replace("::", "_").replace("/", "_")
        duration = round(report.duration, 4)
        status = 1 if report.outcome == "passed" else 0

        test_status.labels(test_name, run_id, str(duration)).set(status)
        test_counter.labels(test_name, run_id).inc()
        test_duration_summary.labels(test_name, run_id).observe(duration)
        test_duration_histogram.labels(test_name, run_id).observe(duration)

        push_to_gateway(PUSH_GW_URL, job=JOB_NAME, registry=registry)