import random
import json
import requests
from django.conf import settings
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone


KPI_CONFIG = {
    'QCP': ['DVX', 'DVT', 'DVM', 'SCA', 'DRR', 'BDACOM'],
    'PEI': ['KPI_A', 'KPI_B', 'KPI_C'],
    'MON': ['KPI_X', 'KPI_Y', 'KPI_Z'],
}


def generate_fake_value(kpi_type):
    ranges = {
        'DVX': (0.5, 3.5),
        'DVT': (0.8, 4.0),
        'DVM': (1.0, 5.0),
        'SCA': (0.1, 2.0),
        'DRR': (0.3, 2.5),
        'BDACOM': (0.5, 3.0),
    }
    low, high = ranges.get(kpi_type, (0.1, 10.0))
    return round(random.uniform(low, high), 3)


def fake_kpi_data(request, zone_code):
    zone_code = zone_code.upper()
    kpi_types = KPI_CONFIG.get(zone_code, ['KPI_GENERIC'])
    now = timezone.now()
    periode = now.date() - timedelta(days=1)
    data = []
    for kpi_type in kpi_types:
        data.append({
            'kpi_type': kpi_type,
            'value': generate_fake_value(kpi_type),
            'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
            'periode_from': str(periode),
            'rsp': zone_code,
        })
    return JsonResponse({'zone': zone_code, 'kpis': data})


def fake_kpi_single(request, zone_code, kpi_type):
    now = timezone.now()
    history = []
    for i in range(7):
        day = now.date() - timedelta(days=i)
        history.append({
            'kpi_type': kpi_type.upper(),
            'value': generate_fake_value(kpi_type.upper()),
            'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
            'periode_from': str(day),
            'rsp': zone_code.upper(),
        })
    return JsonResponse({
        'zone': zone_code.upper(),
        'kpi_type': kpi_type.upper(),
        'history': history
    })


def fetch_kpis(zone_code):
    """
    Fetch KPIs from the API.
    In development: generates fake data directly.
    In production: will call the real Stellantis API.
    """
    try:
        if settings.USE_FAKE_API:
            # Generate fake data directly — no HTTP call needed in dev
            zone_code = zone_code.upper()
            kpi_types = KPI_CONFIG.get(zone_code, ['KPI_GENERIC'])
            from django.utils import timezone
            now = timezone.now()
            periode = now.date() - timedelta(days=1)
            data = []
            for kpi_type in kpi_types:
                data.append({
                    'kpi_type': kpi_type,
                    'value': generate_fake_value(kpi_type),
                    'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
                    'periode_from': str(periode),
                    'rsp': zone_code,
                })
            return data
        else:
            # TODO: call real Stellantis API here
            pass
    except Exception as e:
        print(f"API Error: {e}")
        return []