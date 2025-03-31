from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class newSearchForm(forms.Form):
    search = forms.CharField(label="Search")
def index(request):
    if request.method == "POST":
        request.session["search"] = []
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title) 
    print(entry)
    if entry is None: 
        return render(request, "encyclopedia/error.html")
    else: 
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title)
    })