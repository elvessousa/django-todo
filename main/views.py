from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from main.forms import CreateNewList
from main.models import ToDoList


def index(response, id):
    """ List items page """
    pagename = "page"
    tdlist = ToDoList.objects.get(id=id)

    if tdlist in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)

            if response.POST.get("save"):
                for item in tdlist.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False

                    item.save()

            elif response.POST.get("newItem"):
                text = response.POST.get("new")

                if len(text) > 2:
                    tdlist.item_set.create(text=text, complete=False)
                else:
                    print("invalid input")

        return render(response, "main/list.html", {
            "list": tdlist,
            "pagename": pagename
        })

    return render(response, "main/lists.html", {"pagename": pagename})


def home(response):
    """ Home page """
    pagename = "home"

    return render(response, "main/home.html", {"pagename": pagename})


def create(response):
    """ Create lists page """
    pagename = "page"

    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {
        "form": form,
        "pagename": pagename
    })


def lists(response):
    pagename = "page"
    return render(response, "main/lists.html", {"pagename": pagename})
