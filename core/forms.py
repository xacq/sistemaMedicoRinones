# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class PatientForm(forms.ModelForm):
    """Para que use el doctor (incluye imágenes)"""
    class Meta:
        model = Patient
        fields = [
            'first_name','last_name','date_of_birth','gender',
            'contact','left_kidney_image','right_kidney_image'
        ]

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'contact']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ImagenForm(forms.Form):
    imagen = forms.ImageField(label='Subir imagen para análisis')