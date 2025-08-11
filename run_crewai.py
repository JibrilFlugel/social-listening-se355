from datetime import datetime
from src.social_listening.crew import SL_crew
import os

RESULTS_PATH = "results/final_insights_report.md" 

def run_crewai(topic):
    """
    Hàm chạy crewai với chủ đề từ UI và in kết quả ra màn hình
    """
    if not topic:
        return "❌ Chủ đề không được để trống!"

    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }

    try:
        SL_crew().crew().kickoff(inputs=inputs)  

        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH, "r", encoding="utf-8") as file:
                result = file.read()
                return f"✅ Kết quả phân tích chủ đề '{topic}':\n{result}"
        else:
            return f"⚠️ Không tìm thấy file kết quả: {RESULTS_PATH}"

    except Exception as e:
        return f"❌ Lỗi khi chạy crewai: {e}"
