from flask import current_app
import datetime
from app.models.redis import REDIS


# 1、moment是否全天 是全天直接返回interval 不是全天，计算当前时间是否在moment，是计算，不是返回interval
def compute_interval(limit_alert):
    moment_begin = limit_alert["moment_begin"]
    moment_end = limit_alert["moment_end"]
    if moment_begin == 0 and moment_end == 0:
        return limit_alert["interval"]

    current_time = datetime.datetime.now()
    current_day = datetime.date.today().strftime('%Y-%m-%d')

    now_begin = datetime.datetime.strptime((current_day + " " + moment_begin), '%Y-%m-%d %H:%M')
    now_end = datetime.datetime.strptime((current_day + " " + moment_end), '%Y-%m-%d %H:%M')

    if current_time > now_begin and current_time < now_end:
        return limit_alert["interval"]
    else:
        return current_app.config["INTERVAL"]


class Alert:
    def __init__(self, msg):
        self.msg = msg

        self.limit_when = current_app.config["WHEN"]
        self.limit_when_alertnames = [alert.get("alertname") for alert in self.limit_when]
        self.limit_channels = current_app.config["CHANNELS"]
        self.redis = REDIS()
        self.group_name = self.msg["group_name"]
        self.limit_accounts = current_app.config["ALERT_ACCOUNTS"]

        self.interval = current_app.config["INTERVAL"]

    def is_alert_account(self):
        account = self.msg.get("labels").get("account")
        if str(account) in self.limit_accounts:
            return True
        else:
            return False

    def is_alert_channel(self):
        channel = self.msg.get("labels").get("channel")
        if channel in self.limit_channels:
            print("channel设置该通道不报警",channel)
            return False
        else:
            return True

    def is_resolved(self):
        if self.msg["status"] == "resolved":
            if self.redis.is_exist(self.group_name):
                if self.redis.rdel(str(self.group_name)):
                    return True
                else:
                    print("删除报警失败,报警未发出")
                    return False
            else:
                print("恢复，但是之前没有发生告警，恢复消息未发出")
                return False
        else:
            return False

    def is_alert_time(self):
        if self.redis.is_exist(self.group_name):
            return False
        else:
            return True

    # def is_spec_alertname(self):
    #     if self.group_name == "xttest15":
    #         return True
    #     else:
    #         return False

    # 默认when label 标记一天中不同时间的告警频率 when：[{alertname:test, moment_begin：12:00, moment_end:13:00,interval: x * 60s}] 0 0 全天
    def product_interval(self):
        alertname = self.msg.get("labels").get("alertname")
        if alertname in self.limit_when_alertnames:
            for alert in self.limit_when:
                if alert["alertname"] == alertname:
                    self.interval = compute_interval(alert)

    def status_summary(self):
        self.product_interval()

        # if not self.is_spec_alertname():
        #     return False
        # if self.is_alert_account():

        if not self.is_alert_account():
            return False

        if not self.is_alert_channel():
            return False

        if self.is_resolved():
            print("恢复恢复恢复恢复恢复恢复恢复")
            return True

        if self.is_alert_time():
            if self.redis.rset(self.group_name, 1, self.interval):
                print("告警告警告警告警告警告警")
                return True
            else:
                print("set redis key fail") 
                return False
        else:
            return False
