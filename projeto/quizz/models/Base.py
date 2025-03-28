from django.db import models
from quizz.models.SoftDeleteModel import SoftDeleteModel



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

    def save(self, *args, **kwargs):
        if not self.name and self.type:
            self.name = dict(self.TYPE_CHOICES).get(self.type)
        
        if not self.type and self.name:
            self.type = next((key for key, value in self.TYPE_CHOICES if value == self.name), None)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



