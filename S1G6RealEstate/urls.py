"""S1G6RealEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from eproperty import views
from eproperty.views import logOut, DisplayDashboard, FeatureDelete, UserRole, ViewUsers, CreateUser, \
    UpdateUser, \
    UserEnable, UserDelete, ManagePermission, RoleDelete

urlpatterns = [
    # static pages
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('sell', views.sell, name='sell'),
    path('buy', views.buy, name='buy'),
    path('admin/', admin.site.urls, ),
    path('dashboard/', DisplayDashboard.as_view(), name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', logOut, name='logout'),

    # user pages
    path('users/', ViewUsers.as_view(), name='users'),
    path('users/add/', CreateUser.as_view(), name='createUser'),
    path('users/<int:pk>/', UpdateUser.as_view(), name='updateUser'),
    path('users/<int:pk>/enable-user/', UserEnable.as_view(), name='enableUser'),
    path('users/<int:pk>/delete-user/', UserDelete.as_view(), name='deleteUser'),

    # Roles

    path('roles/', views.all_roles, name='roles'),
    path('roles/new/', views.role, name='createRole'),
    path('roles/<int:pk>/permissions/', ManagePermission.as_view(), name='permissions'),
    path('roles/<int:pk>/delete-role/', RoleDelete.as_view(), name='deleteRole'),

    # features

    path('features/', views.all_features, name='features'),
    path('features/add/', views.feature, name='addFeatures'),
    path('features/<int:pk>/delete/', FeatureDelete.as_view(), name='deleteFeature')

]
