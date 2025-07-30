import time
from typing import Callable, Dict, List, Optional

class CanStateMachine:
    ASYNCHRONOUS = "async"

    def __init__(self, loop_max: int = -1):
        self.states: Dict[str, Callable[[Optional[str]], Optional[str]]] = {}
        self.transitions: List[Dict] = []
        self.data: Dict = {}

        self.metrics = {
            "loop_counter": 0,
            "states": 0,
            "transitions": 0,
            "log": [],
            "execution": {
                "start": None,
                "end": None,
                "duration": None
            }
        }

        self.config_loop_max = loop_max
        self.loop_max = loop_max if loop_max > 0 else float("inf")

        self.current_status: Optional[str] = None
        self.previous_status: Optional[str] = None
        self.next_status: Optional[str] = None
        self.finished = False

    def add_state(self, state_name: str, state_fn: Callable[[Optional[str]], Optional[str]]):
        state_name = state_name.lower()
        if state_name in self.states:
            raise ValueError(f"State '{state_name}' already exists.")
        self.states[state_name] = state_fn

    def add_transition(self, from_state: str, to_state: str, transition_fn: Callable):
        from_state = from_state.lower()
        to_state = to_state.lower()
        if self._find_transition(from_state, to_state):
            raise ValueError(f"Transition from '{from_state}' to '{to_state}' already exists.")
        self.transitions.append({
            "from": from_state,
            "to": to_state,
            "fn": transition_fn
        })

    def _find_transition(self, from_state: Optional[str], to_state: str) -> Optional[Dict]:
        return next((t for t in self.transitions if t["from"] == from_state and t["to"] == to_state), None)

    def check(self) -> bool:
        return "start" in self.states and "end" in self.states

    def start(self):
        if not self.check():
            raise RuntimeError("StateMachine is not properly configured (start/end missing)")

        self.metrics["execution"]["start"] = time.time()
        self.async_proceed("start")

    def async_proceed(self, next_state: str):
        self.next_status = next_state.lower()
        async_wait = False

        while not self.finished and self.next_status and self.metrics["loop_counter"] < self.loop_max and not async_wait:
            self.metrics["loop_counter"] += 1

            transition = self._find_transition(self.current_status, self.next_status)
            if transition:
                self.metrics["log"].append(f"{self.current_status} -> {self.next_status}")
                transition["fn"]()

            self.previous_status = self.current_status
            self.current_status = self.next_status
            self.metrics["log"].append(self.current_status)

            if self.current_status == "end":
                self.finished = True
                break

            state_fn = self.states.get(self.current_status)
            if not state_fn:
                raise ValueError(f"State '{self.current_status}' not defined.")

            self.next_status = state_fn(self.previous_status)
            if self.next_status == CanStateMachine.ASYNCHRONOUS:
                async_wait = True

        if self.metrics["loop_counter"] >= self.loop_max:
            raise RuntimeError(f"Loop max reached: {self.loop_max}")

        if self.finished:
            self.metrics["execution"]["end"] = time.time()
            self.metrics["execution"]["duration"] = self.metrics["execution"]["end"] - self.metrics["execution"]["start"]
