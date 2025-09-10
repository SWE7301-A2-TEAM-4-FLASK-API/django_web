from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            placeholders = {
                'username': 'Enter your username',
                'email': 'Enter your email address',
                'password1': 'Enter your password',
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'role']  # Add/remove fields as needed


