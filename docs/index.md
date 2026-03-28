# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
The dataset used in this project contains raw system performance metrics stored in `data/system_metrics_case.csv`, with each row representing one system observation and including the columns `requests`, `errors`, and `total_latency_ms`.

### Signals
The project uses and creates several analytical signals, including `error_rate`, `avg_latency_ms`, `throughput`, and the added custom signal `success_rate`, which measures the proportion of successful requests.

### Experiments
My main modification experiment was adding the `success_rate` signal to the pipeline so I could compare how a direct reliability metric complements the original error and latency signals.

### Results
After running the updated pipeline, the output artifact included the original metrics plus the new derived columns, and the added `success_rate` column made the results more informative.

### Interpretation
These results show that raw operational data becomes much more useful when transformed into signals, and the added `success_rate` helps provide clearer business intelligence about how reliably the system is handling requests.
