import requests
import json
import random
import string

BASE_URL = "http://localhost:8000"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_create_job_posting():
    job_posting = {
        "job_id": random.randint(1, 1000),
        "job_title": "Software Engineer",
        "company": "Tech Solutions Inc.",
        "required_skills": ["Python", "Django", "REST APIs"],
        "location": "Remote",
        "job_type": "Full-Time",
        "experience_level": "Intermediate"
    }
    response = requests.post(f"{BASE_URL}/job_posting", json=job_posting)
    print(f"Create job posting response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    print("Job posting created successfully")
    return job_posting

def test_create_user_profile():
    user_profile = {
        "name": "Jane Doe",
        "skills": ["Python", "Django", "REST APIs"],
        "experience_level": "Intermediate",
        "preferences": {
            "desired_roles": ["Software Engineer", "Backend Developer"],
            "locations": ["Remote", "New York"],
            "job_type": "Full-Time"
        }
    }
    response = requests.post(f"{BASE_URL}/user_profile", json=user_profile)
    print(f"Create user profile response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    user_id = response.json().get("id")
    assert user_id, "User ID not returned in response"
    print(f"User profile created successfully with ID: {user_id}")
    return user_id

def test_get_job_recommendations(user_id):
    response = requests.get(f"{BASE_URL}/job_recommendations/{user_id}")
    print(f"Get job recommendations response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    recommendations = response.json()
    assert len(recommendations) > 0, "No job recommendations returned"
    print(f"Number of job recommendations received: {len(recommendations)}")
    print(f"Top recommendation: {json.dumps(recommendations[0], indent=2)}")
    assert 'match_score' in recommendations[0], "Match score not present in recommendations"
    print("Job recommendations received successfully")

def test_get_all_job_postings():
    response = requests.get(f"{BASE_URL}/job_postings")
    print(f"Get all job postings response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    job_postings = response.json()
    assert len(job_postings) > 0
    print(f"Number of job postings received: {len(job_postings)}")
    print(f"First job posting: {json.dumps(job_postings[0], indent=2)}")

def test_create_invalid_job_posting():
    invalid_job_posting = {
        "job_title": "Invalid Job",
        # Missing required fields
    }
    response = requests.post(f"{BASE_URL}/job_posting", json=invalid_job_posting)
    print(f"Create invalid job posting response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 422, "Expected validation error"

def test_create_invalid_user_profile():
    invalid_user_profile = {
        "name": "John Doe",
        # Missing required fields
    }
    response = requests.post(f"{BASE_URL}/user_profile", json=invalid_user_profile)
    print(f"Create invalid user profile response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 422, "Expected validation error"

def test_get_job_recommendations_invalid_user_id():
    invalid_user_id = "invalid_id"
    response = requests.get(f"{BASE_URL}/job_recommendations/{invalid_user_id}")
    print(f"Get job recommendations for invalid user ID response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 500, "Expected server error for invalid user ID"

def test_create_multiple_job_postings():
    job_titles = ["Data Scientist", "Frontend Developer", "DevOps Engineer", "Product Manager"]
    for title in job_titles:
        job_posting = {
            "job_id": random.randint(1, 1000),
            "job_title": title,
            "company": f"{title} Corp",
            "required_skills": ["Python", "SQL", "Machine Learning"] if "Data" in title else ["JavaScript", "React", "CSS"],
            "location": random.choice(["Remote", "New York", "San Francisco", "London"]),
            "job_type": random.choice(["Full-Time", "Part-Time", "Contract"]),
            "experience_level": random.choice(["Entry-Level", "Intermediate", "Senior"])
        }
        response = requests.post(f"{BASE_URL}/job_posting", json=job_posting)
        assert response.status_code == 200, f"Failed to create job posting for {title}"
    print("Multiple job postings created successfully")

def test_create_multiple_user_profiles():
    for i in range(5):
        user_profile = {
            "name": f"User {i}",
            "skills": random.sample(["Python", "JavaScript", "SQL", "React", "Django", "Machine Learning", "DevOps"], 3),
            "experience_level": random.choice(["Entry-Level", "Intermediate", "Senior"]),
            "preferences": {
                "desired_roles": random.sample(["Software Engineer", "Data Scientist", "Frontend Developer", "Backend Developer", "DevOps Engineer"], 2),
                "locations": random.sample(["Remote", "New York", "San Francisco", "London", "Berlin"], 2),
                "job_type": random.choice(["Full-Time", "Part-Time", "Contract"])
            }
        }
        response = requests.post(f"{BASE_URL}/user_profile", json=user_profile)
        assert response.status_code == 200, f"Failed to create user profile for User {i}"
    print("Multiple user profiles created successfully")

def main():
    try:
        # Basic tests
        job_posting = test_create_job_posting()
        user_id = test_create_user_profile()
        test_get_job_recommendations(user_id)
        test_get_all_job_postings()

        # Error handling tests
        test_create_invalid_job_posting()
        test_create_invalid_user_profile()
        test_get_job_recommendations_invalid_user_id()

        # Multiple entity creation tests
        test_create_multiple_job_postings()
        test_create_multiple_user_profiles()

        # Retest recommendations after creating multiple entities
        test_get_job_recommendations(user_id)

        print("All tests passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()