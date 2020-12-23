from django.shortcuts import render, redirect, HttpResponse
from .forms import UserForm, LoginForm
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from urllib import request
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import AppUser, Connected, Message
from django.db.models import Q


@login_required
def index(request):
    user = request.user

    s = set([i.second for i in Connected.objects.filter(Q(first__User=user)|Q(second__User=user))])
    all = [i for i in AppUser.objects.all() if i not in s]
    return render(request, 'index.html', {'all': all, 's': s})


def signup(request):
    """
    :param request: request
    :return: Signup Form / Redirect to login
    """
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['cnf_password']:
            obj = User()
            obj.username = form.cleaned_data['username']
            print(form.cleaned_data)
            obj.set_password(form.cleaned_data['password'])
            try:
                obj.save()
                o1 = AppUser()
                o1.User = obj
                o1.firstname = form.cleaned_data['fn']
                o1.lastname = form.cleaned_data['ln']
                o1.age = form.cleaned_data['age']
                o1.save()
                print(AppUser.objects.all())
            except IntegrityError:
                print('triggered')
                # Invoked in case of redundant credentials
                return redirect('login')
            return redirect('login')
    return render(request, 'Registration/signup.html', {'form': form})


def connect_user(request, u_id):
    user = AppUser.objects.get(id=u_id)
    obj = Connected()
    obj.first = AppUser.objects.get(User=request.user)
    obj.second = user
    obj.save()
    return redirect('/')


def message(request, u_id):
    msg = request.GET.get('msg', '')
    obj = Message()
    obj.sender = AppUser.objects.get(User=request.user)
    obj.receiver = AppUser.objects.get(id=u_id)
    obj.data = msg
    obj.save()
    return redirect('/messages/' + str(u_id))


def messages(request, u_id):
    sr = AppUser.objects.get(User=request.user)
    rr = AppUser.objects.get(id=u_id)
    msgs = Message.objects.filter(Q(sender=sr, receiver=rr) | Q(sender=rr, receiver=sr))
    msgs.order_by('date')
    return render(request, 'messages.html', {'msgs': msgs, 'u_id': u_id})
