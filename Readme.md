# Meru University Science Innovators Club API

## 🚀 Project Overview

The Meru University Science Innovators Club API is a comprehensive digital platform designed to empower students and administrators of the Science Innovators Club. This robust API provides a suite of functionalities that foster collaboration, knowledge sharing, and community engagement.

### Key Objectives
- Facilitate seamless communication among club members
- Provide a platform for sharing scientific insights and innovations
- Manage club events, articles, and memberships
- Ensure secure and efficient user interactions

## ✨ Features

- 🔐 Secure User Authentication
- 👤 User Profile Management
- 📅 Event Registration System
- 📝 Article and Blog Publishing
- 📰 Newsletter Subscription
- 🔒 JWT-based Authorization

## 🛠 Technology Stack

- **Backend:** Django
- **Authentication:** Django Rest Framework
- **Token Management:** JSON Web Tokens (JWT)
- **Database:** PostgreSQL/SQLite
- **API Documentation:** Swagger/OpenAPI

## 📡 Authentication Endpoints

### 1. User Registration
**Endpoint:** `POST /api/account/register/`

**Request Body:**
```json
{
    "firstname": "Steven",
    "lastname": "Omondi",
    "email": "stephenondeyo0@gmail.com",
    "username": "Stephen883",
    "password": "Kundan@123456",
    "registration_no": "CT201/106104/22",
    "course": "BCS"
}
```

**Response:**
```json
{
    "message": "Account created successfully",
    "user_id": 5
}
```

### 2. User Login
**Endpoint:** `POST /api/account/login/`

**Request Body:**
```json
{
    "email": "stephenondeyo0@gmail.com",
    "password": "Kundan@123456"
}
```

**Response:**
```json
{
    "status": "success",
    "tokens": {
        "refresh": "...",
        "access": "..."
    },
    "user": {
        "id": 5,
        "email": "stephenondeyo0@gmail.com"
    }
}
```

### 3. Change Password
**Endpoint:** `POST /api/account/change-password/`

**Request Body:**
```json
{
    "old_password": "Kundan@123456",
    "new_password": "Kundan@12345",
    "confirm_password": "Kundan@12345"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Password changed successfully"
}
```

### 4. Token Verification
**Endpoint:** `POST /api/account/token/verify/`

**Request Body:**
```json
{
    "token": "access_token_here"
}
```

**Response:** Empty JSON object `{}`

### 5. Token Refresh
**Endpoint:** `POST /api/account/token/refresh/`

**Request Body:**
```json
{
    "refresh": "refresh_token_here"
}
```

**Response:**
```json
{
    "access": "new_access_token"
}
```

## 🔐 Authentication Workflow

1. Register a new account
2. Login to receive access and refresh tokens
3. Use access token for authenticated requests
4. Refresh token when access token expires

## 📝 Blog Endpoints

### 1. Add a Blog
**Endpoint:** `POST /api/home/blog/`

**Request Body (Form Data):**
- `title`: Blog title
- `blog_text`: Blog content
- `main_image`: Image file for the blog

**Response Body:**
```json
{
    "data": {
        "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21",
        "title": "My First Blog",
        "blog_text": "This is the content of my first blog.",
        "main_image": "/blogs/image.png",
        "user": 5
    },
    "message": "blog created successfully"
}
```

### 2. View Blogs
**Endpoint:** `GET /api/home/blog/`

**Response Body:**
```json
[
    {
        "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21",
        "title": "My First Blog",
        "blog_text": "This is the content of my first blog.",
        "main_image": "/blogs/image.png",
        "user": 5
    },
    {
        "uid": "b19dae4c-0f05-4167-a287-c5362b09ec22",
        "title": "Another Blog",
        "blog_text": "This is another blog.",
        "main_image": "/blogs/another_image.png",
        "user": 5
    }
]
```

### 3. Search Blogs
**Endpoint:** `GET /api/home/blog/?search=<search_query>`

**Example URL:**
`http://127.0.0.1:8000/api/home/blog/?search=recent years, a green revolution has been quietly blooming in our concrete jungles`

**Response Body:**
```json
[
    {
        "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21",
        "title": "My First Blog",
        "blog_text": "This is the content of my first blog.",
        "main_image": "/blogs/image.png",
        "user": 5
    }
]
```

### 4. Update Blog
**Endpoint:** `PATCH /api/home/blog/`

**Request Body:**
```json
{
    "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21",
    "title": "5 Essential Skills Every Aspiring Backend Developer Needs(updated!!!)",
    "blog_text": "Backend development is the engine behind any successful application. Aspiring developers often focus on mastering programming languages like Java, Python, or Node.js. But what sets a great backend engineer apart? Beyond coding, you'll need a deep understanding of database management, API design, cloud platforms, security practices, and scalability strategies. This blog dives into each of these skills, providing resources and examples to help you stand out in the competitive tech landscape(updated)"
}
```

