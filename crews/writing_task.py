import textwrap

from crewai import Task
from .content_writer import content_writer_agent
from .analyst_task import analysis_task
from .research_task import research_task

writing_task = Task(
    agent=content_writer_agent,
    description=textwrap.dedent("""
                Create a comprehensive report on the topic: {topic}

                Your tasks:
                1. Review both research findings and analysis results
                2. Write a well structured, comprehensive report
                3. Ensure clarity and readability for the target audience
                4. Include executive summary, main content, and conclusions
                5. Cite all sources appropriately

                The report should include:
                - Executive summary
                - Introduction
                - Main findings
                - Analysis and insights
                - Conclusions and recommendations
                - Sources and references
        """),
    expected_output="A comprehensive well structured report with executive summary and conclusions",
    context=[research_task, analysis_task],
    output_file="final_report.md"

)