from agents import RunContextWrapper, Agent

from ci_agents.factory import AgentFactory
from ci_agents.types import AnalysisContext, ATScriptAIResponse
from hooks.agent_hook_log import global_log_hook


def script_agent_instructions(context: RunContextWrapper[AnalysisContext], agent: Agent[AnalysisContext]) -> str:
    failure_log = context.context.failure_log
    failed_thread_log = context.context.failed_thread_log
    system_prompt = f"""
    #Role:
    You are a mobile E2E automation expert specializing in analyzing CI automation failure reports. 
    Your expertise lies in diagnosing whether a failure is caused by AT script issue.
    #Tasks:
    Your goal is to determine whether a CI test report failure is caused by automation script by analyzing logs.
    • 

    #Data Provided:
    You will receive the following logs to aid in analysis:
    • {failure_log} → Key error stack trace from the automation framework
    • {failed_thread_log} → Detailed log of the failure event
    """

    requirement = """
    #Output Requirements:
    ##Case 1: If the failure is caused by AT Script, return with json format:
    {
       "root_cause_insight": "Clearly explain the exact root cause of the failure.",
       "action_insight": {
        "api_url": "The API endpoint URL that failed (if applicable).",
          "http_status_code": "The failed API request's status code. ",
          "request_id": "request ID extracted from the logs provided, Do not generate by yourself"
          "detail_log": "Relevant request body or response body extracted from logs message provided."
        },
       "failed_by_at_script": true
    }
    Notes:
    • "rootCauseInsight" should clearly explain the reason for the failure based on log analysis.
    • "actionSuggestion" must include actual extracted log details. If no relevant logs are found, leave the field as an empty string ("") without generating fake data.
    • Ensure the response is strictly in JSON format.

    ##Case 2: If the failure is NOT caused by an at script, return:
    {
      "root_cause_insight": "Explain why the failure is not due to an environment issue. Provide your thought process and references.",
      "failed_by_at_script": false
    }
    """
    return system_prompt + requirement


class ScriptBugAgentFactory(AgentFactory):
    def get_agent(self, mcp=None) -> Agent[AnalysisContext]:
        script_analyse_agent = Agent[AnalysisContext](
            name="script_analyse_agent",
            model="gpt-4o-mini",
            instructions=script_agent_instructions,
            output_type=ATScriptAIResponse,
            hooks=global_log_hook
        )
        return script_analyse_agent


def get_script_analyse_agent(mcp=None) -> Agent[AnalysisContext]:
    factory = ScriptBugAgentFactory()
    return factory.get_agent(mcp)
