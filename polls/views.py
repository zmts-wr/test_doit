from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required

from polls.models import Answer, Question, QuestionGroup
from polls.forms import AnswerForm, LoginForm, SignUpForm

User = get_user_model()


@login_required(login_url='/login')
def home(request):
    qgroups = QuestionGroup.objects.all()
    return render(request, 'polls/index.html', {
        'qgroups': qgroups,
    })

@login_required(login_url='/login')
def qgroup(request, qg_id):
    qgroup = get_object_or_404(QuestionGroup, id=qg_id)
    gr_key = 'qgroup__{}'.format(qg_id)
    collected = request.session.get(gr_key, default={})
    form = None
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            q = get_object_or_404(Question, id=form.cleaned_data['question_id'])
            answer = get_object_or_404(Answer, id=form.cleaned_data['answer'])
            collected[str(q.id)] = [answer.id, answer.is_right,]
            request.session[gr_key] = collected
            if len(collected) == qgroup.question_set.count():
                return redirect(reverse('result', kwargs={ 'qg_id': qg_id }))

    if collected:
        question = qgroup.question_set.exclude(id__in=collected.keys()).first()
    else:
        question = qgroup.question_set.first()
    
    if not question:
        return redirect(reverse('result', kwargs={ 'qg_id': qg_id }))

    return render(request, 'polls/qgroup.html', {
        'form': form,
        'qgroup': qgroup,
        'question': question,
    })

@login_required(login_url='/login')
def result(request, qg_id):
    qgroup = get_object_or_404(QuestionGroup, id=qg_id)
    gr_key = 'qgroup__{}'.format(qg_id)
    collected = request.session.pop(gr_key, default={})
    return render(request, 'polls/result.html', {
        'qgroup': qgroup,
        'sum_total': len(collected),
        'sum_right': sum(collected[item][1] for item in collected),
    })

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

