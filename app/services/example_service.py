from typing import Any

from felix_flow.state import State

from app.flow.flow_example.hello_flow import HelloFlow


class ExampleService:
    @staticmethod
    def flow_execution_example() -> Any:
        return HelloFlow(State()).run_flow()
