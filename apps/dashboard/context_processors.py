from apps.api_connector.views import fetch_kpis


def alerts_processor(request):
    """Adds KPI alerts to every template context automatically."""
    if not request.user.is_authenticated:
        return {'alerts': [], 'alert_count': 0}

    try:
        raw_kpis = fetch_kpis('QCP')
        alerts = []
        for kpi in raw_kpis:
            name   = kpi.get('kpi_type', '')
            value  = kpi.get('value', 0)

            if value >= 0.5:
                status = 'warn' if value <= 1.0 else 'bad'
                alerts.append({
                    'name':   name,
                    'value':  value,
                    'target': 1.0,
                    'status': status,
                    'zone':   'QCP',
                })

        return {
            'alerts':      alerts,
            'alert_count': len(alerts),
        }
    except Exception:
        return {'alerts': [], 'alert_count': 0}