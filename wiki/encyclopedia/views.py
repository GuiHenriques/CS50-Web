from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import markdown2
from . import util

def index(request):
    query = request.GET.get("q")
    if query:
        if util.get_entry(query):
            return entry(request, query)
        else:
            entries = util.list_entries()
            entries = [e for e in entries if query.lower() in e.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": entries
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })

def entry(request, name):
    md = util.get_entry(name)
    if md:
        html = markdown2.markdown(md)
        return render(request, "encyclopedia/entry.html", {
            "html": html,
            "title": name.capitalize(),
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"Entry for '{name}' not found.",
            "title": name,
        })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title").capitalize()
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": f"The entry '{title}' already exists.",
                "title": "Error"
            })
        content = request.POST.get("content")
        util.save_entry(title, content)
        return entry(request, title)

    return render(request, "encyclopedia/new.html", {
        "method": request.method
    })

def edit(request):
    title = request.POST.get("title")
    md = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "content": md,
        "title": title
    })
