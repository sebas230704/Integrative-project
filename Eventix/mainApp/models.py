from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Name(models.Model):
    #campos

class Space(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.IntegerField()
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='default.png')
    
    def __str__(self): #es para que en admin aparezca el nombre del objeto y no "obecjt(x)"
        return self.title



class Organizers(models.Model):
    idOrganizers = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=45)
    description = models.CharField(max_length=808)
    telefono = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=99, null=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'organizers'


class Event(models.Model):
    idEvent = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=808, null=True)
    date = models.DateTimeField()
    city = models.CharField(max_length=45)
    place = models.CharField(max_length=45)
    isPreEvento = models.IntegerField(null=True)
    image = models.ImageField(upload_to='images/', default='default.png')
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'event'
    



class Specialties(models.Model):
    idSpecialty = models.AutoField(primary_key=True)
    name = models.CharField(max_length=77, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'specialties'


class EspecialidadesDeOrganizador(models.Model):
    idOrganizer = models.ForeignKey(Organizers, on_delete=models.CASCADE)
    idSpecialty = models.ForeignKey(Specialties, on_delete=models.CASCADE)

    class Meta:
        db_table = 'especialidadesDeOrganizador'



class Contractors(models.Model):
    idContractor = models.AutoField(primary_key=True)
    idOrganizer = models.ForeignKey(Organizers, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contractors'


class OrganizerRatings(models.Model):
    idOrganizerRatings = models.AutoField(primary_key=True)
    rating = models.IntegerField(null=True)
    comment = models.CharField(max_length=202, null=True)
    date = models.DateTimeField(null=True)
    idOrganizer = models.ForeignKey(Organizers, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idContractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)

    class Meta:
        db_table = 'organizerRatings'



class PreEventos(models.Model):
    idContractor = models.ForeignKey(Contractors, on_delete=models.CASCADE)
    idOrganizer = models.ForeignKey(Organizers, on_delete=models.CASCADE)
    idEvent = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'preEventos'



class EventFigures(models.Model):
    idEventFigure = models.AutoField(primary_key=True)
    nikname = models.CharField(max_length=45)
    caracteristica = models.CharField(max_length=45, null=True)
    idEvent = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'eventFigures'




class FavoriteOrganizers(models.Model):
    idFavoriteOrganizer = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idOrganizer = models.ForeignKey(Organizers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favoriteOrganizers'



class EventCategories(models.Model):
    idEventCategorie = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'eventCategories'


class Event_eventCategories(models.Model):
    idEvent = models.ForeignKey(Event, on_delete=models.CASCADE)
    idEventCategorie = models.ForeignKey(EventCategories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_eventCategories'



class EventImages(models.Model):
    idEvenImage = models.AutoField(primary_key=True)
    urlImage = models.CharField(max_length=404)
    name = models.CharField(max_length=101)
    idEven = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'eventImages'
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    likes = models.CharField(max_length=100, blank=True)
    



    
