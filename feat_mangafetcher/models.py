from django.utils import timezone

from django.db import models

from crashme_manga.settings import DEFAULT_MANGA_DETAIL_CACHE_INVALID_IN_HOURS


class MangaModel(models.Model):
    url = models.URLField(primary_key=True)
    result = models.JSONField(null=True, default=None)
    lastFetchedAt = models.DateTimeField(null=True, default=None)
    createdAt = models.DateTimeField(auto_created=True, auto_now_add=True)

    def should_update(self):
        return self.lastFetchedAt + timezone.timedelta(
            hours=DEFAULT_MANGA_DETAIL_CACHE_INVALID_IN_HOURS
        ) < timezone.now()

    def set_data(self, new_data):
        self.lastFetchedAt = timezone.now()
        self.result = new_data
        self.save()
