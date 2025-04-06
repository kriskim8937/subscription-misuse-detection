# Subscription Misuse Detection

## Overview

This project aims to detect and prevent subscription misuse in a streaming platform. The system ingests user activity data, processes it using scalable data pipelines, applies rule-based and ML-based anomaly detection techniques, and provides an API for enforcing account restrictions. Additionally, a dashboard visualizes flagged accounts and misuse patterns.

## Directory Structure
```plaintext
subscription-misuse-detection/
│
├── data_ingestion/                   # Directory for data ingestion scripts
│   ├── kafka_producer.py             # Kafka producer script for generating user activity data
│   ├── kafka_to_postgres.py          # Kafka consumer that writes data to PostgreSQL
│   └── pubsub_publisher.py            # (Optional) Pub/Sub publisher script (if applicable)
│
├── data_processing/                   # Directory for data processing scripts and models
│   ├── dbt_models/                    # Directory for DBT models
│   │   ├── models/                    # DBT transformation models
│   │   │   └── clean_user_activity.sql # DBT model for cleaning user activity data
│   │   └── dbt_project.yml            # DBT project configuration file
│   └── scio_jobs/                     # (Optional) Directory for Scio (Scala) jobs
│
├── misuse_detection/                  # Directory for misuse detection logic
│   ├── anomaly_detection.py            # (Optional) Script for ML-based anomaly detection
│   └── rule_based_filtering.py         # Script for rule-based filtering of user activities
│
├── backend_api/                       # Directory for FastAPI backend
│   ├── app.py                         # FastAPI application with API endpoints
│   └── models.py                      # (Optional) Data models and Pydantic schemas
│
├── visualization/                     # Directory for Streamlit dashboard
│   ├── dashboard.py                   # Streamlit app for visualizing flagged users
│
├── deployment/                        # Directory for deployment-related files
│   ├── docker-compose.yml             # Docker Compose configuration file
│   └── terraform/                     # (Optional) Terraform scripts for cloud deployment
│
├── tests/                             # Directory for tests (if applicable)
│   ├── test_rule_based_filtering.py    # Tests for rule-based filtering logic
│   └── test_fastapi.py                 # Tests for FastAPI endpoints
│
├── .gitignore                         # Git ignore file
├── LICENSE                            # License file for the project
├── README.md                          # Project documentation
└── requirements.txt                   # Python dependencies for the project
```
## Architecture Overview

The architecture of the Subscription Misuse Detection system is designed to efficiently process and analyze user activity data, detect misuse, and provide insights through a user-friendly dashboard. The following components outline the system architecture:

1. Data Ingestion:

Kafka is used to simulate and stream user activity data into the system. The Kafka producer generates user activity events, while the Kafka consumer (kafka_to_postgres.py) ingests this data and stores it in a PostgreSQL database.

2. Data Storage:

A PostgreSQL database serves as the primary data storage solution. It contains tables for raw user activity (raw_user_activity) and flagged users (flagged_users). The clean_user_activity table is populated through DBT transformations to prepare data for analysis.

3. Data Processing:

DBT is utilized to transform raw activity logs into structured datasets. Transformation models clean and enrich the data for downstream analysis.

4. Misuse Detection:

The rule_based_filtering.py script implements rule-based filtering logic to identify suspicious user activities. Users who meet certain criteria (e.g., accessing multiple locations in a short time) are flagged and stored in the flagged_users table.

5. API Development:

A FastAPI backend exposes APIs for interaction with the system. Key endpoints include:

GET /flagged-users: Retrieves a list of flagged users along with the reasons for flagging.

GET /: A health check endpoint to confirm that the API is running.

6. Visualization:

A Streamlit dashboard provides an interactive interface for visualizing flagged users. Users can filter flagged activities by reason and date, allowing for quick insights into potential misuse.

7. Deployment:

The application is containerized using Docker for easy deployment and management. The docker-compose.yml file orchestrates the various services needed to run the application.

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (3.9 or higher)
- [PostgreSQL](https://www.postgresql.org/download/)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/subscription-misuse-detection.git
cd subscription-misuse-detection
```
2. Build and run the Docker containers:
```bash
docker-compose up --build
```
3. Install Python dependencies in your devcontainer:
```bash
pip install -r requirements.txt
```
4. Create the database and necessary tables by running the following SQL commands in the PostgreSQL container:
```bash
docker exec -it postgres psql -U postgres -d streaming
CREATE TABLE IF NOT EXISTS raw_user_activity (
    user_id TEXT,
    device_id TEXT,
    ip_location TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS flagged_users (
    user_id TEXT PRIMARY KEY,
    reason TEXT,
    flagged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
4. Run DBT
```bash
cd data_processing/dbt_models
dbt debug
dbt run  
```
5. Start the FastAPI server:
```bash
uvicorn backend_api.app:app --reload --host 0.0.0.0 --port 8000
```
6. Run the Streamlit dashboard:
```bash
streamlit run visualization/dashboard.py
```

## Usage
Access the FastAPI API documentation at http://localhost:8000/docs.

View the Streamlit dashboard at http://localhost:8501.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [FastAPI](https://docs.docker.com/get-docker/)
- [DBT](https://docs.docker.com/get-docker/)
- [Kafka](https://docs.docker.com/get-docker/)
- [Streamlit](https://docs.docker.com/get-docker/)

## Ideal Project Enhancements

To align this project more closely with the requirements of the job at Spotify and create a robust, scalable solution, the following features should be implemented:

- **Advanced Anomaly Detection**:
  - Implement machine learning models (e.g., Isolation Forest, clustering) to enhance misuse detection beyond rule-based methods.
  - Incorporate A/B testing frameworks to validate the effectiveness of the misuse detection models.

- **Scio or PySpark Integration**:
  - Utilize **Scio** (Scala) or **PySpark** for more complex data processing tasks, leveraging their capabilities for handling large-scale data.

- **Enhanced API Features**:
  - Add more endpoints to the FastAPI service, such as:
    - `POST /ban-user`: To flag a user based on certain criteria.
    - `GET /user-activity/{user_id}`: To retrieve historical activity for a specific user.

- **Real-time Data Processing**:
  - Integrate **Cloud Pub/Sub** or a similar service for real-time data streaming, allowing for immediate flagging and action on suspicious activities.

- **Data Quality and Monitoring**:
  - Implement monitoring tools to assess the health and performance of data pipelines.
  - Set up alerts for anomalies in data ingestion and processing.

- **Documentation and Testing**:
  - Improve documentation with usage examples, architecture diagrams, and development guidelines.
  - Write unit tests and integration tests for both the API and data processing components to ensure reliability and facilitate maintenance.
