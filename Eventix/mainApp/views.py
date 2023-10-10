from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateNewEvent, supplySpaceForm
from .models import *
from datetime import datetime

# Create your views here.


def home(request):
    eventCategories = EventCategories.objects.all
    return render(request, 'home.html', {
        'eventCategories': eventCategories
    })


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home') #cambiar home a la pagina que tiene el base diferente
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })
    


def createEvent(request):
    if request.method == 'POST':
        form = CreateNewEvent(request.POST)
        if form.is_valid():
            # Varificamos is la instancia email en 'users' conincide con la instancia 'username' en auth_user
            # request.user nos retorna el username la cual es una email
       

            # Obtener datos del formulario
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']
            place = form.cleaned_data['place']
            category_ids = form.cleaned_data['categories']

               
            event = Event(
                name=name,
                descripcion=description,
                date=date,
                city=city,
                place=place,
                idUser=request.user
            )

            event.save()

            for category in category_ids:
                event_eventCategories = Event_eventCategories(
                    idEvent = event,
                    idEventCategorie = category
                )
                event_eventCategories.save()
            print("CATEGORIES_: ", category_ids)
            return redirect('/') 

    else:
        form = CreateNewEvent()

    return render(request, 'createEvent.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form' : AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form' : AuthenticationForm,
                'error' : 'Username or password is incorrect'
            })
            
        else:
            login(request, user)
            return redirect('home')
        
def supplySpace(request):
    
    if request.method == 'GET':
        return render(request, 'supplySpace.html', {
            'form' : supplySpaceForm
        })
    else:
        try:
            form = supplySpaceForm(request.POST)
            new_space = form.save(commit=False)
            new_space.user = request.user
            new_space.save()
            return redirect('home')
        except ValueError:
            return render(request, 'supplySpace.html', {
            'form' : supplySpaceForm,
            'error' : "Please validate your information"
        })
#este sería el verdadero home
def spaces(request):
    spaces = Space.objects.all()
    return render(request, 'spaces.html', {'spaces' : spaces})


def event(request, categoria_id):
    categoria = EventCategories.objects.get(pk=categoria_id)
    # Consulta los eventos relacionados con la categoría
    events = Event.objects.filter(event_eventcategories__idEventCategorie=categoria)
    print("EVENTOS: ", events)
    
    return render(request, 'events.html', {'events': events})        



def defDateTime(date):
    if date:
        dateTime = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        dateTime = None  
    
    return dateTime

