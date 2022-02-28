import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Poll_question(models.Model):
    question_body = models.CharField(max_length=200)
    is_single = models.BooleanField(default=1, verbose_name="Single Choice")
    published_date = models.DateTimeField('Date Published', default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question_body
    
    def was_asked_recently(self):
        return self.published_date >= timezone.now() - datetime.timedelta(days=2)
    
    @property
    def get_vote_count(self):
        return self.individual_vote_set.count()
    
    def user_can_vote(self, user):
        user_votes = user.individual_vote_set.all()
        ques = user_votes.filter(question=self)
        if ques.exists():
            return False
        return True
    
    def get_result_dict(self):
        results = []
        for option in self.poll_option_set.all():
            d = {}
            d['text'] = option.option_body
            d['num_votes'] = option.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (option.get_vote_count / self.get_vote_count)*100
            results.append(d)
        return results
    
    class Meta:
        ordering = ['-published_date']
    
class Poll_option(models.Model):
    question = models.ForeignKey(Poll_question, on_delete=models.CASCADE)
    option_body = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.question.question_body} - {self.option_body}"
    
    @property
    def get_vote_count(self):
        return self.individual_vote_set.count()
    

class Individual_vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Poll_question, on_delete=models.CASCADE)
    option = models.ForeignKey(Poll_option, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.question_body} - {self.option.option_body} - {self.user.username}'
