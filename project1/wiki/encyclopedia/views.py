from django.shortcuts import render
from django.http import HttpResponse 
from . import util
import random
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
        # if search don't found
        if entry == None:
            L = []
            list_name = util.list_entries()
            for i in list_name:
                if q.lower() in i.lower():
                    L.append(i)
            return render(request, "encyclopedia/search.html", {
                "entries": L
            })
        # if search found
        else:
            html_entry = markdown2.markdown(entry)
            
            return render(request, "encyclopedia/entry.html", {
            'entry' : html_entry , 'title' : q.capitalize()
            })
    else:
        return render(request, "encyclopedia/search.html", {
        })

def new(request):
    '''
    creat new entry
    '''
    if request.method == "POST":
        L = []
        name = request.POST["n"]
        data = request.POST["d"]

        # change entry names to lower and add them to new list name L
        L_entries = util.list_entries()
        for i in L_entries:
            L.append(i.lower())
    
        # if name is allready exists
        if name.lower() in L:
            return entry(request, name.capitalize())
        else:
            # creat new file
            path = r'C:\Users\moshe\Desktop\cswab\cs50web\project1\wiki\entries\{}.md'.format(name)
            with open(path, 'w+') as f:
                f.write(data)
            return entry(request, name.capitalize())

    else:
        return render(request, "encyclopedia/new_entry.html", {
    })

def random_page(request):
    '''
    render a random page
    '''
    L = []
    L_entries = util.list_entries()
    for i in L_entries:
        L.append(i)
    e = random.choice(L)

    entry = util.get_entry(e)
    html_entry = markdown2.markdown(entry)

    return render(request, "encyclopedia/entry.html", {
        'entry' : html_entry , 'title' : e
    })

def edit(request):
    '''
    edit page 
    '''
    if request.method == 'POST':
        pass
    else:
        x = request.host_url
        print(x)
        return render(request, "encyclopedia/edit.html", {

        })