**Response Body:**
```json
{
    "data": {
        "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21",
        "title": "5 Essential Skills Every Aspiring Backend Developer Needs(updated!!!)",
        "blog_text": "Backend development is the engine behind any successful application. Aspiring developers often focus on mastering programming languages like Java, Python, or Node.js. But what sets a great backend engineer apart? Beyond coding, you'll need a deep understanding of database management, API design, cloud platforms, security practices, and scalability strategies. This blog dives into each of these skills, providing resources and examples to help you stand out in the competitive tech landscape(updated)",
        "main_image": "/blogs/Screenshot_from_2025-01-24_14-36-56_O0isWQ4.png",
        "user": 5
    },
    "message": "blog updated successfully"
}
```

### 5. Delete Blog
**Endpoint:** `DELETE /api/home/blog/`

**Request Body:**
```json
{
    "uid": "a09cae4c-0f05-4167-a287-c5362b09ec21"
}
```

**Response Body:**
```json
{
    "data": {},
    "message": "blog deleted successfully"
}
```

### 📌 Notes
- Ensure the `uid` matches the blog you want to modify or remove
- `main_image` field contains the URL path to the uploaded image


# Events Management API Documentation

## Overview
This API allows you to manage events and handle event registrations. It provides endpoints for creating, reading, updating, and deleting events, as well as managing event registrations and exporting registration data.

## Base URL
```
http://127.0.0.1:8000
```

## API Endpoints

### Events

#### 1. Create an Event
- **Endpoint:** `POST /events/`
- **Description:** Create a new event
- **Request Body:**
```json
{
    "name": "AI & Machine Learning Summit",
    "title": "The Future of AI: From Theory to Implementation",
    "description": "An intensive summit focused on practical applications of AI and ML, featuring workshops on TensorFlow, PyTorch, and real-world case studies from industry leaders.",
    "image": "base64_image_string_goes_here",
    "date": "2024-11-15T09:00:00Z",
    "location": "Innovation Center, San Francisco",
    "organizer": "TechMinds Institute",
    "contact_email": "ai.summit@example.com",
    "is_virtual": false,
    "registration_link": "https://example.com/ai-summit-2024"
}
```
- **Response Body:**
```json
{
    "id": 5,
    "name": "AI & Machine Learning Summit",
    "title": "The Future of AI: From Theory to Implementation",
    "description": "An intensive summit focused on practical applications of AI and ML, featuring workshops on TensorFlow, PyTorch, and real-world case studies from industry leaders.",
    "image": "event_images/default.png",
    "date": "2024-11-15T09:00:00Z",
    "location": "Innovation Center, San Francisco",
    "organizer": "TechMinds Institute",
    "contact_email": "ai.summit@example.com",
    "is_virtual": false,
    "registration_link": "https://example.com/ai-summit-2024"
}
```

