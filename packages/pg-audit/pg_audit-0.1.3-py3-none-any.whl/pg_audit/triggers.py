def generate_trigger_sql(
    table_name: str,
    audit_table: str = "auditlog",
    track_only: list[str] | None = None,
    exclude_fields: list[str] | None = None,
    log_conditions: str | None = None,
    meta_fields: list[str] | None = None,
) -> str:
    if track_only is not None and exclude_fields is not None:
        raise ValueError(
            f"Cannot specify both track_only and exclude_fields for table {table_name}"
        )

    if track_only is not None:
        ignored_keys = [f"'{k}'" for k in track_only]
        ignored_keys = "ARRAY[" + ", ".join(ignored_keys) + "]"
        # We want to ignore keys NOT in track_only
        ignored_keys_expr = f"(SELECT array_agg(key) FROM jsonb_object_keys(to_jsonb(NEW)) AS key(key) WHERE key.key NOT IN {ignored_keys})"
    elif exclude_fields is not None:
        ignored_keys = [f"'{k}'" for k in exclude_fields]
        ignored_keys_expr = f"ARRAY[{', '.join(ignored_keys)}]"
    else:
        ignored_keys_expr = "ARRAY[]::text[]"

    meta_fields_expr = ""
    if meta_fields:
        meta_fields_pairs = []
        for field in meta_fields:
            meta_fields_pairs.append(f"'{field}', to_jsonb(NEW.{field})")
        meta_fields_expr = ", " + ", ".join(meta_fields_pairs)

    log_conditions_expr = f"WHERE {log_conditions}" if log_conditions else ""

    sql = f"""
CREATE OR REPLACE FUNCTION audit_trigger() RETURNS trigger AS $$
DECLARE
    data JSONB;
    diff JSONB;
    ignored_keys TEXT[] := {ignored_keys_expr};
BEGIN
    IF (TG_OP = 'DELETE') THEN
        data = to_jsonb(OLD);
    ELSE
        data = to_jsonb(NEW);
    END IF;

    IF (TG_OP = 'UPDATE') THEN
        diff = jsonb_strip_nulls(
            jsonb_diff(to_jsonb(OLD), to_jsonb(NEW))
        );
        diff = diff - ignored_keys;
    ELSE
        diff = data - ignored_keys;
    END IF;

    IF TG_OP = 'UPDATE' AND diff = '{{}}'::jsonb THEN
        RETURN NULL;
    END IF;

    INSERT INTO {audit_table} (
        operation, changed_at, content_type_id, object_id, table_name,
        user_id, old_data, new_data, meta, request_id, change_reason, source
    )
    VALUES (
        TG_OP, now(), NULL, NULL, TG_TABLE_NAME,
        NULL, 
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('UPDATE', 'INSERT') THEN to_jsonb(NEW) ELSE NULL END,
        jsonb_build_object({meta_fields_expr}),
        current_setting('session.myapp_request_id', true),
        current_setting('session.myapp_change_reason', true),
        current_setting('session.myapp_source', true)
    );

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_trigger ON {table_name};

CREATE TRIGGER audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON {table_name}
FOR EACH ROW EXECUTE FUNCTION audit_trigger();
{log_conditions_expr}
"""
    return sql.strip()
