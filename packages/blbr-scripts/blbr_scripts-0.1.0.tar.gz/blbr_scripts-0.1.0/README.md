# BLBR Scripts Docker Setup

This directory contains the Docker configuration for running the BLBR scripts with scheduled execution.

## Overview

The setup includes:

1. **Dockerfile**: Configures a Python environment with cron for scheduled task execution
2. **docker-compose.yml**: Orchestrates the scripts container and MongoDB

## Scheduled Tasks

By default, the following sequence runs daily at 7:00 PM IST (19:30 server time):

```
python run_step.py download
python run_step.py trend
python run_step.py mongodb
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system

### Running

```bash
# Start the containers (pulls image from Docker Hub)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

### Testing the Scripts Manually

To run scripts manually without waiting for the scheduled time:

```bash
# Execute into the container
docker exec -it blbr-scripts bash

# Run scripts manually
python run_step.py download
python run_step.py trend
python run_step.py mongodb
```

## Configuration

### Modifying the Schedule

The schedule is configured in the Docker image to run at 7:30 PM IST every day. 

If you need to modify the schedule, you'll need to:

1. Fork the repository containing the Dockerfile
2. Update the cron expression
3. Build and publish your own image
4. Update the docker-compose.yml to use your custom image

### Volume Mounts

The Docker setup uses the following volume mounts:

- `./logs:/app/logs`: Persists log files from the script execution
- `./data:/app/data`: Persists data files
- `/tmp/blbr:/tmp/blbr`: Maps the temporary directory used during processing
- `mongodb_data:/data/db`: Persists the MongoDB data

## Database Access

MongoDB is exposed on port 27017 and can be accessed:

- From host: `mongodb://localhost:27017`
- From other containers: `mongodb://mongodb:27017`
