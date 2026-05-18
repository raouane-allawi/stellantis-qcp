from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.authentication.models import User
from apps.kpi.models import Zone, AuditLog


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('dashboard:zone1')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard_view(request):
    total_users = User.objects.count()
    total_zones = Zone.objects.count()
    recent_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
    return render(request, 'backoffice/dashboard.html', {
        'total_users': total_users,
        'total_zones': total_zones,
        'recent_logs': recent_logs,
    })


@admin_required
def users_list(request):
    users = User.objects.prefetch_related('zone_access').order_by('username')
    total = users.count()
    admins = users.filter(role=User.Role.ADMIN).count()
    supervisors = users.filter(role=User.Role.SUPERVISOR).count()
    operators = users.filter(role=User.Role.OPERATOR).count()
    return render(request, 'backoffice/users_list.html', {
        'users': users,
        'total': total,
        'admins': admins,
        'supervisors': supervisors,
        'operators': operators,
    })


@admin_required
def user_create(request):
    zones = Zone.objects.all()
    if request.method == 'POST':
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        role        = request.POST.get('role')
        password    = request.POST.get('password')
        employee_id = request.POST.get('employee_id')
        zone_ids    = request.POST.getlist('zones')

        user = User.objects.create_user(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
            password=password, role=role,
            employee_id=employee_id if employee_id else None,
        )
        user.zone_access.set(zone_ids)
        user.save()

        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.ActionType.USER_CREATED,
            description=f"Utilisateur {username} créé",
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return redirect('backoffice:users_list')

    return render(request, 'backoffice/user_form.html', {
        'zones': zones, 'action': 'create',
    })


@admin_required
def user_edit(request, pk):
    user  = get_object_or_404(User, pk=pk)
    zones = Zone.objects.all()

    if request.method == 'POST':
        user.first_name  = request.POST.get('first_name')
        user.last_name   = request.POST.get('last_name')
        user.email       = request.POST.get('email')
        user.role        = request.POST.get('role')
        user.employee_id = request.POST.get('employee_id') or None
        zone_ids         = request.POST.getlist('zones')
        user.zone_access.set(zone_ids)
        user.save()

        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.ActionType.USER_UPDATED,
            description=f"Utilisateur {user.username} modifié",
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return redirect('backoffice:users_list')

    return render(request, 'backoffice/user_form.html', {
        'user_obj': user, 'zones': zones, 'action': 'edit',
    })


@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.ActionType.USER_DELETED,
            description=f"Utilisateur {username} supprimé",
            ip_address=request.META.get('REMOTE_ADDR'),
        )
    return redirect('backoffice:users_list')


@admin_required
def zones_list(request):
    zones = Zone.objects.prefetch_related('users').all()
    return render(request, 'backoffice/zones_list.html', {'zones': zones})


@admin_required
def logs_list(request):
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    # ── Filters ──
    search    = request.GET.get('search', '').strip()
    action    = request.GET.get('action', '')
    date_from = request.GET.get('date_from', '')
    date_to   = request.GET.get('date_to', '')

    if search:
        logs = logs.filter(
            user__username__icontains=search
        ) | AuditLog.objects.filter(
            description__icontains=search
        ).order_by('-timestamp')

    if action:
        logs = logs.filter(action=action)

    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)

    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)

    # ── Pagination ──
    paginator   = Paginator(logs, 10)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    return render(request, 'backoffice/logs_list.html', {
        'logs':           page_obj,
        'page_obj':       page_obj,
        'paginator':      paginator,
        'search':         search,
        'action_filter':  action,
        'date_from':      date_from,
        'date_to':        date_to,
        'action_choices': AuditLog.ActionType.choices,
        'total_count':    paginator.count,
    })