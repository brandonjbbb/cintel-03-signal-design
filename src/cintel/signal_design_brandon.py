"""
signal_design_brandon.py - Project script.

Author: Brandon Jean-Baptiste
Date: 2026-03

System Metrics Data

- Data is taken from a system that records operational metrics.
- The data is structured and static for this example.
- Each row represents one observation of system behavior.
- The CSV file includes these columns:
  - requests: number of requests handled
  - errors: number of failed requests
  - total_latency_ms: total response time in milliseconds

Purpose

- Read system metrics from a CSV (comma-separated values) file.
- Design useful signals from the raw measurements.
- Save the resulting signals as a new CSV artifact.
- Log the pipeline process to assist with debugging and transparency.
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P3", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS FOR FOLDER PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

# === DECLARE GLOBAL CONSTANTS FOR FILE PATHS ===

DATA_FILE: Final[Path] = DATA_DIR / "system_metrics_brandon.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "signals_brandon.csv"


def main() -> None:
    """Run the pipeline."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # STEP 1: READ CSV DATA
    df: pl.DataFrame = pl.read_csv(DATA_FILE)
    LOG.info(f"Loaded {df.height} system metric records")

    # STEP 2: DESIGN SIGNALS
    LOG.info("Designing signals from the raw metrics...")

    is_requests_positive: pl.Expr = pl.col("requests") > 0

    calculated_error_rate: pl.Expr = pl.col("errors") / pl.col("requests")
    error_rate_signal_recipe: pl.Expr = (
        pl.when(is_requests_positive)
        .then(calculated_error_rate)
        .otherwise(0.0)
        .alias("error_rate")
    )

    calculated_avg_latency: pl.Expr = pl.col("total_latency_ms") / pl.col("requests")
    avg_latency_signal_recipe: pl.Expr = (
        pl.when(is_requests_positive)
        .then(calculated_avg_latency)
        .otherwise(0.0)
        .alias("avg_latency_ms")
    )

    throughput_signal_recipe: pl.Expr = pl.col("requests").alias("throughput")

    # NEW MODIFICATION: success_rate
    calculated_success_rate: pl.Expr = (
        (pl.col("requests") - pl.col("errors")) / pl.col("requests")
    )
    success_rate_signal_recipe: pl.Expr = (
        pl.when(is_requests_positive)
        .then(calculated_success_rate)
        .otherwise(0.0)
        .alias("success_rate")
    )

    df_with_signals: pl.DataFrame = df.with_columns(
        [
            error_rate_signal_recipe,
            avg_latency_signal_recipe,
            throughput_signal_recipe,
            success_rate_signal_recipe,
        ]
    )

    LOG.info(
        "Created signal columns: error_rate, avg_latency_ms, throughput, success_rate"
    )

    # STEP 3: SELECT COLUMNS TO SAVE
    signals_df = df_with_signals.select(
        [
            "requests",
            "errors",
            "total_latency_ms",
            "error_rate",
            "avg_latency_ms",
            "throughput",
            "success_rate",
        ]
    )

    LOG.info(f"Enhanced signals table has {signals_df.height} rows")

    # STEP 4: SAVE OUTPUT
    signals_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote signals file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


if __name__ == "__main__":
    main()
