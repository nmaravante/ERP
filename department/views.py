from django.shortcuts import render, redirect, reverse, get_object_or_404
from login.models import Dept, Course, Class, Teacher, User

# Create your views here.
def Department(request):
    dept = Dept.objects.all()
    context={
        'department': dept
    }
    return render(request, 'core/list_department.html', context)

def addDepartment(request):
    if request.method=="POST":
        dept = Dept()
        dept.name = request.POST['department']
        dept.short_name = request.POST['s_dept']
        dept.save()
        context={
            'success':"Department Added Successfully"
        }
        return render(request, "core/add_department.html", context)
    return render(request,'core/add_department.html')


def editDepartment(request,id):
    if request.method=="POST":
        dept = Dept.objects.get(id=id)
        dept.name = request.POST['department']
        dept.short_name = request.POST['s_dept']
        dept.save()
        return redirect(reverse('department:department'))

    if request.method =="GET":
        dept = Dept.objects.get(id=id)
        context={
            'department': dept
        }
        return render(request, 'core/edit_department.html', context)

def Courses(request):
    course = Course.objects.all()
    context = {
        'course': course
    }
    return render(request, 'core/list_course.html', context)


def addCourse(request):
    if request.method=="POST":
        print("hi")
        course = Course()
        print(request.POST['course'])
        course.name = request.POST['course']
        course.shortname = request.POST['s_course']
        course.short_code = request.POST['course_code']
        course.dept_id = request.POST['dept']
        course.save()
        context = {
            'department': Dept.objects.all(),
            'success': "Course Added Successfully"
        }
        return render(request, 'core/add_course.html', context)

    dept = Dept.objects.all()
    context={
        'department': dept
    }
    return render(request, 'core/add_course.html', context)


def editCourse(request,id):
    if request.method=="POST":
        course = Course.objects.get(id=id)
        course.name = request.POST['course']
        course.shortname = request.POST['s_course']
        course.short_code = request.POST['course_code']
        course.dept_id = request.POST['dept']
        course.save()
        context = {
            'success': "Course Updated Successfully"
        }
        return render(request, 'core/add_course.html', context)

    if request.method=="GET":
        dept = Dept.objects.all()
        course = Course.objects.get(id=id)
        print(course.dept_id)
        context = {
            'course': course,
            'department': dept
        }
        return render(request, 'core/edit_course.html', context)

def Classes(request):
    class_s = Class.objects.all()
    context={
        'class': class_s
    }
    return render(request, 'core/list_class.html',context)


def addClass(request):
    if request.method == "POST":
        class_s = Class()
        class_s.section = request.POST['section']
        class_s.sem = request.POST['sem']
        class_s.shortname = request.POST['s_name']
        class_s.dept_id = request.POST['dept']
        class_s.save()
        context = {
            'department' : Dept.objects.all(),
            'success': "Class Added Successfully"
        }
        return render(request, 'core/add_class.html', context)
    dept = Dept.objects.all()
    context = {
        'department': dept
    }
    return render(request, 'core/add_class.html', context)


def editClass(request,id):
    if request.method == "POST":
        class_s = Class.objects.get(id=id)
        class_s.section = request.POST['section']
        class_s.shortname = request.POST['s_name']
        class_s.sem = request.POST['sem']
        class_s.dept_id = request.POST['dept']
        class_s.save()
        context = {
            'success': "Class Updated Successfully"
        }
        return render(request, 'core/edit_class.html', context)

    if request.method == "GET":
        dept = Dept.objects.all()
        class_s = Class.objects.get(id=id)
        context = {
            'class_s': class_s,
            'department': dept
        }
        return render(request, 'core/edit_class.html', context)


def Teachers(request):
    teachers = Teacher.objects.all()
    print(teachers)
    context={
        'teachers':teachers
    }
    return render(request,'teacher/list_teacher.html',context)


def addTeacher(request):
    if request.method=="POST":
        if User.objects.filter(username=request.POST['name']).exists():
            context = {
                'info': "Username already Exist"
            }
            return render(request, 'teacher/add_teacher.html', context)
        else:
            user = User()
            user.username = request.POST['name']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()
            teacher = Teacher()
            teacher.user = user
            teacher.dept_id = request.POST['class']
            teacher.set_password(request.POST['password'])
            teacher.t_USN = request.POST['t_USN']
            teacher.name = request.POST['name']
            teacher.email = request.POST['email']
            teacher.sex = request.POST['sex']
            teacher.DOB = request.POST['DOB']
            teacher.phone = request.POST['phone']
            teacher.save()
            context = {
                'class_s': Dept.objects.all(),
                'success': "Teacher Added Successfully"
            }
            return render(request, 'teacher/add_teacher.html', context)
    dept = Dept.objects.all()
    context={
        'department': dept
    }
    return render(request, 'teacher/add_teacher.html', context)

def editTeacher(request,id):
    if request.method=="POST":
        teacher = Teacher.objects.get(id=id)
        teacher.dept_id = request.POST['class']
        teacher.t_USN = request.POST['t_USN']
        teacher.name = request.POST['name']
        teacher.email = request.POST['email']
        teacher.sex = request.POST['sex']
        teacher.DOB = request.POST['DOB']
        teacher.phone = request.POST['phone']
        user = User.objects.get(id = teacher.user.id)
        user.username = request.POST['name']
        user.email = request.POST['email']
        user.save()
        teacher.user = user
        teacher.save()
        context = {
            'class_s': Dept.objects.all(),
            'success': "Teacher updated Successfully"
        }
        return render(request, 'teacher/edit_teacher.html', context)

    if request.method=="GET":
        teacher = Teacher.objects.get(id=id)
        print(teacher.email)
        context={
            'department': Dept.objects.all(),
            'teacher':teacher
        }
        return render(request,'teacher/edit_teacher.html',context)


def teacherClass(request):
    context={
        'class':Class.objects.all(),
        'course':Course.objects.all(),
        'teacher':Teacher.objects.all(),
    }
    return render(request, 'teacher/teacher_class.html', context)
