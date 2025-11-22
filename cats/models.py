from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=128)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=128)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    active_mission = models.ForeignKey(
        'missions.Mission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cat'
    )

    def __str__(self):
        return self.name
