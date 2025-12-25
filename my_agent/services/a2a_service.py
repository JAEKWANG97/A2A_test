from typing import Dict
from google.genai import types
from .runner_pool import RunnerPool
from ..core.exceptions import AgentNotFoundError, ToolExecutionError


class A2AService:
    """Handles agent-to-agent communication via Runner."""
    
    def __init__(self, runner_pool: RunnerPool, session_manager=None):
        self.runner_pool = runner_pool
        self.session_manager = session_manager
    
    async def send_to_agent(
        self,
        agent_name: str,
        message: str,
        user_id: str,
        session_id: str,
        context_prefix: str = ""
    ) -> str:
        """Send message to agent and get response.
        
        Args:
            agent_name: Name of target agent
            message: Message to send
            user_id: User ID for session
            session_id: Session ID
            context_prefix: Optional context to prepend (e.g., user preferences)
        
        Returns:
            Agent's text response
        
        Raises:
            AgentNotFoundError: If agent not found
            ToolExecutionError: If agent execution fails
        """
        if not self.runner_pool.has_agent(agent_name):
            raise AgentNotFoundError(f"Agent '{agent_name}' not found")
        
        try:
            # Ensure session exists before calling agent
            if self.session_manager:
                await self.session_manager.ensure_session(
                    self.runner_pool.app_name,
                    user_id,
                    session_id
                )
            
            runner = self.runner_pool.get_runner(agent_name)
            full_message = context_prefix + message
            content = types.Content(role="user", parts=[types.Part(text=full_message)])
            
            response_text = ""
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        # Extract text parts only
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text += part.text
                    break
            
            return response_text or "No response from agent"
        
        except Exception as e:
            raise ToolExecutionError(f"Failed to communicate with {agent_name}: {str(e)}")
