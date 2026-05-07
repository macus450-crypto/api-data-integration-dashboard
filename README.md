# API Data Integration Dashboard

A small data integration dashboard built with Python, Flask and PostgreSQL.

The application is designed to fetch data from an external REST API, process the received JSON response, store normalized records in a relational database, and display the data in a simple web dashboard.

## Overview

API Data Integration Dashboard is a small backend-oriented project focused on working with external data sources and relational databases.

The main data flow is:

```text
REST Countries API
→ Python requests
→ JSON response
→ data normalization
→ PostgreSQL
→ Flask routes
→ HTML dashboard
```

The project uses REST Countries API as the external data source because it provides stable public data without requiring an API key.

## Features

Planned and implemented features include:

- basic Flask application setup
- external REST API integration
- JSON data processing
- PostgreSQL database connection
- country data storage
- duplicate prevention during synchronization
- synchronization logs
- basic dashboard statistics
- searchable country list
- filtering by region
- simple HTML/CSS interface
- technical documentation

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- psycopg2-binary
- requests
- python-dotenv
- HTML
- CSS
- Git

## Current Status

The project is currently in the initial setup stage.

Completed:

- project directory created
- Python virtual environment configured
- required dependencies installed
- initial Flask application created
- project structure prepared
- Git repository initialized
- initial commit created
- project pushed to GitHub

Next steps:

- configure PostgreSQL
- create database schema
- connect the application to the database
- implement REST Countries API integration
- add data synchronization logic
- build the dashboard views

## Project Structure

```text
api-data-integration-dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   └── countries.html
├── static/
│   └── style.css
├── services/
│   └── api_client.py
├── database/
│   ├── db.py
│   └── schema.sql
└── docs/
    └── architecture.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/macus450-crypto/api-data-integration-dashboard.git
```

Go to the project directory:

```bash
cd api-data-integration-dashboard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows CMD:

```bash
venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in the browser:

```text
http://127.0.0.1:5000
```

## Environment Configuration

The project will use environment variables for database configuration.

Example `.env` file:

```env
DB_NAME=api_dashboard_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The real `.env` file should not be committed to the repository.

Use `.env.example` to document required configuration values.

## Planned Database Schema

The project will use two main tables.

### `countries`

Stores normalized country data fetched from the external API.

Planned fields:

- id
- external_name
- official_name
- region
- subregion
- capital
- population
- area
- created_at
- updated_at

### `sync_logs`

Stores synchronization history.

Planned fields:

- id
- status
- message
- records_imported
- created_at

## Technical Notes

The application follows a simple structure:

- `app.py` contains Flask routes
- `services/api_client.py` handles communication with the external API
- `database/db.py` handles database operations
- `database/schema.sql` contains SQL table definitions
- `templates/` contains HTML views
- `static/` contains CSS
- `docs/` contains technical documentation

The goal is to keep the project small, readable and easy to extend.

## Known Limitations

- The application currently runs locally.
- PostgreSQL configuration is not completed yet.
- API synchronization is not implemented yet.
- Dashboard views are still minimal.
- Authentication is not included.
- Deployment is outside the current MVP scope.

## License

This project is currently created for educational and development purposes.
