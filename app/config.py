REDIS = {"host":"r-2ze20e6829bf47d4.redis.rds.aliyuncs.com", "port":6379, "password":"emV1cy1tYWxs", "db":100}

INTERVAL = 60 * 30

UNIQ_ALERT_LABELS = ["alertname","channel","account"] #分组原则

WHEN = [{}, \
        {}]

CHANNELS = ["miaoxin-marketing-cmpp"]

LIMIT_LENGTH = 10 ##消息太长，只取前10

ALERT_ACCOUNTS = ["55", "70", "12"]