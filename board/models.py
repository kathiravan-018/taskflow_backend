from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "profile"
    )

    name = models.CharField(max_length=100)
    college = models.CharField(max_length=150)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Board(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Column(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="columns"
    )
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
     
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["order"]

class Task(models.Model):

    priority_choices = [
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High'),
    ]
    
    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20,
                                choices=priority_choices,
                                default="Low")
    due_date=models.DateField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ["order"]



