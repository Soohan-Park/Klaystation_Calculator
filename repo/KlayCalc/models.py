import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# Example.
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.question_text

#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


#     def __str__(self):
#         return self.choice_text


# Not Yet
class Donation(models.Model):
    objects = models.Manager()  # To suppress vscode errors

    no = models.IntegerField()
    name = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    donate_date = models.DateTimeField('Date of Donate')
    
    def __str__(self):
        return str(self.name) + " :: " + str(self.amount) + " :: " + str(self.donate_date)


class RateData(models.Model):
    objects = models.Manager()  # To suppress vscode errors

    date = models.DateField('Date of Rate', default=datetime.datetime.now, editable=False)
    rate = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.date) + " :: " + str(self.rate)