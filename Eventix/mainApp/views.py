from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from .forms import *
from .models import *
from datetime import datetime
from django.core.files.base import ContentFile

# Create your views here.

def home(request):
    eventCategories = EventCategories.objects.all()
    events = Event.objects.all()
    userLogger = request.user.is_authenticated


    if request.user.is_authenticated:
        for event in events:
            event_like = EventLikes.objects.filter(idUser=request.user, idEvent=event.idEvent)
        
            if event_like.exists():
                event.like = event_like.first().like 
            else:
                event.like = 0

    return render(request, 'home.html', {
        'eventCategories': eventCategories, 
        'events': events,
        'userLogger': userLogger
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
        form = CreateNewEvent(request.POST, request.FILES)
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
            if 'image' in form.cleaned_data:
                image = form.cleaned_data['image']
            else:
                image = 'images/default.png'

               
            event = Event(
                name=name,
                descripcion=description,
                date=date,
                city=city,
                place=place,
                isPreEvento=0,
                idUser=request.user,
                image=image
            )

            event.save()

            for category in category_ids:
                event_eventCategories = Event_eventCategories(
                    idEvent = event,
                    idEventCategorie = category
                )
                event_eventCategories.save()
            return redirect('/') 

    else:
        form = CreateNewEvent()

    return render(request, 'createEvent.html', {'form': form})


def planPreEvento(request):
    organizers = Organizers.objects.all()
    organizer_list = []

    for organizer in organizers:
        organizer_data = {
            'idOrganizers': organizer.idOrganizers,
            'companyName': organizer.companyName,
            'description': organizer.description,
            'idUser': organizer.idUser.id,
            'especialidades': []
        }
        especialidades = EspecialidadesDeOrganizador.objects.filter(idOrganizer=organizer)
        for especialidad in especialidades:
            speciality_data = {
                'idSpecialty': especialidad.idSpecialty.idSpecialty,
                'name': especialidad.idSpecialty.name
            }
            organizer_data['especialidades'].append(speciality_data)
        organizer_list.append(organizer_data)

    
    if request.method == 'POST':
        selected_organizers = request.POST.getlist('selected_organizers')
        selected_organizers_data = []
        form = CreateNewEvent(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']
            place = form.cleaned_data['place']
            category_ids = form.cleaned_data['categories']
            if 'image' in form.cleaned_data:
                image = form.cleaned_data['image']
            else:
                image = 'images/default.png'

            event = Event(
                name=name,
                descripcion=description,
                date=date,
                city=city,
                place=place,
                isPreEvento=1,
                idUser=request.user,
                image=image
            )
            
            event.save()

            # for category in category_ids:
            #     event_eventCategories = Event_eventCategories(
            #         idEvent = event,
            #         idEventCategorie = category
            #     )
            #     event_eventCategories.save()


            idOrganicerAux = 0
            for organizer_id in selected_organizers:
                organizer = Organizers.objects.get(idOrganizers=organizer_id)
                selected_organizers_data.append({
                    'idOrganizers': organizer.idOrganizers,
                    'companyName': organizer.companyName,
                    'description': organizer.description,
                    'idUser': organizer.idUser.id,
                })

                if organizer_id != idOrganicerAux:

                    idOrganicerAux = idOrganicerAux
                    contractor = Contractors(
                        idOrganizer = organizer,
                        idUser = request.user
                    )

                    contractor.save()

                    preEvent = PreEventos(
                        idContractor = contractor,
                        idOrganizer = organizer,
                        idEvent = event
                    )

                    preEvent.save()
            
            return redirect('myPreEvents')

    if request.method == 'GET':
        return render(request, 'planPre_event.html', {'organizers': organizer_list})



def myPreEvents(request):
    current_user = request.user
    
    events = Event.objects.filter(idUser=current_user)
    
    events_with_organizers = {}
    
    for event in events:
        # Obtener los ID de los organizadores asociados a este evento
        organizers_ids = PreEventos.objects.filter(idEvent=event).values_list('idOrganizer', flat=True)
        
        # Obtener los objetos de Organizers utilizando los IDs obtenidos
        organizers = Organizers.objects.filter(idOrganizers__in=organizers_ids)
        
        # Almacena el evento y sus organizadores en el diccionario
        events_with_organizers[event] = organizers
    
    print(events_with_organizers)

    return render(request, 'myPreEvents.html', {
        'events_with_organizers': events_with_organizers
    })



     

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


def events(request, categoria_id):
    categoria = EventCategories.objects.get(pk=categoria_id)
    # Consulta los eventos relacionados con la categoría
    events = Event.objects.filter(event_eventcategories__idEventCategorie=categoria)
    print("FUNCIONA")
   
    
    return render(request, 'events.html', {'events': events})        


def eventDetail(request, idEvent):
    print("llega idEvent: ", idEvent)

    event = get_object_or_404(Event, idEvent=idEvent)
    
    # Obtener el perfil principal asociado al evento
    principal_profile = get_object_or_404(PrincipalProfile, idUser=event.idUser)

    # Acceder al campo idUser del perfil principal
    userByEvent = principal_profile.idUser

    print(request.user)
    # Verificar si existe un registro en EventLikes con idUser y idEvent específicos
    try:
        # El registro existe
        exists = True
    except EventLikes.DoesNotExist:
        # El registro no existe
        exists = False

    return render(request, 'eventDetail.html', {'event': event, 'userByEvent': userByEvent, 'like_exists': exists, 'principal_profile': principal_profile})




def organizer(request):
    if request.method == 'POST':
        form = CreateOrganizer(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            companyName = form.cleaned_data['companyName']
            description = form.cleaned_data['description']
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            specialties = form.cleaned_data['specialties']
               
            organizer = Organizers(
                companyName=companyName,
                description=description,
                telefono=telefono,
                email=email,
                idUser = request.user
            )
            organizer.save()
            print("specialties", specialties)
            for specialtie in specialties:
                event_eventCategories = EspecialidadesDeOrganizador(
                    idOrganizer = organizer,
                    idSpecialty = specialtie
                )
                event_eventCategories.save()
            return redirect('/') 

    else:
        form = CreateOrganizer()

    return render(request, 'createOrganizer.html', {'form': form})



def defDateTime(date):
    if date:
        dateTime = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        dateTime = None  
    
    return dateTime

def aboutUs(request):
    return render(request, 'about_us.html')

def profile(request):
    return render(request, 'profile.html')

def analyzer(request):
    return render(request, 'analyzer.html')

def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'form': form})


def principalProfile(request, idUser):
    user = User.objects.get(pk=idUser)
    user_events = Event.objects.filter(idUser=idUser)

    esMiPerfil = 0
    myIdUser = request.user.id

    userActual = request.user

    
    if myIdUser == idUser:
        esMiPerfil = 1
    
    try:
        principal_profile = PrincipalProfile.objects.get(idUser=user)
    except PrincipalProfile.DoesNotExist:
        principal_profile = PrincipalProfile.objects.create(idUser=user)
    
    if Organizers.objects.filter(idUser=user).exists():
        organizer = Organizers.objects.get(idUser=user)
        id_organizerIfExist = organizer.idOrganizers
        organizer = get_object_or_404(Organizers, idOrganizers=id_organizerIfExist)
    
        try:
            organizer_rating = OrganizerRatings.objects.get(idOrganizer=organizer, idUser=userActual)
            current_rating = organizer_rating.rating
        except OrganizerRatings.DoesNotExist:
            current_rating = 0
    else: 
        id_organizerIfExist = 0
        current_rating = 0

    if request.method == 'POST':
        if 'profile_photo' in request.FILES:
            principal_profile.profilePhoto = request.FILES['profile_photo']
            principal_profile.save()
        if 'secondary_photo' in request.FILES:
            principal_profile.secondaryPhoto = request.FILES['secondary_photo']
            principal_profile.save()

    return render(request, 'principalProfile.html', {'esMiPerfil': esMiPerfil, 'principal_profile': principal_profile, 'user_events': user_events, 'id_organizerIfExist': id_organizerIfExist, 'current_rating': current_rating})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def toggle_like(request, evento_id):
    if request.method == 'POST':
        user_id = request.user.id  # Obtén el ID del usuario de alguna manera (deberías usar el ID del usuario actual)

        evento = get_object_or_404(Event, pk=evento_id)
        user_liked = EventLikes.objects.filter(idEvent=evento_id, idUser=user_id).first()

        if user_liked:
            user_liked.delete()
            liked = False
        else:
            EventLikes.objects.create(idUser_id=user_id, idEvent_id=evento_id, like=1)
            liked = True

        likes_count = EventLikes.objects.filter(idEvent=evento_id).count()

        return JsonResponse({'liked': liked, 'likes_count': likes_count})



def rate_organizer(request, idOrganizer):
    if request.method == 'POST':
        user = request.user
        rating = int(request.POST.get('rating'))

        organizer = get_object_or_404(Organizers, idOrganizers=idOrganizer)

        try:
            # Verificar si ya existe una calificación para este usuario y organizador
            organizer_rating = OrganizerRatings.objects.get(idOrganizer=organizer, idUser=user)
            if rating == organizer_rating.rating:
                organizer_rating.delete()
            else:
                organizer_rating.rating = rating
                organizer_rating.save()
        except OrganizerRatings.DoesNotExist:
            # Si no existe, crea una nueva calificación
            organizer_rating = OrganizerRatings.objects.create(
                rating=rating,
                idUser=user,
                idOrganizer=organizer
            )
        
        return JsonResponse({'message': 'Calificación exitosa'})

    return JsonResponse({'message': 'Error en la calificación'})



