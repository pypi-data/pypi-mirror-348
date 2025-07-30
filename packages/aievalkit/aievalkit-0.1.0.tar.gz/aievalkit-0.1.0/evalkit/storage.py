import abc
import requests # Added
# import json # Not strictly needed if HttpStorage is simplified/timestamp-less
# import httpx # Not strictly needed if HttpStorage is simplified/timestamp-less
from typing import List, Dict, Optional, Any, Union # Ensure Union is here if models use it
from .models import TaskData, SpanData, Agent, BasePrompt, Experiment, ExperimentPromptVersion, Feedback
from dataclasses import asdict
# import time # No longer needed
import uuid

class BaseStorage(abc.ABC):
    """Abstract base class for storing task and span data."""

    @abc.abstractmethod
    def save_task(self, task: TaskData):
        """Save a new task."""
        pass

    @abc.abstractmethod
    def save_span(self, span: SpanData):
        """Save a new span."""
        pass

    @abc.abstractmethod
    def update_span_output(self, span_id: str, output: Optional[str]):
        """Update the output for an existing span."""
        pass
    
    @abc.abstractmethod
    def update_span_feedback(self, span_id: str, feedback: Optional[str], status: Optional[str]):
        """Update the user feedback and status for a span."""
        pass

    @abc.abstractmethod
    def get_task(self, task_id: str) -> Optional[TaskData]:
        """Retrieve a specific task by ID."""
        pass

    @abc.abstractmethod
    def get_spans_for_task(self, task_id: str) -> List[SpanData]:
        """Retrieve all spans associated with a specific task ID."""
        pass

    @abc.abstractmethod
    def get_span(self, span_id: str) -> Optional[SpanData]:
        """Retrieve a specific span by ID."""
        pass

    @abc.abstractmethod
    def get_all_tasks(self) -> List[TaskData]:
        """Retrieve all tasks."""
        pass

    @abc.abstractmethod
    def get_all_spans(self) -> List[SpanData]:
        """Retrieve all spans."""
        pass

    @abc.abstractmethod
    def end_task(self, task_id: str):
        """Marks a task as ended. Optional: could record end time if timestamps were used."""
        pass

    # --- Abstract methods for Agent --- 
    @abc.abstractmethod
    def get_all_agents(self) -> List[Agent]:
        pass

    @abc.abstractmethod
    def save_agent(self, agent: Agent) -> Agent:
        """Saves a new agent or updates an existing one based on ID."""
        pass

    @abc.abstractmethod
    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Retrieves an agent by its name."""
        pass

    # --- Abstract methods for BasePrompt --- 
    @abc.abstractmethod
    def get_all_base_prompts(self) -> List[BasePrompt]:
        pass
    
    @abc.abstractmethod
    def get_base_prompts_for_agent(self, agent_id: str) -> List[BasePrompt]:
        pass

    # --- Abstract methods for Experiment --- 
    @abc.abstractmethod
    def create_experiment(self, experiment: Experiment) -> Experiment:
        pass

    @abc.abstractmethod
    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        pass

    @abc.abstractmethod
    def get_all_experiments(self) -> List[Experiment]:
        pass

    @abc.abstractmethod
    def delete_experiment(self, experiment_id: str) -> None:
        pass

    # --- Abstract methods for ExperimentPromptVersion --- 
    @abc.abstractmethod
    def get_experiment_prompt_versions_for_experiment(self, experiment_id: str) -> List[ExperimentPromptVersion]:
        pass

    @abc.abstractmethod
    def update_experiment_prompt_version_content(self, epv_id: str, new_content: str) -> Optional[ExperimentPromptVersion]:
        pass
    
    @abc.abstractmethod
    def get_feedback_for_experiment_prompt_version(self, epv_id: str) -> List[Feedback]:
        pass

    @abc.abstractmethod
    def save_experiment_prompt_version(self, epv: ExperimentPromptVersion) -> ExperimentPromptVersion:
        """Saves or updates an ExperimentPromptVersion."""
        pass

    # --- Abstract methods for Feedback --- 
    @abc.abstractmethod
    def get_feedback(self, feedback_id: str) -> Optional[Feedback]:
        pass

class MemoryStorage(BaseStorage):
    """In-memory implementation of the storage interface."""
    def __init__(self):
        self._tasks: Dict[str, TaskData] = {}
        self._spans: Dict[str, SpanData] = {}
        self._spans_by_task: Dict[str, List[str]] = {}
        # New storage dictionaries
        self._agents: Dict[str, Agent] = {}
        self._base_prompts: Dict[str, BasePrompt] = {}
        self._experiments: Dict[str, Experiment] = {}
        self._experiment_prompt_versions: Dict[str, ExperimentPromptVersion] = {}
        self._feedback: Dict[str, Feedback] = {}
        print("Timestamp-less MemoryStorage initialized.")

    def save_task(self, task: TaskData):
        if task.id not in self._tasks:
            self._tasks[task.id] = task
            self._spans_by_task[task.id] = []
        else:
            self._tasks[task.id].metadata.update(task.metadata)

    def save_span(self, span: SpanData):
        if span.id not in self._spans:
            self._spans[span.id] = span
            if span.task_id in self._spans_by_task:
                self._spans_by_task[span.task_id].append(span.id)
            else:
                self._spans_by_task[span.task_id] = [span.id]
        else:
            self._spans[span.id] = span # Simple overwrite

    def update_span_output(self, span_id: str, output: Optional[str]):
        span = self._spans.get(span_id)
        if span:
            span.output = output
        else:
            print(f"Warning: Cannot update output for span {span_id}. Not found.")

    def update_span_feedback(self, span_id: str, feedback: Optional[str], status: Optional[str]):
        span = self._spans.get(span_id)
        if span:
            if feedback is not None:
                span.userFeedback = feedback
            if status is not None:
                span.status = status
            elif feedback is not None and status is None:
                 span.status = "labeled"
            return span
        else:
            print(f"Warning: Cannot update feedback for span {span_id}. Not found.")
            return None

    def get_task(self, task_id: str) -> Optional[TaskData]:
        return self._tasks.get(task_id)

    def get_spans_for_task(self, task_id: str) -> List[SpanData]:
        span_ids = self._spans_by_task.get(task_id, [])
        return [self._spans[span_id] for span_id in span_ids if span_id in self._spans]

    def get_span(self, span_id: str) -> Optional[SpanData]:
        return self._spans.get(span_id)

    def get_all_tasks(self) -> List[TaskData]:
        return list(self._tasks.values())

    def get_all_spans(self) -> List[SpanData]:
        return list(self._spans.values())
    
    def end_task(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            # In a real scenario with timestamps, you might set an end_time here.
            # For now, it's a no-op on the data itself, but good for API completeness.
            print(f"[MemoryStorage] Task '{task_id}' marked as ended.")
        else:
            print(f"[MemoryStorage] Warning: Cannot end task {task_id}. Not found.")

    # --- Implementations for Agent --- 
    def get_all_agents(self) -> List[Agent]:
        return list(self._agents.values())
    
    def save_agent(self, agent: Agent) -> Agent:
        self._agents[agent.id] = agent
        # print(f"[MemoryStorage] Saved Agent: {agent.id} - {agent.name}")
        return agent

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        # This assumes agent names are unique if used as a lookup key.
        # If agent ID is the name itself, this is equivalent to get_agent(id=name)
        # For a more general case where name might not be ID:
        for agent in self._agents.values():
            if agent.name == name:
                return agent
        return None

    # --- Implementations for BasePrompt --- 
    def save_base_prompt(self, base_prompt: BasePrompt) -> BasePrompt:
        self._base_prompts[base_prompt.id] = base_prompt
        return base_prompt

    def get_base_prompt(self, base_prompt_id: str) -> Optional[BasePrompt]:
        return self._base_prompts.get(base_prompt_id)
    
    def get_all_base_prompts(self) -> List[BasePrompt]:
        return list(self._base_prompts.values())

    def get_base_prompts_for_agent(self, agent_id: str) -> List[BasePrompt]:
        return [bp for bp in self._base_prompts.values() if bp.agentId == agent_id]

    # --- Implementations for Experiment --- 
    def save_experiment(self, experiment: Experiment) -> Experiment:
        self._experiments[experiment.id] = experiment
        return experiment

    def create_experiment(self, experiment: Experiment) -> Experiment:
        # Ensure ID is set if not already, as mock data might provide it
        if not experiment.id:
            experiment.id = f"exp_{uuid.uuid4().hex[:8]}"
        return self.save_experiment(experiment)

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        return self._experiments.get(experiment_id)

    def get_all_experiments(self) -> List[Experiment]:
        return list(self._experiments.values())

    def delete_experiment(self, experiment_id: str) -> bool: # Changed to return bool
        if experiment_id in self._experiments:
            del self._experiments[experiment_id]
            return True
        return False

    # --- Implementations for ExperimentPromptVersion --- 
    def save_experiment_prompt_version(self, epv: ExperimentPromptVersion) -> ExperimentPromptVersion:
        """Saves or updates an ExperimentPromptVersion in memory."""
        # Ensure ID if not set (though typically EPV would have it from model default)
        if not epv.id:
            epv.id = f"epv_{uuid.uuid4().hex[:8]}"
        self._experiment_prompt_versions[epv.id] = epv
        # print(f"[MemoryStorage] Saved/Updated EPV: {epv.id}")
        return epv

    def get_experiment_prompt_versions_for_experiment(self, experiment_id: str) -> List[ExperimentPromptVersion]:
        return [epv for epv in self._experiment_prompt_versions.values() if epv.experimentId == experiment_id]

    def update_experiment_prompt_version_content(self, epv_id: str, new_content: str) -> Optional[ExperimentPromptVersion]:
        epv = self._experiment_prompt_versions.get(epv_id)
        if epv:
            epv.currentWorkingContent = new_content
            return epv
        return None
    
    def get_feedback_for_experiment_prompt_version(self, epv_id: str) -> List[Feedback]:
        return [f for f in self._feedback.values() if f.experimentPromptVersionId == epv_id]

    # --- Implementations for Feedback --- 
    def get_feedback(self, feedback_id: str) -> Optional[Feedback]:
        return self._feedback.get(feedback_id)

    # New method implementation
    def save_feedback(self, feedback: Feedback) -> Feedback:
        """Saves a new feedback entry."""
        if feedback.id in self._feedback:
            print(f"Warning: Feedback {feedback.id} already exists. Overwriting.")
        self._feedback[feedback.id] = feedback
        return feedback


# --- NEW HttpStorage --- 

# Helper function to serialize TaskData/SpanData correctly
def data_to_dict(data_obj): 
    if hasattr(data_obj, '__dict__'): # Handle dataclasses
        return asdict(data_obj)
    elif isinstance(data_obj, dict):
        return data_obj
    # Add handling for other types if necessary
    return str(data_obj)

class HttpStorage(BaseStorage):
    """Sends task and span data to a remote backend via HTTP."""
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip('/')
        self.ingest_url = f"{self.base_url}/api/ingest"
        self.api_url = f"{self.base_url}/api"
        self.timeout = timeout
        print(f"HttpStorage initialized. Ingest URL: {self.ingest_url}, API URL: {self.api_url}")

    def _send_request(self, method: str, url: str, json_data: Optional[Dict] = None, expect_json_response: bool = True):
        print(f"HTTP {method} to {url} with data: {json_data if json_data else 'No data'}") # Keep for logging
        try:
            response = requests.request(method, url, json=json_data, timeout=self.timeout)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            if expect_json_response:
                # Check if response is empty before trying to parse JSON
                if response.content:
                    return response.json()
                else:
                    return None # Or {} or raise an error, depending on expected behavior for empty success
            return response # For non-JSON responses (e.g., 204 No Content for DELETE)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected error occurred with the request: {req_err}")
        return None # Return None if any error occurs or if no JSON response expected and not returning raw response

    def save_task(self, task: TaskData):
        task_dict = data_to_dict(task)
        self._send_request("POST", f"{self.ingest_url}/task", json_data=task_dict)

    def save_span(self, span: SpanData):
        span_dict = data_to_dict(span)
        self._send_request("POST", f"{self.ingest_url}/span", json_data=span_dict)

    def update_span_output(self, span_id: str, output: Optional[str]):
        self._send_request("PUT", f"{self.ingest_url}/span/{span_id}/output", json_data={"output": output})
    
    def update_span_feedback(self, span_id: str, feedback: Optional[str], status: Optional[str]):
        payload = {}
        if feedback is not None:
            payload['userFeedback'] = feedback
        if status is not None:
            payload['status'] = status
        if payload:
            return self._send_request("PUT", f"{self.api_url}/spans/{span_id}/feedback", json_data=payload)
        return None

    def get_task(self, task_id: str) -> Optional[TaskData]:
        response = self._send_request("GET", f"{self.api_url}/tasks/{task_id}")
        return TaskData(**response) if response else None

    def get_spans_for_task(self, task_id: str) -> List[SpanData]:
        response = self._send_request("GET", f"{self.api_url}/tasks/{task_id}/spans") # Assuming endpoint
        return [SpanData(**span_data) for span_data in response] if response else []

    def get_span(self, span_id: str) -> Optional[SpanData]:
        response = self._send_request("GET", f"{self.api_url}/spans/{span_id}")
        return SpanData(**response) if response else None

    def get_all_tasks(self) -> List[TaskData]:
        response = self._send_request("GET", f"{self.api_url}/tasks")
        return [TaskData(**task_data) for task_data in response] if response else []

    def get_all_spans(self) -> List[SpanData]:
        response = self._send_request("GET", f"{self.api_url}/spans")
        return [SpanData(**span_data) for span_data in response] if response else []
    
    def end_task(self, task_id: str):
        self._send_request("PUT", f"{self.ingest_url}/task/{task_id}/end", expect_json_response=False)

    # --- HttpStorage implementations for the lean set of new model methods ---

    def get_all_agents(self) -> List[Agent]:
        response = self._send_request("GET", f"{self.api_url}/agents/")
        return [Agent(**agent_data) for agent_data in response] if response else []

    def save_agent(self, agent: Agent) -> Agent:
        """Placeholder: SDK typically doesn't register agents this way via HttpStorage."""
        print(f"Warning: HttpStorage.save_agent called for {agent.id}. This typically does not send data.")
        return agent # Return as is to satisfy interface

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Placeholder: HttpStorage would need a specific API endpoint for this."""
        print(f"Warning: HttpStorage.get_agent_by_name called for {name}. Not implemented for remote calls.")
        # To avoid errors, try to list all and filter, though inefficient for HTTP
        # For a real implementation, this would be a specific API call like /api/agents?name={name}
        all_agents = self.get_all_agents()
        for ag in all_agents:
            if ag.name == name:
                return ag
        return None

    def get_all_base_prompts(self) -> List[BasePrompt]:
        response = self._send_request("GET", f"{self.api_url}/base_prompts/")
        return [BasePrompt(**bp_data) for bp_data in response] if response else []

    def get_base_prompts_for_agent(self, agent_id: str) -> List[BasePrompt]:
        response = self._send_request("GET", f"{self.api_url}/base_prompts/?agent_id={agent_id}")
        return [BasePrompt(**bp_data) for bp_data in response] if response else []

    def create_experiment(self, experiment: Experiment) -> Experiment:
        exp_data = asdict(experiment)
        response = self._send_request("POST", f"{self.api_url}/experiments/", json_data=exp_data)
        return Experiment(**response) if response else None # type: ignore

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        response = self._send_request("GET", f"{self.api_url}/experiments/{experiment_id}")
        return Experiment(**response) if response else None

    def get_all_experiments(self) -> List[Experiment]:
        response = self._send_request("GET", f"{self.api_url}/experiments/")
        return [Experiment(**exp_data) for exp_data in response] if response else []

    def delete_experiment(self, experiment_id: str) -> None:
        self._send_request("DELETE", f"{self.api_url}/experiments/{experiment_id}", expect_json_response=False)

    def get_experiment_prompt_versions_for_experiment(self, experiment_id: str) -> List[ExperimentPromptVersion]:
        response = self._send_request("GET", f"{self.api_url}/experiments/{experiment_id}/prompt_versions/")
        return [ExperimentPromptVersion(**epv_data) for epv_data in response] if response else []

    def update_experiment_prompt_version_content(self, epv_id: str, new_content: str) -> Optional[ExperimentPromptVersion]:
        payload = {"currentWorkingContent": new_content}
        response = self._send_request("PUT", f"{self.api_url}/experiment_prompt_versions/{epv_id}", json_data=payload)
        return ExperimentPromptVersion(**response) if response else None

    def get_feedback_for_experiment_prompt_version(self, epv_id: str) -> List[Feedback]:
        response = self._send_request("GET", f"{self.api_url}/experiment_prompt_versions/{epv_id}/feedback/")
        return [Feedback(**fb_data) for fb_data in response] if response else []

    def save_experiment_prompt_version(self, epv: ExperimentPromptVersion) -> ExperimentPromptVersion:
        """Placeholder implementation for HttpStorage.
        This method is required by BaseStorage but not typically used by the client-side SDK via HttpStorage.
        EPVs are generally managed and created by the backend during experiment setup.
        """
        print(f"Warning: HttpStorage.save_experiment_prompt_version called for {epv.id}. This typically does not send data to a remote server via HttpStorage.")
        # To satisfy the type hint and allow instantiation, we return the passed EPV.
        # In a real scenario where HttpStorage might need this, it would make a POST request.
        return epv

    def get_feedback(self, feedback_id: str) -> Optional[Feedback]:
        response = self._send_request("GET", f"{self.api_url}/feedback/{feedback_id}") # Assuming endpoint
        return Feedback(**response) if response else None

    # --- Methods from BaseStorage that HttpStorage WON'T implement (aligning with lean approach) ---
    # save_agent, get_agent (covered by get_all_agents for listing)
    # save_base_prompt, get_base_prompt (covered by get_all_base_prompts/get_base_prompts_for_agent for listing)
    # update_base_prompt_content
    # save_experiment_prompt_version, get_experiment_prompt_version, update_experiment_prompt_version_status
    # save_feedback, get_feedback
    # These will just not be defined here, and BaseStorage won't require them.
    # If a method from BaseStorage is NOT here, it means HttpStorage doesn't provide it.
    # The `raise NotImplementedError()` lines from before will be implicitly gone for removed abstract methods. 