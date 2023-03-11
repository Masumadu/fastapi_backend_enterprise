# Backend Directory Structure With Fastapi, Postgres And Redis For Rest API Development

### This is a directory structure for developing backend application using fastapi and postgres

### This directory structure is built with Python Poetry and uses the Factory Design Pattern with Clean Code Practices

#### The directory structure incorporates pre-commit hooks with several python linters

### Testing has been incorporated into the directory with pytest for unit tests

## DEPENDENCIES
- Python
- Poetry
- Postgres
- Redis
- Docker
- Docker-Compose

# USAGE:
  ## Local Development Setup
  - clone repository to your preferred location on your local development
  - create a file '.env' in the project root directory
  - set environment variables by referencing file 'env'
  - from the terminal, change directory to your project root directory
  - activate a python virtual environment in your terminal
  - run
    1. `poetry install` to install dependencies
    2. `uvicorn app.asgi:app` to start application
  - visit http://localhost:8000/ to access application
  - run `pytest -v` to run unit tests


  ## Docker Compose Setup
  - clone repository to your preferred location on your local development
  - create a file '.env' in the root directory
  - set environment variables by referencing file 'env'
  - from the terminal, change directory to your root directory
  - run
    1. `docker-compose up --build` to start application with docker
- visit http://localhost:5000/ to access application


The structure can be modified to suit your needs to help kickstart application development fast.
With this directory structure, developers can spend less time thinking about how to structure
a fastapi application with postgres and rather focus on the business logic
