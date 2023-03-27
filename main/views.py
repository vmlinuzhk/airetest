from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from main.models import Bug, User
from main.forms import BugForm, PersonForm

# Create your views here.


def home(request):
    tab = "people" if "pp" in request.GET else "bugs"

    bugs = Bug.objects.all()
    bug_page_number = int(request.GET.get('bp', default=1))
    bug_paginator = Paginator(bugs, 20)
    bug_page = bug_paginator.page(bug_page_number)

    people = User.objects.all()
    people_page_number = int(request.GET.get('pp', default=1))
    people_paginator = Paginator(people, 20)
    people_page = people_paginator.page(people_page_number)

    return render(request, "home.html", {"bugpage": bug_page, "peoplepage": people_page, "tab": tab})


def bug(request, bugid):
    bug = Bug.objects.get(id=bugid)
    people = User.objects.all()
    if request.method == "POST":
        personid = int(request.POST.get('owner', None))
        person = User.objects.get(id=personid)
        bug.owner = person
        bug.save()
        messages.success(request, "Bug owner updated")
    return render(request, "bug.html", {"bug": bug, "people": people})


def closebug(request, bugid):
    bug = get_object_or_404(Bug, pk=bugid)

    if bug.closed:
        messages.error(request, "Cannot close bug - already closed")
    else:
        bug.closed = True
        bug.save()
    return redirect(bug)


def newbug(request):
    if request.method == "GET":
        form = BugForm()
    elif request.method == "POST":
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save()
            return redirect(bug)
    return render(request, "newbug.html", {"form": form})


def people(request):
    people = User.objects.all()
    return render(request, "people.html", {"people": people})


def newperson(request):
    name = request.POST.get("name", None)
    if name:
        person = User(name=name)
        person.save()
        messages.success(request, "New person added")
    else:
        messages.error(request, "No name given")
    return redirect("/?pp=1")


def person(request):
    if request.method == "GET":
        return redirect("/")
    elif request.method == "POST":
        newname = request.POST.get("name", None)
        personid = int(request.POST.get("personid", 0))
        person = User.objects.get(id=personid)
        person.name = newname
        person.save()
        messages.success(request, "Person name updated")
        return redirect("/?pp=1")
