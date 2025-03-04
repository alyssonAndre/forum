from django.db import models
from setup.models.SoftDeleteModel import SoftDeleteModel



class Course(SoftDeleteModel):
    TYPE_CHOICES = [
        ('software', 'Engenharia de Software'),
        ('quimica', 'Engenharia Quimica'),
        ('eletrica', 'Engenharia Eletrica'),
        ('civil', 'Engenharia Civil'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name



