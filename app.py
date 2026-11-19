import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

AGENT_MODEL_VARIABLES = (
	"RESEARCH_AGENT_LLM",
	"ANALYST_AGENT_LLM",
	"WRITER_AGENT_LLM",
)
AGENT_TEMPERATURE_VARIABLES = (
	"RESEARCH_AGENT_TEMP",
	"ANALYST_AGENT_TEMP",
	"WRITER_AGENT_TEMP",
)
AGENTS = (
	"Research Specialist",
	"Data Analyst",
	"Content Writer",
)
RESEARCH_STAGES = (
	"Research findings",
	"Analysis report",
	"Final report",
)
API_KEY_BY_PROVIDER = {
	"groq": "GROQ_API_KEY",
	"openai": "OPENAI_API_KEY",
	"openrouter": "OPENROUTER_API_KEY",
}


def get_required_api_keys():
	required_api_keys = {"SERPER_API_KEY"}

	for variable in AGENT_MODEL_VARIABLES:
		model = os.getenv(variable, "").strip()
		if not model:
			continue

		provider = model.split("/", 1)[0].lower()
		api_key = API_KEY_BY_PROVIDER.get(provider)
		if api_key:
			required_api_keys.add(api_key)

	return sorted(required_api_keys)


def get_missing_api_keys():
	return [
		api_key
		for api_key in get_required_api_keys()
		if not os.getenv(api_key, "").strip()
	]


def get_missing_agent_settings():
	return [
		variable
		for variable in AGENT_MODEL_VARIABLES + AGENT_TEMPERATURE_VARIABLES
		if not os.getenv(variable, "").strip()
	]


def run_research(topic, on_stage_complete):
	from crews.crew import research_crew

	original_callbacks = [task.callback for task in research_crew.tasks]
	try:
		for task, stage in zip(research_crew.tasks, RESEARCH_STAGES):
			task.callback = lambda _output, stage=stage: on_stage_complete(stage)
		return research_crew.kickoff(inputs={"topic": topic})
	finally:
		for task, callback in zip(research_crew.tasks, original_callbacks):
			task.callback = callback


st.set_page_config(page_title="AI Research Assistant", page_icon="🔎")
st.title("🔎 AI Research Assistant")
st.write("Enter a topic to research it with the configured CrewAI agents.")

with st.sidebar:
	st.header("System status")
	missing_api_keys = get_missing_api_keys()
	if missing_api_keys:
		st.error("❌ API keys missing")
		st.caption("Add these to .env: " + ", ".join(missing_api_keys))
	else:
		st.success("✅ API keys configured")

	missing_agent_settings = get_missing_agent_settings()
	if missing_agent_settings:
		st.warning("⚠️ Agent settings missing")
		st.caption("Add these to .env: " + ", ".join(missing_agent_settings))
	else:
		st.success("✅ Agent settings configured")

	st.subheader("Research agents")
	for agent in AGENTS:
		st.markdown(f"- {agent}")

topic = st.text_area(
	"Research topic",
	placeholder="For example: Recent advances in renewable energy storage",
)
with st.expander("API settings"):
	st.caption(
		"Add your model-provider API key(s), SERPER_API_KEY, and agent model "
		"settings to the project's .env file. Key values are never shown here."
	)
	missing_configuration = get_missing_api_keys() + get_missing_agent_settings()
	if missing_configuration:
		st.warning("Missing .env settings: " + ", ".join(missing_configuration))
	else:
		st.success("Required API keys and agent model settings are configured.")

if st.button("Start research", type="primary", use_container_width=True):
	if not topic.strip():
		st.warning("Please enter a research topic.")
	else:
		missing_configuration = get_missing_api_keys() + get_missing_agent_settings()
		if missing_configuration:
			st.error(
				"Configure these settings in .env before starting: "
				+ ", ".join(missing_configuration)
			)
		else:
			st.subheader("Research progress")
			stage_placeholders = [st.empty() for _stage in RESEARCH_STAGES]
			completed_stages = set()

			def update_progress(completed_stage):
				if completed_stage:
					completed_stages.add(completed_stage)
				current_stage_index = len(completed_stages)
				for index, (stage, placeholder) in enumerate(
					zip(RESEARCH_STAGES, stage_placeholders)
				):
					if stage in completed_stages:
						status = "✅ Completed"
					elif index == current_stage_index:
						status = "🔄 In progress"
					else:
						status = "⏳ Waiting"
					placeholder.markdown(f"**{stage}:** {status}")

			update_progress(None)
			with st.spinner("Researching..."):
				result = run_research(topic.strip(), update_progress)

			task_outputs = getattr(result, "tasks_output", [])
			reports = [
				getattr(output, "raw", "")
				for output in task_outputs[: len(RESEARCH_STAGES)]
			]
			tabs = st.tabs(list(RESEARCH_STAGES))
			for index, (tab, stage) in enumerate(zip(tabs, RESEARCH_STAGES)):
				with tab:
					report = reports[index] if index < len(reports) else ""
					if report:
						st.markdown(report)
					else:
						st.info(f"No {stage.lower()} was returned.")
