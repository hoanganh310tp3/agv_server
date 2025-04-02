# AGV Management System

This is a web-based system for managing and monitoring Automated Guided Vehicles (AGVs) in industrial environments. The system provides real-time tracking, task management, and administration capabilities for AGV fleets.

## System Overview

This application is built with:
- Django/Django Channels: Web framework and WebSocket support
- PostgreSQL: Primary database
- Redis: Cache and WebSocket channel layers
- MQTT: Communication with AGVs and IoT devices
- Docker: Containerization for easy deployment

## Installation and Setup

### Option 1: Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agv_3.git
   cd agv_3/Server/web_management
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the web application at http://localhost:8000

4. Monitor the database with pgAdmin:
   - Access pgAdmin at http://localhost:5050
   - Login with:
     - Email: admin@example.com
     - Password: admin
   - Add a new server with these details:
     - Name: AGV Database
     - Host: db
     - Port: 5432
     - Database: agv_database12
     - Username: agv
     - Password: 123456hadz

### Option 2: Manual Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agv_3.git
   cd agv_3/Server/web_management
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set environment variable:
   ```bash
   # On Windows
   set DJANGO_SETTINGS_MODULE=web_management.settings
   
   # On macOS/Linux
   export DJANGO_SETTINGS_MODULE=web_management.settings
   ```

6. Start the application:
   ```bash
   uvicorn web_management.asgi:application --host 127.0.0.1 --port 8000 --lifespan off
   ```

## Configuration

### Environment Variables
The application can be configured using the following environment variables:

- `DJANGO_SETTINGS_MODULE=web_management.settings`
- `POSTGRES_DB=agv_database12`
- `POSTGRES_USER=agv`
- `POSTGRES_PASSWORD=123456hadz`
- `POSTGRES_HOST=db` (use `localhost` for manual setup)
- `POSTGRES_PORT=5432`
- `MQTT_SERVER=mosquitto` (use appropriate address for manual setup)
- `MQTT_PORT=1883`

### Docker Compose Configuration
For Docker deployment, you can modify the settings in the `docker-compose.yml` file.

## Database Management

### Database Setup
The system uses PostgreSQL as its primary database. When using Docker, the database is automatically configured and migrations are applied.

### Accessing and Managing the Database
1. Using pgAdmin (recommended):
   - Connect to pgAdmin as described in the installation section
   - Use the GUI to manage tables, run queries, and export/import data

2. Direct SQL Access (for advanced users):
   - Connect to the database container:
     ```bash
     docker exec -it web_management_db_1 bash
     ```
   - Launch PostgreSQL client:
     ```bash
     psql -U agv -d agv_database12
     ```

### Database Maintenance
To clear data and reset identity counters:
```sql
TRUNCATE TABLE table_name RESTART IDENTITY;
VACUUM table_name;
```

## Troubleshooting

### Port Conflicts
If you encounter port conflicts:

1. Find the process using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/macOS
   lsof -i :8000
   ```

2. Kill the process:
   ```bash
   # Windows
   taskkill /PID <PID> /F
   
   # Linux/macOS
   kill -9 <PID>
   ```

### Docker Issues
- Restart containers: `docker-compose down && docker-compose up -d`
- Check logs: `docker-compose logs -f web`
- Rebuild containers: `docker-compose build --no-cache`

### Database Connectivity Issues
1. Verify database container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Ensure correct connection settings in your configuration


