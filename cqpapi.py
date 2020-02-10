import requests
import json
from constants import group_id, yama_qq


class API(object):
    def __init__(self):
        """
        看看登上没有
        """
        self.res = requests.post('http://127.0.0.1:5700/get_credentials')
        if json.loads(self.res.content.decode("utf-8", "ignore"))['status'] != 'ok':
            raise Exception

    def send_msg(self, msg):
        """
        给肛奇美拉群发消息
        """
        self.res = requests.post('http://127.0.0.1:5700/send_group_msg', {
            'group_id': group_id,
            'message': msg
        })

    def send_yama_msg(self, msg):
        self.res = requests.post('http://127.0.0.1:5700/send_private_msg', {
            'user_id': yama_qq,
            'message': msg
        })
