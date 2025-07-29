from psycopg2 import sql

def dict_keys_to_sql_identifiers(data_dict):
    return [sql.Identifier(k) for k in data_dict.keys()]

def dict_values_to_sql_literals(data_dict):
    return [sql.Literal(v) for v in data_dict.values()]

def build_where_clause(conditions):
    clauses = []
    values = []
    for key, value in conditions.items():
        clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
        values.append(value)
    return sql.SQL(" AND ").join(clauses), values

def sanitize_column_list(columns):
    if not columns:
        return sql.SQL("*")
    return sql.SQL(", ").join([sql.Identifier(col) for col in columns])

def sanitize_order_by(order_by):
    if not order_by:
        return sql.SQL("")
    return sql.SQL(" ORDER BY ") + sql.SQL(", ").join(sql.SQL(o) for o in order_by)