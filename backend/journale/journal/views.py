import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets

from journale.journal.models import Journal
from journale.journal.serilizers import JournalSerializer

from journale.journal.forms import JournalForm


def get_journals(request):
    if request.user.is_authenticated:
        user = request.user
        journals = Journal.objects.filter(owner=user)
        context = {
            "count": journals.count(),
            "journals": journals
        }
        return render(request, "home.html", context=context)
    else:
        return redirect("/users/login")


def create_journal(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = JournalForm(request.POST)
            if form.is_valid():
                owner = request.user
                journal = form.save(commit=False)
                journal.owner = owner
                journal.save()
                messages.success(request, "Journal created successfully.")
                return redirect("/")
            messages.error(request, "Error saving Journal!")
        form = JournalForm()
        return render(request, "journal/new_journal.html", context={"new_journal": form})
    else:
        return redirect("/users/login")

def update_journal(request, id):
    if request.user.is_authenticated:
        journal = get_object_or_404(Journal, id=id, owner=request.user)
        if request.method =="POST":
            form = JournalForm(request.POST or None, instance=journal)
            if form.is_valid():
                journ = form.save(commit=False)
                journ.owner = journal.owner
                journ.save()
                messages.success(request, "Journal Updated successfully.")
                return redirect("/")
            messages.error(request, "Error Updating Journal!")
        form = JournalForm(instance=journal)
        return render(request, "journal/update_journal.html", context={"form":form})
    else:
        return redirect("/users/login")

# API
class JournalViewset(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


