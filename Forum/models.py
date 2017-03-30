from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
class Question(models.Model):
    question_title = models.CharField(max_length=256)
    question_description = models.TextField()
    questioned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_count = models.IntegerField(default=0)
    active = models.DateTimeField(auto_now=True, blank=True)

    def time_difference(self):
        old_time = self.active.replace(tzinfo=None)
        seconds = (datetime.now()-old_time).total_seconds() - (5*60*60) - (30*60)

        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days / 7
        months = weeks / 52
        years = months / 12

        if years>1:
            return str(int(years)) + " years ago"
        elif months>1:
            return str(int(months)) + " months ago"
        elif weeks>1:
            return str(int(weeks)) + " weeks ago"
        elif days>1:
            return str(int(days)) + " days ago"
        elif hours>1:
            return str(int(hours)) + " hours ago"
        elif minutes>1:
            return str(int(minutes)) + " minutes ago"
        elif seconds>1:
            return str(int(seconds)) + " seconds ago"
        else:
            return "0 secs ago"

class Answer(models.Model):
    answer_description = models.TextField()
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answered_to = models.ForeignKey(Question, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_description = models.TextField()
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_to_answer = models.ForeignKey(Answer, on_delete=models.CASCADE,blank=True,null=True)
    commented_to_question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=True,null=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=32)

class Tag_Question_Link(models.Model):
    question_link = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag_link = models.ForeignKey(Tag, on_delete=models.CASCADE)