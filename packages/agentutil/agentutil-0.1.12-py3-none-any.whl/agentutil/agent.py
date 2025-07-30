from abc import ABC, abstractmethod
from agentutil.utils.agentAssistant import AgentAssistant, TestAgentAssistant
from django.forms import Form


# 🎭 Abstract Base Class for Agents
class Agent(ABC):
    def __init__(self, assistant: AgentAssistant=None, form: Form=None):
        self.form = form
        if assistant:
            self.assistant = assistant
        else:
            self.assistant = TestAgentAssistant()
    @abstractmethod
    async def run(self, data):
        pass
