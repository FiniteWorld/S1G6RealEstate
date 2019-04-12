from django.forms import Form, ModelForm, TextInput, EmailInput, DateInput, DateField, PasswordInput, \
    ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from ..models import User, Role, Permission, User, UserRole, RolePermission
from django import forms

class CreateUser2(forms.Form):
    userName = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CreateUser1(ModelForm):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'userName']
        widgets = {
            'firstName': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'lastName': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'userName': TextInput(attrs={'class': 'input', 'placeholder': 'User Name'}),
            'password': PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})
        }

    def is_valid(self):

        valid = super(CreateUser1, self).is_valid()
        if not valid:
            return valid

        # Duplicate Username & Email check
        try:
            user = User.objects.get(email=self.cleaned_data['email'])

            if user is not None:
                self.add_error('email', 'Email Already Exists!')
                return False

        except User.DoesNotExist:
            pass

        return True

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['userName'], self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        user.last_name = self.cleaned_data['lastName']
        user.first_name = self.cleaned_data['firstName']
        user.save()
        profile = User(user=user)
        profile.save()
        return user


class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'userName']
        widgets = {
            'firstName': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'lastName': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'userName': TextInput(attrs={'class': 'input', 'placeholder': 'User Name', 'readonly': 'readonly'})
        }

    def save(self, commit=True):
        user = super(UpdateUser, self).save(commit)
        return user


class AssignRole(Form):
    roles = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), queryset=Role.objects.all())

    def save(self, user, selected_roles):
        user_roles = UserRole.objects.filter(user=user)
        for role in user_roles:
            if role.role_id not in selected_roles:
                role.delete()

        for role_id in selected_roles:
            if role_id not in [a.role_id for a in user_roles]:
                ur = UserRole(user=user, role_id=role_id)
                ur.save()


class ManagePermissions(Form):
    features = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), queryset=Permission.objects.all())

    def save(self, role, selected_features):
        role_permissions = RolePermission.objects.filter(role=role)
        for permission in role_permissions:
            if permission.permission_id not in selected_features:
                permission.delete()

        for permission_id in selected_features:
            if permission_id not in [a.permission_id for a in role_permissions]:
                ur = RolePermission(role=role, permission_id=permission_id)
                ur.save()


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name']


class Feature(ModelForm):
    class Meta:
        model = Permission
        fields = ['sysFeature']
