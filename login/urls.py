from django.urls import path,include
from . import views
from django.conf.urls import url

app_name = "home"
urlpatterns = [
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('register', views.Register, name='register'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    url(r'^resetPassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.passwordResetActivate, name='password_reset_confirm'),
    path('newPassword/<int:pk>', views.newPassword, name='newPassword'),
    path('changePassword/',views.changePassowrd, name="changePassowrd"),
    path('',views.Dashboard,name="dashboard"),
    path('addUser/', views.addUser, name="addUser"),
    path('listuser/', views.ListUser, name="listuser"),
    path('editUser/<int:user_id>/', views.editUser, name="editUser"),
    path('addRole/', views.addRole, name="addRole"),
    path('listRole/', views.ListRole, name="listRole"),
    path('editRole/<int:role_id>/', views.editRole, name="editRole"),

]

