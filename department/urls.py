from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = "department"
urlpatterns = [
    path('department/', views.Department, name="department"),
    path('addDepartment/', views.addDepartment, name="addDepartment"),
    path('editDepartment/<int:id>', views.editDepartment, name="editDepartment"),
    path('course/', views.Courses, name="course"),
    path('addCourse/', views.addCourse, name="addCourse"),
    path('course/<int:id>', views.editCourse, name="editCourse"),
    path('class/', views.Classes, name="class"),
    path('addClass/', views.addClass, name="addClass"),
    path('class/<int:id>', views.editClass, name="editClass"),
    path('teachers/',views.Teachers,name="teachers"),
    path('addTeacher/',views.addTeacher,name="addTeacher"),
    path('teacher/<int:id>',views.editTeacher, name="editTeacher"),
    path('teacher_class', views.teacherClass, name="teacher_class"),
]
