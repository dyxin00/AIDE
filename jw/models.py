from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):

    user = models.OneToOneField(User)
    student_id = models.IntegerField()
    student_passcode = models.CharField(max_length=30)
    sex = models.IntegerField()


class Curriculum(models.Model):

    user = models.ForeignKey(Account)
    yesr = models.IntegerField()
    term = models.IntegerField()


class Lesson(models.Model):

    curriculum = models.ForeignKey(Curriculum)
    lesson_name = models.CharField(max_length=60)
    week = models.IntegerField()
    lesson_room = models.CharField(max_length=100)
    day_start = models.IntegerField()
    day_end = models.IntegerField()
    week_start = models.IntegerField()
    week_end = models.IntegerField()
    odd_week = models.IntegerField()

