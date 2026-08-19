from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.moderation.models import ModerationRequest
from apps.moderation.services.queue import ModerationQueue
from apps.parser.models import TelegramChannel
from apps.users.models import User


class ModerationRequestTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="moderator-requester",
            email="requester@example.com",
            password="password",
            role="user",
        )
        self.channel = TelegramChannel.objects.create(
            channel_id=1001,
            username="tech_channel",
            title="Tech channel",
        )

    def create_request(self, **overrides: object) -> ModerationRequest:
        data: dict[str, object] = {
            "submitted_by": self.user,
            "channel_identifier": "@tech_channel",
            "category": "technology",
            "country": "RU",
            "language": "ru",
        }
        data.update(overrides)
        return ModerationRequest.objects.create(**data)

    def test_pending_status_is_used_by_default(self) -> None:
        moderation_request = self.create_request()

        self.assertEqual(moderation_request.status, "pending")
        self.assertIsNone(moderation_request.channel_by)
        self.assertIsNone(moderation_request.moderator)
        self.assertIsNone(moderation_request.reject_reason)
        self.assertIsNone(moderation_request.resolved_at)

    def test_pending_queue_is_ordered_by_created_at_then_id(self) -> None:
        older_request = self.create_request(channel_by=self.channel)
        newer_request = self.create_request(channel_identifier="@new_channel")
        tied_request = self.create_request(channel_identifier="@tied_channel")
        self.create_request(status="approved")
        self.create_request(status="rejected")
        self.create_request(status="duplicate")

        now = timezone.now()
        ModerationRequest.objects.filter(pk=older_request.pk).update(
            created_at=now + timedelta(minutes=1)
        )
        ModerationRequest.objects.filter(pk=newer_request.pk).update(
            created_at=now
        )
        ModerationRequest.objects.filter(pk=tied_request.pk).update(
            created_at=now
        )

        queue = list(ModerationRequest.objects.pending_queue())

        self.assertEqual(
            [request.id for request in queue],
            [newer_request.id, tied_request.id, older_request.id],
        )

    def test_empty_queue_returns_empty_list(self) -> None:
        self.assertEqual(ModerationQueue().get_queue(), [])

    def test_queue_serializes_requests_with_and_without_channel(self) -> None:
        request_with_channel = self.create_request(channel_by=self.channel)
        resolved_at = timezone.now()
        request_without_channel = self.create_request(
            channel_identifier="https://t.me/new_channel",
            category="business",
            country="US",
            language="en",
            reject_reason="Needs review",
            resolved_at=resolved_at,
        )
        self.create_request(status="approved")
        self.create_request(status="rejected")
        self.create_request(status="duplicate")

        queue = ModerationQueue().get_queue()

        self.assertEqual(
            [item["id"] for item in queue],
            [request_with_channel.id, request_without_channel.id],
        )
        self.assertEqual(
            queue[0]["submitted_by"],
            {"id": self.user.id, "username": self.user.username},
        )
        self.assertEqual(
            queue[0]["channel"],
            {
                "id": self.channel.id,
                "username": self.channel.username,
                "title": self.channel.title,
            },
        )
        self.assertIsNone(queue[1]["channel"])
        self.assertEqual(
            queue[1]["channel_identifier"], "https://t.me/new_channel"
        )
        self.assertEqual(
            {
                "category": queue[0]["category"],
                "country": queue[0]["country"],
                "language": queue[0]["language"],
                "status": queue[0]["status"],
            },
            {
                "category": "technology",
                "country": "RU",
                "language": "ru",
                "status": "pending",
            },
        )
        self.assertIsNone(queue[0]["reject_reason"])
        self.assertEqual(
            queue[0]["created_at"], request_with_channel.created_at.isoformat()
        )
        self.assertIsNone(queue[0]["resolved_at"])
        self.assertEqual(
            {
                "category": queue[1]["category"],
                "country": queue[1]["country"],
                "language": queue[1]["language"],
                "status": queue[1]["status"],
            },
            {
                "category": "business",
                "country": "US",
                "language": "en",
                "status": "pending",
            },
        )
        self.assertEqual(queue[1]["reject_reason"], "Needs review")
        self.assertEqual(
            queue[1]["created_at"],
            request_without_channel.created_at.isoformat(),
        )
        self.assertEqual(queue[1]["resolved_at"], resolved_at.isoformat())
