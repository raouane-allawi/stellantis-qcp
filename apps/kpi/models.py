from django.db import models
from django.conf import settings


class Zone(models.Model):

    class ZoneCode(models.TextChoices):
        QCP = 'QCP', 'QCP'
        PEI = 'PEI', 'PEI'
        FER = 'FER', 'FER'
        MON = 'MON', 'MON'

    name = models.CharField(max_length=100, verbose_name='Nom de la zone')
    code = models.CharField(
        max_length=10,
        choices=ZoneCode.choices,
        unique=True,
        verbose_name='Code RSP'
    )
    description = models.TextField(blank=True, verbose_name='Description')
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='zone_access',
        blank=True,
        verbose_name='Utilisateurs autorisés'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class KPIRecord(models.Model):

    class KPIType(models.TextChoices):
        DVX = 'DVX', 'DVX'
        DVT = 'DVT', 'DVT'
        DVM = 'DVM', 'DVM'
        SCA = 'SCA', 'SCA'
        DRR = 'DRR', 'DRR'
        BDACOM = 'BDACOM', 'BDACOM'
        UNKNOWN = 'UNKNOWN', 'Inconnu'

    class DataSource(models.TextChoices):
        FAKE_API = 'FAKE', 'Fake API (dev)'
        REAL_API = 'REAL', 'API réelle'
        MANUAL = 'MANUAL', 'Saisie manuelle'

    kkpi_type = models.CharField(
    max_length=50,
    verbose_name='Type KPI'
    # No choices= here — accepts any KPI name freely
)
    value = models.FloatField(verbose_name='Valeur')
    datetime_extraction = models.DateTimeField(
        verbose_name="Date d'extraction"
    )
    periode_from = models.DateField(
        verbose_name='Période (journée de production)'
    )
    rsp = models.CharField(max_length=10, verbose_name='RSP')
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        related_name='kpi_records',
        verbose_name='Zone'
    )
    source = models.CharField(
        max_length=10,
        choices=DataSource.choices,
        default=DataSource.FAKE_API,
        verbose_name='Source'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Enregistrement KPI'
        verbose_name_plural = 'Enregistrements KPI'
        ordering = ['-datetime_extraction']
        indexes = [
            models.Index(fields=['periode_from']),
            models.Index(fields=['datetime_extraction']),
        ]

    def __str__(self):
        return f"{self.kpi_type} = {self.value} ({self.periode_from})"


class KPIConfig(models.Model):

    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        related_name='kpi_configs'
    )
    kpi_type = models.CharField(max_length=20, choices=KPIRecord.KPIType.choices)
    target_value = models.FloatField(null=True, blank=True, verbose_name='Valeur cible')
    alert_threshold = models.FloatField(null=True, blank=True, verbose_name='Seuil alerte')
    unit = models.CharField(max_length=20, blank=True, verbose_name='Unité')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Configuration KPI'
        unique_together = ['zone', 'kpi_type']

    def __str__(self):
        return f"Config {self.kpi_type} — {self.zone}"


class AuditLog(models.Model):

    class ActionType(models.TextChoices):
        LOGIN = 'LOGIN', 'Connexion'
        LOGOUT = 'LOGOUT', 'Déconnexion'
        USER_CREATED = 'USER_CREATED', 'Utilisateur créé'
        USER_UPDATED = 'USER_UPDATED', 'Utilisateur modifié'
        USER_DELETED = 'USER_DELETED', 'Utilisateur supprimé'
        KPI_VIEWED = 'KPI_VIEWED', 'KPI consulté'
        KPI_EXPORTED = 'KPI_EXPORTED', 'KPI exporté'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=30, choices=ActionType.choices)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Log d'audit"
        verbose_name_plural = "Logs d'audit"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} — {self.action} ({self.timestamp})"