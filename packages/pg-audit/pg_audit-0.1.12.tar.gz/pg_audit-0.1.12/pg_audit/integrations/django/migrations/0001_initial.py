from django.db import migrations

from pg_audit.integrations.django.settings import audit_settings
from pg_audit.schema import (
    generate_auditlog_table_sql,
    generate_auditlog_partitions_sql,
    generate_jsonb_diff_function_sql,
)


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="\n\n".join([
                generate_auditlog_table_sql(audit_settings.table_name),
                generate_jsonb_diff_function_sql(),
                generate_auditlog_partitions_sql(audit_settings.table_name, months_ahead=3),
            ]),
            reverse_sql=f"DROP TABLE IF EXISTS {audit_settings.table_name} CASCADE;",
        ),
    ]
