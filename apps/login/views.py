from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django import forms


def index(request):
    if 'id' in request.session:
        return redirect('/quotes')
    else:
        return render(request, "login/index.html")


def register(request):
    if request.method == "POST":
        check = User.objects.register(
            request.POST['name'],
            request.POST['lname'],
            request.POST['email'],
            request.POST['password'],
            request.POST['confirm']
        )
    if not check['valid']:
        for error in check['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['id'] = check['id']
        return redirect('/quotes')


def login(request):
    if request.method == "POST":
        check = User.objects.login(
            request.POST['email'],
            request.POST['password'],
        )
        if not check["valid"]:
            for error in check['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['id'] = check['id']
            return redirect('/quotes')


def logout(request):
    if 'id' in request.session:
        request.session.clear()
        messages.add_message(request, messages.SUCCESS, "See you later")
        return redirect('/')
    else:
        return render(request, "login/index.html")


def quotes(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        all_messages = Quote.objects.all()
        context = {
            "all_messages": all_messages,
            "user": user,
        }
        return render(request, "login/dashboard.html", context)
    else:
        return redirect("/")


def post_quote(request):
    if request.method == "POST":
        errors = Quote.objects.basic_validator1(request.POST)
        if len(request.POST['author']) < 1:
            messages.error(request, "Author name cannot be blank.")
        if len(request.POST['author']) < 3:
            messages.error(request, "Author name need more than 3 characters.")
        if len(request.POST['quote']) < 10:
            messages.error(request, "The quote has to be more than 10 char.")
            return redirect('/')
        else:
            user = User.objects.get(id=request.session['id'])
            Quote.objects.create(
                message_body=request.POST['quote'], uploaded_by=user, author=request.POST['author'])
            print(Quote.objects.last())
            return redirect('/quotes')


def delete(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        quote = Quote.objects.get(id=request.POST['quote_id'])
        quote.delete()
        return redirect('/quotes')
    else:
        return redirect("/")


def users_id(request, id):
    if 'id' in request.session:
        context = {
            "user": User.objects.get(id=id),
            "all_messages": Quote.objects.filter(uploaded_by=id),
        }
    return render(request, "login/user_id.html", context)


def edit(request, id):
    if 'id' in request.session:
        context = {
            "user": User.objects.get(id=id)
        }
        return render(request, "login/edit.html", context)
    else:
        return redirect("/")


def update(request, id):
    if 'id' in request.session:
        if request.method == "POST":
            errors = User.objects.basic_validator(request.POST)
            if len(request.POST['name']) < 1:
                messages.error(request, "First name cannot be blank.")
            if len(request.POST['name']) < 3:
                messages.error(request, "First name need more than 3 characters.")
            if len(request.POST['lname']) < 1:
                messages.error(request, "Last name cannot be blank.")
            if len(request.POST['lname']) < 3:
                messages.error(request, "Last name need more than 3 characters.")
                return redirect("/user/"+id+"/edit")
            else:
                c = User.objects.get(id=id)
                c.name = request.POST['name']
                c.lname = request.POST['lname']
                c.email = request.POST['email']
                c.save()
                # return redirect("/user/"+id+"/edit")
                return redirect('/')
