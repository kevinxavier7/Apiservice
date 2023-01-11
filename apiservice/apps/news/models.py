from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    commentary = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return f'{self.title}'