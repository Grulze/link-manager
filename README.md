# Link Manager API

This project is a Django-based RESTful API that allows users to manage their personal collections of links. Users can
create accounts, authenticate, and manage collections containing various types of links. The API automatically fetches
link metadata from Open Graph tags or fallback HTML tags if Open Graph data is not available.

## Key Features

### 1. User Authentication and Account Management
- **Registration**: Users can register by providing an email and password.
- **Password Management**: Users can change or reset their passwords.
- **Login**: Users can authenticate to access and manage their links and collections.

### 2. Link Management
- **Add Links**: Users can add a link by providing only a URL; the API automatically retrieves metadata.
- **Edit Links**: Users can update link details.
- **Delete Links**: Users can delete unwanted links.
- **Link Metadata**: The API gathers metadata such as the title, description, preview image, and type from the link’s Open
Graph data or standard HTML tags as a fallback.

### 3. Collection Management
- **Add Collections**: Users can create collections with a title and optional description.
- **Edit Collections**: Users can update collection details.
- **Delete Collections**: Users can delete collections they no longer need.
- **View Collections**: Collections can contain multiple links, and a single link can belong to multiple collections. Users
can view all their collections along with the associated links.

## Quick Start

### Installation

**Clone the repository**:
   ```sh
   git clone https://github.com/Grulze/link-manager
   ```

### Start with Docker

1. **Before Starting**:
    Make sure you have the following installed on your local machine:
   - [Docker](https://www.docker.com/)

2. **Build Docker containers**:
   Run the following command to build the Docker containers for the app, PostgreSQL, and Redis.
   ```sh
   docker compose build
   ```

3. **Start the services**:
   Bring up the application and the associated services (PostgreSQL and Redis) using Docker Compose.
   ```sh
   docker compose up
   ```

4. **Stopping the services**:
   To stop the application and services, press `Ctrl+C` in the terminal where app is running, or run:
    ```sh
    docker compose down
    ```
   
### Start without Docker

1. **Before Starting**:
   Make sure you have the following installed on your local machine:
   - [PostgreSQL](https://www.postgresql.org)

2. **Check the parameters**:
   Check the settings for connecting the services, and if they do not match, edit them.
   ```sh
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASS=postgres
   ```

3. **Installing dependencies**:
   Run the command.
   ```sh
   pip install -r requirements.txt
   ```

4. **Start the services**:
   Bring up the associated services (PostgreSQL).
   And then run the application.
   ```sh
   python manage.py runserver
   ```
   
5. **Stopping the services**:
   To stop the application , press `Ctrl+C` in the terminal where app is running.


### The application will now be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

**Access API documentation**:
   FastAPI provides interactive API documentation, which can be accessed at:
   - **Swagger UI**: [http://127.0.0.1:8000/api/v1/swagger/](http://127.0.0.1:8000/api/v1/swagger/)
   - **ReDoc**: [http://127.0.0.1:8000/api/v1/redoc/](http://127.0.0.1:8000/api/v1/redoc/)

## Project Foreword

To access information, you need to authenticate, obtain a token, and insert it into the appropriate field in Swagger.