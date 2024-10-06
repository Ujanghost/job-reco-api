from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["job_matching_db"]
    job_postings_collection = db["job_postings"]
    user_profiles_collection = db["user_profiles"]
    client.admin.command('ismaster')
except ConnectionFailure:
    print("Server not available")

class Preferences(BaseModel):
    desired_roles: List[str]
    locations: List[str]
    job_type: str

class UserProfile(BaseModel):
    name: str
    skills: List[str]
    experience_level: str
    preferences: Preferences

class JobPosting(BaseModel):
    job_id: int
    job_title: str
    company: str
    required_skills: List[str]
    location: str
    job_type: str
    experience_level: str

def match_job_postings(user_profile: UserProfile) -> List[JobPosting]:
    matching_jobs = []
    for job in job_postings_collection.find():
        if (
            job["job_title"] in user_profile.preferences.desired_roles
            and job["location"] in user_profile.preferences.locations
            and job["job_type"] == user_profile.preferences.job_type
            and job["experience_level"] == user_profile.experience_level
            and any(skill in job["required_skills"] for skill in user_profile.skills)
        ):
            matching_jobs.append(JobPosting(**job))
    return matching_jobs

@app.post("/user_profile")
async def create_user_profile(user_profile: UserProfile):
    try:
        result = user_profiles_collection.insert_one(user_profile.dict())
        return {"message": "User profile created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user profile: {str(e)}")

@app.get("/job_recommendations/{user_id}")
async def get_job_recommendations(user_id: str):
    try:
        user_profile = user_profiles_collection.find_one({"_id": ObjectId(user_id)})
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        matching_jobs = match_job_postings(UserProfile(**user_profile))
        return matching_jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job recommendations: {str(e)}")

@app.post("/job_posting")
async def create_job_posting(job_posting: JobPosting):
    try:
        result = job_postings_collection.insert_one(job_posting.dict())
        return {"message": "Job posting created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job posting: {str(e)}")

@app.get("/job_postings")
async def get_all_job_postings():
    try:
        job_postings = list(job_postings_collection.find())
        return [JobPosting(**job) for job in job_postings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job postings: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)