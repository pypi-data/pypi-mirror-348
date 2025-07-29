"""
Main CrewAI adapter implementation.
"""

from typing import Any, Dict, Optional

from crewai import Agent, Crew, Task

from hivetrace.adapters.base_adapter import BaseAdapter
from hivetrace.adapters.crewai.monitored_agent import MonitoredAgent
from hivetrace.adapters.crewai.monitored_crew import MonitoredCrew
from hivetrace.adapters.crewai.tool_wrapper import wrap_tool
from hivetrace.adapters.utils.logging import process_agent_params
from hivetrace.utils.uuid_generator import generate_uuid


class CrewAIAdapter(BaseAdapter):
    """
    Integration adapter for monitoring CrewAI agents with Hivetrace.
    """

    def __init__(
        self,
        hivetrace,
        application_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        """
        Initialize the CrewAI adapter.

        Parameters:
        - hivetrace: The hivetrace instance for logging
        - application_id: ID of the application in Hivetrace
        - user_id: ID of the user in the conversation
        - session_id: ID of the session in the conversation
        - agent_id_mapping: Mapping from agent role names to their IDs
        """
        super().__init__(hivetrace, application_id, user_id, session_id)
        self.agent_id_mapping = agent_id_mapping if agent_id_mapping is not None else {}
        self.agents_info = {}

    def _get_agent_mapping(self, role: str) -> Dict[str, str]:
        """
        Gets agent ID and description from the mapping.

        Parameters:
        - role: Role name of the agent

        Returns:
        - Dictionary with agent ID and description
        """
        if self.agent_id_mapping and role in self.agent_id_mapping:
            mapping_data = self.agent_id_mapping[role]
            if isinstance(mapping_data, dict):
                return {
                    "id": mapping_data.get("id", generate_uuid()),
                    "description": mapping_data.get("description", ""),
                }
            elif isinstance(mapping_data, str):
                return {"id": mapping_data, "description": ""}
        return {"id": generate_uuid(), "description": ""}

    async def output_async(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Asynchronously logs agent output to Hivetrace.

        Parameters:
        - message: The message to log
        - additional_params: Additional parameters for the log
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        processed_params = process_agent_params(additional_params)

        self._prepare_and_log(
            "output",
            True,
            message_content=message,
            additional_params_from_caller=processed_params,
        )

    def output(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Synchronously logs agent output to Hivetrace.

        Parameters:
        - message: The message to log
        - additional_params: Additional parameters for the log
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        processed_params = process_agent_params(additional_params)

        self._prepare_and_log(
            "output",
            False,
            message_content=message,
            additional_params_from_caller=processed_params,
        )

    def agent_callback(self, message: Any) -> None:
        """
        Callback for agent actions.

        Parameters:
        - message: The message from the agent
        """
        message_text: str
        additional_params_for_log: Dict[str, Any]

        if isinstance(message, dict) and message.get("type") == "agent_thought":
            agent_id_from_message = message.get("agent_id")
            role = message.get("role", "")

            agent_mapping = self._get_agent_mapping(role)
            final_agent_id = agent_id_from_message or agent_mapping.get("id")

            agent_info_details = {
                "name": message.get("agent_name", role),
                "description": agent_mapping.get(
                    "description", message.get("agent_description", "Agent thought")
                ),
            }
            message_text = f"Thought from agent {role}: {message['thought']}"
            additional_params_for_log = {"agents": {final_agent_id: agent_info_details}}
        else:
            message_text = str(message)
            additional_params_for_log = {"agents": self.agents_info}

        self._prepare_and_log(
            "input",
            self.async_mode,
            message_content=message_text,
            additional_params_from_caller=additional_params_for_log,
        )

    def task_callback(self, message: Any) -> None:
        """
        Handler for task messages.
        Formats and logs task messages to Hivetrace.

        Parameters:
        - message: The message from the task
        """
        message_text = ""
        agent_info_for_log = {}

        if hasattr(message, "__dict__"):
            details = []
            for key, value in message.__dict__.items():
                if key not in [
                    "__dict__",
                    "__weakref__",
                    "callback",
                ]:
                    details.append(f"{key}: {value}")
                    if key == "agent":
                        current_agent_role = ""
                        if isinstance(value, str):
                            current_agent_role = value
                        elif hasattr(value, "role"):
                            current_agent_role = value.role

                        if current_agent_role:
                            agent_mapping = self._get_agent_mapping(current_agent_role)
                            mapped_id = agent_mapping["id"]
                            agent_info_for_log = {
                                mapped_id: {
                                    "name": current_agent_role,
                                    "description": agent_mapping["description"]
                                    or (
                                        getattr(value, "goal", "")
                                        if hasattr(value, "goal")
                                        else "Task agent"
                                    ),
                                }
                            }
            message_text = f"[Task] {' | '.join(details)}"
        else:
            message_text = f"[Task] {str(message)}"

        self._prepare_and_log(
            "output",
            self.async_mode,
            message_content=message_text,
            additional_params_from_caller={"agents": agent_info_for_log},
        )

    def _wrap_agent(self, agent: Agent) -> Agent:
        """
        Wraps an agent to monitor its actions.

        Parameters:
        - agent: The agent to wrap

        Returns:
        - Monitored version of the agent
        """
        agent_mapping = self._get_agent_mapping(agent.role)
        agent_id_for_monitored_agent = agent_mapping["id"]

        agent_props = agent.__dict__.copy()

        original_tools = getattr(agent, "tools", [])
        wrapped_tools = [wrap_tool(tool, agent.role, self) for tool in original_tools]
        agent_props["tools"] = wrapped_tools

        for key_to_remove in ["id", "agent_executor", "agent_ops_agent_id"]:
            if key_to_remove in agent_props:
                del agent_props[key_to_remove]

        monitored_agent = MonitoredAgent(
            adapter_instance=self,
            callback_func=self.agent_callback,
            agent_id=agent_id_for_monitored_agent,
            **agent_props,
        )

        return monitored_agent

    def _wrap_task(self, task: Task) -> Task:
        """
        Adds monitoring to the task.
        Wraps existing task callbacks to add logging.

        Parameters:
        - task: The task to wrap

        Returns:
        - Task with monitoring added
        """
        original_callback = task.callback

        def combined_callback(message):
            self.task_callback(message)
            if original_callback:
                original_callback(message)

        task.callback = combined_callback
        return task

    def wrap_crew(self, crew: Crew) -> Crew:
        """
        Adds monitoring to the existing CrewAI crew.
        Wraps all agents and tasks in the crew, as well as the kickoff methods.

        Parameters:
        - crew: The crew to wrap

        Returns:
        - Monitored version of the crew
        """
        current_agents_info = {}
        for agent_instance in crew.agents:
            if hasattr(agent_instance, "role"):
                agent_mapping = self._get_agent_mapping(agent_instance.role)
                agent_id = agent_mapping["id"]
                description = agent_mapping["description"] or getattr(
                    agent_instance, "goal", ""
                )
                current_agents_info[agent_id] = {
                    "name": agent_instance.role,
                    "description": description,
                }
        self.agents_info = current_agents_info

        wrapped_agents = [self._wrap_agent(agent) for agent in crew.agents]
        wrapped_tasks = [self._wrap_task(task) for task in crew.tasks]

        monitored_crew_instance = MonitoredCrew(
            original_crew_agents=wrapped_agents,
            original_crew_tasks=wrapped_tasks,
            original_crew_verbose=crew.verbose,
            manager_llm=getattr(crew, "manager_llm", None),
            memory=getattr(crew, "memory", None),
            process=getattr(crew, "process", None),
            config=getattr(crew, "config", None),
            adapter=self,
        )
        return monitored_crew_instance
