from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    person_name = models.CharField(max_length=50)
    birth = models.DateField()

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    leader = models.ForeignKey(Person)

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    detail = models.CharField(max_length=200,default="null")

class Task(models.Model):
    task_name = models.CharField(max_length=50)
    deadline = models.DateTimeField()
    detail = models.CharField(max_length=200,default="null")

class Event(models.Model):
    event_name = models.CharField(max_length=50)
    time = models.DateTimeField()
    detail = models.CharField(max_length=200,default="null")

class in_team(models.Model):
    person = models.ForeignKey(Person)
    team = models.ForeignKey(Team)
    class Meta:
        unique_together = ("person","team")

class involve_project(models.Model):
    project = models.ForeignKey(Project)
    team = models.ForeignKey(Team)
    class Meta:
        unique_together = ("project","team")

class have_task(models.Model):
    person = models.ForeignKey(Person)
    task = models.ForeignKey(Task)
    class Meta:
        unique_together = ("person","task")

class happen_event(models.Model):
    team = models.ForeignKey(Team)
    event = models.ForeignKey(Event)
    class Meta:
        unique_together = ("team","event")
