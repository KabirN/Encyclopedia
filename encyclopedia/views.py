import secrets

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class':'form-control col-md-8 col-lg-8'}))
    # initial is used for initializing the form with a dictionary of values via the "initial" argument directly on the form instance declared in the view method.
    #
    content = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-8', 'rows':10}))
    edit = forms.BooleanField(initial = False,widget=forms.HiddenInput(), required = False)
#widget=forms.HiddenInput()
#enter your views here

def index(request):
    return render(request, "encyclopedia/index.html", {
      "entries": util.list_entries()
    })

def entry(request,entry):
    markdowner = Markdown()
    entrypage =  util.get_entry(entry)
    if entrypage is None:
        return render(request, "encyclopedia/entrynotexist.html",{
        "entrytitle" : entry
        })

    else:
        return render(request, "encyclopedia/entry.html", {
      "entry" : markdowner.convert(entrypage) ,
      "entrytitle" : entry
    })

def search(request):
    value = request.GET.get("q",'')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry':value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper(): #.upper() is used for case sensitive like we can write css instead of CSS.
                subStringEntries.append(entry) #["append(value)"] is used for adding title to my growing list of entry or list of entry.

        return render(request, "encyclopedia/search.html",{
            "entries" : subStringEntries,
            "search" : True,
            "value" : value
           })


def newEntry(request):
    if request.method == "POST":
        #POST, generate form with data from the request
        form = NewEntryForm(request.POST)#creating a form variable for taking value submitted by user & (request.POST)contains the all data that user input.
        #reference is now a bound instance with user data sent in POST.
        # process data , insert into DB, generate content ,redirect into nw URL,etc

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]# "cleaned_data" that will give me access to all of data that user submitted.

            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                # Reference form instance (bound/unbound) is sent to template for rendering template.
                return render(request, "encyclopedia/newEntry.html",{
                "form" : form,
                "existing" : True,
                "entry" : title
                })
        else:
            return render(request, "encyclopedia/newEntry.html",{
            "form" : form,
            "existing" : False
            })
    else:
        return render(request, "encyclopedia/newEntry.html",{
         "form": NewEntryForm(),
         "existing" : False
         })

def edit(request,entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/entrynotexist.html",{
        "entrytitle" : entryPage
        })

    else:
        form = NewEntryForm()

        form.fields["title"].initial = entry
        #form.fields["title"].widget = forms.HiddenInput() # it is for hiding the title field in edit page
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True #

        return render(request, "encyclopedia/newEntry.html",{#we'll use "signin.html"page to link it with signin & edit page
        "form": form,
        "edit": form.fields["edit"].initial,
        "entrytitle": form.fields["title"].initial # or we can write "entry"
        })

def signin(request):
    if request.method=="POST":
        username = request.POST["username"]
        Password = reuqest.POST["password"]
        user = authenticate(reuqest, username, password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('random'))
        else:
            return render(request,"encyclopedia/index.html")

    return render(request,"encyclopedia/signin.html")


def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry",kwargs={'entry': randomEntry}))




def __init__(self, *args, **kwargs):
     #Get 'initial' argument if any
    initial_arguments = kwargs.get('initial',None)
    updated_initial = {}
    if initial_arguments:
    # we initial arguments , fetch 'user' placeholder variables if any
        user = initial_arguments.get('user',None)
       # Now update the form's initial values if user
        if user:
            updated_initial['name'] = getattr(user, 'first_name', None)
            updated_initial['email'] = getattr(user, 'email', None)

        # You can also initialize form fields with hardcoded values
        # or perform complex DB logic here to then perform initialization
        updated_initial['comment'] = 'Please provide a comment '

        #Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        super(ContactForm, self).__init__(*args, **kwargs)
