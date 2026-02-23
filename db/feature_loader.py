# db/feature_loader.py

import psycopg

DB_CONFIG = dict(
    host="localhost",
    dbname="mydb",
    user="myuser",
    password="123456"
)

#特征查询
def load_features(shipment_ids: list):
    """
    从数据库加载模型所需特征
    """
    conn = psycopg.connect(**DB_CONFIG)

    sql = """
        SELECT
            shipment_id,
            plan_delv_to_real_delv_diff AS delay_hours,
            insured_amount,
            route_type,
            CASE WHEN goods_category = 'fresh' THEN 1 ELSE 0 END AS is_fresh
        FROM fact_shipment
        WHERE shipment_id = ANY(%s)
    """

    features = []
    with conn.cursor() as cur:
        cur.execute(sql, (shipment_ids,))
        for row in cur.fetchall():
            features.append({
                "shipment_id": row[0],
                "delay_hours": row[1],
                "insured_amount": row[2],
                "route_type": row[3],
                "is_fresh": row[4]
            })

    conn.close()
    return features
