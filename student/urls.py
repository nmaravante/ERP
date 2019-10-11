from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = "student"
urlpatterns = [
    path('students/', views.Students, name="students"),
    path('addStudent/', views.addStudent, name="addStudent"),
    path('student/<int:id>', views.editStudent, name="editStudent")
    
]
