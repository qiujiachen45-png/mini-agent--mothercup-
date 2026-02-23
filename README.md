基于python对于物流数据审计智能体
这是一个物流数据审计agent，按照业务逻辑审理物流数据，输出异常点报告。
根据业务语境制定审计规则，而且其输出的审计结果具备可解释性。

现有情形下，物流数据审计主要依赖人工完成数据清洗与规则判断。该模式在小规模、低频次场景下尚可运作，但在面对大范围、高频次的审计需求时，人工流程在覆盖能力、稳定性与一致性上均存在明显局限，难以支持持续性的审计执行。
本系统通过构建物流数据审计 agent，将数据清理、业务规则执行与异常判定流程进行统一整合，实现对大规模物流数据的自动化审计。系统审计逻辑紧密贴合实际业务语境，能够在保证结论可追溯、可解释的前提下，稳定执行复杂审计规则，具备良好的工程落地价值。

针对上述情况，本系统通过构建物流数据审计 Agent，将数据清洗、规则执行和异常判断等流程集成到程序中，实现对物流数据的自动化审计。系统根据物流业务的实际情况设定审计规则，并在发现异常时给出明确的判断依据，使审计结果具有一定的可解释性，便于理解和后续分析。

总体来看，该系统能够在减少人工工作量的同时，对大规模物流数据进行稳定、持续的审计，具有一定的实用价值和学习意义

其输出结果也可以通过和sql连接进行powerbi可视化。

代码运行要提取配置sql库
将Mathorcup的物流项目数据提前写进sql库，网址为https://www.saikr.com/c/nd/34795 

                                                                                                                                                                         
 架构模式 |          名称          |  类型  | 拥有者
----------+------------------------+--------+--------
 public   | agent_decision_log     | 数据表 | myuser
 public   | audit_abnormal_records | 数据表 | myuser
 public   | audit_batch            | 数据表 | myuser
 public   | audit_causal_result    | 数据表 | myuser
 public   | audit_causal_results   | 数据表 | myuser
 public   | audit_decision_log     | 数据表 | myuser
 public   | audit_problem_cluster  | 数据表 | myuser
 public   | dim_product            | 数据表 | myuser                                                                                                                               
 public   | fact_complaint         | 数据表 | myuser                                                                                                                               
 public   | fact_shipment          | 数据表 | myuser                                                                                                                               
 public   | fact_shipment_cleaned  | 数据表 | myuser                                                                                                                               
 public   | feature_node_stats     | 数据表 | myuser                                                                                                                               
 public   | shipments              | 数据表 | myuser                                                                                                                               
 public   | shipments2             | 数据表 | myuser 

每个库为一下结构
 table_schema |       table_name       |           column_name           |          data_type          | is_nullable |                      column_default                         
