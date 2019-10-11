from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . models import User, Permissions, Role
from .decorators import permission_required
import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, passwordResetToken
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate

from django.core.exceptions import ObjectDoesNotExist


# Create your views here


def Register(request):
    if request.method=="POST":
        user = User()
        user.username = request.POST['username']
        user.email = request.POST['email']
        if request.POST['password'] == request.POST['repassword']:
            print("password matched")
            user.set_password(request.POST['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = 'Activate your blog account.'
            to_email = request.POST['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, "registration/confirm_link.html")
    return render(request,"registration/registration.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "registration/confirm_mail.html")
    else:
        return HttpResponse('Activation link is invalid!')


def forgotPassword(request):
    if request.method == "POST":
        user = User.objects.get(email=request.POST['email'])
        current_site = get_current_site(request)
        message = render_to_string('password/pas_reset_email.html', {
            'user': user, 'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Reset your password'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
        return render(request, "password/reset_link_confirm.html")
    return render(request, "password/reset.html")


def passwordResetActivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_id = user.id
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        return render(request, "password/reset_password_page.html", {'user': user})
    else:
        return HttpResponse('Activation link is invalid!')


def newPassword(request,pk):
    if request.method == "POST":
        user= User.objects.get(id=pk)
        if request.POST['password'] == request.POST['repassword']:
            print("password matched")
            user.set_password(request.POST['password'])
            user.save()
            return render(request, "password/reset_sucess.html")



@login_required
def changePassowrd(request):
    if request.method == "POST":    
        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(request.POST['old_password']):
                if request.POST['new_pass'] == request.POST['con_new_pass']:
                    user.set_password(request.POST['new_pass'])
                    user.save()
                    context={
                        "success" :"Your password successfully upadated"
                    }
                else:
                    context = {
                        "info" :"Your new password and conform password not matching"
                    }             
            else:
                context = {
                    "warning" : "Old password not matching "
                }
        except ObjectDoesNotExist:
            context = {
                "danger" :"User not Exist"
            }

        return render(request, "password/change_password.html",context)
    return render(request,"password/change_password.html")

@login_required
def Dashboard(request):
    return render(request,"core/dashboard.html")

@permission_required("add_user")
def addUser(request):
    if request.method == "GET":
        context = {
            "roles": Role.objects.all(),
            "permissions": Permissions.objects.all()

        }
        return render(request, 'core/addUser.html', context=context)

    if request.method == "POST":
        user = User()

        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.set_password(request.POST['password'])
        user.roles = Role.objects.get(id=request.POST["role"])

        user.is_active = True
        user.created_date = datetime.datetime.now()
        user.updated_date = datetime.datetime.now()
        user.save()
        for each in request.POST.getlist('permissions'):
            user.permissions.add(Permissions.objects.get(id=each))
        user.save()
        return redirect(reverse("home:listuser"))


@login_required
@permission_required("list_user")
def ListUser(request):
    context = {"users": User.objects.all()}
    return render(request, "core/list_user.html", context)


@login_required
@permission_required("edit_user")
def editUser(request, user_id):
    if request.method == "GET":
        context = {
            "user": User.objects.get(id=user_id),
            "roles": Role.objects.all(),
            "permissions": Permissions.objects.all()

        }
        return render(request, 'core/edit_user.html', context=context)

    if request.method == "POST":
        user = User.objects.get(id=user_id)
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        if request.POST["password"] != "":
            user.set_password(request.POST['password'])
        user.roles = Role.objects.get(id=request.POST["role"])

        user.is_active = True
        user.created_date = datetime.datetime.now()
        user.updated_date = datetime.datetime.now()
        user.save()
        user.permissions.clear()
        for each in request.POST.getlist('permissions'):

            user.permissions.add(Permissions.objects.get(id=each))
        user.save()
        context = {"users": User.objects.all()}
        return redirect(reverse("home:listuser"))



@login_required
@permission_required("add_role")
def addRole(request):
    if request.method == "GET":
        context = {
            "permissions": Permissions.objects.all()
        }
        return render(request, 'core/add_role.html', context=context)

    if request.method == "POST":
        role = Role()
        role.name = request.POST['role_name']
        role.save()
        for each in request.POST.getlist('permissions'):
            role.permissions.add(Permissions.objects.get(id=each))
        role.save()
        return redirect(reverse("home:listRole"))


@login_required
@permission_required("list_role")
def ListRole(request):
    context = {"roles": Role.objects.all()}
    return render(request, "core/list_role.html", context)


@login_required
@permission_required("edit_role")
def editRole(request, role_id):

    if request.method == "GET":
        context = {
            "role": Role.objects.get(id=role_id),
            "permissions": Permissions.objects.all()
        }
        return render(request, 'core/edit_role.html', context=context)

    if request.method == "POST":
        role = Role.objects.get(id=role_id)
        role.name = request.POST["name"]
        role.permissions.clear()
        for each in request.POST.getlist('permissions'):
            role.permissions.add(Permissions.objects.get(id=each))
        role.save()
        return redirect(reverse("home:listRole"))
