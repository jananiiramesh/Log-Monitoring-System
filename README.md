# Log Monitoring System

This project implements a complete log monitoring system with Kafka, MySQL, and Grafana visualization. The system consists of several components:

1. Flask API: Provides various endpoints that generate logs
2. Log Generator: Makes requests to the Flask API endpoints
3. Kafka Producer: Sends logs to Kafka topics based on status codes
4. Kafka Consumer: Reads logs from Kafka and stores them in MySQL
5. Grafana: Visualizes log metrics from the MySQL database

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the System

1. Clone this repository to your local machine
2. Navigate to the project directory
3. Run Docker Compose to start all services:

```bash
docker-compose up -d
```

4. Wait a few moments for all services to start up (this might take a minute or two)

### Accessing Services

- **Flask API**: http://localhost:5000
- **Grafana**: http://localhost:3000
  - Username: admin
  - Password: admin

### Monitoring Logs

1. Open Grafana in your browser: http://localhost:3000
2. Log in with the default credentials (admin/admin)
3. The "Log System Dashboard" should be automatically available
4. You can see:
   - Log count by topic over time
   - Total logs by topic
   4. You can see:
   - Log count by topic over time
   - Total logs by topic
   - Recent logs table
   - Average system uptime
   - Status code distribution

### System Architecture

The system uses the following Docker containers:

- **mysql**: MySQL database for storing logs
- **zookeeper**: Required for Kafka operation
- **kafka**: Message broker for distributing logs
- **kafka-setup**: Creates the necessary Kafka topics
- **flask-api**: Provides endpoints that generate logs
- **log-generator**: Makes requests to the API endpoints
- **consumer**: Processes logs from Kafka and stores them in MySQL
- **grafana**: Visualizes log data with dashboards

### Data Flow

1. The log generator makes requests to the Flask API endpoints
2. The Flask API processes the requests and returns HTTP status codes
3. The Kafka producer sends log messages to appropriate topics:
   - HTTP 200-399: info-logs
   - HTTP 400-499: warning-logs
   - HTTP 500+: error-logs
4. The Kafka consumer reads from all topics and stores logs in MySQL
5. Grafana queries the MySQL database to visualize the log data

### Customization

- To modify the Flask API endpoints, edit `main.py`
- To change the log generation pattern, edit `log.py`
- To adjust the Kafka topic routing, edit `producer.py`
- To customize the Grafana dashboard, log in to Grafana and edit the dashboard

### Troubleshooting

If any component isn't working properly:

1. Check container logs:
   ```bash
   docker-compose logs [service-name]
   ```

2. Ensure all containers are running:
   ```bash
   docker-compose ps
   ```

3. Restart a specific service:
   ```bash
   docker-compose restart [service-name]
   ```

4. Restart the entire system:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Shutting Down

To stop all services:

```bash
docker-compose down
```

To remove all data volumes (will delete all stored logs):

```bash
docker-compose down -v
```
