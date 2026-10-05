from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, FirecrawlSearchTool, EXASearchTool, ScrapeWebsiteTool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def get_job_scout_tools():
    """Get available tools for job_scout based on configured API keys."""
    tools = [SerperDevTool(), FirecrawlSearchTool(), ScrapeWebsiteTool()]
    
    # Add EXASearchTool only if API key is available
    if os.getenv("EXA_API_KEY"):
        tools.append(EXASearchTool())
    
    return tools

@CrewBase
class JobScout():
    """JobScout crew"""

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
            verbose=True
        )

    @agent
    def cv_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_strategist'], # type: ignore[index]
            verbose=True
        )

    @agent
    def job_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['job_scout'], # type: ignore[index]
            tools=get_job_scout_tools(),
            verbose=True
        )

    @agent
    def opportunity_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['opportunity_reviewer'], # type: ignore[index]
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
        """Creates the JobScout crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",
                "config": {"model_name": "text-embedding-3-large"}
            },
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
