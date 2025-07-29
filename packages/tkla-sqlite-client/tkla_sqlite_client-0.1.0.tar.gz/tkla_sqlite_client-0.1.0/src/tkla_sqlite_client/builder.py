from .logger import logger

def create_tables(schema_dict, client):
    try:
        for table, fields in schema_dict.items():
            columns_sql = []
            for name, props in fields.items():
                col_type = props.get("data_type", "TEXT").upper()
                length = props.get("length")
                nullable = "NOT NULL" if not props.get("nullable", True) else ""
                default = f"DEFAULT '{props['default']}'" if "default" in props else ""
                primary = "PRIMARY KEY" if props.get("primary_key") else ""
                unique = "UNIQUE" if props.get("unique") else ""

                type_def = f"{col_type}({length})" if col_type == "VARCHAR" and length else col_type
                col_def = f"{name} {type_def} {primary} {unique} {nullable} {default}".strip()
                columns_sql.append(col_def)

            columns_sql.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns_sql)});"
            client._execute(sql, commit=True)
        return {"success": True, "message": "Tablas creadas exitosamente."}
    except Exception as e:
        logger.error("Error al crear tablas", exc_info=True)
        return {"success": False, "message": str(e)}