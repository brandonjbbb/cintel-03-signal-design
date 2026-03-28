# cintel-03-signal-design

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence and signal design.

## Overview

This project analyzes system performance data by reading a CSV file of raw operational metrics and transforming it into more useful analytical signals.

The pipeline uses raw columns such as:
- `requests`
- `errors`
- `total_latency_ms`

and creates derived signals such as:
- `error_rate`
- `avg_latency_ms`
- `throughput`
- `success_rate`

These signals make it easier to understand reliability, efficiency, and workload.

## What the project does

This project reads input data from:

```text
data/system_metrics_case.csv
