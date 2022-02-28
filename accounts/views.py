from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from polls.models import Poll_question
from .models import User_meta_data
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            user_meta = User_meta_data.objects.get(id=request.user.id)
            polls = Poll_question.objects.all()
            count = 0
            for poll in polls:
                if poll.user_can_vote(user):
                    count += 1
            context = {"logged_in": True, "count": count, "user": user_meta}
            return render(request, 'home.html', context)
        else:
            messages.error(request, "Username Or Password is incorrect!",)

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request):
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password did not match!')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists!')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Email already registered!')
            if check1 or check2 or check3:
                messages.error(
                    request, "Registration Failed!")
                return redirect('accounts:register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                usermeta = User_meta_data.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    user=user,
                )
                usermeta.save()
                messages.success(request, f'Thanks for registering {user.username}.')
                return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
