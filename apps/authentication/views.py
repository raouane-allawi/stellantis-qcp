from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.kpi.models import AuditLog


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('backoffice:dashboard_view')
        return redirect('dashboard:home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action=AuditLog.ActionType.LOGIN,
                description=f"{user.username} s'est connecté",
                ip_address=request.META.get('REMOTE_ADDR'),
            )
            if user.is_admin:
                return redirect('backoffice:dashboard_view')
            return redirect('dashboard:home')
        else:
            error = "Matricule ou mot de passe incorrect."

    preview_kpis = [
        {'name': 'DVX',    'value': '0.324', 'trend': 'up',   'change': '+0.12'},
        {'name': 'DVT',    'value': '0.817', 'trend': 'down', 'change': '-0.05'},
        {'name': 'DVM',    'value': '0.943', 'trend': 'up',   'change': '+0.08'},
        {'name': 'SCA',    'value': '0.102', 'trend': 'up',   'change': '+0.03'},
        {'name': 'DRR',    'value': '0.587', 'trend': 'down', 'change': '-0.11'},
        {'name': 'BDACOM', 'value': '0.741', 'trend': 'up',   'change': '+0.22'},
    ]

    return render(request, 'authentication/login.html', {
        'error': error,
        'preview_kpis': preview_kpis,
    })


def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.ActionType.LOGOUT,
            description=f"{request.user.username} s'est déconnecté",
            ip_address=request.META.get('REMOTE_ADDR'),
        )
    logout(request)
    return redirect('auth:login')


def password_reset_view(request):
    return render(request, 'authentication/password_reset.html')


@login_required
def profile_view(request):
    success = None
    error   = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name  = request.POST.get('last_name', '')
            request.user.email      = request.POST.get('email', '')
            request.user.phone      = request.POST.get('phone', '')
            request.user.save()
            success = "Informations mises à jour avec succès."

        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm      = request.POST.get('confirm_password')

            if not request.user.check_password(old_password):
                error = "Mot de passe actuel incorrect."
            elif new_password != confirm:
                error = "Les nouveaux mots de passe ne correspondent pas."
            elif len(new_password) < 8:
                error = "Le mot de passe doit contenir au moins 8 caractères."
            else:
                request.user.set_password(new_password)
                request.user.save()
                user = authenticate(request,
                                    username=request.user.username,
                                    password=new_password)
                if user:
                    login(request, user)
                success = "Mot de passe changé avec succès."

    last_login = AuditLog.objects.filter(
        user=request.user,
        action=AuditLog.ActionType.LOGIN
    ).order_by('-timestamp').first()

    return render(request, 'authentication/profile.html', {
        'success':     success,
        'error':       error,
        'last_login':  last_login,
        'last_update': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
    })