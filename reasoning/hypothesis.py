CAUSAL_HYPOTHESES = {
    "delay_extreme": [
        {
            "cause": "长距离线路整体拥堵",
            "conditions": [
                ("delay_hours", ">", 48)
            ],
            "confidence": 0.7
        },
        {
            "cause": "末端配送节点异常",
            "conditions": [
                ("delay_hours", ">", 72)
            ],
            "confidence": 0.85
        }
    ],

    "fresh_without_coldchain": [
        {
            "cause": "冷链资源未分配",
            "conditions": [
                ("coldchain_flag", "==", 0)
            ],
            "confidence": 0.9
        }
    ]
}
