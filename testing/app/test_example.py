import unittest

from app.flow import HelloFlow
from felix_flow.state import State

class TestExample(unittest.TestCase):
    def __init__(self, methodName: str = "TestExample") -> None:
        super().__init__(methodName)
        self.flow: HelloFlow = HelloFlow(State())

    def test_flow(self) -> None:
        self.assertIsInstance(self.flow.run_flow(), dict)