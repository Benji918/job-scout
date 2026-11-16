#!/usr/bin/env python
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from job_scout_nz.crew import JobScoutNZ
from job_scout_nz.seen_jobs import format_for_prompt, load_ledger, record_from_report

def _resume_text() -> str:
    """The candidate's actual resume, stored as knowledge/user_resume.txt."""
    path = Path(__file__).resolve().parents[2] / "knowledge" / "user_resume.txt"
    return path.read_text(encoding="utf-8")

def get_inputs():
    return {
        "previously_seen_jobs": format_for_prompt(load_ledger()),
        "cv_content": _resume_text(),
        "job_description": "Any New Zealand software engineering role (software engineer, backend developer, Python developer, platform/DevOps, AI/ML engineer) with a Python backend focus: REST APIs, Django, Flask, FastAPI, databases, Docker/Kubernetes, CI/CD. From an INZ accredited employer or with explicit visa sponsorship (AEWV, Straight-to-Residence, Green List). Posted within the past 2 weeks. Open to Auckland, Wellington, Christchurch, Hamilton, Dunedin, or remote-within-NZ."
    }

def run():
    """
    Run the crew.
    """
    inputs = get_inputs()
    seen_count = len(load_ledger())
    print(f"Initiating Job Search Run... ({seen_count} previously seen listing(s) excluded)")
    result = JobScoutNZ().crew().kickoff(inputs=inputs)
    added = record_from_report(result.raw)
    print(f"Recorded {added} new listing(s) in the seen-jobs ledger.")
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