from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from .tools import FileReaderTool
from dotenv import load_dotenv
import os

load_dotenv()

# Ensure results directory exists
os.makedirs('results', exist_ok=True)

# Instantiate tools
search_tool = SerperDevTool(country='vn', locale='vi')
safe_file_reader = FileReaderTool()
llm = LLM(model="ollama/qwen2.5", base_url="http://localhost:11434")

@CrewBase
class SL_crew():    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],
            tools=[search_tool],
            verbose=True,
            llm=llm,
            max_retry_limit=2
        )

    @agent
    def trend_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_analyzer'],
            tools=[safe_file_reader],
            verbose=True,
            llm=llm,
            max_retry_limit=2
        )

    @agent
    def sentiment_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_specialist'],
            tools=[safe_file_reader],
            verbose=True,
            llm=llm,
            max_retry_limit=2
        )

    @agent
    def insights_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['insights_reporter'],
            tools=[safe_file_reader],
            verbose=True,
            llm=llm,
            max_retry_limit=2
        )

    @task
    def data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_collection'],
            agent=self.data_collector(),
            output_file='results/raw_data.jsonl',
            expected_output="A valid JSONL file with each line as a separate JSON object containing: content_text, source_platform, author_handle, timestamp, direct_url, engagement_metrics, and content_type. Minimum 10 entries required."
        )

    @task
    def trend_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_analysis'],
            agent=self.trend_analyzer(),
            context=[self.data_collection_task()],
            output_file='results/trend_report.md',
            expected_output="A complete markdown report analyzing trends from the collected data. Must include: top 5 hashtags, key narratives, viral content analysis, and demographic insights."
        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_analysis'],
            agent=self.sentiment_specialist(),
            context=[self.data_collection_task()],
            output_file='results/sentiment_report.md',
            expected_output="A complete markdown report with sentiment analysis including: overall sentiment percentages, positive/negative themes, emotional drivers, and sentiment trends over time."
        )

    @task
    def insights_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['insights_generation'],
            agent=self.insights_reporter(),
            context=[self.trend_analysis_task(), self.sentiment_analysis_task()],
            output_file='results/final_insights_report.md',
            expected_output="A comprehensive strategic report with executive summary, key findings, actionable recommendations, risks/opportunities, and strategic next steps."
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Social Listening crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            max_rpm=10
        )
