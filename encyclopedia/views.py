from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title) 
    if entry is None: 
        return render(request, "encyclopedia/error.html")
    else: 
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title)
    })

def search(request):
    if request.method == "GET":
        search_term = request.GET.get("q")
        print(search_term)
        entry = util.get_entry(search_term) 
        if entry is None: 
            return render(request, "encyclopedia/error.html")
        else: 
            return render(request, "encyclopedia/entry.html", {
            "title": search_term,
            "entry": util.get_entry(search_term)
        })