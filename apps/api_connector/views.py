import random
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone


KPI_CONFIG = {
    'RTCH': [
        'Encours',
        'Duree_Veillissement',
        'Temps_Retouche',
        'Taux_Remplissage',
        'Consommation_RTCH',
        'NBR_ALT',
        'NBR_Accidents',
        'PDS_NOK_RTCH',
        'NBR_Machines_Panne',
        'NBR_Effectif',
        'NBR_Irritants_Sociaux',
        'Audits_5S',
        'Bloquages_Reactivite',
        'Bloquages_Ingenierie',
    ],
    'CONTROLE': [
        'DVX',
        'DPV',
        'NR_QCP',
        'iPPM',
        'BD_BuyOff',
        'Detection_Buyoff',
        'Detection_SCA',
        'DVR',
        'FRB00',
        'Veh_Bloque',
        'Post_it_Total',
        'Post_it_Recidives',
        'NBR_PDS',
        'Temps_Reactivite',
        'NBR_SPA_Fab',
    ],
    'REACTIVITE': [
        'DRR_Buyoff',
        'DPV_SCA_SPA',
        'Suivi_PACT',
        'Duree_Reactivite_Fournisseur',
        'NBR_Retard_PACT',
        'NBR_AMADEUS',
        'Total_Cost_AMADEUS',
        'Return_Cost_AMADEUS',
        'GAP_AMADEUS',
        'NBR_Plant_ALT',
        'Temps_Reactivite',
        'YH_Standby',
    ],
}


def generate_fake_value(kpi_type):
    ranges = {
        'Encours':                    (0.0, 5.0),
        'Duree_Veillissement':        (0.0, 3.0),
        'Temps_Retouche':             (0.0, 4.0),
        'Taux_Remplissage':           (0.0, 2.0),
        'Consommation_RTCH':          (0.0, 3.0),
        'NBR_ALT':                    (0.0, 2.0),
        'NBR_Accidents':              (0.0, 1.0),
        'PDS_NOK_RTCH':               (0.0, 2.0),
        'NBR_Machines_Panne':         (0.0, 2.0),
        'NBR_Effectif':               (0.0, 2.0),
        'NBR_Irritants_Sociaux':      (0.0, 2.0),
        'Audits_5S':                  (0.0, 2.0),
        'Bloquages_Reactivite':       (0.0, 2.0),
        'Bloquages_Ingenierie':       (0.0, 2.0),
        'DVX':                        (0.0, 3.0),
        'DPV':                        (0.0, 3.0),
        'NR_QCP':                     (0.0, 2.0),
        'iPPM':                       (0.0, 3.0),
        'BD_BuyOff':                  (0.0, 2.0),
        'Detection_Buyoff':           (0.0, 2.0),
        'Detection_SCA':              (0.0, 2.0),
        'DVR':                        (0.0, 2.0),
        'FRB00':                      (0.0, 2.0),
        'Veh_Bloque':                 (0.0, 2.0),
        'Post_it_Total':              (0.0, 2.0),
        'Post_it_Recidives':          (0.0, 2.0),
        'NBR_PDS':                    (0.0, 2.0),
        'Temps_Reactivite':           (0.0, 2.0),
        'NBR_SPA_Fab':                (0.0, 2.0),
        'DRR_Buyoff':                 (0.0, 2.0),
        'DPV_SCA_SPA':                (0.0, 2.0),
        'Suivi_PACT':                 (0.0, 2.0),
        'Duree_Reactivite_Fournisseur': (0.0, 2.0),
        'NBR_Retard_PACT':            (0.0, 2.0),
        'NBR_AMADEUS':                (0.0, 2.0),
        'Total_Cost_AMADEUS':         (0.0, 3.0),
        'Return_Cost_AMADEUS':        (0.0, 2.0),
        'GAP_AMADEUS':                (0.0, 2.0),
        'NBR_Plant_ALT':              (0.0, 2.0),
        'YH_Standby':                 (0.0, 2.0),
    }
    low, high = ranges.get(kpi_type, (0.0, 2.0))
    return round(random.uniform(low, high), 3)


def fake_kpi_data(request, zone_code):
    zone_code = zone_code.upper()
    kpi_types = KPI_CONFIG.get(zone_code, [])
    now = timezone.now()
    periode = now.date() - timedelta(days=1)
    data = []
    for kpi_type in kpi_types:
        data.append({
            'kpi_type':     kpi_type,
            'value':        generate_fake_value(kpi_type),
            'datetime':     now.strftime('%Y-%m-%d %H:%M:%S'),
            'periode_from': str(periode),
            'rsp':          zone_code,
        })
    return JsonResponse({'zone': zone_code, 'kpis': data})


def fake_kpi_single(request, zone_code, kpi_type):
    now = timezone.now()
    history = []
    for i in range(7):
        day = now.date() - timedelta(days=i)
        history.append({
            'kpi_type':     kpi_type.upper(),
            'value':        generate_fake_value(kpi_type),
            'datetime':     now.strftime('%Y-%m-%d %H:%M:%S'),
            'periode_from': str(day),
            'rsp':          zone_code.upper(),
        })
    return JsonResponse({
        'zone':     zone_code.upper(),
        'kpi_type': kpi_type.upper(),
        'history':  history,
    })


def fetch_kpis(zone_code):
    """
    Fetch KPIs from the API.
    In development: generates fake data directly.
    In production: will call the real Stellantis API.
    """
    try:
        zone_code = zone_code.upper()
        kpi_types = KPI_CONFIG.get(zone_code, [])
        now = timezone.now()
        periode = now.date() - timedelta(days=1)
        data = []
        for kpi_type in kpi_types:
            data.append({
                'kpi_type':     kpi_type,
                'value':        generate_fake_value(kpi_type),
                'datetime':     now.strftime('%Y-%m-%d %H:%M:%S'),
                'periode_from': str(periode),
                'rsp':          zone_code,
            })
        return data
    except Exception as e:
        print(f"API Error: {e}")
        return []