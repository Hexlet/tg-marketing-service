from typing import Optional

from models import Post, PostAnalysis

from .ai_provider import (
    AIAnalysisResult,
    BaseAIProvider,
    DeterministicFallbackProvider,
)


class PostAnalysisService:
    def __init__(self, provider: Optional[BaseAIProvider] = None):
        self.provider = provider or DeterministicFallbackProvider()

    def get_analysis(
        self, post: Post, force_regenerate: bool = False
    ) -> PostAnalysis:
        # 1. Попытка получить из кеша (БД)
        if not force_regenerate:
            existing = PostAnalysis.objects.filter(post=post).first()
            if existing:
                return existing

        # 2. Генерация через провайдера
        metrics = {
            "views": post.views,
            "forwards": post.forwards,
            "comments": post.comments_count,
        }

        try:
            data: AIAnalysisResult = self.provider.analyze(post.text, metrics)
        except Exception:
            # 3. Фолбэк на заглушку при любой ошибке провайдера
            data = DeterministicFallbackProvider().analyze(post.text, metrics)

        # 4. Сохранение/Обновление в PostAnalysis
        analysis, created = PostAnalysis.objects.update_or_create(
            post=post,
            defaults={
                "why_worked": "\n".join(data["why_worked"]),
                "how_to_improve": "\n".join(data["how_to_improve"]),
                "model_version": self.provider.__class__.__name__,
            },
        )

        # Обновление ManyToMany (similar_posts)
        analysis.similar_posts.clear()
        if data["similar_posts_ids"]:
            analysis.similar_posts.set(data["similar_posts_ids"])

        return analysis
