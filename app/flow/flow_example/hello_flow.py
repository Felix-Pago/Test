from typing import Any, Optional

import requests
from felix_flow.exceptions.flow_error import FlowError
from felix_flow.flow import Flow
from felix_flow.state import State


class HelloFlow(Flow):
    def __init__(self, state: State) -> None:
        super().__init__(state)

    def run_flow(self) -> Any:
        self.with_exception_handler(self.error_handler) \
            .with_time_reporter(self.time_handler) \
            .next('hello_world', self.hello_world) \
            .in_parallel('in_parallel', [self.get_kenny_quote, self.get_random_cat]) \
            .next('print_results', self.print_results) \
            .run()

        return self.get_state().service_response

    def error_handler(self, state: State, flow_error: FlowError) -> None:
        print(f'Coming from the handler {flow_error}')

    def time_handler(self, node_name: str, time: float, state: State) -> None:
        print(f"Node {node_name} took {time}")

    def hello_world(self, state: State) -> None:
        print('Hello World')

    def get_kenny_quote(self, state: State) -> None:
        response: requests.Response = requests.get('https://api.kanye.rest/')
        quote: str = 'Something went wrong'
        if response.status_code == 200:
            quote = response.json().get('quote', quote)
        state.quote = quote

    def get_random_cat(self, state: State) -> None:
        response: requests.Response = requests.get('https://cataas.com/cat?json=true')
        cat_url: Optional[str] = None
        if response.status_code == 200:
            cat_url = response.json().get('url')
        state.cat_url = f'https://cataas.com{cat_url}'

    def print_results(self, state: State) -> None:
        response: str = f'''A bit of wisdom from Kanye: {state.quote}
        Not good? Check this kitty then: {state.cat_url}'''

        state.service_response = {'response': response}
        print(response)
