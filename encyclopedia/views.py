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
        entry = util.get_entry(search_term) 
        if entry is None: 
            entries = util.list_entries()
            matching_titles = [title for title in entries if search_term.lower() in title.lower()]
            print(matching_titles)
            if not matching_titles:
                return render(request, "encyclopedia/error.html")
            else: 
                return render(request, "encyclopedia/results.html", {
                    "results": matching_titles
                })
        else: 
            return render(request, "encyclopedia/entry.html", {
            "title": search_term,
            "entry": util.get_entry(search_term)
        })

def results(request):
    return render(request, "encyclopedia/results.html")