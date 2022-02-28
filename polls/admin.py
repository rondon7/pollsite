from django.contrib import admin
from .models import Poll_question, Poll_option, Individual_vote
# Register your models here.

admin.site.register(Poll_question)
admin.site.register(Poll_option)
admin.site.register(Individual_vote)