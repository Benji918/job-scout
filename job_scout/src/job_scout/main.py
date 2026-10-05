from asyncio import subprocess
import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FirecrawlScrapeWebsiteTool

import sys
from pathlib import Path

# 1. Load environment variables from .env
load_dotenv()

BASE_DIR = Path(__file__).parent

# 2. Load YAML Configurations safely
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Paths updated to point to the config directory relative to this script
agents_config = load_yaml(BASE_DIR / 'config' / 'agents.yaml')
tasks_config = load_yaml(BASE_DIR / 'config' / 'tasks.yaml')

# 3. Initialize Tools
search_tool = SerperDevTool()
scrape_tool = FirecrawlScrapeWebsiteTool()

# 4. Initialize Agents
search_orchestrator = Agent(config=agents_config['search_orchestrator'])
cv_strategist = Agent(config=agents_config['cv_strategist'])
opportunity_reviewer = Agent(config=agents_config['opportunity_reviewer'])

# Tools are explicitly injected ONLY into the scout
job_scout = Agent(
    config=agents_config['job_scout'],
    tools=[search_tool, scrape_tool] 
)

# 5. Initialize Tasks
analyze_profile_task = Task(
    config=tasks_config['analyze_profile_task'],
    agent=cv_strategist
)

scout_jobs_task = Task(
    config=tasks_config['scout_jobs_task'],
    agent=job_scout
)

review_opportunities_task = Task(
    config=tasks_config['review_opportunities_task'],
    agent=opportunity_reviewer
)

orchestrate_search_task = Task(
    config=tasks_config['orchestrate_search_task'],
    agent=search_orchestrator
)

# 6. Assemble the Crew
job_search_crew = Crew(
    agents=[
        search_orchestrator,
        cv_strategist,
        job_scout,
        opportunity_reviewer
    ],
    tasks=[
        analyze_profile_task,
        scout_jobs_task,
        review_opportunities_task,
        orchestrate_search_task
    ],
    process=Process.sequential, 
    verbose=True
)

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
    result = job_search_crew.kickoff(inputs=inputs)
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
        job_search_crew.train(n_iterations=n_iterations, filename=filename, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        task_id = sys.argv[1]
        job_search_crew.replay(task_id=task_id)
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
        job_search_crew.test(n_iterations=n_iterations, eval_llm=openai_model_name, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    run()

if __name__ == "__main__":
    run()