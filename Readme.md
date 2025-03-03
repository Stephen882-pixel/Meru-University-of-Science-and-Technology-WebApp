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


## 📡 Authentication Endpoints

### 1. User Registration
**Endpoint:** `POST /api/account/register/`

**Request Body:**
```json
{
    "firstname":"Stephen",
    "lastname":"Ondeyo",
    "email":"stephenonyango@students.must.ac.ke",
    "username":"Stephen885",
    "password":"Kundan@123456",
    "registration_no":"CT201/106107/22",
    "course":"BCS"
}
```

**Response:**
```json
{
    "message": "Account created successfully. Please check your email for verification instructions.",
    "user_data": {
        "username": "stephen885",
        "email": "stephenonyango@students.must.ac.ke",
        "first_name": "Stephen",
        "last_name": "Ondeyo",
        "registration_no": "CT201/106107/22",
        "course": "BCS"
    }
}
```

### 2. User Login
**Endpoint:** `POST /api/account/login/`

**Request Body:**
```json
{
    "email":"newtonwamiti@gmail.com",
    "password":"Kundan@123456"
}

```

**Response:**
```json
{
    "status": "success",
    "tokens": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODQ4MDQ3NCwiaWF0IjoxNzM4Mzk0MDc0LCJqdGkiOiI4YTU0MjY0NDZhMTA0YWNhOWUzNTY1MzQyMzk5OTAxMCIsInVzZXJfaWQiOjIyfQ.ei4R03K8u1crRgFFZtTpHW3jf3dTHpzfquSdPinWctk",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4Mzk3Njc0LCJpYXQiOjE3MzgzOTQwNzQsImp0aSI6ImQ3ZjBjN2VmYmViODRkOTFiNGUyZTQxNjNjOGMyZWZmIiwidXNlcl9pZCI6MjJ9.VhFFPBGCi1zYA_iEiH53U1ZVuYSRYMaKmX9_y95DOFM"
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
### 5. Get User Data
**Endpoint:** `POST /api/account/get-user-data/`

**Make sure you pass the access token in the authorization headers**

**Response Body:**

```
{
    "message": "User data retrieved successfully",
    "user_data": {
        "username": "newton882",
        "email": "newtonwamiti@gmail.com",
        "first_name": "Newton",
        "last_name": "Wamiti",
        "registration_no": "CT201/106106/22",
        "course": "BCS"
    }
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

# Contact API Documentation

## Overview
This API provides endpoints for managing events, event registrations, newsletter subscriptions, and user communications. It enables event organization, participant registration, newsletter management, and handling user inquiries.


## Contact & Newsletter APIs

### Newsletter Management

#### 1. Subscribe to Newsletter
- **Endpoint:** `POST /subscribe/`
- **Description:** Subscribe an email address to the newsletter
- **Request Body:**
```json
{
    "email": "kizahkevinianh001@gmail.com"
}
```
- **Response Body:**
```json
{
    "message": "kizahkevinianh001@gmail.com email was successfully subscribed to our newsletter!"
}
```

#### 2. Send Newsletter
- **Endpoint:** `POST /newsletter/`
- **Description:** Send a broadcast email to all newsletter subscribers
- **Request Body:**
```json
{
    "subject": "Resumption of classes",
    "message": "Classes resuming sooon"
}
```
- **Response Body:**
```json
{
    "message": "Email sent successfully"
}
```

### Contact Form

#### 1. Submit Contact Form
- **Endpoint:** `POST /contact/`
- **Description:** Submit a contact form message for questions, concerns, or feedback
- **Request Body:**
```json
{
    "message_name": "Onyango Stephen Omondi",
    "message_email": "stephenondeyo0@gmail.com",
    "message": "Food waste is a pressing issue, with millions of tons of edible food discarded every year. By taking small steps, we can make a big impact. Start by planning your meals in advance and buying only what you need. Look for stores or apps that sell near-expiry products at discounted prices to save money while preventing waste. Donate excess food to local charities or compost leftovers to reduce landfill waste. Together, we can create a more sustainable and waste-free world."
}
```
- **Response Body:** `200 OK`

## Data Models

### Newsletter Subscription
| Field | Type | Description |
|-------|------|-------------|
| email | Email | Subscriber's email address |

### Newsletter Message
| Field | Type | Description |
|-------|------|-------------|
| subject | String | Email subject line |
| message | Text | Email content |

### Contact Message
| Field | Type | Description |
|-------|------|-------------|
| message_name | String | Sender's full name |
| message_email | Email | Sender's email address |
| message | Text | Message content |

## Usage Examples

### Subscribe to Newsletter
```bash
curl -X POST http://127.0.0.1:8000/subscribe/ \
-H "Content-Type: application/json" \
-d '{
    "email": "example@domain.com"
}'
```

### Send Newsletter
```bash
curl -X POST http://127.0.0.1:8000/newsletter/ \
-H "Content-Type: application/json" \
-d '{
    "subject": "Important Update",
    "message": "Here is our latest news..."
}'
```

### Submit Contact Form
```bash
curl -X POST http://127.0.0.1:8000/contact/ \
-H "Content-Type: application/json" \
-d '{
    "message_name": "John Doe",
    "message_email": "john@example.com",
    "message": "I have a question about..."
}'
```

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 400: Bad Request (e.g., invalid email format)
- 500: Server Error

Common error scenarios:
- Invalid email format
- Empty required fields
- Server unable to send emails

## Notes
- Newsletter broadcasts are sent to all subscribed email addresses
- Contact form submissions should receive an automated acknowledgment
- All email addresses are validated before processing
- Message content should not be empty

# Communities API Documentation

## Overview
The Communities API enables management of technical communities, their members, and meeting sessions. It provides endpoints for creating communities, managing memberships, and scheduling community sessions.

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints

### 1. Communities Management

#### Create Community
- **URL:** `POST /communities/`
- **Description:** Create a new technical community
- **Request Body:**
```json
{
    "name": "Artificial Intelligence & Machine Learning",
    "community_lead": "Sarah Chen",
    "description": "Our AI/ML community focuses on understanding and implementing cutting-edge machine learning algorithms..."
}
```
- **Response:** Returns created community object with assigned ID
```json
{
    "id": 2,
    "name": "Artificial Intelligence & Machine Learning",
    "community_lead": "Sarah Chen",
    "description": "...",
    "members": [],
    "total_members": 0,
    "sessions": []
}
```

#### List Communities
- **URL:** `GET /communities/`
- **Description:** Retrieve all communities with their details
- **Response:** Returns paginated list of communities
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Cyber Security",
            "community_lead": "Shadrack Mwabe",
            "members": [...],
            "sessions": [...]
        }
    ]
}
```

### 2. Community Membership

#### Join Community
- **URL:** `POST /communities/{id}/join/`
- **Description:** Request to join a specific community
- **Parameters:** 
  - `id`: Community ID (in URL)
- **Request Body:**
```json
{
    "name": "Kevin Ochieng",
    "email": "kizahkevinianh001@gmail.com"
}
```
- **Response:**
```json
{
    "message": "Successfully joined the community!"
}
```

#### List Community Members
- **URL:** `POST /communities/{id}/members`
- **Description:** Get list of members for a specific community
- **Parameters:**
  - `id`: Community ID (in URL)
- **Response:**
```json
[
    {
        "id": 14,
        "name": "Stephen Omondi",
        "email": "ondeyostephen0@gmail.com",
        "joined_at": "2025-01-24T18:56:28.069007Z"
    }
]
```

### 3. Community Sessions

#### Add Session
- **URL:** `POST /communities/{id}/sessions/`
- **Description:** Schedule a regular meeting session for a community
- **Parameters:**
  - `id`: Community ID (in URL)
- **Request Body:**
```json
{
    "day": "MONDAY",
    "start_time": "1700",
    "end_time": "1900",
    "meeting_type": "HYBRID",
    "location": "ECA19"
}
```
- **Response:**
```json
{
    "day": "MONDAY",
    "start_time": "17:00:00",
    "end_time": "19:00:00",
    "meeting_type": "HYBRID",
    "location": "ECA19"
}
```

## Data Models

### Community
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Name of the community |
| community_lead | string | Yes | Name of the lead member |
| description | text | Yes | Detailed description of community |
| co_lead | string | No | Name of co-lead member |
| treasurer | string | No | Name of treasurer |
| secretary | string | No | Name of secretary |
| email | string | No | Contact email |
| phone_number | string | No | Contact phone number |
| github_link | string | No | Community GitHub URL |
| linkedin_link | string | No | Community LinkedIn URL |
| founding_date | date | No | Community establishment date |
| is_recruiting | boolean | No | Whether accepting new members |
| tech_stack | string | No | Technologies used |

### Member
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| name | string | Member's full name |
| email | string | Member's email address |
| joined_at | datetime | Timestamp of joining |

### Session
| Field | Type | Description |
|-------|------|-------------|
| day | string | Meeting day (e.g., MONDAY) |
| start_time | time | Session start time (24hr format) |
| end_time | time | Session end time (24hr format) |
| meeting_type | string | HYBRID/ONLINE/PHYSICAL |
| location | string | Meeting venue |

## Usage Notes

1. **Session Scheduling**
   - Communities typically hold sessions at least twice weekly
   - Times should be provided in 24-hour format (e.g., "1700" for 5:00 PM)
   - Location is required for PHYSICAL and HYBRID sessions

2. **Meeting Types**
   - HYBRID: Both in-person and online attendance options
   - ONLINE: Virtual meeting only
   - PHYSICAL: In-person meeting only

3. **Community Membership**
   - Members can join multiple communities
   - Each member gets a unique ID within the community
   - Joining timestamp is automatically recorded

4. **Community Management**
   - Communities can have optional leadership roles (co-lead, treasurer, secretary)
   - Tech stack and other optional fields can be updated later
   - Session details can be updated by community admins

## Example Requests

### Create a Community
```bash
curl -X POST http://127.0.0.1:8000/communities/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Web Development",
    "community_lead": "John Doe",
    "description": "A community focused on modern web technologies..."
}'
```

### Join a Community
```bash
curl -X POST http://127.0.0.1:8000/communities/1/join/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Kevin Ochieng",
    "email": "kevin@example.com"
}'
```

### Add a Session
```bash
curl -X POST http://127.0.0.1:8000/communities/1/sessions/ \
-H "Content-Type: application/json" \
-d '{
    "day": "MONDAY",
    "start_time": "1700",
    "end_time": "1900",
    "meeting_type": "HYBRID",
    "location": "Room 101"
}'
```

