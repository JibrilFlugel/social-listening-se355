# Social listening agentic system
<p align="center">
  <img src="https://github.com/user-attachments/assets/53fe5291-c245-4fad-bb49-912f28adf690" />
</p>
A multi-agent system for analyzing public discourse using LLM and real-time data. Designed to mimic a real-world social insights team

This project leverages [CrewAI](https://crewai.com/), [Ollama](https://ollama.com/), and the [Serper API](https://serper.dev/) to collect, analyze, and summarize public sentiment and trends around any topic.

## Features

- **Data Collector Agent**: Collect real-time mentions, discussions, and trends from online platforms.
- **Trend Analyzer Agent**: Identify and interpret emerging trends, hashtags, and viral topics.
- **Sentiment Specialist Agent**: Detect and summarize the emotional tone and sentiment behind online conversations.
- **Insights Reporter**: Synthesize insights from all agents and provide an actionable summary.
- Fully autonomous agent orchestration using [CrewAI](https://crewai.com/)

## Tech Stack

- **[CrewAI](https://crewai.com/)** – Agent orchestration framework
- **[Ollama](https://ollama.com/)** – Local LLM hosting
- **[Serper API](https://serper.dev/)** – Google Search & News search engine

## How to run

Before running the project locally, ensure you have the following prerequisites set up:
**Environment Variables**: Create a `.env` file in the root directory of the project and add the following variables (refer to `.env.example` for guidance):

```env
//Ollama base url (Ollama uses port 11434 by default when running locally)
API_BASE=
//Your serper api key
SERPER_API_KEY=
```

Once you have these prerequisites set up, follow the steps below to run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/JibrilFlugel/social-listening-se355.git
   ```
2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create the `.env` file and add the environment variables as mentioned above.

6. Start Ollama local server before running the project:

   ```bash
   ollama serve
   ```

7. Run the project:
   ```bash
   python ui.py
   ```
