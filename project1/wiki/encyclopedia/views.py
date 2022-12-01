from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    entry = util.get_entry(name)
    if entry == None:
        return HttpResponse("entry not found")
    else:
        html_entry = markdown2.markdown(entry)
        
        return render(request, "encyclopedia/entry.html", {
          'entry' : html_entry , 'title' : name
        })
