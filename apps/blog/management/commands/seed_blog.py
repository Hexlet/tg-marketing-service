from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime

from apps.blog.models import BlogArticle
from apps.blog.seed_data import ARTICLES


class Command(BaseCommand):
    help = (
        "Создаёт или обновляет статьи блога из seed_data.py. "
        "Повторный запуск не создаёт дубли, а обновляет существующие."
    )

    def handle(self, *args, **options):
        author = get_user_model().objects.filter(is_superuser=True).first()
        created = 0
        updated = 0

        with transaction.atomic():
            for data in ARTICLES:
                defaults = dict(data)
                defaults.pop("slug")
                defaults["author"] = author
                defaults["published_at"] = parse_datetime(
                    defaults["published_at"]
                )
                _, was_created = BlogArticle.objects.update_or_create(
                    slug=data["slug"],
                    defaults=defaults,
                )
                created += was_created
                updated += not was_created

        self.stdout.write(
            self.style.SUCCESS(
                f"Статей создано: {created}, обновлено: {updated}"
            )
        )
