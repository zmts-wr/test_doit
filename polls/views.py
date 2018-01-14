from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model, login

from polls.forms import LoginForm, SignUpForm

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        return render(request, 'polls/index.html')
    else:
        return redirect(reverse('login'))


def login_signup(request, signup=False):
    if request.method == 'POST':
        if signup:
            form = SignUpForm(data=request.POST)
            error = None
            if form.is_valid():
                try:
                    user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['username'], form.cleaned_data['password'])
                except:
                    error = "Can't create user. Try another email and(or) password."
                else:
                    login(request, user)
                    return redirect(reverse('home'))
            
            return render(request, 'polls/login.html', {
                'signup_form': form,
                'error': error,
                'signup': True,
            })
        else:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = authenticate(request, **form.cleaned_data)
                if user:
                    login(request, user)
                    return redirect(reverse('home'))

            return render(request, 'polls/login.html', {
                'login_form': form,
                'error': 'Incorrect user name or password',
            })
    else:
        return render(request, 'polls/login.html')

