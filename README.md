# Pokemon API - Prvolt Technical Test

A Django REST API that provides Pokemon data by interfacing with the PokeAPI. This project demonstrates API development skills and external service integration.

## Features

- **Pokemon by ID**: Get detailed Pokemon information by ID
- **Pokemon by Name**: Search Pokemon by name
- **Pokemon List**: Paginated list of all Pokemon
- **Pokemon by Type**: Get Pokemon names filtered by type
- **Health Check**: API status endpoint
- **Interactive Documentation**: Swagger UI and ReDoc available

## Tech Stack

- Django 5.0+
- Django REST Framework 3.14+
- drf-spectacular (OpenAPI/Swagger)
- httpx (async HTTP client)
- django-cors-headers

## Setup Instructions

### Prerequisites

- Python 3.10+
- uv

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prvolt_test
   ```

2. **Install dependencies**
   ```bash

   uv sync

   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI Schema**: http://localhost:8000/schema/

## External Dependencies

This project integrates with [PokeAPI](https://pokeapi.co/), a free RESTful Pokemon API. No API key required.
