from django.contrib import admin
from login.models import (User, Dept, Course, Class, Student, Teacher, Permissions, 
                          Role, Assign, AssignTime)
# Register your models here.


class ClassInline(admin.TabularInline):
    model = Class
    extra = 0


class DeptAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')
    ordering = ['name']


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'name', 'dept')
    search_fields = ('short_code', 'name', 'dept__name')
    ordering = ['dept', 'short_code']


class ClassAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'dept', 'sem', 'section')
    search_fields = ('shortname', 'dept__name', 'sem', 'section')
    ordering = ['dept__name', 'sem', 'section']
    inlines = [StudentInline]


class StudentAdmin(admin.ModelAdmin):
    list_display = ('USN', 'name', 'class_id')
    search_fields = ('USN', 'name', 'class_id__id', 'class_id__dept__name')
    ordering = ['class_id__dept__name', 'class_id__id', 'USN']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'dept')
    search_fields = ('name', 'dept__name')
    ordering = ['dept__name', 'name']


class AssignTimeInline(admin.TabularInline):  
    model = AssignTime
    extra = 0


class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('class_id', 'course', 'teacher')
    search_fields = ('class_id__dept__name', 'class_id__id',
                     'course__name', 'teacher__name', 'course__shortname')
    ordering = ['class_id__dept__name', 'class_id__id', 'course__id']
    raw_id_fields = ['class_id', 'course', 'teacher']

admin.site.register(User)
admin.site.register(Permissions)
admin.site.register(Role)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(AssignTime)
