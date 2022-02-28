from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from numpy import equal
from .models import Poll_question, Poll_option, Individual_vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from accounts.models import User_meta_data

@login_required()
def polls_list(request):
    all_questions = Poll_question.objects.all()
    user_meta = User_meta_data.objects.get(id=request.user.id)
    context = {
        'polls': all_questions,
        'media_icons': False,
        'user': user_meta
    }
    return render(request, 'polls/polls_list.html', context)

@login_required()
def list_by_user(request):
    all_questions = Poll_question.objects.filter(creator=request.user)
    user_meta = User_meta_data.objects.get(id=request.user.id)
    context = {
        'polls': all_questions,
        'media_icons': True,
        'user': user_meta
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def polls_add(request):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid:
            poll = form.save(commit=False)
            poll.creator = request.user
            poll.save()
            # Poll_option(question=poll, option_body=form.cleaned_data['choice1']).save()
            # Poll_option(question=poll, option_body=form.cleaned_data['choice2']).save()
            options = request.POST.getlist('options')
            print(options)
            for option in options:
                if option != "":
                    Poll_option(question=poll, option_body=option).save()
            messages.success(request, "Poll added successfully.")
            return redirect('polls:list')
    else:
        form = PollAddForm()
    context = {
        'form': form,
        'user': user_meta
    }
    return render(request, 'polls/add_poll.html', context)

@login_required
def polls_edit(request, pk):
    question = get_object_or_404(Poll_question, pk=pk)
    user_meta = User_meta_data.objects.get(id=request.user.id)
    if request.user != question.creator:
        return redirect('home')
    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=question)
        if form.is_valid:
            form.save()
            return redirect("polls:list")
    else:
        form = EditPollForm(instance=question)
    return render(request, "polls/poll_edit.html", {'form': form, 'poll': question, 'user': user_meta})


@login_required
def polls_delete(request, pk):
    question = get_object_or_404(Poll_question, pk=pk)
    if request.user != question.creator:
        return redirect('home')
    question.delete()
    return redirect("polls:list")


@login_required
def add_choice(request, pk):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    question = get_object_or_404(Poll_question, pk=pk)
    if request.user != question.creator:
        return redirect('home')
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.question = question
            new_choice.save()
            return redirect('polls:edit', question.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
        'user': user_meta
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_edit(request, pk):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    option = get_object_or_404(Poll_option, pk=pk)
    question = get_object_or_404(Poll_question, pk=option.question.id)
    if request.user != question.creator:
        return redirect('home')
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=option)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.question = question
            new_choice.save()
            return redirect('polls:edit', question.id)
    else:
        form = ChoiceAddForm(instance=option)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': option,
        'user': user_meta
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, pk):
    option = get_object_or_404(Poll_option, pk=pk)
    question = get_object_or_404(Poll_question, pk=option.question.id)
    if request.user != question.creator:
        return redirect('home')
    option.delete()
    return redirect('polls:edit', question.id)


def poll_detail(request, pk):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    question = get_object_or_404(Poll_question, pk=pk)
    owner = False
    if request.user == question.creator:
        owner = True
    if not question.user_can_vote(request.user):
        chosen_options = question.individual_vote_set.filter(user=request.user)
        options = []
        if len(chosen_options) > 1:
            messages.error(request, f"You already voted this poll! Your choices were:\n")
            for chosen_option in chosen_options:
                options.append(chosen_option.option.option_body)
                messages.error(request, f"%s" % (chosen_option.option.option_body))
        else:  
            for chosen_option in chosen_options:
                messages.error(request, f"You already voted this poll! Your choice was: ")
                messages.error(request, f"%s" % (chosen_option.option.option_body))
                options.append(chosen_option.option.option_body)
        return render(request, 'polls/poll_result.html', {'poll': question, 'choice': options, 'owner': owner, 'pk': pk, 'user': user_meta})
    loop_count = question.poll_option_set.count()
    context = {
        'poll': question,
        'loop_time': range(0, loop_count),
        'owner': owner,
        'pk': pk,
        'user': user_meta
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, pk):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    question = get_object_or_404(Poll_question, pk=pk)
    owner = False
    if request.user == question.creator:
        owner = True
    options_ids = request.POST.getlist('choice')
    if not question.user_can_vote(request.user):
        messages.error(request, "You already voted this poll!")
        return render(request, 'polls/poll_result.html', {'poll': question, 'owner': owner, 'pk': pk, 'user': user_meta})
    if len(options_ids) > 0:
        for option_id in options_ids:
            option = Poll_option.objects.get(id=option_id)
            vote = Individual_vote(user=request.user, question=question, option=option)
            vote.save()
        return render(request, 'polls/poll_result.html', {'poll': question, 'owner': owner, 'pk': pk, 'user': user_meta})
    else:
        messages.error(request, "No choice selected!")
        return redirect("polls:detail", pk)


@login_required
def poll_result(request, pk):
    user_meta = User_meta_data.objects.get(id=request.user.id)
    question = get_object_or_404(Poll_question, pk=pk)
    owner = False
    if request.user == question.creator:
        owner = True
    return render(request, 'polls/poll_result.html', {'poll': question, 'owner': owner, 'pk': pk, 'user': user_meta})
