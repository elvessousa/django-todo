from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from main.forms import CreateNewList
from main.models import ToDoList


def index(response, id):
    """ List items page """

    tdlist = ToDoList.objects.get(id=id)

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
        "list": tdlist
    })


def home(response):
    """ Home page """

    return render(response, "main/home.html", {})


def create(response):
    """ Create lists page """

    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()

        return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {
        "form": form
    })