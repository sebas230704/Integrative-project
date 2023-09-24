from django.shortcuts import render, redirect
from .models import Users
from .forms import CreateNewName

# Create your views here.
def hello(request):
  if request.method == 'GET':
    return render(request, 'index.html', {
       'form': CreateNewName()
    })
  elif request.method == 'POST':
    name = request.POST.get('name')  
    lastName = request.POST.get('lastName')
    
    if name is not None and lastName is not None:
        Users.objects.create(name=name,
                          lastName=lastName)    
        return redirect('/nombres/')



def nombres(request):
    #Users.objects.create(title=request.GET(['nombre']))
    nombres = Users.objects.all
    return render(request, 'mostrarNombres.html', {
        'nombres': nombres,
    })
