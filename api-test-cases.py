import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_job_posting():
    job_posting = {
        "job_id": 1,
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
    if not user_id:
        raise ValueError("User ID not returned in response")
    print(f"User profile created successfully with ID: {user_id}")
    return user_id

def test_get_job_recommendations(user_id):
    response = requests.get(f"{BASE_URL}/job_recommendations/{user_id}")
    print(f"Get job recommendations response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    recommendations = response.json()
    assert len(recommendations) > 0
    print(f"Job recommendations received: {json.dumps(recommendations, indent=2)}")

def test_get_all_job_postings():
    response = requests.get(f"{BASE_URL}/job_postings")
    print(f"Get all job postings response: {response.status_code}")
    print(f"Response content: {response.text}")
    assert response.status_code == 200
    job_postings = response.json()
    assert len(job_postings) > 0
    print(f"All job postings received: {json.dumps(job_postings, indent=2)}")

if __name__ == "__main__":
    test_create_job_posting()
    user_id = test_create_user_profile()
    test_get_job_recommendations(user_id)
    test_get_all_job_postings()