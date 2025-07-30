from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union
import uuid
from pydantic import BaseModel, Field
from pydantic import ConfigDict
import time # Import time for timestamps

# Removed Enum for EvaluationStatus as status is now just a string field in SpanData

@dataclass
class SpanData:
    # Identifiers (Non-defaults first)
    task_id: str
    agent_id: str
    id: str = field(default_factory=lambda: f"span_{uuid.uuid4().hex[:8]}")
    name: Optional[str] = None
    
    # Static/Config Info (Passed via trace_span metadata usually)
    prompt_template: Optional[str] = None 
    callable_agents: Optional[List[str]] = None # Can be extracted from metadata
    metadata: Dict[str, Any] = field(default_factory=dict) # Other custom static metadata. For MVP, frontend primarily uses this for { 'is_golden': boolean }

    # Execution Data (Inputs Dict, Output String)
    inputs: Dict[str, Any] = field(default_factory=dict) # Flexible Dictionary
    output: Optional[Union[str, Dict[str, Any]]] = None # Changed to Union[str, Dict[str, Any]]
    
    # Evaluation Data (Managed Separately)
    status: str = "unlabeled" # For MVP: 'unlabeled', 'labeled'
    userFeedback: Optional[str] = None

    def end(self): 
        # if self.end_time is None: # Removed for MVP
        #     self.end_time = time.time()
        #     if self.start_time: # Ensure start_time exists # Removed for MVP
        #         self.duration_ms = (self.end_time - self.start_time) * 1000 # Removed for MVP
        pass # Method kept for API compatibility if storage layer expects it, but no timing logic for MVP

@dataclass
class TaskData:
    id: str = field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str = "Untitled Task" # Added name field with a default
    metadata: Dict[str, Any] = field(default_factory=dict) # Can contain grouping hints

    def end(self): 
        #  if self.end_time is None: # Removed for MVP
        #     self.end_time = time.time()
        #     if self.start_time: # Ensure start_time exists # Removed for MVP
        #        self.duration_ms = (self.end_time - self.start_time) * 1000 # Removed for MVP
        pass # Method kept for API compatibility if storage layer expects it, but no timing logic for MVP

# Removed old Rule, UserLabelData, Evaluation classes 

# --- New Models for Experiments --- 

@dataclass
class Agent:
    name: str
    id: str = field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")
    description: Optional[str] = None

@dataclass
class BasePrompt:
    agentId: str 
    name: str
    content: str
    id: str = field(default_factory=lambda: f"bp_{uuid.uuid4().hex[:8]}")
    version: int = 1

@dataclass
class Experiment:
    name: str
    id: str = field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    description: Optional[str] = None
    sourceTaskName: Optional[str] = None # Added for linking to a source task name

@dataclass
class ExperimentPromptVersion:
    experimentId: str
    basePromptId: str
    agentId: str # Denormalized from BasePrompt for easier query
    nameInExperiment: str # Can be BasePrompt.name or custom for the experiment
    originalContentAtExperimentStart: str
    currentWorkingContent: str
    id: str = field(default_factory=lambda: f"epv_{uuid.uuid4().hex[:8]}")
    statusInExperiment: str = "draft" # E.g., 'draft', 'ready_for_test', 'tested', 'archived'

@dataclass
class Feedback:
    experimentPromptVersionId: str
    feedbackText: str 
    id: str = field(default_factory=lambda: f"fb_{uuid.uuid4().hex[:8]}")
    sourceDescription: Optional[str] = None # E.g., "User report #123", "Golden dataset item #45"
    # aiEngineeredSuggestionText: Optional[str] = None # Removed as per discussion
    originalInput: Optional[Dict[str, Any]] = field(default=None)
    originalPromptUsed: Optional[str] = field(default=None)
    originalOutputGenerated: Optional[str] = field(default=None) 