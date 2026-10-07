from datetime import date, timedelta

from src.digest_service import Learner, due_learners


def test_digest_targets_unfinished_deadlines_in_next_week():
    today = date(2026, 9, 14)
    learners = [
        Learner("a@example.com", "RAG 101", today + timedelta(days=2)),
        Learner("b@example.com", "Agents", today + timedelta(days=8)),
        Learner("c@example.com", "RAG 101", today + timedelta(days=1), completed=True),
    ]
    assert [item.email for item in due_learners(learners, today)] == ["a@example.com"]
