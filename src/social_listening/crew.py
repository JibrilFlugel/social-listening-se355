from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

search_tool = SerperDevTool(
		country='vn',
		locale='vi',
	)

@CrewBase
class SL_crew():
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def data_collector(self) -> Agent:
		return Agent(
			config=self.agents_config['data_collector'],
			verbose=True,
			tools=[search_tool]
		)
  
	@agent
	def trend_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['trend_analyzer'],
			verbose=True,
			tools=[search_tool]
		)
  
	@agent
	def sentiment_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['sentiment_specialist'],
			verbose=True
		)

	@agent
	def insights_reporter(self) -> Agent:
		return Agent(
			config=self.agents_config['insights_reporter'],
			verbose=True
		)

	@task
	def data_collection(self) -> Task:
		return Task(
			config=self.tasks_config['data_collection'],
			output_file='results/data_collection.txt'
		)
  
	@task
	def trend_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['trend_analysis'],
			output_file='results/trends.txt'
		)
  
	@task
	def sentiment_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['sentiment_analysis'],	
			output_file='results/public_pov.txt'
		)

	@task
	def insights_generation(self) -> Task:
		return Task(
			config=self.tasks_config['insights_generation'],
   			output_file = 'results/final_report.txt'
		)

	@crew
	def crew(self) -> Crew:

		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)
