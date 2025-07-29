from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PgAuditIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pg_audit.integrations.django"
    label = "pg_audit_django"
    verbose_name = "PostgreSQL Audit (pg_audit)"

    def ready(self):
        from .hooks import register_post_migrate_hook

        post_migrate.connect(register_post_migrate_hook, sender=self)
