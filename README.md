# Django REST API - Senior Backend Software Engineer - Technical Challenge

This is a Django REST API that's containerized with Docker.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker and Docker Compose installed on your machine. 

### Running the project

1. Build the Docker image:

```bash
docker-compose build
```

2. Start the Docker container:

```bash
docker-compose up -d
```

3. Make Django migrations:

```bash
docker-compose exec web python manage.py makemigrations
```

4. Apply Django migrations:

```bash
docker-compose exec web python manage.py migrate --noinput
```

Now, your Django REST API should be up and running in a Docker container.

5. Swagger 

Access the Swagger documentation at:

```bash
http://localhost:8000/swagger/
```
6. Postman Collection

Access the Postman collection at:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://bold-meteor-776316.postman.co/collection/13893557-1630e338-089f-4d2d-a949-fd192f77cfb5?source=rip_markdown)