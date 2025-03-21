from django.shortcuts import render

from . import util


def index(request):
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