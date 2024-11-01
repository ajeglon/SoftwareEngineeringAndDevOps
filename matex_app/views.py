from datetime import timedelta

from django.shortcuts import render, redirect
from .models import CertificateHolder, CertificateInfo
from .forms import CertificateHolderForm, CertificateInfoForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Succesfully logged in')
            return redirect('index')
        else:
            messages.success(request, 'There was an error loggin in, please try again')
            return redirect('index')
    else:
        return render(request, 'index.html', {})


def certificateholders(request):
    if request.user.is_authenticated:
        all_certificate_holders = CertificateHolder.objects.all()
        return render(request, 'certificate-holders.html', {'cert_holders': all_certificate_holders})
    else:
        messages.success(request, 'Please log in to view this page')
        return redirect('index')


def certificates(request):
    if request.user.is_authenticated:
        all_certificates = CertificateInfo.objects.all()
        return render(request, 'certificates.html', {'certs': all_certificates})
    else:
        messages.success(request, 'Please log in to view this page')
        return redirect('index')


def addholder(request):
    form = CertificateHolderForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_holder = form.save()
                messages.success(request, "Holder Added Successfully")
                return redirect('certificate-holders')
        return render(request, 'add-holder.html', {'form': form})
    else:
        messages.success(request, "Please log in to view this page")
        return redirect('index')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'User has been successfully registered')
            return redirect('index')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def holder_info(request, pk):
    if request.user.is_authenticated:
        holder_record = CertificateHolder.objects.get(id=pk)
        return render(request, 'holder-info.html', {'holder_record': holder_record})
    else:
        messages.success(request, 'Please log in to view this page')
        return redirect('index')


def delete_cert_holder(request, pk):
    if request.user.is_superuser:
        delete_info = CertificateHolder.objects.get(id=pk)
        delete_info.delete()
        messages.success(request, 'Certificate holder deleted successfully')
        return redirect('certificate-holders')
    else:
        messages.success(request, "Admin login required")
        return redirect('certificate-holders')


def update_cert_holder(request, pk):
    if request.user.is_authenticated:
        current_record = CertificateHolder.objects.get(id=pk)
        form = CertificateHolderForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate Holder updated successfully')
            return redirect('certificate-holders')
        return render(request, 'update-certificate-holder.html', {'form': form})
    else:
        messages.success(request, "Please login to update")
        return redirect('certificate-holders')


def certificate_info(request, pk):
    if request.user.is_authenticated:
        certificate_record = CertificateInfo.objects.get(certificate_number=pk)
        return render(request, 'certificate-info.html', {'certificate_record': certificate_record})
    else:
        messages.success(request, 'Please log in to view this page')
        return redirect('index')


def add_certificate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CertificateInfoForm(request.POST)
            if form.is_valid():
                certificate = form.save()
                messages.success(request, "Certificate Added Successfully")

                return redirect('certificates')
        else:
            form = CertificateInfoForm(request.POST)
        return render(request, 'add-certificate.html', {'form': form})
    else:
        messages.success(request, "Please log in to view this page")
        return redirect('index')


def delete_certificate(request, pk):
    if request.user.is_superuser:
        delete_cert = CertificateInfo.objects.get(certificate_number=pk)
        delete_cert.delete()
        messages.success(request, 'Certificate deleted successfully')
        return redirect('certificates')
    else:
        messages.success(request, "Admin login required")
        return redirect('certificates')


def update_certificate(request, pk):
    if request.user.is_authenticated:
        current_record = CertificateInfo.objects.get(certificate_number=pk)
        form = CertificateInfoForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate updated successfully')
            return redirect('certificates')
        return render(request, 'update-certificate.html', {'form': form})
    else:
        messages.success(request, "Please login to update")
        return redirect('certificates')
