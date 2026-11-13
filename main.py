from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent_engine import AgenticWorkflowEngine

app = FastAPI(
    title="Enterprise LLM Agentic Workflow Pipeline",
    description="Autonomous agent framework featuring multi-step reasoning, tool execution loops, and dynamic task orchestration.",
    version="1.0.0"
)

engine = AgenticWorkflowEngine()

class AgentRunRequest(BaseModel):
    goal: str = Field(..., example="Calculate total revenue for Q3 based on numbers 45000 + 12000")
    tool_name: str = Field(..., example="calculator")
    tool_input: str = Field(..., example="45000 + 12000")

@app.post("/v1/agent/run", summary="Execute Autonomous Agent Workflow")
def run_agent_workflow(payload: AgentRunRequest):
    try:
        result = engine.execute_workflow(
            goal=payload.goal,
            tool_name=payload.tool_name,
            tool_input=payload.tool_input
        )
        return {
            "status": "success",
            "agent_execution": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
