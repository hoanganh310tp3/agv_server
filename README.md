# AGV Server

A sophisticated server application for managing and controlling Automated Guided Vehicles (AGVs) in an industrial environment. This project implements advanced algorithms for path planning, collision avoidance, and resource optimization.

## Features

- Real-time AGV fleet management
- Dynamic path planning and routing
- Collision avoidance using Dynamic Shared Point Allocation (DSPA)
- Material handling and inventory management
- Battery and energy consumption monitoring
- Automated parking management
- Web-based monitoring and control interface

## Technology Stack

- **Backend Framework**: Django with FastAPI integration
- **Database**: PostgreSQL
- **Real-time Communication**: WebSocket
- **Development Tools**: Python, Django ORM

## Core Algorithms (BLL - Business Logic Layer)

1. **Collision Avoidance (DSPA)**
   - Dynamic Shared Point Allocation for preventing AGV collisions
   - Real-time path adjustment and waiting time calculation
   - Deadlock detection and resolution (heading-on and loop deadlocks)

2. **Path Planning**
   - Optimal route calculation considering distance and energy consumption
   - Dynamic obstacle avoidance
   - Traffic management in shared spaces

3. **Resource Management**
   - Intelligent AGV selection based on current load and position
   - Energy consumption optimization
   - Automated parking space allocation

4. **Scheduling System**
   - Priority-based task scheduling
   - Real-time schedule adjustment
   - Conflict resolution in multi-AGV scenarios

## Getting Started

### Prerequisites

1. Python virtual environment
2. PostgreSQL database
3. Required Python packages

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix
   venv\Scripts\activate     # For Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variable:
   ```bash
   # Windows
   set DJANGO_SETTINGS_MODULE=web_management.settings
   
   # Unix
   export DJANGO_SETTINGS_MODULE=web_management.settings
   ```

4. Start the server:
   ```bash
   uvicorn web_management.asgi:application --host 127.0.0.1 --port 8000 --lifespan off
   ```

## Database Management

### Renaming Applications
If you need to rename Django applications, use these SQL commands:
```sql
UPDATE django_content_type SET app_label = 'new_app_name' WHERE app_label = 'old_app_name';
UPDATE django_migrations SET app = 'new_app_name' WHERE app = 'old_app_name';
```

### Cleaning Database Tables
To clean and reset a table:
```sql
TRUNCATE TABLE table_name RESTART IDENTITY;
VACUUM table_name;
```

## Troubleshooting

### Port Management
To check ports in use:
```bash
netstat -ano | findstr :port_number
```

To kill a process using a specific port:
```bash
taskkill /PID <PID> /F
```

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

This project is proprietary and confidential. All rights reserved.
