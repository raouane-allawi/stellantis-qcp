from apps.api_connector.views import fetch_kpis
from apps.dashboard.views import build_kpis, get_status


def alerts_processor(request):
    if not request.user.is_authenticated:
        return {'alerts': [], 'alert_count': 0, 'user_zones': []}

    try:
        # User zones
        if request.user.is_admin:
            user_zones = ['RTCH', 'CONTROLE', 'REACTIVITE']
        else:
            user_zones = list(request.user.zone_access.values_list('code', flat=True))

        # Build alerts from all accessible zones
        alerts = []
        zone_labels = {
            'RTCH':       'RTCH',
            'CONTROLE':   'Contrôle',
            'REACTIVITE': 'Réactivité',
        }

        for zone_code in user_zones:
            kpis = build_kpis(zone_code)
            for kpi in kpis:
                if kpi['status'] != 'good':
                    alerts.append({
                        'name':   kpi['label'],
                        'value':  kpi['value'],
                        'target': kpi['target'],
                        'status': kpi['status'],
                        'zone':   zone_labels.get(zone_code, zone_code),
                    })

        return {
            'alerts':      alerts,
            'alert_count': len(alerts),
            'user_zones':  user_zones,
        }
    except Exception:
        return {'alerts': [], 'alert_count': 0, 'user_zones': []}