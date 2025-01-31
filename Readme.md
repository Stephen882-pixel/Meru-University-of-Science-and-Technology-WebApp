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