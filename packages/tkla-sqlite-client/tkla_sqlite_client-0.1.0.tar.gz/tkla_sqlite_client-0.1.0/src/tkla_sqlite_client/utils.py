def build_where_clause(conditions):
    if not conditions:
        return "", []
    clause = "WHERE " + " AND ".join([f"{k}=?" for k in conditions])
    values = list(conditions.values())
    return clause, values