# Coffee Shop Sales Data Ingestion

## Overview

This project automates the ingestion of coffee shop sales data from Kaggle (CSV format) into a ClickHouse database. The pipeline is orchestrated using Apache Airflow and runs in a Dockerized environment, ensuring efficient and scalable data processing.

---

## Key Features

- Automated Data Extraction: Downloads sales data from Kaggle.

- Data Transformation: Cleans and structures raw CSV data.

- Database Integration: Loads processed data into ClickHouse.

- Airflow Automation: Schedules and manages the data ingestion workflow.

- Dockerized Setup: Ensures easy deployment and reproducibility.

---

## Tech Stack

- Kaggle API → Fetch sales data in CSV format

- Python → Data processing & transformation

- ClickHouse → High-performance columnar database

- Apache Airflow → Workflow automation

- Docker → Containerized environment for deployment

---

## Key Steps in the Project

- Data Extraction: Download sales data from Kaggle.

- Data Cleaning & Transformation: Process and normalize data.

- Data Loading: Store the transformed data in ClickHouse.

- Airflow Pipeline: Automate the entire workflow.

- Validation & Logging: Ensure data integrity and track pipeline execution.

---

## Project Limitations

- Static / Dummy Data: The project currently uses static datasets from Kaggle, which may not fully reflect real-world transactional changes.

- No Real-Time Data Processing: The ingestion is batch-based and not real-time.

- Limited Data Sources: Only integrates with Kaggle datasets at this stage.
