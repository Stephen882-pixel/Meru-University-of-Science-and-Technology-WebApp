

# Meru University Science Innovators Club API Documentation

## Introduction
The Meru University Science Innovators Club API provides a set of endpoints for managing events, subscribing to the newsletter, and contacting the club administrators. This API is designed to be used by the club's administrators and members.

## Authentication
To access certain protected endpoints, such as sending the newsletter, authentication is required. The API uses a JWT-based authentication system with access and refresh tokens.

### Obtaining Access and Refresh Tokens
To obtain an access and refresh token, make a POST request to the `/api/token/` endpoint with the following payload:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

The response will contain the access and refresh tokens:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

To use the access token, include it in the `Authorization` header of your requests as a Bearer token:

```
Authorization: Bearer <access_token>
```

If the access token expires, you can use the refresh token to obtain a new access token by making a POST request to the `/api/token/refresh/` endpoint with the following payload:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Endpoints

### Events

#### Create an Event
**Endpoint**: `POST /events/`
**Request Body**:
```json
{
    "name": "Python Programming Workshop",
    "title": "Beginner's Guide to Python",
    "description": "Learn the fundamentals of Python programming in this hands-on workshop. Suitable for those new to coding.",
    "image": "base64_image_string_goes_here",
    "date": "2023-06-15T10:00:00Z",
    "location": "Online",
    "organizer": "John Doe",
    "contact_email": "info@example.com",
    "is_virtual": true,
    "registration_link": "https://example.com/python-workshop-registration"
}
```

#### List All Events
**Endpoint**: `GET /events/`

#### Update an Event
**Endpoint**: `PUT /events/{id}/`
**Request Body**:
```json
{
    "name": "AI Ethics Workshop",
    "title": "Navigating the Ethical Landscape of AI",
    "description": "Explore the key ethical considerations in the development and deployment of artificial intelligence systems.",
    "image": "base64_image_string_goes_here",
    "date": "2023-09-01T09:00:00Z",
    "location": "Hybrid (in-person and virtual)",
    "organizer": "Jane Smith",
    "contact_email": "jane@example.com",
    "is_virtual": true,
    "registration_link": "https://example.com/ai-ethics-workshop"
}
```

#### Partially Update an Event
**Endpoint**: `PATCH /events/{id}/`
**Request Body**:
```json
{
    "organizer": "Collins Munene",
    "contact_email": "collinsmunene9@gmail.com"
}
```

#### Delete an Event
**Endpoint**: `DELETE /events/{id}/`

### Newsletter

#### Subscribe to the Newsletter
**Endpoint**: `POST /subscribe/`
**Request Body**:
```json
{
    "email": "newtonwamiti0@gmail.com"
}
```

#### Send a Newsletter
**Endpoint**: `POST /newsletter/`
**Request Body**:
```json
{
    "subject": "Newsletter Title",
    "message": "Newsletter content goes here..."
}
```

### Contact Us
**Endpoint**: `POST /contact/`
**Request Body**:
```json
{
    "message_name": "Onyango Stephen Omondi",
    "message_email": "stephenondeyo0@gmail.com",
    "message": "Subject: Assistance Required for FileNotFoundError in Django Project\nDear Admin,\nI hope this message finds you well. I am reaching out regarding an issue I encountered while\nworking on my Django project, specifically related to file handling in my settings configuration.\nBest regards,\nStephen\n"
}
```



# Blog API Documentation for Meru University Science Innovators Club Website

## Introduction

This API allows users to register, log in, create, view, update, and delete blog posts. It uses JWT authentication to secure endpoints and ensures that only authenticated users can perform certain actions like creating, updating, or deleting blog posts.

---

## Base URL
`http://127.0.0.1:8000/api/`

---

## Endpoints

### 1. **User Registration**
**Endpoint**: `account/register/`  
**Method**: POST  
**Description**: Allows a user to create an account.  

**Request Body**:  
```json
{
  "firstname": "string",
  "lastname": "string",
  "email": "string",
  "username": "string",
  "password": "string"
}
```

**Response Example**:  
```json
{
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe"
  }
}
```

---

### 2. **User Login**
**Endpoint**: `account/login/`  
**Method**: POST  
**Description**: Authenticates a user and returns access and refresh tokens.  

**Request Body**:  
```json
{
  "email": "string",
  "password": "string"
}
```

**Response Example**:  
```json
{
  "message": "Login successful",
  "data": {
    "token": {
      "refresh": "refresh_token_here",
      "access": "access_token_here"
    }
  }
}
```

---

### 3. **Create Blog Post**
**Endpoint**: `home/blog/`  
**Method**: POST  
**Description**: Allows an authenticated user to create a new blog post.  

**Headers**:  
`Authorization: Bearer <access_token>`

**Request Body**:  
```json
{
  "title": "string",
  "blog_text": "string",
  "image": "file"
}
```

**Response Example**:  
```json
{
  "message": "Blog post created successfully",
  "blog": {
    "id": 1,
    "title": "My First Blog",
    "blog_text": "This is the content of the blog.",
    "image_url": "http://127.0.0.1:8000/media/uploads/blog_image.jpg",
    "author": "johndoe",
    "created_at": "2024-11-16T12:00:00Z"
  }
}
```

---

### 4. **View Blog Posts**
**Endpoint**: `home/blog/`  
**Method**: GET  
**Description**: Retrieves all blog posts.  

**Response Example**:  
```json
[
  {
    "id": 1,
    "title": "My First Blog",
    "blog_text": "This is the content of the blog.",
    "image_url": "http://127.0.0.1:8000/media/uploads/blog_image.jpg",
    "author": "johndoe",
    "created_at": "2024-11-16T12:00:00Z"
  }
]
```

---

### 5. **Update Blog Post**
**Endpoint**: `home/blog/`  
**Method**: PUT  
**Description**: Allows an authenticated user to update their blog post.  

**Headers**:  
`Authorization: Bearer <access_token>`

**Request Body**:  
```json
{
  "uid": "string",
  "title": "string",
  "blog_text": "string"
}
```

**Response Example**:  
```json
{
  "message": "Blog post updated successfully",
  "blog": {
    "id": 1,
    "title": "Updated Blog Title",
    "blog_text": "Updated blog content."
  }
}
```

---

### 6. **Delete Blog Post**
**Endpoint**: `home/blog/`  
**Method**: DELETE  
**Description**: Allows an authenticated user to delete their blog post.  

**Headers**:  
`Authorization: Bearer <access_token>`

**Request Body**:  
```json
{
  "uid": "string"
}
```

**Response Example**:  
```json
{
  "message": "Blog post deleted successfully"
}
```

---

## JWT Authentication

- **Access Token**: Required for actions like creating, updating, or deleting blog posts.  
- **Refresh Token**: Use this to generate a new access token when it expires.  

---

## Example Login Response
Upon logging in, the user receives the following response:  
```json
{
  "message": "Login successful",
  "data": {
    "token": {
      "refresh": "refresh_token_here",
      "access": "access_token_here"
    }
  }
}
```

Use the `access_token` in the `Authorization` header as follows:  
`Authorization: Bearer <access_token>`

---

  



