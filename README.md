# Dev environment for FastAPI-DynamoDB-Local

Welcome to the FastAPI-DynamoDBLocal project, where we combine the power of FastAPI and DynamoDB within a Docker container to create efficient API endpoints.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Docker
- Docker Compose

### Installation

1. Clone the Repository

   ```bash
   git clone https://github.com/ChirawatCh/fastapi-dynamodb.git
   cd fastapi-dynamodb
   ```

2. Build the Docker Image and Start the Container

   ```bash
   docker-compose up -d
   ```

This command will initiate the FastAPI application and DynamoDB local container. You can access the FastAPI app at [http://localhost](http://localhost).

Additionally, the system will automatically import data from the `projects.csv` file into a DynamoDB table named `ProjectHours`.

The FastAPI application is preconfigured to interact with the `ProjectHours` table, ensuring seamless data operations.

**Swagger UI**

You can access the Swagger documentation for the API by visiting [http://localhost/docs](http://localhost/docs). Swagger UI provides an interactive and user-friendly way to explore and test the API endpoints.

DynamoDB local can be accessed on port 8000.

Enjoy using FastAPI-DynamoDBLocal for building powerful API endpoints with ease!

### Architecture

The Docker Compose file runs two containers:

- `app-node` - The FastAPI application
- `dynamodb-local` - The official DynamoDB local container

The app container mounts the `data` and `src` directories, so you can modify the Python code without having to rebuild the image.

### Development

To run the FastAPI app independently for development:

```
uvicorn src.main:app --reload
```

Make sure DynamoDB local is still running in a separate terminal.

The app is configured to connect to DynamoDB local on `http://dynamodb-local:8000`.

Enjoy using FastAPI-DynamoDBLocal for building powerful API endpoints with ease!
