# Job Matching API

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Running the API](#running-the-api)
8. [API Endpoints](#api-endpoints)
9. [Data Models](#data-models)
10. [Testing](#testing)
11. [Error Handling](#error-handling)
12. [Future Improvements](#future-improvements)
13. [Contributing](#contributing)
14. [License](#license)

## Introduction

The Job Matching API is a RESTful service built with FastAPI and MongoDB. It provides functionality to create user profiles, post job listings, and match job seekers with suitable job postings based on their skills, experience, and preferences.

## Features

- Create and store user profiles
- Create and store job postings
- Match job seekers with suitable job postings
- Retrieve all job postings

## Technologies Used

- Python 3.7+
- FastAPI
- MongoDB
- Uvicorn (ASGI server)
- Pydantic for data validation

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed
- MongoDB installed and running
- pip (Python package manager) installed

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-matching-api.git
   cd job-matching-api
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install fastapi pymongo uvicorn
   ```

## Configuration

1. MongoDB Configuration:
   - The API is configured to connect to MongoDB at `mongodb://localhost:27017/`
   - It uses a database named `job_matching_db`
   - If you need to change these settings, modify the `MongoClient` connection string in `main.py`

## Running the API

1. Ensure MongoDB is running on your system.

2. From the project directory, run:
   ```
   uvicorn main:app --reload
   ```

3. The API will be available at `http://localhost:8000`

4. To access the interactive API documentation, go to `http://localhost:8000/docs` in your web browser.

## API Endpoints

1. **Create User Profile**
   - URL: `/user_profile`
   - Method: POST
   - Request Body: UserProfile object

2. **Get Job Recommendations**
   - URL: `/job_recommendations/{user_id}`
   - Method: GET
   - Path Parameter: user_id (string)

3. **Create Job Posting**
   - URL: `/job_posting`
   - Method: POST
   - Request Body: JobPosting object

4. **Get All Job Postings**
   - URL: `/job_postings`
   - Method: GET

## Data Models

### UserProfile

```python
class UserProfile(BaseModel):
    name: str
    skills: List[str]
    experience_level: str
    preferences: Preferences

class Preferences(BaseModel):
    desired_roles: List[str]
    locations: List[str]
    job_type: str
```

### JobPosting

```python
class JobPosting(BaseModel):
    job_id: int
    job_title: str
    company: str
    required_skills: List[str]
    location: str
    job_type: str
    experience_level: str
```

## Testing

1. Ensure the API is running.

2. Run the test script:
   ```
   python test_api.py
   ```

3. The test script performs the following operations:
   - Creates a job posting
   - Creates a user profile
   - Retrieves job recommendations for the user
   - Retrieves all job postings

4. Check the console output for test results and any error messages.

## Error Handling

The API uses FastAPI's `HTTPException` for error handling. Common errors include:

- 404 Not Found: When a requested resource doesn't exist
- 500 Internal Server Error: For unexpected server-side errors

Detailed error messages are returned in the response body.

## Future Improvements

1. Implement user authentication and authorization
2. Add more sophisticated matching algorithms
3. Implement pagination for large result sets
4. Add CRUD operations for user profiles and job postings
5. Implement logging for better debugging and monitoring
6. Add more comprehensive test coverage

## Contributing

Contributions to the Job Matching API are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.