# Get_Stat

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-brightgreen)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Get_Stat** is a monitoring system designed to track computer usage, application activity, and system metrics (e.g., CPU and RAM usage) across multiple machines. It features a Django-based backend server, a Python client-side agent for data collection, and a lightweight HTML dashboard for visualization for testing.

## Features

- **Real-Time Monitoring**: Captures and displays CPU, RAM, and application usage data with minimal latency.
- **Multi-Computer Tracking**: Supports monitoring multiple machines, each identified by a unique ID.
- **Secure API**: Provides authenticated endpoints for data ingestion and retrieval using API keys.
- **Cross-Platform Agent**: Written in Python, the agent runs on any platform with Python support (Windows executable also available).
- **Extensible**: Easily adaptable for additional metrics or integrations.

## Architecture

- **Backend (Django)**: Manages data storage, processing, and API interactions.
  - **Models**: `Computer`, `AppUsage`, `SystemMetrics`.
  - **Endpoints**: `/api/data` (data submission), `/api/stats` (data retrieval).
- **Agent (Python)**: Collects system metrics and application data, sending it to the backend periodically.
- **Frontend (HTML/JS)**: A simple dashboard (`data.html`) using Chart.js and Axios for visualization.

## Installation

### Prerequisites

- **Python 3.8+**: Required for both server and agent.
- **Django**: Installed via `requirements.txt`.
- **Git**: For cloning the repository.

### Server Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BotirBakhtiyarov/Get_Stat.git
   cd Get_Stat
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   cd StatsProject
   python manage.py migrate
   ```

5. **Generate an API Key**:
   ```bash
   python manage.py createapikey
   ```
   - Save the generated API key; it’s required for authenticating requests to `/api/stats`.

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   - Access the server at `http://localhost:8000`.

### Agent Setup

The agent collects and sends metrics to the server every 5 minutes.

#### Option 1: Run from Source (Cross-Platform)

1. **Install Dependencies**:
   ```bash
   pip install psutil requests pywin32  # Omit pywin32 on non-Windows platforms
   ```

2. **Configure the Server URL**:
   - In `agent.py`, set `SERVER_URL` to your server’s `/api/data` endpoint (e.g., `http://your-server-ip:8000/api/data`).

3. **Launch the Agent**:
   ```bash
   python agent.py
   ```

#### Option 2: Pre-Built Executable (Windows Only)

- Download `setup.exe` from the [latest release](https://github.com/yourusername/Get_Stat/releases).
- Install and run `setup.exe`.
- **Note**: The default `SERVER_URL` is `http://192.168.1.6:8000`. Update the source and rebuild the executable if your server uses a different address.

### Viewing Data for testing

1. Open `data.html` in a browser.
2. Input the API key from the server setup.
3. Select a time filter (e.g., "Last 5 Minutes", "Last 1 Hour").
4. Click "Load Data" to view metrics.
   - Displays CPU, RAM, and app usage per computer.
   - **Note**: Update the URL in `data.html`’s `loadData()` function if the server isn’t on `localhost:8000`.

## API Documentation

### Endpoints

- **POST /api/data**  
  - **Purpose**: Submits metrics from the agent.  
  - **Payload**: JSON with `computer_id`, `username`, `timestamp`, `cpu`, `ram`, and `apps`.  
  - **Authentication**: None (open for agents).

- **GET /api/stats**  
  - **Purpose**: Retrieves aggregated stats.  
  - **Query Params**: `time_filter` (optional; `latest`, `1h`, `1d`).  
  - **Authentication**: Requires `Authorization: Api-Key YOUR_API_KEY` header.

### Example Request

```bash
curl -H "Authorization: Api-Key YOUR_API_KEY" "http://localhost:8000/api/stats?time_filter=1h"
```

## Customization

- **Agent**: Edit `agent.py` to add metrics or adjust the polling interval.
- **Backend**: Modify `models.py` to store additional data.
- **Frontend**: Enhance `data.html` with new visualizations for testing API.

## Security Considerations

- **API Key**: Keep it confidential to secure `/api/stats`.
- **CORS**: In production, disable `CORS_ALLOW_ALL_ORIGINS` in `settings.py` and whitelist specific origins.
- **HTTPS**: Use HTTPS in production to encrypt traffic.

## Troubleshooting

- **Agent Issues**: Verify `SERVER_URL` and server accessibility.
- **API Key Problems**: Ensure the key matches the one generated and is correctly entered in `data.html`.
- **Time Zones**: Default is UTC+8 (Asia/Shanghai); adjust in `settings.py` and `agent.py` if needed.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
