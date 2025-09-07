from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    fullname = forms.CharField(max_length=150, required=False, label='Full Name')
    address = forms.CharField(max_length=255, required=False, label='Address')
    phone = forms.CharField(max_length=20, required=False, label='Phone')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'fullname', 'address', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and helpful placeholders to all widgets for visibility
        placeholders = {
            'fullname': 'Jane Doe',
            'username': 'jane_doe',
            'email': 'jane@example.com',
            'address': '123 Main St, City',
            'phone': '+44 7700 900123',
            'password1': 'Create a password',
            'password2': 'Confirm your password',
        }
        for name, field in self.fields.items():
            if name == 'role':
                field.widget.attrs.update({'class': 'form-select'})
            else:
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs.update({'class': (existing + ' form-control').strip()})
            if name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[name])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.fullname = self.cleaned_data.get('fullname', '')
        user.address = self.cleaned_data.get('address', '')
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user

class RoleAuthenticationForm(AuthenticationForm):
    ROLE_CHOICES = [
        ('consumer', 'Consumer'),
        ('researcher', 'Researcher'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label='Role', widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        # Bootstrap styling on username/password
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def confirm_login_allowed(self, user):
        # First run default checks
        super().confirm_login_allowed(user)
        # Then enforce role matching
        selected_role = self.cleaned_data.get('role')
        if selected_role and getattr(user, 'role', None) != selected_role:
            raise forms.ValidationError('Selected role does not match your account role.', code='invalid_role')


