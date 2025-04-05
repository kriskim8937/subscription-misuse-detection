# Subscription Misuse Detection

## Overview

This project aims to detect and prevent subscription misuse in a streaming platform. The system ingests user activity data, processes it using scalable data pipelines, applies rule-based and ML-based anomaly detection techniques, and provides an API for enforcing account restrictions. Additionally, a dashboard visualizes flagged accounts and misuse patterns.

## What Has Been Implemented

- **Data Ingestion**: 
  - Simulated streaming data ingestion using **Kafka**.
  - Data is stored in a **PostgreSQL** database for further processing.

- **Data Processing**:
  - Used **DBT** to transform raw activity logs into clean datasets.
  - Created models for data transformation in `dbt_models`.

- **Misuse Detection**:
  - Implemented rule-based filtering logic in **Python** to identify suspicious user activities (e.g., multiple locations in a short time).
  - A dedicated FastAPI service to expose APIs for flagged users.

- **API Development**:
  - Created a **FastAPI** backend service to retrieve flagged users with endpoints:
    - `GET /flagged-users`: Fetches a list of flagged users and their reasons for flagging.
    - `GET /`: Health check endpoint.

- **Dashboard**:
  - Built a **Streamlit** dashboard to visualize flagged users.
  - Allows filtering of flagged users by reason and date.

## Added Features

- **Database Integration**:
  - Set up **PostgreSQL** with tables for raw user activity and flagged users.
  
- **User-friendly Dashboard**:
  - An interactive Streamlit dashboard for displaying flagged users with filtering options.

- **Environment Setup**:
  - Dockerized the application for easy setup and deployment.
  - Used a `devcontainer.json` for a consistent development environment.

- **Scalability**:
  - Implemented a modular approach to the data pipeline using DBT for scalability.
  
- **Testing and Validation**:
  - Basic validation checks on API responses.

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

## Added Features

- **Database Integration**:
  - Configured **PostgreSQL** with tables for storing raw user activity and flagged users.

- **User-friendly Dashboard**:
  - Implemented an interactive Streamlit dashboard to display flagged users, with filtering capabilities.

- **Environment Setup**:
  - Dockerized the application to streamline setup and deployment processes.
  - Configured a `devcontainer.json` for a consistent development environment using VS Code.

- **Scalability**:
  - Adopted a modular approach in the data pipeline using DBT for enhanced scalability and maintainability.

- **Testing and Validation**:
  - Implemented basic validation checks on API responses to ensure reliability.

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
