from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.db import models
from django.utils import timezone
from datetime import timedelta, date


sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

time_slots = (
    ('7:30 - 8:30', '7:30 - 8:30'),
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 11:50', '11:00 - 11:50'),
    ('11:50 - 12:40', '11:50 - 12:40'),
    ('12:40 - 1:30', '12:40 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

class Permissions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Permissions'


class Role(models.Model):
    name = models.CharField(max_length=256)
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return self.name



class User(AbstractUser):
    roles = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    permissions = models.ManyToManyField(Permissions)
    created_date =models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # @property
    # def is_student(self):
    #     if hasattr(self, 'student'):
    #         return True
    #     return False

    # @property
    # def is_teacher(self):
    #     if hasattr(self, 'teacher'):
    #         return True
    #     return False

    # def __str__(self):
    #     return self.first_name


class Dept(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    short_code = models.CharField(max_length=100, blank=True, null=True)
    shortname = models.CharField(max_length=50, default='X')

    def __str__(self):
        return self.name


class Class(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    sem = models.IntegerField()
    shortname = models.CharField(max_length=50, default='X')

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        d = Dept.objects.get(name=self.dept)
        return '%s : %d %s' % (d.name, self.sem, self.section)


class Student(AbstractBaseUser):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)
    USN = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    sex = models.CharField(max_length=50, choices=sex_choice, default='Male')
    DOB = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    t_USN = models.CharField(max_length=100, blank=True, null=True)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    sex = models.CharField(max_length=50, choices=sex_choice, default='Male')
    DOB = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.name


class Assign(models.Model):            #Assign
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course', 'class_id', 'teacher'),)

    def __str__(self):
        cl = Class.objects.get(id=self.class_id_id)
        cr = Course.objects.get(id=self.course_id)
        te = Teacher.objects.get(id=self.teacher_id)
        return '%s : %s : %s' % (te.name, cr.shortname, cl)


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots, default='11:00 - 11:50')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
