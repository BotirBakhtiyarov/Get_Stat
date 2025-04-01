# Get_Stat - Multi-Computer Usage Monitoring System

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-brightgreen)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A distributed system monitoring solution that tracks computer resource usage and application metrics across multiple machines.

## Features

- Real-time system metrics monitoring (CPU/RAM)
- Application usage tracking with duration
- Cross-platform monitoring agent (Windows-focused)
- Secure API key authentication
- Web-based dashboard with interactive charts
- Historical data analysis with time filters

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or SQLite
- Redis (for caching - optional)
- Windows machine for agent (Linux support planned)

### Installation

1. Clone repository:
```bash
git clone https://github.com/BotirBakhtiyarov/Get_Stat.git
cd Get_Stat
```

2. Set up virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database in `StatsProject/settings.py`

5. Run migrations:
```bash
python manage.py migrate
```

6. Create API key:
```bash
python manage.py createapikey
```

### Usage

1. Start Django server:
```bash
python manage.py runserver 0.0.0.0:8000
```

2. Run monitoring agent (on target machines):
```bash
python agent.py
```

3. Access dashboard at `http://localhost:8000/data.html`

## API Documentation

### Endpoints

- `POST /api/data` - Submit metrics data (used by agent)
- `GET /api/stats` - Retrieve aggregated statistics

### Authentication
Include API key in headers:
```http
Authorization: Api-Key YOUR_API_KEY
```

## License
Distributed under the MIT License. See `LICENSE` for more information.




