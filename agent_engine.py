import json
from typing import List, Dict, Any

class AgenticWorkflowEngine:
    def __init__(self):
        self.available_tools = {
            "calculator": self.tool_calculator,
            "text_analyzer": self.tool_text_analyzer
        }

    def tool_calculator(self, expression: str) -> str:
        try:
            # Safe evaluation for basic arithmetic expressions in agent workflows
            allowed_chars = "0123456789+-*/(). "
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"Calculation Result: {result}"
            return "Error: Invalid characters in mathematical expression."
        except Exception as e:
            return f"Calculation Error: {str(e)}"

    def tool_text_analyzer(self, text: str) -> str:
        words = text.split()
        return json.dumps({
            "word_count": len(words),
            "character_count": len(text),
            "estimated_reading_time_sec": round(len(words) / 3.0, 2)
        })

    def execute_workflow(self, goal: str, tool_name: str, tool_input: str) -> Dict[str, Any]:
        """Executes a multi-step agent reasoning loop with tool invocation."""
        execution_steps = []
        
        # Step 1: Goal Decomposition & Planning
        execution_steps.append({
            "step": 1,
            "action": "Plan Generation",
            "status": "COMPLETED",
            "details": f"Decomposed goal into task: Execute tool '{tool_name}' with payload."
        })
        
        # Step 2: Tool Execution
        tool_output = "Error: Tool not found."
        if tool_name in self.available_tools:
            try:
                tool_output = self.available_tools[tool_name](tool_input)
                tool_status = "SUCCESS"
            except Exception as e:
                tool_output = f"Execution failed: {str(e)}"
                tool_status = "FAILED"
        else:
            tool_status = "NOT_FOUND"

        execution_steps.append({
            "step": 2,
            "action": f"Tool Invocation [{tool_name}]",
            "status": tool_status,
            "output": tool_output
        })
        
        # Step 3: Synthesis & Final Answer
        execution_steps.append({
            "step": 3,
            "action": "Response Synthesis",
            "status": "COMPLETED",
            "details": "Synthesized tool output into final structured agent response."
        })

        return {
            "goal": goal,
            "total_steps": len(execution_steps),
            "workflow_status": "SUCCESS" if tool_status == "SUCCESS" else "FAILED",
            "steps": execution_steps,
            "final_output": tool_output
        }
