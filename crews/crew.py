from crewai import Crew

from .research_specialist import research_specialist_agent
from .data_analyst import data_analyst_agent
from .content_writer import content_writer_agent
from .research_task import research_task
from .analyst_task import analysis_task
from .writing_task import writing_task

research_crew = Crew(
    agents=[
        research_specialist_agent,
        data_analyst_agent,
        content_writer_agent],
    tasks=[research_task,
           analysis_task,
           writing_task],
    verbose=True
)