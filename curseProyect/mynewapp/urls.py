from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('nombres/', views.nombres),
    #path('consulta/<int:id>', views.project),

]
