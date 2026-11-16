from crewai import Agent, Crew, Process, Task, PlanningConfig
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, FirecrawlSearchTool, EXASearchTool, ScrapeWebsiteTool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def get_job_scout_tools():
    """Get available tools for job_scout_nz based on configured API keys.

    Each tool is only loaded when its API key is set, so a missing key
    fails that search path gracefully instead of crashing the crew.
    """
    tools = []

    if os.getenv("SERPER_API_KEY"):
        tools.append(SerperDevTool())
    if os.getenv("FIRECRAWL_API_KEY"):
        tools.append(FirecrawlSearchTool())
    tools.append(ScrapeWebsiteTool())

    # Add EXASearchTool only if API key is available
    if os.getenv("EXA_API_KEY"):
        tools.append(EXASearchTool())

    if not tools:
        raise RuntimeError(
            "No job-scout tools could be created: set at least one of "
            "SERPER_API_KEY, FIRECRAWL_API_KEY or EXA_API_KEY in .env"
        )
    return tools

@CrewBase
class JobScoutNZ():
    """JobScout NZ crew for New Zealand accredited-employer / visa-sponsored roles"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def search_orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['search_orchestrator'], # type: ignore[index]
            inject_date=True,
            verbose=True
        )

    @agent
    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_strategist'], # type: ignore[index]
            inject_date=True,
            verbose=True
        )

    @agent
    def job_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['job_scout'], # type: ignore[index]
            tools=get_job_scout_tools(),
            planning_config=PlanningConfig(
                reasoning_effort="medium",
                max_attempts=2,
                max_steps=12,
                max_replans=1,
                max_step_iterations=8,
                step_timeout=180,
            ),
            inject_date=True,
            max_iter=40,
            max_execution_time=1500, # hard 25-minute cap for the scout
            max_rpm=30,
            verbose=True
        )

    @agent
    def opportunity_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['opportunity_reviewer'], # type: ignore[index]
            planning_config=PlanningConfig(reasoning_effort="medium", max_attempts=2),
            inject_date=True,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_profile_task'], # type: ignore[index]
        )

    @task
    def scout_jobs_task(self) -> Task:
        return Task(
            config=self.tasks_config['scout_jobs_task'], # type: ignore[index]
        )

    @task
    def review_opportunities_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_opportunities_task'], # type: ignore[index]
        )

    @task
    def orchestrate_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['orchestrate_search_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JobScout NZ crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            planning=True, # CrewPlanner writes a step plan into each task before kickoff
            skills=["./skills"], # Aggressive-sourcing methodology injected into every agent
            knowledge_sources=[
                TextFileKnowledgeSource(file_paths=["user_resume.txt"])
            ], # The candidate's actual resume (paths resolve under knowledge/), RAG-searchable
            memory=True,
            embedder={
                "provider": "openai",
                "config": {"model_name": "text-embedding-3-large"}
            },
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
