import sqlite3
import json
from .logger import logger
from .utils import build_where_clause

class SQLiteClient:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = self._connect()

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            logger.info("Conexión a SQLite establecida.")
            return conn
        except Exception as e:
            logger.error("Error al conectar con SQLite", exc_info=True)
            return None

    def _execute(self, query, values=None, commit=False):
        response = {"success": False, "data": [], "message": ""}
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values or [])
            if commit:
                self.connection.commit()
            if cursor.description:
                response["data"] = [dict(row) for row in cursor.fetchall()]
            response["success"] = True
            response["message"] = "Operación realizada con éxito."
        except Exception as e:
            self.connection.rollback()
            logger.error("Error en ejecución SQLite", exc_info=True)
            response["message"] = str(e)
        return response

    def select_data(self, query_dict):
        try:
            for table, props in query_dict.items():
                columns = ", ".join(props.get("columns", ["*"]))
                where_clause, values = build_where_clause(props.get("conditions", {}))
                order_by = " ORDER BY " + ", ".join(props["order_by"]) if "order_by" in props else ""
                limit = f" LIMIT {props['limit']}" if "limit" in props else ""
                query = f"SELECT {columns} FROM {table} {where_clause}{order_by}{limit};"
                return self._execute(query, values)
        except Exception as e:
            logger.error("Error construyendo SELECT", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def insert_data(self, insert_dict):
        try:
            for table, data in insert_dict.items():
                columns = ", ".join(data.keys())
                placeholders = ", ".join(["?"] * len(data))
                values = list(data.values())
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
                return self._execute(query, values, commit=True)
        except Exception as e:
            logger.error("Error en INSERT", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def update_data(self, update_dict):
        try:
            for table, props in update_dict.items():
                values_dict = props.get("values", {})
                conditions = props.get("conditions", {})
                if not conditions:
                    return {"success": False, "data": [], "message": "Condiciones obligatorias para UPDATE."}
                set_clause = ", ".join([f"{k}=?" for k in values_dict])
                where_clause, where_vals = build_where_clause(conditions)
                query = f"UPDATE {table} SET {set_clause} {where_clause};"
                return self._execute(query, list(values_dict.values()) + where_vals, commit=True)
        except Exception as e:
            logger.error("Error en UPDATE", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def delete_data(self, delete_dict):
        try:
            for table, props in delete_dict.items():
                conditions = props.get("conditions", {})
                if not conditions:
                    return {"success": False, "data": [], "message": "Condiciones obligatorias para DELETE."}
                where_clause, values = build_where_clause(conditions)
                query = f"DELETE FROM {table} {where_clause};"
                return self._execute(query, values, commit=True)
        except Exception as e:
            logger.error("Error en DELETE", exc_info=True)
            return {"success": False, "data": [], "message": str(e)}

    def exists(self, exists_dict):
        try:
            for table, props in exists_dict.items():
                conditions = props.get("conditions", {})
                where_clause, values = build_where_clause(conditions)
                query = f"SELECT 1 FROM {table} {where_clause} LIMIT 1;"
                result = self._execute(query, values)
                return bool(result["data"])
        except Exception as e:
            logger.error("Error en EXISTS", exc_info=True)
            return False

    def count(self, count_dict):
        try:
            for table, props in count_dict.items():
                conditions = props.get("conditions", {})
                if conditions:
                    where_clause, values = build_where_clause(conditions)
                    query = f"SELECT COUNT(*) as total FROM {table} {where_clause};"
                else:
                    query = f"SELECT COUNT(*) as total FROM {table};"
                    values = []
                result = self._execute(query, values)
                return result["data"][0]["total"] if result["success"] else 0
        except Exception as e:
            logger.error("Error en COUNT", exc_info=True)
            return 0

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Conexión SQLite cerrada.")