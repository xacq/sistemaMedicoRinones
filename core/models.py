from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ROLE_CHOICES = (
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    )
    name = models.CharField("Rol", max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username} - {self.role}"



class Patient(models.Model):
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)
    date_of_birth = models.DateField("Fecha de Nacimiento")
    gender = models.CharField("Género", max_length=10, choices=(('male','Masculino'),('female','Femenino'),('other','Otro')))
    contact = models.CharField("Contacto", max_length=200, blank=True)
    
    # Imágenes de ultrasonido de cada riñón (corte longitudinal)
    left_kidney_image = models.ImageField("Imagen del Riñón Izquierdo", upload_to='patient_images/', blank=True, null=True)
    right_kidney_image = models.ImageField("Imagen del Riñón Derecho", upload_to='patient_images/', blank=True, null=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
