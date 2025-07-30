import unittest
from can_state_machine import CanStateMachine

class TestCanStateMachine(unittest.TestCase):
    def test_basic_flow(self):
        sm = CanStateMachine()

        sm.add_state("start", lambda prev: "middle")
        sm.add_state("middle", lambda prev: "end")
        sm.add_state("end", lambda prev: None)

        sm.add_transition("start", "middle", lambda: print("Transition: start → middle"))
        sm.add_transition("middle", "end", lambda: print("Transition: middle → end"))

        sm.start()

        print(f"Final state: {sm.current_status}")
        print(f"Log: {sm.metrics['log']}")

        self.assertTrue(sm.finished)
        self.assertEqual(sm.current_status, "end")
        self.assertIn("middle", sm.metrics["log"])

if __name__ == '__main__':
    unittest.main()