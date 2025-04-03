# Subscription Misuse Detection and Prevention System

## Overview
This project is designed to detect and prevent subscription misuse in a streaming platform. The system ingests user activity data, processes it using scalable data pipelines, applies rule-based and ML-based anomaly detection techniques, and provides an API for enforcing account restrictions. Additionally, a dashboard visualizes flagged accounts and misuse patterns.

## Features
- **Data Ingestion**: Simulated streaming data using Kafka or Cloud PubSub.
- **Data Processing**: DBT models for transforming raw activity logs.
- **Misuse Detection**: Rule-based and ML-based fraud detection (Isolation Forest, clustering).
- **Backend API**: FastAPI-based service to retrieve flagged users and enforce account restrictions.
- **Visualization**: Streamlit dashboard for data analysis.
- **Cloud Deployment**: Docker, Kubernetes, and cloud data storage (BigQuery/Snowflake/PostgreSQL).

## Tech Stack
- **Data Pipeline**: DBT, Scio (Scala) / PySpark
- **Programming Languages**: Python, Scala, SQL
- **Backend**: FastAPI (Python), Java (optional for backend services)
- **Storage**: BigQuery, PostgreSQL, Snowflake
- **Cloud Services**: GCP (Cloud PubSub, BigQuery), AWS (RDS, Lambda)
- **Visualization**: Looker, Tableau, Streamlit

## Project Structure
```
subscription-misuse-detection/
│── data_ingestion/
│   ├── kafka_producer.py
│   ├── pubsub_publisher.py
│── data_processing/
│   ├── dbt_models/
│   ├── scio_jobs/
│   ├── spark_jobs/
│── misuse_detection/
│   ├── anomaly_detection.py
│   ├── rule_based_filtering.py
│── backend_api/
│   ├── app.py
│   ├── models.py
│── visualization/
│   ├── dashboard.py
│── deployment/
│   ├── docker-compose.yml
│   ├── terraform/
│── tests/
│── README.md
```

## Setup Instructions
### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- DBT (Data Build Tool)
- Kafka (if using local ingestion)
- GCP SDK (if using Cloud PubSub & BigQuery)

### Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/subscription-misuse-detection.git
   cd subscription-misuse-detection
   ```
2. **Set up a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Project
#### 1. Start Data Ingestion
- **Kafka-based ingestion**:
  ```sh
  python data_ingestion/kafka_producer.py
  ```
- **Cloud PubSub ingestion**:
  ```sh
  python data_ingestion/pubsub_publisher.py
  ```

#### 2. Process Data Using DBT
```sh
dbt run --profiles-dir ./dbt_profiles
```

#### 3. Run Misuse Detection
```sh
python misuse_detection/anomaly_detection.py
```

#### 4. Start the Backend API
```sh
uvicorn backend_api.app:app --host 0.0.0.0 --port 8000
```

#### 5. Run the Visualization Dashboard
```sh
streamlit run visualization/dashboard.py
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/flagged_accounts` | GET | Retrieve flagged users |
| `/block_user/{user_id}` | POST | Block a specific user |

## Deployment
### Docker Deployment
```sh
docker-compose up --build
```

### Cloud Deployment (GCP)
1. Deploy the backend API using Cloud Run:
   ```sh
   gcloud run deploy misuse-detection-api --source . --region europe-west1
   ```
2. Use BigQuery for storage:
   ```sql
   CREATE TABLE user_activity (
       user_id STRING, device_id STRING, ip_location STRING, timestamp TIMESTAMP
   );
   ```

## Testing
Run unit tests with:
```sh
pytest tests/
```

## Next Steps
- Improve ML model accuracy with advanced anomaly detection techniques.
- Implement real-time fraud detection with streaming analytics.
- Integrate automated alerts for flagged accounts.

## License
MIT License. See `LICENSE` file for details.

## Contact
For questions, reach out to [kriskim8937@gmail.com](mailto:your-email@example.com).

