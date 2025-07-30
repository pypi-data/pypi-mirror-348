import asyncio
import os
from datetime import datetime, timezone
from dotenv import load_dotenv 
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.llm import GeminiLLM
from cneura_ai.memory import MemoryManager, PersistentWorkingMemory
from cneura_ai.agent import Agent
from lib.tools import create_tool, get_knowledge_base_memory, get_long_term_memory, get_short_term_memory, get_tool, research, run_tool, set_long_term_memory, set_short_term_memory, shell


load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "meta_agent_in")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "meta_agent_out")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "meta_agent_error")
REMOTE_URL = os.getenv("REMOTE_URL") 
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = os.getenv("CHROMA_PORT", 8000)


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

def main(message):
    try:
        data = message.get("body")
        task_id = data.get("task_id")
        state_id = data.get("state_id", None)
        query = data.get("query", None)
        timestamp = str(datetime.now(timezone.utc))

        tools = {
            "create_tool": create_tool,
            "get_tool": get_tool,
            "run_tool": run_tool,
            "research": research,
            "set_short_term_memory": set_short_term_memory,
            "get_short_term_memory": get_short_term_memory,
            "set_long_term_memory": set_long_term_memory,
            "get_long_term_memory": get_long_term_memory,
            "get_knowledge_base_memory": get_knowledge_base_memory,
            "shell": shell
        }

        tools_doc = [
            {
                "name": "create_tool",
                "description": "Creates a new tool with a provided description.",
                "args": ["description: string"],
                "example": {
                    "tool": "create_tool",
                    "args": ["Create a tool that calculates the sum of two numbers."]
                },
                "returns": "dict",
                "instant": False
            },
            {
                "name": "get_tool",
                "description": "Queries a tool based on a given query and retrieves the top matching tool.",
                "args": ["query: string"],
                "example": {
                    "tool": "get_tool",
                    "args": ["sum of numbers"]
                },
                "returns": "dict"
            },
            {
                "name": "run_tool",
                "description": "Executes a tool with the given initialization and run arguments.",
                "args": ["url: string", "args: dict"],
                "example": {
                    "tool": "run_tool",
                    "args": ["http://localhost:8001/tools/run", {"init": "args_data"}]
                },
                "returns": "dict"
            },
            {
                "name": "research",
                "description": "Sends a query to the research API and returns the result.",
                "args": ["query: string"],
                "example": {
                    "tool": "research",
                    "args": ["What are the latest advancements in AI?"]
                },
                "returns": "dict"
            },
            {
                "name": "set_short_term_memory",
                "description": "Stores a piece of memory in the agent's short-term memory.",
                "args": ["memory: string"],
                "example": {
                    "tool": "set_short_term_memory",
                    "args": ["The user asked about AI advancements."]
                },
                "returns": "None"
            },
            {
                "name": "get_short_term_memory",
                "description": "Retrieves information from the agent's short-term memory.",
                "args": ["query: string"],
                "example": {
                    "tool": "get_short_term_memory",
                    "args": ["What did the user ask previously?"]
                },
                "returns": "list"
            },
            {
                "name": "set_long_term_memory",
                "description": "Stores a piece of memory in the agent's long-term memory.",
                "args": ["memory: string"],
                "example": {
                    "tool": "set_long_term_memory",
                    "args": ["AI alignment is a key concern for safe deployment."]
                },
                "returns": "None"
            },
            {
                "name": "get_long_term_memory",
                "description": "Retrieves information from the agent's long-term memory.",
                "args": ["query: string"],
                "example": {
                    "tool": "get_long_term_memory",
                    "args": ["What is AI alignment?"]
                },
                "returns": "list"
            },
            {
                "name": "get_knowledge_base_memory",
                "description": "Retrieves information from the agent's knowledge base memory.",
                "args": ["query: string"],
                "example": {
                    "tool": "get_knowledge_base_memory",
                    "args": ["What is the capital of France?"]
                },
                "returns": "list"
            },
            {
                "name": "shell",
                "description": "Executes a shell command in the agent environment.",
                "args": [["command: string"]],
                "example": {
                    "tool": "shell",
                    "args":[ ["ls /app"]]
                },
                "returns": "dict"
            }
        ]


        personality = {
            "name": "Tools Agent",
            "description": "The manager of the tools library. "
        }

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        memory = PersistentWorkingMemory(MONGO_URI)
        memory_manager = MemoryManager(host=CHROMA_HOST, port=CHROMA_PORT, llm=llm)
        agent = Agent(llm=llm, personality=personality, memory_manager=memory_manager, working_memory=memory, memory_state_id=state_id)
        agent.set_tools_and_docs(tools, tools_doc)

        async def run():
            result = await agent(query)
            state_id = agent.save_current_memory()
            return result, state_id

        result, state_id = asyncio.run(run())
        if isinstance(result, str):
            return {"data":{"header":{"from": "meta_agent", "timestamp":timestamp},"body":{"task_id": task_id, "message": result, "state_id":state_id}}, "queue": OUTPUT_QUEUE}
        
        if isinstance(result, dict):
            if result.get("is_tool", False):
                logger.info("calling tool")
                tool_output = result.get("data")
                return {"data":{"header":{"from": "meta_agent", "timestamp":timestamp},"body":{"task_id": task_id, "state_id": state_id, "task_description": tool_output.get("tool_description")}}, "queue": tool_output.get("queue")}
        
        if result is None:
            logger.error("Something went wrong. The agent returns a 'None'")
            return {"data":{"header":{"from": "meta_agent", "timestamp":timestamp},"body":{"task_id": task_id}}, "queue": ERROR_QUEUE}

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        return {"data":{"header":{"from": "meta_agent", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

if __name__ == "__main__":
    try:
        worker = MessageWorker(
            input_queue=INPUT_QUEUE,
            process_message=main,
            host=RABBITMQ_HOST,
            username=RABBITMQ_USER,
            password=RABBITMQ_PASS
        )
        logger.info("MessageWorker started successfully.")
        worker.start()
    except Exception as e:
        logger.error(f"Failed to start MessageWorker: {e}")
    
