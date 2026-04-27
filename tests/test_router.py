import unittest
import re

from backend.router import infer_workflow, route_query
from backend.schemas import QueryRequest


class RouterTests(unittest.TestCase):
    def test_routes_onboarding_questions(self):
        response = route_query(QueryRequest(query="How do I get laptop and VPN access?"))

        self.assertEqual(response.workflow, "onboarding")
        self.assertTrue(response.first_week_tasks)
        self.assertTrue(response.documents_to_read)
        self.assertTrue(response.people_to_contact)
        self.assertTrue(response.meetings)

    def test_routes_weekly_reporting_requests(self):
        response = route_query(QueryRequest(query="Generate a weekly status summary"))

        self.assertEqual(response.workflow, "weekly_reporting")
        self.assertTrue(response.completed_work)
        self.assertTrue(response.in_progress_work)
        self.assertTrue(response.blockers)
        self.assertTrue(response.owner_task_counts)
        self.assertTrue(response.next_steps)

        counts = [int(value) for value in re.findall(r"(\d+) item\(s\)|(\d+) blocker\(s\)", response.summary) for value in value if value]
        self.assertEqual(counts[0], len(response.completed_work))
        self.assertEqual(counts[1], len(response.in_progress_work))
        self.assertEqual(counts[2], len(response.blockers))

    def test_asks_for_clarification_when_route_is_unclear(self):
        response = route_query(QueryRequest(query="Can you help me with this?"))

        self.assertIsNone(response.workflow)
        self.assertIn("Please clarify", response.summary)
        self.assertEqual(response.sources, [])

    def test_inference_scores_are_visible(self):
        decision = infer_workflow("status report for onboarding access")

        self.assertIsNone(decision.workflow)
        self.assertEqual(decision.scores["onboarding"], decision.scores["weekly_reporting"])


if __name__ == "__main__":
    unittest.main()
