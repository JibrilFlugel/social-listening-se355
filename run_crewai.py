from datetime import datetime
from src.social_listening.crew import SL_crew
import os

RESULTS_PATH = "results/final_insights_report.md" 

def run_crewai(topic):
    if not topic:
        return "Topic cannot be empty!"

    inputs = {
        'topic': topic,
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }

    try:
        SL_crew().crew().kickoff(inputs=inputs)  

        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH, "r", encoding="utf-8") as file:
                result = file.read()
                return f"Analysis results for topic '{topic}':\n{result}"
        else:
            return f"Results file not found: {RESULTS_PATH}"

    except Exception as e:
        return f"Error running crewai: {e}"