AUDIT_SQL = {

    "delay_extreme": """
        WITH p AS (
            SELECT percentile_cont(0.95::double precision)
                   WITHIN GROUP (ORDER BY plan_delv_to_real_delv_diff::double precision) AS p95
            FROM shipments
        )
        SELECT
            id,
            plan_delv_to_real_delv_diff AS delay_hours
        FROM shipments, p
        WHERE plan_delv_to_real_delv_diff::double precision > p.p95
    """,

    "fresh_without_coldchain": """
        SELECT
            id,
            is_fresh_and_delv_promise AS coldchain_flag
        FROM shipments
        WHERE goods_category = 'fresh'
          AND is_fresh_and_delv_promise::integer = 0
    """
}
