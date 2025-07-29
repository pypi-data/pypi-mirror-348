from psycopg2 import sql
from .logger import logger

def create_tables(schema_dict, client) -> dict:
    response = {"success": False, "message": ""}
    try:
        for table_name, columns in schema_dict.items():
            column_defs = []
            constraints = []

            for col_name, props in columns.items():
                col_type = props.get("data_type", "text").upper()
                length = props.get("length")
                nullable = props.get("nullable", True)
                default = props.get("default")
                primary_key = props.get("primary_key", False)
                unique = props.get("unique", False)
                comment = props.get("comment")
                foreign_key = props.get("foreign_key")

                type_def = sql.SQL(col_type + (f"({length})" if length else ""))

                parts = [sql.Identifier(col_name), type_def]

                if not nullable:
                    parts.append(sql.SQL("NOT NULL"))
                if default is not None:
                    parts.append(sql.SQL("DEFAULT %s"))
                if unique:
                    parts.append(sql.SQL("UNIQUE"))
                if primary_key:
                    parts.append(sql.SQL("PRIMARY KEY"))

                column_defs.append(sql.SQL(" ").join(parts))
                if foreign_key:
                    ref = foreign_key["reference"]
                    ref_table, ref_col = ref.split("(")
                    ref_col = ref_col.strip(")")
                    fk = sql.SQL("FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col})").format(
                        col=sql.Identifier(col_name),
                        ref_table=sql.Identifier(ref_table),
                        ref_col=sql.Identifier(ref_col)
                    )
                    constraints.append(fk)

            column_defs.append(sql.SQL("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
            all_defs = column_defs + constraints

            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({fields});").format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(all_defs)
            )

            values = [v for c in columns.values() if c.get("default") is not None for v in [c.get("default")]]
            result = client._execute(query, values, commit=True)
            if not result["success"]:
                return result

        response["success"] = True
        response["message"] = "Tablas creadas exitosamente."
    except Exception as e:
        logger.error("Error construyendo CREATE TABLE", exc_info=True)
        response["message"] = str(e)

    return response
