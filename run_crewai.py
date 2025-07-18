from datetime import datetime
from src.social_listening.crew import SL_crew
import os

RESULTS_PATH = "results/final_insights_report.md" 

def run_crewai(topic):
    if not topic:
        return "❌ Topic can't be empty!"

    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }

    try:
        SL_crew().crew().kickoff(inputs=inputs)  

        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH, "r", encoding="utf-8") as file:
                result = file.read()
                return f"✅ Social listening result for '{topic}':\n{result}"
        else:
            return f"⚠️ Cannot find result file: {RESULTS_PATH}"

    except Exception as e:
        return f"❌ Error when running Crewai: {e}"
