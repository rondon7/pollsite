from multiprocessing import context
from django.shortcuts import render
from polls.models import Poll_question
from accounts.models import User_meta_data

def home(request):
    context = {}
    if request.user.is_authenticated:
        polls = Poll_question.objects.all()
        user = User_meta_data.objects.get(id=request.user.id)
        count = 0
        for poll in polls:
            if poll.user_can_vote(request.user):
                count += 1
        context = {"logged_in": True, "count": count, "user": user}
    else:
        context = {"logged_in": False, "count": 0}
    return render(request, 'home.html', context)
