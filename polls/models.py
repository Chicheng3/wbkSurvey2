import datetime
from typing import Any

from django.db import models
from django.utils import timezone

# Create your models here.
class Dimension(models.Model):
    class Meta:
        verbose_name = ("dimension") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("2. Stellengrößen")
    dimension_name = models.CharField(max_length=200, help_text="bitte eine Stellengröße eingeben")
    def __str__(self):
        return self.dimension_name
#Umfrage

class Factor(models.Model):
    class Meta:
        verbose_name = ("factor") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("1. Regelgrößen")
    factor_name = models.CharField(max_length=200, help_text="bitte eine Regelgröße eingeben")
    def __str__(self):
        return self.factor_name


class Survey(models.Model):
    class Meta:
        verbose_name = ("Survey") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("3. Fragebögen")    
    title = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, blank= True) 
    impl_level = models.PositiveSmallIntegerField(default= '')
    showing = models.BooleanField(default=True)
    #questions = models.ManyToManyField("Question",blank = True,help_text="Fragen können im Nachgang gewählt werden!  ")
    


    def __str__(self):
        return self.title






#Fragen die in eine Umfrage eingebunden werden
class Question(models.Model):
    class Meta:
        verbose_name = ("question") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("4. Fragen")
    related_survey = models.ForeignKey(Survey, on_delete=models.CASCADE, default="")
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    impl_level = models.PositiveSmallIntegerField(default=0)
    added_to_survey = models.BooleanField(default=True)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE,  default=Survey._meta.get_field('factor').get_default())
    #choices = models.ManyToManyField("Choice", blank = True, help_text="Antworten können im Nachgang gewählt werden!  ")
   

    def __str__(self):
        return self.question_text

    def get_survey_title(self):
        return self.survey.title

    def get_chioce_count(self):
        return self.choice_set.count()

    def get_vote_count(self):
        _count = 0
        for choice in self.choice_set.all():
            _count += choice.votes
        return _count
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


#Antwortoptionen
class Choice(models.Model):
    class Meta:
        verbose_name = ("result") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("5. Resultate")
    
    related_survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null = True, default= "")#choice mit zugehöriger survey verbinden
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, default="" )#choice mit zugehöriger question verbinden
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    score = models.PositiveSmallIntegerField()

    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    stellengröße = models.ForeignKey(Dimension, on_delete=models.CASCADE, default = "")
    def __str__(self):
        return self.factor
        
    def __str__(self):
        return self.choice_text
    
        



#user
class User(models.Model):
    class Meta:
        verbose_name = ("user") #anzuzeigender Name AdminSeite
        verbose_name_plural = ("5. Nutzerdaten")
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    pub_date = models.DateField('date published')
    def __str__(self):
        return '<%s:%s>' % (self.name, self.gender)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
