#!/usr/bin/env python
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from job_scout.crew import JobScout

def get_inputs():
    return {
        "cv_content": """
        Senior Python Developer with 4+ years of experience.
        Backend Engineer specializing in Python, with hands-on production experience building REST APIs, optimizing databases, and shipping backend systems for multi-user platforms. 
        Background spans contract roles, an internship, and independent project work — all remote. Comfortable working across the full backend lifecycle: API design, 
        database optimization, testing, CI/CD, deployment, monitoring, and cross-functional collaboration with frontend/client teams.
        Frameworks: Django, Flask, FastAPI
        Databases: MySQL, MongoDB, PostgreSQL, Redis
        DevOps/Infra: Docker, Kubernetes, Git, GitHub Actions, HashiCorp Vault, Grafana, Loki, DigitalOcean
        Best-fit job titles:
        - Backend Engineer / Backend Developer (Python)
        - Python Developer
        - API Engineer
        - Django/FastAPI Developer
        - Junior–Mid Backend Engineer
        """,
        "job_description": "Remote Python Backend Developer with 3–4 years of hands-on production experience. Comfortable working across the full backend lifecycle: API design, database optimization, testing, CI/CD, deployment, monitoring, and cross-functional collaboration with frontend/client teams. Backend Engineer specializing in Python, with hands-on production experience building REST APIs, optimizing databases, and shipping backend systems for multi-user platforms. Background spans contract roles, an internship, and independent project work — all remote. Comfortable working across the full backend lifecycle: API design, database optimization, testing, CI/CD, deployment, monitoring, and cross-functional collaboration with frontend/client teams. Frameworks: Django, Flask, FastAPI Databases: MySQL, MongoDB, PostgreSQL, Redis DevOps/Infra: Docker, Kubernetes, Git, GitHub Actions, HashiCorp Vault, Grafana, Loki, DigitalOcean"
    }

def run():
    """
    Run the crew.
    """
    inputs = get_inputs()
    print("Initiating Job Search Run...")
    result = JobScout().crew().kickoff(inputs=inputs)
    print("\n==============================================\n")
    print("FINAL JOB SEARCH DOSSIER:\n")
    print(result)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = get_inputs()
    try:
        n_iterations = int(sys.argv[1])
        filename = sys.argv[2]
        JobScout().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        task_id = sys.argv[1]
        JobScout().crew().replay(task_id=task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = get_inputs()
    try:
        n_iterations = int(sys.argv[1])
        openai_model_name = sys.argv[2]
        JobScout().crew().test(n_iterations=n_iterations, eval_llm=openai_model_name, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    run()

if __name__ == "__main__":
    run()