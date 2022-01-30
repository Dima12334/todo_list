from django.db import models
# Create your models here.

#from todo_app.models import Tod o


class Todo(models.Model):
    day = models.CharField(max_length=25)
    month = models.IntegerField()
    year = models.IntegerField()
    time = models.IntegerField(null=True)
    task = models.CharField(max_length=200)