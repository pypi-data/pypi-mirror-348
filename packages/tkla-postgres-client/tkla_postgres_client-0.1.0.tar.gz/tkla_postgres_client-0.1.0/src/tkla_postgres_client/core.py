import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from .logger import logger
from .utils import build_where_clause, sanitize_column_list, sanitize_order_by

class PostgresClient:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = self._connect()

    def _connect(self):
        try:
            conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
            logger.info("Conexión a PostgreSQL establecida exitosamente.")
            return conn
        except Exception as e:
            logger.error("Error al conectar con PostgreSQL", exc_info=True)
            return None

    def _execute(self, query, values=None, commit=False):
        response = {"success": False, "data": [], "message": ""}
        if not self.connection:
            response["message"] = "Conexión no disponible."
            return response

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                if commit:
                    self.connection.commit()
                if cursor.description:
                    response["data"] = cursor.fetchall()
                response["success"] = True
                response["message"] = "Operación realizada con éxito."
        except Exception as e:
            self.connection.rollback()
            logger.error("Error durante la ejecución de la consulta", exc_info=True)
            response["message"] = str(e)
        return response

    def select_data(self, query_dict):
        try:
            for table, props in query_dict.items():
                columns = sanitize_column_list(props.get("columns"))
                where_clause, values = build_where_clause(props.get("conditions", {}))
                order = sanitize_order_by(props.get("order_by"))
                limit = sql.SQL(" LIMIT %s") if props.get("limit") else sql.SQL("")
                limit_val = [props["limit"]] if props.get("limit") else []

                query = sql.SQL("SELECT {fields} FROM {table} WHERE {where}{order}{limit}").format(
                    fields=columns,
                    table=sql.Identifier(table),
                    where=where_clause,
                    order=order,
                    limit=limit
                )
                return self._execute(query, values + limit_val)
        except Exception as e:
            logger.error("Error construyendo SELECT", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def insert_data(self, insert_dict):
        try:
            for table, data in insert_dict.items():
                columns = data.keys()
                values = list(data.values())
                placeholders = ["%s"] * len(values)

                query = sql.SQL("""
                    INSERT INTO {table} ({fields})
                    VALUES ({placeholders})
                    ON CONFLICT DO NOTHING
                    RETURNING *;
                """).format(
                    table=sql.Identifier(table),
                    fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                    placeholders=sql.SQL(", ").join(sql.SQL(p) for p in placeholders)
                )

                return self._execute(query, values, commit=True)
        except Exception as e:
            logger.error("Error construyendo INSERT", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def update_data(self, update_dict):
        try:
            for table, details in update_dict.items():
                values_dict = details.get("values", {})
                conditions = details.get("conditions", {})
                if not conditions:
                    return {"success": False, "data": [], "message": "Las condiciones son obligatorias para UPDATE."}

                set_clause = sql.SQL(", ").join([
                    sql.SQL("{} = %s").format(sql.Identifier(k)) for k in values_dict.keys()
                ])
                where_clause, where_values = build_where_clause(conditions)

                query = sql.SQL("UPDATE {table} SET {set} WHERE {where} RETURNING *;").format(
                    table=sql.Identifier(table),
                    set=set_clause,
                    where=where_clause
                )
                return self._execute(query, list(values_dict.values()) + where_values, commit=True)
        except Exception as e:
            logger.error("Error construyendo UPDATE", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def delete_data(self, delete_dict):
        try:
            for table, details in delete_dict.items():
                conditions = details.get("conditions", {})
                if not conditions:
                    return {"success": False, "data": [], "message": "Las condiciones son obligatorias para DELETE."}
                where_clause, values = build_where_clause(conditions)
                query = sql.SQL("DELETE FROM {table} WHERE {where} RETURNING *;").format(
                    table=sql.Identifier(table),
                    where=where_clause
                )
                return self._execute(query, values, commit=True)
        except Exception as e:
            logger.error("Error construyendo DELETE", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def exists(self, exists_dict):
        try:
            for table, details in exists_dict.items():
                conditions = details.get("conditions", {})
                if conditions:
                    where_clause, values = build_where_clause(conditions)
                    query = sql.SQL("SELECT 1 FROM {table} WHERE {where} LIMIT 1;").format(
                        table=sql.Identifier(table),
                        where=where_clause
                    )
                else:
                    query = sql.SQL("SELECT 1 FROM {table} LIMIT 1;").format(
                        table=sql.Identifier(table)
                    )
                    values = []
                result = self._execute(query, values)
                return bool(result["data"])
        except Exception as e:
            logger.error("Error en EXISTS", exc_info=True)
            return False

    def count(self, count_dict):
        try:
            for table, details in count_dict.items():
                conditions = details.get("conditions", {})
                if conditions:
                    where_clause, values = build_where_clause(conditions)
                    query = sql.SQL("SELECT COUNT(*) as total FROM {table} WHERE {where};").format(
                        table=sql.Identifier(table),
                        where=where_clause
                    )
                else:
                    query = sql.SQL("SELECT COUNT(*) as total FROM {table};").format(
                        table=sql.Identifier(table)
                    )
                    values = []
                result = self._execute(query, values)
                return result["data"][0]["total"] if result["success"] else 0
        except Exception as e:
            logger.error("Error en COUNT", exc_info=True)
            return 0

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Conexión a PostgreSQL cerrada.")