# Multi-Agent Research Assistant

A Python research workflow built with [CrewAI](https://www.crewai.com/). Three agents work in sequence to research a topic, analyze the findings, and write a final report.

## How it works

1. **Research Specialist** uses `SerperDevTool` to search the web and saves findings to `research_findings.md`.
2. **Data Analyst** reads the research findings with `FileReadTool`, identifies trends and insights, and saves `analysis_report.md`.
3. **Content Writer** uses the research and analysis task outputs as context, then writes `final_report.md` with `FileWriterTool`.

The agents run in the order listed in `crews/crew.py`. Each agent gets its model and temperature from environment variables. The example configuration uses OpenRouter with `openai/gpt-oss-20b`.

## Project structure

```text
.
├── crews/
│   ├── crew.py                 # Crew definition and agent/task order
│   ├── research_specialist.py  # Research agent and web search tool
│   ├── research_task.py        # Research instructions and output
│   ├── data_analyst.py         # Analyst agent and file-reading tool
│   ├── analyst_task.py         # Analysis instructions and output
│   ├── content_writer.py       # Writer agent and file-writing tool
│   └── writing_task.py         # Final report instructions and output
├── src/mult_agent_research_assistant/
│   └── __init__.py             # Packaging scaffold; not used by main.py
├── main.py                     # Loads .env and starts the research crew
├── app.py                      # Reserved for a future Streamlit interface
├── .env.example                # Safe template for required settings
├── pyproject.toml              # Project metadata and dependencies
└── uv.lock                     # Locked dependency versions
```

`main.py` currently starts a run for the hard-coded topic `"AI Agents"`. Edit that value near the bottom of the file to research a different topic. The report files are generated in the project root and are ignored by Git.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- An [OpenRouter API key](https://openrouter.ai/settings/keys)
- A [Serper API key](https://serper.dev/) for web search

## Set up and run

1. Clone the repository and enter its folder:

   ```powershell
   git clone https://github.com/<your-github-username>/multi-agent-research-assistant.git
   cd multi-agent-research-assistant
   ```

2. Install the project dependencies:

   ```powershell
   uv sync
   ```

3. Create your local environment file and add your API keys:

   ```powershell
   Copy-Item .env.example .env
   ```

   Open `.env` and replace the placeholder values for `OPENROUTER_API_KEY` and `SERPER_API_KEY`. Keep `.env` private; it is excluded from Git.

4. Run the workflow from the project folder:

   ```powershell
   uv run python main.py
   ```

If creating `.venv` inside a synced or restricted folder causes a permissions error, use an environment location outside that folder in the same PowerShell window:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv\envs\multi-agent-research-assistant"
uv sync
uv run python main.py
```

## Packages and tools

- **CrewAI** defines the agents, tasks, and sequential crew.
- **CrewAI Tools** provides `SerperDevTool`, `FileReadTool`, and `FileWriterTool`.
- **LiteLLM**, enabled through the `crewai[litellm]` extra, connects CrewAI to OpenRouter.
- **python-dotenv** loads local settings from `.env`.
- **Streamlit** is listed as a dependency for a future UI; `app.py` does not currently implement one.

## Configuration

See `.env.example` for all required variable names. The three agent model variables use LiteLLM's OpenRouter format:

```text
openrouter/openai/gpt-oss-20b
```

The corresponding `*_TEMP` variables control each agent's temperature. The Serper key is used by the research agent; the OpenRouter key is used for model requests.
