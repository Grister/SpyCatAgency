from django.db import models


class Mission(models.Model):
    cat = models.ForeignKey(
        'cats.Cat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='missions'
    )
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f'Mission #{self.pk}'


class Target(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='targets'
    )
    name = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
