from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool
from dotenv import load_dotenv

load_dotenv()

# Instantiate tools
search_tool = SerperDevTool(country='vn', locale='vi')
file_read_tool_raw_data = FileReadTool(file_path='results/raw_data.jsonl')
file_read_tool_trend = FileReadTool(file_path='results/trend_report.md')
file_read_tool_sentiment = FileReadTool(file_path='results/sentiment_report.md')
llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

@CrewBase
class SL_crew():
	"""TestProj crew"""
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],
            tools=[search_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def trend_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_analyzer'],
            tools=[file_read_tool_raw_data],
            verbose=True,
            llm=llm
        )

    @agent
    def sentiment_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_specialist'],
            tools=[file_read_tool_raw_data],
            verbose=True,
            llm=llm
        )

    @agent
    def insights_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['insights_reporter'],
            # reads the reports from the previous agents.
            tools=[file_read_tool_raw_data, file_read_tool_trend, file_read_tool_sentiment],
            verbose=True,
            llm=llm
        )

    @task
    def data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_collection'],
            agent=self.data_collector(),
            output_file='results/raw_data.jsonl',
            expected_output="A JSONL file ('results/raw_data.jsonl') with each line containing content_text, source_platform, author_handle, timestamp, direct_url, engagement_metrics, and content_type for {topic}.",        )

    @task
    def trend_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_analysis'],
            agent=self.trend_analyzer(),
            context=[self.data_collection_task()],
            output_file='results/trend_report.md',
            expected_output="A markdown report ('results/trend_report.md') with top 5 hashtags, 3-4 narratives, viral content, comparisons, and demographics for {topic}.",        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_analysis'],
            agent=self.sentiment_specialist(),
            # uses on the previous two tasks for full context.
            context=[self.data_collection_task(), self.trend_analysis_task()],
            output_file='results/sentiment_report.md',
            expected_output="A markdown report ('results/sentiment_report.md') with sentiment breakdown, themes, emotional analysis for {topic}.",        )

    @task
    def insights_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['insights_generation'],
            agent=self.insights_reporter(),
            # uses the trend and sentiment reports as context.
            context=[self.trend_analysis_task(), self.sentiment_analysis_task()],
            output_file='results/final_insights_report.md',
            expected_output="A markdown report ('results/final_insights_report.md') with executive summary, trends, sentiment, influencers, risks/opportunities, and 3+ recommendations for {topic}.",        )

	@crew
	def crew(self) -> Crew:
		"""Creates the TestProj crew"""

		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)
