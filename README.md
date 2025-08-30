# Django Advanced Pagination API

A Django REST API project demonstrating advanced pagination techniques with comprehensive error handling and custom pagination classes.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Pagination Types](#pagination-types)
- [Request Parameters](#request-parameters)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)
- [Testing](#testing)

## Overview

This project provides a RESTful API for managing articles with two different pagination implementations:
1. **Standard Pagination** - Basic Django REST framework pagination
2. **Custom Pagination** - Advanced pagination with detailed metadata

## Features

- ✅ Two pagination strategies (Standard & Custom)
- ✅ Comprehensive error handling for invalid parameters
- ✅ Detailed pagination metadata
- ✅ Published articles filtering
- ✅ Configurable page sizes
- ✅ Input validation with descriptive error messages
- ✅ Management command for populating test data

## Installation

### Prerequisites
- Python 3.8+
- Django 5.0+
- Django REST Framework

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assign-pagination
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Populate test data** (Optional)
   ```bash
   python manage.py populate_articles
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Base URL
```
http://localhost:8000/api/articles/
```

### Available Endpoints

| Endpoint | Method | Description | Pagination Type |
|----------|--------|-------------|-----------------|
| `/api/articles/` | GET | List articles with standard pagination | PageNumberPagination |
| `/api/articles/custom-blog` | GET | List articles with custom pagination | CustomArticlePagination |

## Pagination Types

### 1. Standard Pagination (`/api/articles/`)

Uses Django REST Framework's built-in `PageNumberPagination` with:
- Default page size: 15 (configured in settings)
- Simple response format
- Basic error handling

### 2. Custom Pagination (`/api/articles/custom-blog`)

Uses custom `CustomArticlePagination` with:
- Default page size: 8
- Maximum page size: 50
- Enhanced metadata
- Advanced error handling
- Item range information

## Request Parameters

### Query Parameters

| Parameter | Type | Description | Default | Valid Range |
|-----------|------|-------------|---------|-------------|
| `page` | integer | Page number to retrieve | 1 | 1 to total_pages |
| `page_size` | integer | Number of items per page (Custom pagination only) | 8 | 1 to 50 |

### Examples
```bash
# Get first page
GET /api/articles/?page=1

# Get specific page
GET /api/articles/?page=3

# Custom pagination with page size
GET /api/articles/custom-blog?page=2&page_size=10
```

## Response Formats

### Standard Pagination Response

```json
{
    "count": 120,
    "next": "http://localhost:8000/api/articles/?page=3",
    "previous": "http://localhost:8000/api/articles/?page=1",
    "results": [
        {
            "id": 1,
            "title": "Sample Article Title",
            "content": "Article content here...",
            "author": "John Doe",
            "created_at": "2024-01-15T10:30:00Z",
            "is_published": true
        }
    ]
}
```

### Custom Pagination Response

```json
{
    "page_info": {
        "current_page": 2,
        "total_pages": 15,
        "has_next": true,
        "has_previous": true,
        "next_page": 3,
        "previous_page": 1
    },
    "items_info": {
        "count_on_page": 8,
        "total_items": 120,
        "page_size": 8,
        "item_range": {
            "start": 9,
            "end": 16
        }
    },
    "links": {
        "next": "http://localhost:8000/api/articles/custom-blog?page=3",
        "previous": "http://localhost:8000/api/articles/custom-blog?page=1"
    },
    "results": [
        {
            "id": 9,
            "title": "Another Article",
            "content": "Content of the article...",
            "author": "Jane Smith",
            "created_at": "2024-01-14T15:45:00Z",
            "is_published": true
        }
    ]
}
```

### Article Object Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique article identifier |
| `title` | string | Article title (max 100 characters) |
| `content` | string | Article content |
| `author` | string | Author name (max 50 characters) |
| `created_at` | datetime | Article creation timestamp |
| `is_published` | boolean | Publication status |

## Error Handling

The API provides detailed error responses for various scenarios:

### Invalid Page Number

**Status Code:** `404 Not Found`

```json
{
    "error": "Invalid page number",
    "detail": "Page numbers must be positive integers starting from 1.",
    "provided_page": "0"
}
```

### Non-integer Page Parameter

**Status Code:** `404 Not Found`

```json
{
    "error": "Invalid page number",
    "detail": "Page must be a valid integer. Received: \"abc\"",
    "provided_page": "abc"
}
```

### Page Out of Range

**Status Code:** `404 Not Found`

```json
{
    "error": "Page out of range",
    "detail": "Page 100 does not exist.",
    "total_pages": 15,
    "provided_page": 100,
    "valid_range": "1 to 15"
}
```

### Invalid Page Size (Custom Pagination Only)

**Status Code:** `400 Bad Request`

```json
{
    "error": "Invalid page_size parameter",
    "detail": "Page size cannot exceed 50",
    "valid_range": "1 to 50"
}
```

## Usage Examples

### Using cURL

#### Get first page with standard pagination
```bash
curl -X GET "http://localhost:8000/api/articles/"
```

#### Get specific page
```bash
curl -X GET "http://localhost:8000/api/articles/?page=3"
```

#### Get custom pagination with specific page size
```bash
curl -X GET "http://localhost:8000/api/articles/custom-blog?page=2&page_size=12"
```

### Using Python requests

```python
import requests

# Standard pagination
response = requests.get('http://localhost:8000/api/articles/')
data = response.json()

# Custom pagination
response = requests.get(
    'http://localhost:8000/api/articles/custom-blog',
    params={'page': 2, 'page_size': 10}
)
data = response.json()

# Access articles
articles = data['results']
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Author: {article['author']}")
```

### Using JavaScript (Fetch API)

```javascript
// Standard pagination
fetch('http://localhost:8000/api/articles/?page=1')
    .then(response => response.json())
    .then(data => {
        console.log('Articles:', data.results);
        console.log('Total count:', data.count);
    });

// Custom pagination
fetch('http://localhost:8000/api/articles/custom-blog?page=1&page_size=5')
    .then(response => response.json())
    .then(data => {
        console.log('Articles:', data.results);
        console.log('Page info:', data.page_info);
        console.log('Items info:', data.items_info);
    });
```

## Testing

### Manual Testing

1. **Test standard pagination:**
   ```bash
   curl "http://localhost:8000/api/articles/"
   ```

2. **Test custom pagination:**
   ```bash
   curl "http://localhost:8000/api/articles/custom-blog?page_size=5"
   ```

3. **Test error scenarios:**
   ```bash
   # Invalid page number
   curl "http://localhost:8000/api/articles/?page=0"

   # Page out of range
   curl "http://localhost:8000/api/articles/?page=999"

   # Invalid page size
   curl "http://localhost:8000/api/articles/custom-blog?page_size=100"
   ```

### Running Unit Tests

```bash
python manage.py test blog.tests
```

## Project Structure

```
assign-pagination/
├── blog/
│   ├── management/commands/
│   │   └── populate_articles.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── pagination.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3
└── README.md
```

## Configuration

### Settings

Key settings in `config/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15
}
```

### Custom Pagination Settings

In `blog/pagination.py`:

```python
class CustomArticlePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 50
```
## Feel Free to Contact

Email: [kumarpriyanshu.py@gmil.com](mailto:kumarpriyanshu.py@gmil.com)
