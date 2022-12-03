from django.shortcuts import render
from django.http import HttpResponse 
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    '''
    find entry and render web page
    '''
    entry = util.get_entry(name)
    if entry == None:
        return HttpResponse("entry not found")
    else:
        html_entry = markdown2.markdown(entry)
        
        return render(request, "encyclopedia/entry.html", {
          'entry' : html_entry , 'title' : name
        })

def search(request):
    '''
    search bar    
    '''
    if request.method == "POST":
        q = request.POST["q"]
        entry = util.get_entry(q)
        # if search dont found
        if entry == None:
            L = []
            list_name = util.list_entries()
            for i in list_name:
                if q.lower() in i.lower():
                    print(type(q))
                    print(type(i))
                    L.append(i)
            return render(request, "encyclopedia/search.html", {
                "entries": L
            })
        # if search found
        else:
            html_entry = markdown2.markdown(entry)
            
            return render(request, "encyclopedia/entry.html", {
            'entry' : html_entry , 'title' : q
            })
    else:
        return render(request, "encyclopedia/search.html", {
        })

