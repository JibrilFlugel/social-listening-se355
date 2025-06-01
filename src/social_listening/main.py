import warnings

from datetime import datetime

from social_listening.crew import SL_crew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    user_input = input("Enter the name of the topic you want to research: ")

    inputs = {
        'topic': user_input,
        'current_year': str(datetime.now().year)
    }
    
    try:
        SL_crew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
