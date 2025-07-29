from django.db import migrations

from pg_audit.integrations.django.settings import audit_settings
from pg_audit.schema import generate_auditlog_table_sql


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql=generate_auditlog_table_sql(audit_settings.table_name),
            reverse_sql=f"DROP TABLE IF EXISTS {audit_settings.table_name} CASCADE;",
        ),
    ]
