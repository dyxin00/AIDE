from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):

    user = models.OneToOneField(User)
    student_id = models.IntegerField(unique=True)
    student_passcode = models.CharField(max_length=30)
    sex = models.IntegerField(null=True)
    full_name = models.CharField(max_length=30, null=True)
    college = models.CharField(max_length=60, null=True)
    school_year = models.CharField(max_length=30, null=True)
    team = models.CharField(max_length=60, null=True)
    course = models.CharField(max_length=60, null=True)
    specialty = models.CharField(max_length=60, null=True)

    def get_student_info(self):

        return {
                'full_name' : self.full_name,
                'course' : self.course,
                'college' : self.college,
                'school_year' : self.school_year,
                'team' : self.team,
                'student_id' : self.student_id,
                'specialty' : self.specialty
                }


class Curriculum(models.Model):

    user = models.ForeignKey(Account)
    year = models.IntegerField()
    term = models.IntegerField()

    class Meta:
        unique_together = (('user', 'year', 'term'),)


'''
class LeesonManager(models.Manager):
    def create_lesson(self, **kwargs):
        lesson = self. 
'''
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

    def get_lesson_dict(self):

        return {
                'lesson_name' : self.lesson_name,
                'lesson_room' : self.lesson_room,
                'week' : self.week,
                'day_start' : self.day_start,
                'day_end' : self.day_end,
                'week_start' : self.week_start,
                'week_end' : self.week_end,
                'odd_week' : self.odd_week
                }


