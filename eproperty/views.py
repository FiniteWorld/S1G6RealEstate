from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms.access_form import *
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms.access_form import CreateUser1, CreateUser2


# Create your views here.

def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def buy(request):
    return render(request, 'pages/buy.html')


def sell(request):
    return render(request, 'pages/sell.html')


def contact(request):
    return render(request, 'pages/contactus.html')


class DisplayDashboard(TemplateView):
    template_name = 'pages/admin_dashboard.html'


def login(request):
    if request.method == "POST" :
        form = CreateUser2(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['userName']
            password = form.cleaned_data['password']
            if User.objects.filter(userName=userName).filter(password=password):
                return redirect('index')
            else:
                return render(request, 'pages/signUp.html',
                              {'error_message': 'Wrong Login Credentials. Please verify!'})
    else:
        form = CreateUser2()
    return render(request, 'pages/index.html', {'form': form, 'error': None})


class Login(View):
    template_name = 'login.html'

    def post(self, request):

        username = request.POST.get('userName')
        password = request.POST.get('encryptedPassword')

        if User.objects.filter(userName__exact=username):

            if Password.objects.filter(password__encryptedPassword__exact=password):
                return redirect('pages/index.html')

        else:
            return render(request, self.template_name, {'error_message': 'Wrong Login Credentials. Please verify!'})


def logOut(request):
    return render(request, 'pages/index.html')


def all_features(request):
    return render(request, 'pages/list_feature.html',
                  {'title': 'Manage Features',
                   'features': Permission.objects.all()})


def feature(request):
    p = Permission()
    if request.method == 'POST':
        form = Feature(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('features')
    else:
        form = Feature(instance=p)
    return render(request, 'pages/feature.html',
                  {'title': 'Add Feature',
                   'form': form})


class FeatureDelete(DeleteView):
    model = Permission
    template_name = 'pages/delete_feature.html'
    success_url = 'features'


def all_roles(request):
    return render(request, 'pages/list_role.html',
                  {'title': 'Manage Roles',
                   'roles': Role.objects.all()})


def role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            return redirect('roles')
    else:
        form = RoleForm(instance=Role)
    return render(request, 'pages/role.html',
                  {'title': 'Add Role',
                   'form': form})


class ManagePermission(FormView):
    template_name = 'pages/manage_permission.html'
    success_url = 'roles'

    def get(self, request, *args, **kwargs):
        roleid = Role.objects.get(pk=self.kwargs['pk'])
        role_permissions = RolePermission.objects.filter(role=roleid)
        form = ManagePermissions(initial={'features': [a.permission_id for a in role_permissions]}) \
            if any(role_permissions) else ManagePermissions()
        return render(request, self.template_name, {'role': roleid, 'form': form})

    def post(self, request, *args, **kwargs):
        roleid = Role.objects.get(pk=self.kwargs['pk'])
        form = ManagePermissions(request.POST)
        selected_features = request.POST.getlist('features')
        form.save(role, selected_features)
        return HttpResponseRedirect(self.success_url)


class RoleDelete(DeleteView):
    model = Role
    template_name = 'pages/delete_role.html'
    success_url = 'roles'


class ViewUsers(ListView):
    model = User
    template_name = 'pages/list_user.html'
    context_object_name = 'users'


class CreateUser(CreateView):
    model = User
    form_class = CreateUser1
    template_name = 'pages/user.html'
    success_url = 'users'

    def get_success_url(self):
        return self.success_url


class UpdateUser(UpdateView):
    model = User
    form_class = UpdateUser
    template_name = 'pages/user.html'
    success_url = 'users'

    def get_form(self, form_class=form_class):
        form = super(UpdateUser, self).get_form(form_class)
        username = form.instance.username
        profile = User.objects.get(user__username=username)
        form.fields['account_expiry_date'].initial = profile.account_expiry_date
        return form


class UserDelete(DeleteView):
    model = User
    template_name = 'pages/delete_user.html'
    success_url = 'users'


class UserEnable(FormView):
    template_name = 'pages/enable.html'
    success_url = 'users'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        text = 'disable' if user.is_active else 'enable'
        return render(request, self.template_name, {'user': user, 'text': text})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.is_active = not user.is_active
        user.save()
        return HttpResponseRedirect(self.success_url)


class AssignRole(FormView):
    template_name = 'pages/assign_role.html'
    success_url = 'users'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        user_roles = UserRole.objects.filter(user=user)
        form = AssignRole(initial={'roles': [a.role_id for a in user_roles]}) if any(
            user_roles) else AssignRole()
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        form = AssignRole(request.POST)
        selected_roles = request.POST.getlist('roles')
        form.save(user, selected_roles)
        return HttpResponseRedirect(self.success_url)
