from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from random import choice
import markdown2

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput())
    entry = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request):
    if request.method == "GET":
        title = request.GET.get("title")
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "form": EditForm(initial={'title': title, 'entry': util.get_entry(title)})
        })
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            updated_entry = form.cleaned_data["entry"]
            print(title)
            util.save_entry(title, updated_entry)
            return HttpResponseRedirect(title)
    return render(request, "encyclopedia/edit.html", {
        "form": EditForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None: 
        return render(request, "encyclopedia/error.html")
    else: 
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
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

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            if util.get_entry(title) is None:
                util.save_entry(title, entry)
                return HttpResponseRedirect(title)
            else:
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": True
                })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def random(request):
    entries = util.list_entries()
    page_title = choice(entries)
    return HttpResponseRedirect(page_title)