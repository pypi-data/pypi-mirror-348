from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient

from spryx_agents.types.agent import LlmModel


class Agents:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client
        self._base_url = client.base_url

    async def list_agents(
        self,
        page: int = 1,
        limit: int = 10,
        order: str = "asc",
    ) -> dict:
        """List all agents."""
        return await self._client.get(
            f"{self._base_url}/agents",
            params={"page": page, "limit": limit, "order": order},
        )

    async def create_agent(
        self,
        name: str,
        instructions: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        vector_store_id: str = NOT_GIVEN,
        input_guardrail_instructions: str = NOT_GIVEN,
        output_guardrail_instructions: str = NOT_GIVEN,
        llm_model: LlmModel = LlmModel.GPT_4O_MINI,
        description: str = NOT_GIVEN,
        icon: str = NOT_GIVEN,
        color: str = NOT_GIVEN,
        icon_type: str = NOT_GIVEN,
        is_active: bool = True,
        metadata: dict = None,
        resources: list = None,
        handoff_rules: list = None,
    ) -> dict:
        """Create a new agent."""
        payload = {
            "name": name,
            "instructions": instructions,
            "temperature": temperature,
            "top_p": top_p,
            "llm_model": llm_model.value,
            "is_active": is_active,
        }

        if is_given(vector_store_id):
            payload["vector_store_id"] = vector_store_id
        
        if is_given(input_guardrail_instructions):
            payload["input_guardrail_instructions"] = input_guardrail_instructions
        
        if is_given(output_guardrail_instructions):
            payload["output_guardrail_instructions"] = output_guardrail_instructions
        
        if is_given(description):
            payload["description"] = description
        
        if is_given(icon):
            payload["icon"] = icon
        
        if is_given(color):
            payload["color"] = color
        
        if is_given(icon_type):
            payload["icon_type"] = icon_type

        if resources:
            payload["resources"] = resources
        
        if handoff_rules:
            payload["handoff_rules"] = handoff_rules
            
        if metadata:
            payload["metadata"] = metadata

        return await self._client.post(f"{self._base_url}/agents", json=payload)

    async def get_agent(
        self,
        agent_id: str,
    ) -> dict:
        """Retrieve a specific agent by ID."""
        return await self._client.get(f"{self._base_url}/agents/{agent_id}")

    async def update_agent(
        self,
        agent_id: str,
        name: str,
        instructions: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        vector_store_id: str = NOT_GIVEN,
        input_guardrail_instructions: str = NOT_GIVEN,
        output_guardrail_instructions: str = NOT_GIVEN,
        llm_model: LlmModel = LlmModel.GPT_4O_MINI,
        description: str = NOT_GIVEN,
        icon: str = NOT_GIVEN,
        color: str = NOT_GIVEN,
        icon_type: str = NOT_GIVEN,
        is_active: bool = True,
        metadata: dict = None,
        resources: list = None,
        handoff_rules: list = None,
    ) -> dict:
        """Update an existing agent."""
        payload = {
            "name": name,
            "instructions": instructions,
            "temperature": temperature,
            "top_p": top_p,
            "llm_model": llm_model.value,
            "is_active": is_active,
        }

        if is_given(vector_store_id):
            payload["vector_store_id"] = vector_store_id
        
        if is_given(input_guardrail_instructions):
            payload["input_guardrail_instructions"] = input_guardrail_instructions
        
        if is_given(output_guardrail_instructions):
            payload["output_guardrail_instructions"] = output_guardrail_instructions
        
        if is_given(description):
            payload["description"] = description
        
        if is_given(icon):
            payload["icon"] = icon
        
        if is_given(color):
            payload["color"] = color
        
        if is_given(icon_type):
            payload["icon_type"] = icon_type

        if resources:
            payload["resources"] = resources
        
        if handoff_rules:
            payload["handoff_rules"] = handoff_rules
            
        if metadata:
            payload["metadata"] = metadata

        return await self._client.put(f"{self._base_url}/agents/{agent_id}", json=payload)

    async def invoke_agent(
        self,
        agent_id: str,
        user_prompt: list,
        chat_id: str = NOT_GIVEN,
    ) -> dict:
        """Invoke an agent with a user prompt."""
        payload = {
            "user_prompt": user_prompt,
        }

        if is_given(chat_id):
            payload["chat_id"] = chat_id

        return await self._client.post(f"{self._base_url}/agents/{agent_id}/invoke", json=payload)
