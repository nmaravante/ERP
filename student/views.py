from django.shortcuts import render, redirect, reverse
from login.models import Dept, Course, Class,Student

def Students(request):
    students = Student.objects.all()
    context={
        'students': students
    }
    return render(request,'student/students.html',context)

def addStudent(request):
    if request.method=="POST":
        student = Student()
        student.class_id_id = request.POST['class']
        student.USN = request.POST['USN']
        student.name = request.POST['name']
        student.sex = request.POST['sex']
        student.DOB = request.POST['DOB']
        student.phone = request.POST['phone']
        student.save()
        context={
            'class_s': Class.objects.all(),
            'success':"Student Added Successfully"
        }
        return render(request, 'student/add_student.html', context)
    class_s = Class.objects.all()
    context={
        'class_s': class_s
    }
    return render(request, 'student/add_student.html', context)

def editStudent(request,id):
    if request.method=="POST":
        student=Student.objects.get(id=id)
        student.class_id_id = request.POST['class']
        student.USN = request.POST['USN']
        student.name = request.POST['name']
        student.sex = request.POST['sex']
        student.DOB = request.POST['DOB']
        student.phone = request.POST['phone']
        student.save()
        context = {
            'class_s': Class.objects.all(),
            'success': "Student Updated Successfully"
        }
        return render(request, 'student/edit_student.html', context)
    if request.method=="GET":
        student = Student.objects.get(id=id)
        print(student)
        context={
            'class_s': Class.objects.all(),
            'student': student
        }
        return render(request, 'student/edit_student.html', context)
