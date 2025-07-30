import contextvars
import functools
import inspect
import uuid
from typing import Optional, Dict, Any, Callable, Generator, TypeVar, Generic
from contextlib import contextmanager

from .storage import BaseStorage, MemoryStorage, HttpStorage
from .models import TaskData, SpanData, Agent

# Consolidated Context Variables
_CURRENT_TASK_ID_CONTEXT_VAR: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("maple_current_task_id", default=None)
# Store the whole TaskData object in context to access its name easily
_CURRENT_TASK_OBJECT_CONTEXT_VAR: contextvars.ContextVar[Optional[TaskData]] = contextvars.ContextVar("maple_current_task_object", default=None)

class SpanContext:
    """Context manager for tracing a single span."""
    def __init__(self, kit_instance: 'EvalKit', task_id: str, agent_id: str, inputs: Dict[str, Any], prompt: Optional[str], metadata: Optional[Dict[str, Any]]):
        self._kit = kit_instance
        self.span = SpanData(
            task_id=task_id,
            agent_id=agent_id,
            inputs=inputs,
            prompt_template=prompt,
            callable_agents=metadata.pop('callable_agents', None) if metadata else None,
            metadata=metadata if metadata else {},
        )
        self._kit.storage.save_span(self.span)

    @property
    def span_id(self) -> str:
        return self.span.id

    def set_output(self, output_data: Optional[str]):
        self.span.output = output_data
        self._kit.storage.update_span_output(self.span.id, output_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._kit.storage.end_span(self.span.id)
        if exc_type:
            pass 
        return False

class TaskContext:
    """Context manager for tracing a task (group of spans)."""
    def __init__(self, kit_instance: 'EvalKit', task_name: str, task_id: Optional[str], metadata: Optional[Dict[str, Any]]):
        self._kit = kit_instance
        self.task = TaskData(
            id=task_id if task_id else f"task_{uuid.uuid4().hex[:8]}",
            name=task_name, # Task name is stored here
            metadata=metadata if metadata else {}
        )
        self._kit.storage.save_task(self.task)

    @property
    def task_id(self) -> str:
        return self.task.id

    def trace_span(self, agent_id: str, inputs: Dict[str, Any], prompt: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> SpanContext:
        return SpanContext(
            kit_instance=self._kit, 
            task_id=self.task_id, 
            agent_id=agent_id, 
            inputs=inputs, 
            prompt=prompt, 
            metadata=metadata
        )

    def __enter__(self):
        self._token_id = _CURRENT_TASK_ID_CONTEXT_VAR.set(self.task.id)
        # Store the whole task object in the new context var
        self._token_task_object = _CURRENT_TASK_OBJECT_CONTEXT_VAR.set(self.task)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._kit.storage.end_task(self.task.id)
        if exc_type:
            pass
        _CURRENT_TASK_ID_CONTEXT_VAR.reset(self._token_id)
        _CURRENT_TASK_OBJECT_CONTEXT_VAR.reset(self._token_task_object) # Reset the new context var
        return False

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent):
        self._agents[agent.id] = agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def get_or_create_agent(self, agent_id: str, agent_name: Optional[str] = None) -> Agent:
        lookup_key = agent_name or agent_id 
        if lookup_key not in self._agents:
            id_to_use = agent_name or agent_id
            name_to_use = agent_name or agent_id
            new_agent = Agent(id=id_to_use, name=name_to_use)
            self.register_agent(new_agent)
            return new_agent
        return self._agents[lookup_key]

class EvalKit:
    """Main entry point for the evaluate library."""
    def __init__(self, storage: Optional[BaseStorage] = None, agent_registry: Optional[AgentRegistry] = None, export_to_endpoint: Optional[str] = None):
        if export_to_endpoint:
            from .storage import HttpStorage # Lazy import
            # Corrected HttpStorage instantiation
            self.storage = HttpStorage(base_url=export_to_endpoint)
            # print(f"EvalKit configured to export data to: {export_to_endpoint}") # This is now printed by HttpStorage
        elif storage:
            self.storage = storage
        else:
            self.storage = MemoryStorage() # Default to in-memory storage
            print("EvalKit initialized with MemoryStorage (data will not be persisted beyond the session).")
        
        self.agent_registry = agent_registry if agent_registry else AgentRegistry()
        self._grouping_strategies: Dict[str, Callable] = {} # Retain for register/get grouping_strategy

    @contextmanager
    def trace_task(self, task_name: str, metadata: Optional[Dict[str, Any]] = None) -> Generator[TaskContext, None, None]: # Yield TaskContext
        # This context manager now creates and yields a TaskContext instance.
        # The TaskContext instance itself handles setting/resetting context vars.
        task_context = TaskContext(
            kit_instance=self,
            task_name=task_name,
            task_id=None, # TaskContext will generate ID if None
            metadata=metadata
        )
        with task_context: # Enter/exit TaskContext to manage context vars
            try:
                yield task_context
            finally:
                # end_task is called by TaskContext.__exit__
                pass

    def trace_interaction(self, agent_name: str, prompt_template_arg_name: Optional[str] = None, span_metadata: Optional[Dict[str, Any]] = None):
        self.agent_registry.get_or_create_agent(agent_id=agent_name, agent_name=agent_name)

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                task_id = _CURRENT_TASK_ID_CONTEXT_VAR.get()
                current_task_object = _CURRENT_TASK_OBJECT_CONTEXT_VAR.get() # Get the current task object

                if not task_id or not current_task_object:
                    print(f"[Maple Warning] No active task context for '{func.__name__}'. Span not recorded.")
                    return func(*args, **kwargs)

                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                inputs_dict = {}
                prompt_template_value = None
                
                current_span_metadata = span_metadata.copy() if span_metadata else {}
                
                # Inject task_name into span metadata for grouping/categorization
                current_span_metadata["task_name_for_grouping"] = current_task_object.name

                for param_name, value in bound_args.arguments.items():
                    is_prompt_arg = prompt_template_arg_name and param_name == prompt_template_arg_name
                    if is_prompt_arg:
                        if isinstance(value, (str, dict)):
                            prompt_template_value = value
                        elif hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
                            prompt_template_value = value.to_dict()
                        else:
                            try: prompt_template_value = str(value)
                            except: prompt_template_value = "<unserializable_prompt>"
                    try:
                        if isinstance(value, (str, int, float, bool, list, dict, tuple)) or value is None:
                             inputs_dict[param_name] = value
                        elif hasattr(value, 'model_dump') and callable(getattr(value, 'model_dump')):
                            inputs_dict[param_name] = value.model_dump()
                        elif hasattr(value, 'dict') and callable(getattr(value, 'dict')):
                            inputs_dict[param_name] = value.dict()
                        else:
                             inputs_dict[param_name] = str(value)
                    except Exception:
                        inputs_dict[param_name] = "<unserializable_input>"

                output_value = func(*args, **kwargs)
                serializable_output = output_value
                if not isinstance(output_value, (str, dict, type(None))):
                    try: serializable_output = str(output_value)
                    except: serializable_output = "<unserializable_output>"

                span_id = f"span_{uuid.uuid4().hex[:8]}"
                span_data = SpanData(
                    id=span_id, task_id=task_id, agent_id=agent_name, name=agent_name,
                    inputs=inputs_dict,
                    prompt_template=str(prompt_template_value) if prompt_template_value is not None else None,
                    output=serializable_output,
                    metadata=current_span_metadata
                )
                if self.storage:
                    self.storage.save_span(span_data)
                return output_value
            return wrapper
        return decorator

    def register_grouping_strategy(self, name: str, func: Callable):
        if not callable(func):
            raise TypeError("Provided strategy must be a callable function.")
        self._grouping_strategies[name] = func
        print(f"Grouping strategy registered: '{name}'")

    def get_grouping_strategy(self, name: str) -> Optional[Callable]:
        return self._grouping_strategies.get(name) 