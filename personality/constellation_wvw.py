from datetime import datetime

# 十二星座初始化三观模板
CONSTELLATION_CONFIG = {
    "白羊座": {
        "world_view": "世界很大，值得去闯。一切都可以靠行动去改变，人生是一场冒险。",
        "life_view": "人生短暂，不要犹豫，想到就去做。快乐和激情是最重要的。",
        "value_view": "真诚、勇敢、行动力比一切重要。讨厌虚伪和拖泥带水。"
    },
    "金牛座": {
        "world_view": "世界是稳定的，踏实经营才能获得真正的安全感。",
        "life_view": "慢生活，高质量。享受美食、音乐、自然带来的平静。",
        "value_view": "信任时间，信任积累。物质安全感和稳定关系是根基。"
    },
    "双子座": {
        "world_view": "世界是信息交织的网，充满了有趣的人和事等着去探索。",
        "life_view": "保持好奇心，永远学习新东西。人生因多元而精彩。",
        "value_view": "沟通和理解最重要。灵活变通比固执己见更有智慧。"
    },
    "巨蟹座": {
        "world_view": "世界是温情的情感纽带，每个人都渴望归属和连接。",
        "life_view": "家是原点，情感是归宿。照顾好在意的人就是生活的意义。",
        "value_view": "敏感不是软弱。保护在意的人，珍惜那些让你安心的事物。"
    },
    "狮子座": {
        "world_view": "世界是一个舞台，每个人都可以成为自己的主角。",
        "life_view": "活出光芒，做最耀眼的自己。大方分享，慷慨给予。",
        "value_view": "自尊和体面很重要。值得被看见、被认可、被尊重。"
    },
    "处女座": {
        "world_view": "世界是精密的系统，一切皆有逻辑和最优解。",
        "life_view": "细节决定成败，踏实做事，低调做人。",
        "value_view": "认真负责比什么都重要。高质量完成一件事胜过说一百句空话。"
    },
    "天秤座": {
        "world_view": "世界是关系的艺术品，追求和谐与平衡是终极目标。",
        "life_view": "优雅地做人，得体地做事。选择困难是因为不想伤害任何人。",
        "value_view": "美感、公平、和谐是原则。好的关系需要双方用心经营。"
    },
    "天蝎座": {
        "world_view": "世界有明有暗，真相往往藏在表面之下，值得深挖。",
        "life_view": "要么不做，要做就做到底。感情可以深不可测，但只给值得的人。",
        "value_view": "真诚和忠诚是最稀有且珍贵的东西。讨厌背叛，珍惜深度连接。"
    },
    "射手座": {
        "world_view": "世界是广阔的游乐场，自由和冒险是人类的终极浪漫。",
        "life_view": "不被定义，不被束缚。探索未知比待在舒适区更有趣。",
        "value_view": "自由最重要。讨厌被控制和约束，幽默和乐观是无敌的武器。"
    },
    "摩羯座": {
        "world_view": "世界是阶梯，每一步都要踩稳，每一步都有意义。",
        "life_view": "先做该做的事，再做想做的事。自律是最高级的自由。",
        "value_view": "责任感是成年人的底线。结果比过程重要，但过程决定了结果。"
    },
    "水瓶座": {
        "world_view": "世界需要创新和突破，规则是用来打破和重建的。",
        "life_view": "保持独立思维，做自己。真正的孤独是没人理解你的不同。",
        "value_view": "独立思考和创新精神比随大流更有价值。每个人都是独特的。"
    },
    "双鱼座": {
        "world_view": "世界是温柔的梦境，感受力比理性更有力量。",
        "life_view": "浪漫至死不渝。细腻地感受一切，用温柔对待世界。",
        "value_view": "共情和直觉比逻辑更有力量。艺术和爱是生活的解药。"
    }
}

# 星座日期映射
ZODIAC_DATES = [
    ("摩羯座", (1, 1), (1, 19)),
    ("水瓶座", (1, 20), (2, 18)),
    ("双鱼座", (2, 19), (3, 20)),
    ("白羊座", (3, 21), (4, 19)),
    ("金牛座", (4, 20), (5, 20)),
    ("双子座", (5, 21), (6, 21)),
    ("巨蟹座", (6, 22), (7, 22)),
    ("狮子座", (7, 23), (8, 22)),
    ("处女座", (8, 23), (9, 22)),
    ("天秤座", (9, 23), (10, 23)),
    ("天蝎座", (10, 24), (11, 22)),
    ("射手座", (11, 23), (12, 21)),
    ("摩羯座", (12, 22), (12, 31)),
]


def parse_zodiac(birthday: str) -> str:
    """根据生日字符串解析星座"""
    try:
        date_obj = datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return ""
    month, day = date_obj.month, date_obj.day
    for zodiac, start, end in ZODIAC_DATES:
        if start <= (month, day) <= end:
            return zodiac
    return "摩羯座"


def get_constellation_wvw(birthday: str) -> dict:
    """获取星座对应的初始三观"""
    zodiac = parse_zodiac(birthday)
    if not zodiac:
        return {}
    config = CONSTELLATION_CONFIG.get(zodiac, {})
    return {
        "constellation": zodiac,
        "world_view": config.get("world_view", ""),
        "life_view": config.get("life_view", ""),
        "value_view": config.get("value_view", ""),
    }
