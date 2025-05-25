from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .forms import RegistrationForm, PatientForm
from .models import Patient, Profile, Role
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PatientProfileForm  # Asegúrate de tener este formulario definido
from .models import Patient  # Asegúrate de tener este modelo definido
from .forms import PatientProfileForm

@login_required
def patient_profile_edit(request):
    # Intentamos recuperar el paciente de este usuario
    patient = Patient.objects.filter(created_by=request.user).first()
    if not patient:
        # Si aún no existe, mostramos el formulario vacío para crearlo
        # (o podrías bloquear esta ruta si prefieres que sólo el doctor cree el perfil)
        form = PatientProfileForm(request.POST or None)
    else:
        # Si existe, lo editamos
        form = PatientProfileForm(request.POST or None, request.FILES or None, instance=patient)

    if request.method == 'POST' and form.is_valid():
        new_patient = form.save(commit=False)
        if not patient:
            new_patient.created_by = request.user
        new_patient.save()
        return redirect('dashboard_patient')

    return render(request, 'core/patient_profile_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            # Asignar grupo según el rol elegido (medico o usuario)
            role = form.cleaned_data.get('role')
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required
def patient_list(request):
    patients = Patient.objects.all()  # Se puede filtrar según el usuario o rol
    return render(request, 'core/patient_list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'core/patient_detail.html', {'patient': patient})


@login_required
def patient_create(request):
    if request.user.profile.role.name != 'medico':
        return redirect('dashboard')  # o mostrar “Acceso denegado”
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'core/patient_form.html', {'form': form})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'core/patient_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            # Obtener el rol seleccionado y crear el perfil
            selected_role = form.cleaned_data.get('role')
            role_instance, created = Role.objects.get_or_create(name=selected_role)
            Profile.objects.create(user=user, role=role_instance)

            login(request, user)
            return redirect('dashboard')  # Aquí podrías redirigir a la vista según el rol
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Se asume que el usuario ya tiene un perfil asociado
    profile = request.user.profile

    if profile.role.name == 'medico':
        # Redirigir o renderizar el dashboard para médicos
        return render(request, 'core/dashboard.html', {
            # Variables para el dashboard del médico
        })
    elif profile.role.name == 'paciente':
        # Redirigir al dashboard del paciente
        return redirect('dashboard_patient')


@login_required
def dashboard_patient(request):
    # Aquí puedes agregar la lógica y las variables específicas para el dashboard del paciente
    return render(request, 'core/dashboard_patient.html', {})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def patient_history(request):
    # Aquí obtén el historial de exámenes del paciente actual.
    # Por ejemplo, asumiendo que tienes un modelo Exam o similar:
    # history_exams = Exam.objects.filter(patient=request.user.profile)
    # En este ejemplo usaremos una lista vacía para ilustrar.
    history_exams = []  
    return render(request, 'core/patient_history.html', {'history_exams': history_exams})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def patient_results(request):
    # Aquí debes obtener los resultados de diagnóstico del paciente.
    # Por ejemplo, si tienes un modelo "Result" que almacena los diagnósticos:
    # results = Result.objects.filter(patient=request.user.profile)
    # En este ejemplo usaremos una lista vacía como placeholder.
    results = []
    return render(request, 'core/patient_results.html', {'results': results})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def patient_exam_detail(request, pk):
    # Suponiendo que tienes un modelo Exam para almacenar los detalles de un examen,
    # descomenta y ajusta la siguiente línea:
    # exam = get_object_or_404(Exam, pk=pk)
    
    # Para fines de demostración, usaremos datos de ejemplo:
    exam = {
        'id': pk,
        'date': '2025-03-23',
        'exam_type': 'Ultrasonido renal',
        'result': 'Normal',
        'notes': 'Sin hallazgos patológicos.'
    }
    
    return render(request, 'core/patient_exam_detail.html', {'exam': exam})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def patient_result_detail(request, pk):
    # Suponiendo que eventualmente tendrás un modelo Result, podrías obtener el resultado así:
    # result = get_object_or_404(Result, pk=pk)
    # Por ahora, usaremos un diccionario de ejemplo:
    result = {
        'id': pk,
        'date': '2025-03-24',
        'description': 'Diagnóstico: Litiasis renal',
        'status': 'Atención requerida',
        'notes': 'Se observan anomalías en la ecografía del riñón derecho.'
    }
    return render(request, 'core/patient_result_detail.html', {'result': result})