--------------+------------------------+---------------------------------+-----------------------------+-------------+-----------------------------------------------------------   
 public       | agent_decision_log     | id                              | integer                     | NO          | nextval('agent_decision_log_id_seq'::regclass)
 public       | agent_decision_log     | batch_id                        | integer                     | NO          |
 public       | agent_decision_log     | event_time                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP
 public       | agent_decision_log     | decision_type                   | character varying           | YES         |
 public       | agent_decision_log     | rule_id                         | character varying           | YES         |
 public       | agent_decision_log     | related_key                     | character varying           | YES         |
 public       | agent_decision_log     | content                         | text                        | YES         |
 public       | agent_decision_log     | confidence                      | numeric                     | YES         |
 public       | agent_decision_log     | agent_version                   | character varying           | YES         |                                                             
 public       | audit_abnormal_records | batch_id                        | bigint                      | YES         |                                                             
 public       | audit_abnormal_records | rule_id                         | text                        | YES         |                                                             
 public       | audit_abnormal_records | rule_desc                       | text                        | YES         |                                                             
 public       | audit_abnormal_records | shipment_id                     | bigint                      | YES         |                                                             
 public       | audit_abnormal_records | metric_name                     | text                        | YES         |                                                             
 public       | audit_abnormal_records | metric_value                    | double precision            | YES         |                                                             
 public       | audit_abnormal_records | detected_at                     | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | audit_abnormal_records | risk_score                      | double precision            | YES         |                                                             
 public       | audit_batch            | batch_id                        | bigint                      | NO          | nextval('audit_batch_batch_id_seq'::regclass)               
 public       | audit_batch            | started_at                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | audit_batch            | finished_at                     | timestamp without time zone | YES         |                                                             
 public       | audit_batch            | agent_version                   | text                        | YES         |                                                             
 public       | audit_causal_result    | causal_id                       | bigint                      | NO          | nextval('audit_causal_result_causal_id_seq'::regclass)      
 public       | audit_causal_result    | batch_id                        | bigint                      | YES         |                                                             
 public       | audit_causal_result    | shipment_id                     | bigint                      | YES         |                                                             
 public       | audit_causal_result    | rule_id                         | text                        | YES         |                                                             
 public       | audit_causal_result    | inferred_cause                  | text                        | YES         |                                                             
 public       | audit_causal_result    | confidence                      | numeric                     | YES         |                                                             
 public       | audit_causal_result    | created_at                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | audit_causal_results   | id                              | integer                     | NO          | nextval('audit_causal_results_id_seq'::regclass)            
 public       | audit_causal_results   | batch_id                        | integer                     | NO          |                                                             
 public       | audit_causal_results   | rule_id                         | text                        | NO          |                                                             
 public       | audit_causal_results   | shipment_id                     | bigint                      | NO          |                                                             
 public       | audit_causal_results   | cause                           | text                        | NO          |                                                             
 public       | audit_causal_results   | confidence                      | double precision            | YES         |                                                             
 public       | audit_causal_results   | created_at                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | audit_decision_log     | id                              | integer                     | NO          | nextval('audit_decision_log_id_seq'::regclass)              
 public       | audit_decision_log     | batch_id                        | integer                     | NO          |                                                             
 public       | audit_decision_log     | decision                        | text                        | NO          |                                                             
 public       | audit_decision_log     | reason                          | text                        | NO          |                                                             
 public       | audit_decision_log     | signal                          | jsonb                       | YES         |                                                             
 public       | audit_decision_log     | created_at                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | audit_problem_cluster  | cluster_id                      | bigint                      | NO          | nextval('audit_problem_cluster_cluster_id_seq'::regclass)   
 public       | audit_problem_cluster  | batch_id                        | bigint                      | YES         |                                                             
 public       | audit_problem_cluster  | rule_id                         | text                        | YES         |                                                             
 public       | audit_problem_cluster  | cluster_key                     | text                        | YES         |                                                             
 public       | audit_problem_cluster  | shipment_count                  | integer                     | YES         |                                                             
 public       | audit_problem_cluster  | created_at                      | timestamp without time zone | YES         | CURRENT_TIMESTAMP                                           
 public       | dim_product            | goods_category                  | text                        | YES         |                                                             
 public       | dim_product            | goods_level                     | text                        | YES         |                                                             
 public       | fact_complaint         | source                          | text                        | YES         |                                                             
 public       | fact_complaint         | real_delv_to_case_create_diff   | text                        | YES         |                                                             
 public       | fact_complaint         | customer_role                   | text                        | YES         |                                                             
 public       | fact_complaint         | bc_source                       | text                        | YES         |                                                             
 public       | fact_shipment          | route_type                      | text                        | YES         |                                                             
 public       | fact_shipment          | is_customer_to_customer         | boolean                     | YES         |                                                             
 public       | fact_shipment          | is_fresh_and_delv_promise       | boolean                     | YES         |                                                             
 public       | fact_shipment          | waybill_price_protect_money     | text                        | YES         |                                                             
 public       | fact_shipment          | start_city_id                   | text                        | YES         |                                                             
 public       | fact_shipment          | end_city_id                     | text                        | YES         |                                                             
 public       | fact_shipment          | consigner_id                    | text                        | YES         |                                                             
 public       | fact_shipment          | receiver_id                     | text                        | YES         |                                                             
 public       | fact_shipment          | is_staff                        | boolean                     | YES         |                                                             
 public       | fact_shipment          | plan_delv_to_real_delv_diff     | text                        | YES         |                                                             
 public       | fact_shipment          | abnormal_reason                 | text                        | YES         |                                                             
 public       | fact_shipment          | payment_contract_money          | text                        | YES         |                                                             
 public       | fact_shipment          | payment_real_money              | double precision            | YES         |                                                             
 public       | fact_shipment          | delay_group                     | text                        | YES         |                                                             
 public       | fact_shipment          | business_mode                   | text                        | YES         |                                                             
 public       | fact_shipment_cleaned  | start_city_id                   | text                        | YES         |                                                             
 public       | fact_shipment_cleaned  | plan_delv_to_real_delv_diff     | text                        | YES         |                                                             
 public       | fact_shipment_cleaned  | delay_days                      | bigint                      | YES         |                                                             
 public       | feature_node_stats     | start_city_id                   | text                        | YES         |                                                             
 public       | feature_node_stats     | start_node_waybill_num          | text                        | YES         |                                                             
 public       | feature_node_stats     | start_node_accident_rate        | text                        | YES         |                                                             
 public       | feature_node_stats     | start_node_real_claim_num_ratio | text                        | YES         |                                                             
 public       | feature_node_stats     | end_city_id                     | text                        | YES         |                                                             
 public       | feature_node_stats     | end_node_waybill_num            | text                        | YES         |                                                             
 public       | feature_node_stats     | end_node_accident_rate          | text                        | YES         |                                                             
 public       | feature_node_stats     | end_node_real_claim_num_ratio   | text                        | YES         |                                                             
 public       | shipments              | id                              | bigint                      | NO          | nextval('shipments_id_seq'::regclass)                       
 public       | shipments              | route_type                      | text                        | YES         |                                                             
 public       | shipments              | is_customer_to_customer         | text                        | YES         |                                                             
 public       | shipments              | is_fresh_and_delv_promise       | text                        | YES         |                                                             
 public       | shipments              | waybill_price_protect_money     | text                        | YES         |                                                             
 public       | shipments              | start_city_id                   | text                        | YES         |                                                             
 public       | shipments              | end_city_id                     | text                        | YES         |                                                             
 public       | shipments              | consigner_id                    | text                        | YES         |                                                             
 public       | shipments              | receiver_id                     | text                        | YES         |                                                             
 public       | shipments              | is_staff                        | text                        | YES         |                                                             
 public       | shipments              | plan_delv_to_real_delv_diff     | text                        | YES         |                                                             
 public       | shipments              | abnormal_reason                 | text                        | YES         |                                                             
 public       | shipments              | source                          | text                        | YES         |                                                             
 public       | shipments              | real_delv_to_case_create_diff   | text                        | YES         |                                                             
 public       | shipments              | payment_contract_money          | text                        | YES         |                                                             
 public       | shipments              | goods_category                  | text                        | YES         |                                                             
 public       | shipments              | goods_level                     | text                        | YES         |                                                             
 public       | shipments              | bc_source                       | text                        | YES         |                                                             
 public       | shipments              | customer_role                   | text                        | YES         |                                                             
 public       | shipments              | start_node_waybill_num          | text                        | YES         |                                                             
 public       | shipments              | start_node_accident_rate        | text                        | YES         |                                                             
 public       | shipments              | start_node_real_claim_num_ratio | text                        | YES         |                                                             
 public       | shipments              | end_node_waybill_num            | text                        | YES         |                                                             
 public       | shipments              | end_node_accident_rate          | text                        | YES         |                                                             
 public       | shipments              | end_node_real_claim_num_ratio   | text                        | YES         |                                                             
 public       | shipments              | payment_real_money              | text                        | YES         |                                                             
 public       | shipments2             | id                              | bigint                      | NO          | nextval('shipments2_id_seq'::regclass)                      
 public       | shipments2             | route_type                      | text                        | YES         |                                                             
 public       | shipments2             | is_customer_to_customer         | text                        | YES         |                                                             
 public       | shipments2             | is_fresh_and_delv_promise       | text                        | YES         |                                                             
 public       | shipments2             | waybill_price_protect_money     | text                        | YES         |                                                             
 public       | shipments2             | start_city_id                   | text                        | YES         |                                                             
 public       | shipments2             | end_city_id                     | text                        | YES         |                                                             
 public       | shipments2             | consigner_id                    | text                        | YES         |                                                             
 public       | shipments2             | receiver_id                     | text                        | YES         |                                                             
 public       | shipments2             | is_staff                        | text                        | YES         |                                                             
 public       | shipments2             | plan_delv_to_real_delv_diff     | text                        | YES         |                                                             
 public       | shipments2             | abnormal_reason                 | text                        | YES         |                                                             
 public       | shipments2             | source                          | text                        | YES         |                                                             
 public       | shipments2             | real_delv_to_case_create_diff   | text                        | YES         |                                                             
 public       | shipments2             | payment_contract_money          | text                        | YES         |                                                             
 public       | shipments2             | goods_category                  | text                        | YES         |                                                             
 public       | shipments2             | goods_level                     | text                        | YES         |                                                             
 public       | shipments2             | bc_source                       | text                        | YES         |                                                             
 public       | shipments2             | customer_role                   | text                        | YES         |                                                             
 public       | shipments2             | start_node_waybill_num          | text                        | YES         |                                                             
 public       | shipments2             | start_node_accident_rate        | text                        | YES         |                                                             
 public       | shipments2             | start_node_real_claim_num_ratio | text                        | YES         |                                                             
 public       | shipments2             | end_node_waybill_num            | text                        | YES         |                                                             
 public       | shipments2             | end_node_accident_rate          | text                        | YES         |                                                             
 public       | shipments2             | end_node_real_claim_num_ratio   | text                        | YES         |                              

