from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from random import choice
import markdown2
from . import util


def get_normalized_entry_from_post(request):
    title = request.POST.get("title")
    content = request.POST.get("content").replace('\r\n', '\n')
    return title, content

def index(request):
    query = request.GET.get("q")
    if query:
        entry = util.get_entry(query)
        if entry:
            return redirect("entry", name=query)
        entries = [e for e in util.list_entries() if query.lower() in e.lower()]
        return render(request, "encyclopedia/search.html", {"entries": entries})
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, name):
    if request.method == "POST":
        title, content = get_normalized_entry_from_post(request)
        util.save_entry(title, content)
        return redirect("entry", name=title)
    
    md = util.get_entry(name)
    if md:
        html = markdown2.markdown(md)
        return render(request, "encyclopedia/entry.html", {
            "content": html,
            "title": name.capitalize(),
        })

    return render_error(request, f"Entry for '{name}' not found.", name)

def new(request):
    if request.method == "POST":
        title, content = get_normalized_entry_from_post(request)
        title = title.capitalize()
        if title in util.list_entries():
            return render_error(request, f"The entry '{title}' already exists.")
        
        util.save_entry(title, content)
        return redirect("entry", name=title)

    return render(request, "encyclopedia/new.html", {
        "method": request.method,
    })

def edit(request):
    title = request.POST.get("title")
    md = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "content": md,
        "title": title,
    })

def random(req):
    title = choice(util.list_entries())
    return redirect("entry", name=title)

def render_error(request, message, title="Error"):
    return render(request, "encyclopedia/error.html", {
        "message": message,
        "title": title,
    })