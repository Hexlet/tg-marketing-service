from unittest.mock import MagicMock, patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.parser.models import Post, PostAnalysis, TelegramChannel
from apps.parser.services.analysis import PostAnalysisService


@override_settings(SECRET_KEY="test-key-for-testing")
class PostAIAnalysisAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.channel = TelegramChannel.objects.create(
            channel_id=123456, title="Test Channel", username="test"
        )
        self.post = Post.objects.create(
            channel=self.channel,
            telegram_message_id=12345,
            text="Original post text",
            published_at=timezone.now(),
        )

    def test_endpoint_404_if_post_not_found(self):
        url = reverse(
            "parser:post_ai_analysis",
            kwargs={"channel_id": self.channel.id, "post_id": 99999},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @patch("apps.parser.services.analysis.PostAnalysisService.get_analysis")
    def test_endpoint_cache_hit(self, mock_get_analysis):
        analysis = PostAnalysis.objects.create(
            post=self.post,
            why_worked="Reason 1\nReason 2",
            how_to_improve="Improve 1",
        )
        mock_get_analysis.return_value = analysis

        url = reverse(
            "parser:post_ai_analysis",
            kwargs={"channel_id": self.channel.id, "post_id": 12345},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["why_worked"], ["Reason 1", "Reason 2"]
        )

    def test_endpoint_cache_miss_and_llm_call(self):
        """
        Если анализа нет, вызывается провайдер (LLM) и данные сохраняются.
        Здесь мы внедряем (inject) мок прямо в сервис.
        """
        # 1. Создаем мок провайдера
        mock_provider = MagicMock()
        mock_provider.analyze.return_value = {
            "why_worked": ["AI Reason"],
            "how_to_improve": ["AI Improvement"],
            "similar_posts_ids": [],
        }

        # 2. Инициализируем сервис с моком
        service = PostAnalysisService(provider=mock_provider)

        with patch(
            "apps.parser.views.PostAnalysisService", return_value=service
        ):
            url = reverse(
                "parser:post_ai_analysis",
                kwargs={"channel_id": self.channel.id, "post_id": 12345},
            )

            response = self.client.get(url)

            # Проверки
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["why_worked"], ["AI Reason"])

            # Проверка, что данные сохранились в БД
            self.assertTrue(
                PostAnalysis.objects.filter(post=self.post).exists()
            )

            # Проверка повторного вызова (должен быть кеш)
            response_second = self.client.get(url)
            self.assertEqual(response_second.status_code, 200)
            self.assertEqual(mock_provider.analyze.call_count, 1)
