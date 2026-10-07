from dataclasses import dataclass
from datetime import date

from .infrai_client import InfraiClient


@dataclass(frozen=True)
class Learner:
    email: str
    course: str
    deadline: date
    completed: bool = False


def due_learners(learners: list[Learner], today: date) -> list[Learner]:
    """Select enrolled learners with an unfinished deadline within seven days."""
    return [item for item in learners if not item.completed and 0 <= (item.deadline - today).days <= 7]


def send_digest(learners: list[Learner], today: date, client: InfraiClient) -> int:
    selected = due_learners(learners, today)
    if not selected:
        return 0
    client.queue_publish("deadline-digest", {"recipients": [item.email for item in selected], "date": today.isoformat()})
    messages = [{"to": item.email, "subject": f"{item.course} deadline digest", "text": f"Your {item.course} work is due on {item.deadline.isoformat()}."} for item in selected]
    client.email_batch_send(messages)
    return len(messages)


def schedule_digest(webhook_url: str, client: InfraiClient) -> str:
    result = client.cron_create("0 8 * * 1", webhook_url)
    return result["job_id"]


if __name__ == "__main__":
    today = date.today()
    sent = send_digest(
        [Learner("chenhua@changba.com", "Deadline digest", today)],
        today,
        InfraiClient(),
    )
    print(f"Sent {sent} deadline digest email(s).")
