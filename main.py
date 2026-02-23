# main.py
#一下三组为规则使用与解释
from agent.planner import plan_audit
#审计规则

from agent.sql_generator import AUDIT_SQL
#数据查询sql码

from agent.explainer import explain
#分析结果解释器


from agent.model_predictor import predict_risk
#模型评分模块

from db.executor import execute_sql
#数据库连接，字节处理

from db.feature_loader import load_features
#特征查询


from db.writer import (
    create_audit_batch,
    finish_audit_batch,
    write_abnormal_records,
    update_risk_score,
    write_causal_result,
    write_problem_cluster,
)
#1.插入
#2.更新数据库
#3.日志撰写
#4.在日志写入风险
#5.原因推理 audit_problem_cluster
#6.原因聚类 audit_decision_log


from db.report_loader import load_daily_stats
#信息汇总

from db.decision_logger import write_decision_log
#整体数据写入

from agent.report.daily_reporter import generate_daily_report
#日数据汇总


from reasoning.reasoner import infer_cause
#原因选择

from reasoning.cluster import cluster_by_route
#路线分类

from safety.main import safe_execute
#安全审查

from agent.decision.decider import make_decision
#决策系统

AGENT_VERSION = "v1.5"
MODEL_ID = "claim_risk_v1"


def run_audit():
    # =========================
    # 0️⃣ 创建审计批次
    # =========================
    batch_id = create_audit_batch(AGENT_VERSION)
    #数据源来源sql_generator AGENT_VERSION
    #函数来自writer
    #选取95的plan_delv_to_real_delv_diff 进入delay_extreme
    #筛选数组包含id和coldchain_flag
    #而且通过goods_category="fresh"和is_fresh_and_delv_promise=0
    #筛选新鲜的，却没有冷链的
    print(f"[INFO] Audit batch started: {batch_id}")
    #输出检查的次数
    write_decision_log(
        batch_id=batch_id,
        decision_type="SYSTEM",
        content="审计批次启动",
        related_key="system",
        agent_version=AGENT_VERSION,
    )
    #函数来源decision_logger
    #调整字符并在 agent_decision_log里面插入以下内容
    #batch_id,
    #decision_type,
    #rule_id,
    #related_key,
    #content,
    #confidence,
    #agent_version
    # =========================
    # 1️⃣ 执行规则审计
    # =========================
    for rule in plan_audit():
        #返还错误原因
        sql = AUDIT_SQL[rule["rule_id"]]
        #给出符号条件的大类
        _, rows = safe_execute(sql, execute_sql)
        #函数来源executor
        #数据库执行SQL查询、获取所有结果数据并提取列名的完整数据获取流程
        #安全测试
        msg = explain(rule, rows)
        #使用解释器
        print(msg)

        # 规则执行日志
        write_decision_log(
            batch_id=batch_id,
            decision_type="RULE",
            rule_id=rule["rule_id"],
            related_key="system",
            content=msg,
            agent_version=AGENT_VERSION,
        )
        #写入异常订单号
        #函数源来自db.decision_logger
        if not rows:
            continue

        # =========================
        # 2️⃣ 规则级异常落库
        # =========================
        write_abnormal_records(batch_id, rule, rows)
        #在audit_abnormal_records写入异常订单好
        # =========================
        # 3️⃣ 模型风险评分
        # =========================
        shipment_ids = [r[0] for r in rows]
        feature_rows = load_featres(shipment_ids)
        #来自db.feature_loader
        #查询变量特征
        scores = predict_risk(MODEL_ID, feature_rows)
        #评分
        for f, score in zip(feature_rows, scores):
            update_risk_score(batch_id, f["shipment_id"], score)

        # =========================
        # 4️⃣ 单订单因果推理
        # =========================

        for row in rows:
            record = {
                "shipment_id": row[0],
                rule["metric"]: row[1],
            }

            cause = infer_cause(rule["rule_id"], record)
            if cause:
                write_causal_result(
                    batch_id=batch_id,
                    rule_id=rule["rule_id"],
                    shipment_id=row[0],
                    cause=cause["cause"],
                    confidence=cause["confidence"],
                )

                write_decision_log(
                    batch_id=batch_id,
                    decision_type="CAUSE",
                    rule_id=rule["rule_id"],
                    related_key=str(row[0]),
                    content=f"推断原因：{cause['cause']}",
                    confidence=cause["confidence"],
                    agent_version=AGENT_VERSION,
                )

        # =========================
        # 5️⃣ 多异常联合推理（聚类）
        # =========================
        clusters = cluster_by_route(feature_rows)

        for key, items in clusters.items():
            if len(items) >= 3:
                write_problem_cluster(
                    batch_id=batch_id,
                    rule_id=rule["rule_id"],
                    cluster_key=key,
                    size=len(items),
                )

                write_decision_log(
                    batch_id=batch_id,
                    decision_type="CLUSTER",
                    rule_id=rule["rule_id"],
                    related_key=str(key),
                    content=f"检测到异常聚类：{key}，共 {len(items)} 单",
                    agent_version=AGENT_VERSION,
                )

    # =========================
    # 6️⃣ 生成数据库健康日报
    # =========================
    stats = load_daily_stats(batch_id)
    report = generate_daily_report(stats)
    print(report)

    write_decision_log(
        batch_id=batch_id,
        decision_type="SUMMARY",
        related_key="system",
        content=report,
        agent_version=AGENT_VERSION,
    )

    # =========================
    # 7️⃣ 决策层输出（是否人工介入）
    # =========================
    decision = make_decision(stats)

    write_decision_log(
        batch_id=batch_id,
        decision_type="DECISION",
        related_key="system",
        content=f"决策：{decision['decision']}｜原因：{decision['reason']}",
        confidence=decision.get("confidence"),
        agent_version=AGENT_VERSION,
    )

    print(f"\n🧠 决策结论：是否需要人工介入 → {decision['decision']}")
    print(f"原因：{decision['reason']}")

    # =========================
    # 8️⃣ 结束批次
    # =========================
    finish_audit_batch(batch_id)
    print(f"[INFO] Audit batch finished: {batch_id}")


if __name__ == "__main__":
    run_audit()
