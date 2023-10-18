# Build API endpoints using FastAPI-DynamoDBLocal

This project uses FastAPI and DynamoDB together in a Docker container. 

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repo

   ```bash
   git clone https://github.com/ChirawatCh/fastapi-dynamodb.git
   cd fastapi-dynamodb
   ```

2. Build the Docker image

   ```bash
   docker-compose build
   ```

3. Start the container

   ```bash
   docker-compose up -d
   ```

This will start the FastAPI app and DynamoDB local container. The FastAPI app will be available at http://localhost:8000.

DynamoDB local will be available on port 8000.

### Loading Data

To load sample data into DynamoDB, run:

```
docker-compose run --rm app python data/import_csv.py
```

This will import the `projects.csv` file into a DynamoDB table called `projects`.

The FastAPI application is preconfigured to connect to the `projects` table.

### Architecture

The Docker Compose file runs two containers:

- `app` - The FastAPI application
- `dynamodb-local` - The official DynamoDB local container

The app container mounts the `data` and `src` directories, so you can modify the Python code without having to rebuild the image.

### Development

To run the FastAPI app independently for development:

```
uvicorn src.main:app --reload
```

Make sure DynamoDB local is still running in a separate terminal.

The app is configured to connect to DynamoDB local on `http://dynamodb-local:8000`.

Let me know if you have any other questions!