#### 2. List Events
- **Endpoint:** `GET /events/`
- **Description:** Retrieve a list of all events
- **Response Body:**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Web Development Bootcamp",
            "title": "Master Frontend and Backend Basics",
            "description": "A thought-provoking session discussing the ethical challenges and societal impacts of AI technologies, featuring leading experts in the field.",
            "image": "event_images/default.png",
            "date": "2024-12-15T17:00:00Z",
            "location": "Virtual Event",
            "organizer": "AI for Good Initiative",
            "contact_email": "aiethics@example.com",
            "is_virtual": true,
            "registration_link": "https://example.com/ai-ethics-registration"
        },
        // ... more events
    ]
}
```

#### 3. Update an Event
- **Endpoint:** `PUT /events/{id}/`
- **Description:** Update all fields of an existing event
- **Request Body:**
```json
{
    "name": "AI Ethics and Society",
    "title": "Exploring Ethical Implications of Artificial Intelligence",
    "description": "A thought-provoking session discussing the ethical challenges and societal impacts of AI technologies, featuring leading experts in the field.",
    "image": "base64_image_string_goes_here",
    "date": "2024-12-15T17:00:00Z",
    "location": "Virtual Event",
    "organizer": "AI for Good Initiative",
    "contact_email": "aiethics@example.com",
    "is_virtual": true,
    "registration_link": "https://example.com/ai-ethics-registration"
}
```
- **Response Body:**
```json
{
    "id": 5,
    "name": "AI Ethics and Society",
    "title": "Exploring Ethical Implications of Artificial Intelligence",
    "description": "A thought-provoking session discussing the ethical challenges and societal impacts of AI technologies, featuring leading experts in the field.",
    "image": "event_images/default.png",
    "date": "2024-12-15T17:00:00Z",
    "location": "Virtual Event",
    "organizer": "AI for Good Initiative",
    "contact_email": "aiethics@example.com",
    "is_virtual": true,
    "registration_link": "https://example.com/ai-ethics-registration"
}
```

#### 4. Partial Update an Event
- **Endpoint:** `PATCH /events/{id}/`
- **Description:** Update specific fields of an existing event
- **Request Body:**
```json
{
    "name": "Web Development Bootcamp(updated!!!)",
    "title": "Master Frontend and Backend Basics(updated)"
}
```
- **Response Body:**
```json
{
    "id": 5,
    "name": "Web Development Bootcamp(updated!!!)",
    "title": "Master Frontend and Backend Basics(updated)",
    "description": "A thought-provoking session discussing the ethical challenges and societal impacts of AI technologies, featuring leading experts in the field.",
    "image": "event_images/default.png",
    "date": "2024-12-15T17:00:00Z",
    "location": "Virtual Event",
    "organizer": "AI for Good Initiative",
    "contact_email": "aiethics@example.com",
    "is_virtual": true,
    "registration_link": "https://example.com/ai-ethics-registration"
}
```

#### 5. Delete an Event
- **Endpoint:** `DELETE /events/{id}/`
- **Description:** Remove an event
- **Response:** 204 No Content

### Event Registrations

#### 1. Register for an Event
- **Endpoint:** `POST /event-registrations/`
- **Description:** Register a participant for an event
- **Request Body:**
```json
{
    "full_name": "Stephen Onyango",
    "email": "ondeyostephen0@gmail.com",
    "age_bracket": "22-24",
    "course": "BCS",
    "educational_level": "year_4",
    "event": "5"
}
```
- **Response Body:**
```json
{
    "uid": "c97249b3-a73d-4a82-8c20-ce6ca0fc1db6",
    "full_name": "Stephen Onyango",
    "email": "stephenonyango@students.ac.ke",
    "age_bracket": "22-24",
    "course": "BCS",
    "educational_level": "year_4",
    "phone_number": null,
    "registration_timestamp": "2025-01-31T12:26:25.011601Z",
    "ticket_number": "bcee1e25-2b95-49d3-a19a-79842ffa39f0",
    "event": 5
}
```

#### 2. List Registrations
- **Endpoint:** `GET /event-registrations/`
- **Description:** Retrieve all event registrations
- **Response Body:**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "uid": "e7eca62f-974c-4ba1-a825-88973b886642",
            "full_name": "Stephen Omondi",
            "email": "ondeyostephen0@gmail.com",
            "age_bracket": "22-24",
            "course": "BCS",
            "educational_level": "year_4",
            "phone_number": null,
            "registration_timestamp": "2025-01-24T19:10:51.507585Z",
            "ticket_number": "4107c4ad-8937-4e67-a777-4b1c18a6c024",
            "event": 1
        },
        // ... more registrations
    ]
}
```

#### 3. Export Registrations
- **Endpoint:** `GET /event-registrations/export_registrations/`
- **Query Parameters:** `event_id={id}`
- **Description:** Export registration data for a specific event to a spreadsheet
- **Response:** Returns a downloadable spreadsheet file

## Data Models

### Event
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Auto-generated primary key |
| name | String | Name of the event |
| title | String | Title/subtitle of the event |
| description | Text | Detailed description |
| image | File/String | Event image |
| date | DateTime | Event date and time (ISO format) |
| location | String | Physical or virtual location |
| organizer | String | Event organizer name |
| contact_email | Email | Contact email for inquiries |
| is_virtual | Boolean | Whether the event is virtual |
| registration_link | URL | External registration link |

### Event Registration
| Field | Type | Description |
|-------|------|-------------|
| uid | UUID | Unique identifier for registration |
| full_name | String | Participant's full name |
| email | Email | Participant's email |
| age_bracket | String | Age range of participant |
| course | String | Course/program of study |
| educational_level | String | Current education level |
| phone_number | String | Optional contact number |
| registration_timestamp | DateTime | When registration occurred |
| ticket_number | UUID | Unique ticket identifier |
| event | Integer | Reference to event ID |

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 404: Not Found
- 500: Server Error

## Usage Examples

### Creating an Event
```bash
curl -X POST http://127.0.0.1:8000/events/ \
-H "Content-Type: application/json" \
-d '{
    "name": "AI & Machine Learning Summit",
    "title": "The Future of AI: From Theory to Implementation",
    "description": "An intensive summit focused on practical applications of AI and ML",
    "date": "2024-11-15T09:00:00Z",
    "location": "Innovation Center, San Francisco",
    "organizer": "TechMinds Institute",
    "contact_email": "ai.summit@example.com",
    "is_virtual": false,
    "registration_link": "https://example.com/ai-summit-2024"
}'
```

### Registering for an Event
```bash
curl -X POST http://127.0.0.1:8000/event-registrations/ \
-H "Content-Type: application/json" \
-d '{
    "full_name": "Stephen Onyango",
    "email": "ondeyostephen0@gmail.com",
    "age_bracket": "22-24",
    "course": "BCS",
    "educational_level": "year_4",
    "event": "5"
}'
```