"""
Monitored Crew implementation for CrewAI.
"""

from typing import Any

from crewai import Crew


class MonitoredCrew(Crew):
    """
    A monitored version of CrewAI's Crew class that logs all actions to HiveTrace.
    """

    model_config = {"extra": "allow"}

    def __init__(
        self,
        adapter,
        original_crew_agents,
        original_crew_tasks,
        original_crew_verbose,
        **kwargs,
    ):
        """
        Initialize the monitored crew.

        Parameters:
        - adapter: The CrewAI adapter instance
        - original_crew_agents: List of agents for the crew
        - original_crew_tasks: List of tasks for the crew
        - original_crew_verbose: Verbose flag from original crew
        - **kwargs: Additional parameters for the Crew class
        """
        super().__init__(
            agents=original_crew_agents,
            tasks=original_crew_tasks,
            verbose=original_crew_verbose,
            **kwargs,
        )
        self._adapter = adapter

    def _log_kickoff_result(self, result: Any):
        """
        Log the final result of the crew execution.

        Parameters:
        - result: The result to log
        """
        if result:
            final_message = f"[Final Result] {str(result)}"
            agent_info_for_log = {}
            for agent in self.agents:
                if hasattr(agent, "agent_id") and hasattr(agent, "role"):
                    agent_info_for_log[agent.agent_id] = {
                        "name": agent.role,
                        "description": getattr(agent, "goal", ""),
                    }

            additional_params = {
                "agents": agent_info_for_log,
            }
            self._adapter._prepare_and_log(
                "output",
                self._adapter.async_mode,
                message_content=final_message,
                additional_params_from_caller=additional_params,
            )

    def kickoff(self, *args, **kwargs):
        """
        Start the crew's work and log the result.

        Returns:
        - Result of the crew's work
        """
        result = super().kickoff(*args, **kwargs)
        self._log_kickoff_result(result)
        return result

    async def kickoff_async(self, *args, **kwargs):
        """
        Start the crew's work asynchronously and log the result.

        Returns:
        - Result of the crew's work
        """
        if not hasattr(super(), "kickoff_async"):
            raise NotImplementedError(
                "Async kickoff is not supported by the underlying crew's superclass"
            )

        result = await super().kickoff_async(*args, **kwargs)
        self._log_kickoff_result(result)
        return result
