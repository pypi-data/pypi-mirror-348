# pytest_prometheus_pushgw

A lightweight **pytest plugin** to export test execution metrics to **Prometheus Pushgateway**.

## 🚀 Features

- Automatically tracks:
  - Test pass/fail status
  - Test duration
  - Test execution counts
  - Histogram and summary of durations
- Pushes metrics to Prometheus Pushgateway after each test


## 🧪 Installation

```bash
pip install pytest_prometheus_pushgw
```

- Variables
    - `PUSH_GW_URL`: To set push gateway URL. Default is: `localhost:9091`
    -  `JOB_NAME` : To set job name. Default is:  `pytest_execution_result_job`
