from flask import current_app
from app.lib.alert_helper import Alert


class Msg:
    def __init__(self, msg):
        self.origin_msg = msg
        self.msg = ""

    def make(self):
        alert = Alert(self.origin_msg)
        if alert.status_summary():
            self.product_msg()
            return self.msg
        else:
            return None

    def product_msg(self):
        if self.origin_msg["status"] == "resolved":
            title = "恢复"
        else:
            title = "报警"
        self.msg += "【{}】\n".format(title)
        labels = self.origin_msg.get("labels")
        for k, v in labels.items():
            self.msg += "【{}】{}\n".format(k, v)
        annotations = self.origin_msg.get("annotations")
        for k, v in annotations.items():
            self.msg += "【{}】{}\n".format(k, v)
        # self.msg += "-----------------------------\n"


class Message:
    def __init__(self, b_data):
        self.msgs = []
        self.b_data = b_data
        self.message_limit_length = current_app.config["LIMIT_LENGTH"]

    def product(self):
        if not self.b_data:
            self.msgs.append("request data abnormal")
        data = eval(self.b_data.decode("utf-8"))
        repeat_msgs = data["alerts"]
        self.msgs = self.discard_repeat_msgs(repeat_msgs)
        handled_msgs = [Msg(m).make() for m in self.msgs]
        handled_msg = ""
        f = 0
        for m in handled_msgs:
            if f > self.message_limit_length:
                break
            if m:
                f += 1
                if f > 1:
                    handled_msg = handled_msg + "-----------------------------\n" + m
                else:
                    handled_msg += m
        return handled_msg

    def discard_repeat_msgs(self, repeat_msgs):
        msgs = []
        group_names = []
        group_labels = current_app.config["UNIQ_ALERT_LABELS"]
        for ms in repeat_msgs:
            labels = ms.get("labels")
            group_name = ""

            for label in group_labels:
                if labels.get(label):
                    group_name += str(labels.get(label))

            if not group_name in group_names:
                ms["group_name"] = group_name
                msgs.append(ms)
            group_names.append(group_name)
        return msgs
