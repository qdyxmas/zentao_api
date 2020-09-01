# -*- coding: utf-8 -*-
# @Author : qdyxmas
# @time : 2020-09-01
# @file : zentao_api.py
# @zentao_version : 12.3.2

import json
import requests
import time

class ZenTao():
    """
    禅道统计类
    """
    def __init__(self, s, host, username, password):
        self.s = s
        self.host = host
        self.username = username
        self.password = password
        self.get_sessions()
    def get_sessions(self):
        """
         获取登录页的sessions api
         :return:
         """
        url = self.host + "api-getSessionID.json"
        getsessionid = self.s.get(url)
        getsessionid_str = json.loads(getsessionid.content)
        sessionID = json.loads(getsessionid_str['data'])["sessionID"]
        self.sessionID = sessionID
        return sessionID

    def get_zentaosid(self):
        """
        用户登录api
        :return:
        """
        url = self.host + "user-login.json?zentaosid=" + self.sessionID
        data = {"account": self.username, "password": self.password}
        req = self.s.post(url, data=data)
        get_zentaosid_str = json.loads(req.content)
        # print(get_zentaosid_str)
        return get_zentaosid_str
        
    def login(self):
        url = self.host + "/zentao/www/user-login-[referer]-[from].json"
        # data = {"referer":self.get_sessions(),"from":}
        
    def get_bugs(self):
        """
        获取所有BUG
        :return:
        """
        url = self.host + "bug.json?zentaosid=" + self.sessionID
        loginResp = json.loads(self.s.get(url).content)
        # print(loginResp)
        data = loginResp['data']
        # print(data)
        data_json = json.loads(data)['bugs']
        # print(data_json)
        return data_json
    #    
    def create_bug(self):
        url = self.host + "bug-create-3-0.json?zentaosid=" + self.sessionID
        data = {'product': '3', 'branch': '0', 'module': '0', 'project': '3', 'plan': '0', 'story': '9', 'storyVersion': '1', 'task': '0', 'toTask': '0', 'toStory': '0', 'title': "{}".format(time.time()), 'openedBuild': 'trunk'}
        req = self.s.post(url, data=data)
        print("create_bug=",json.loads(req.content))
    def bugs_lists(self):
        """
        对获取的BUG处理，过滤出需要的字段，重新返回列表bugs_list
        :return:
        """
        bugs_list = []
        for bug in self.get_bugs():
            title = bug['title']
            severity = bug['severity']
            status = bug['status']
            bug_dict = {'title': title, 'severity': severity, 'status': status}
            bugs_list.append(bug_dict)
        print(bugs_list)
        return bugs_list



if __name__ == '__main__':
    s = requests.session()
    z = ZenTao(s, "http://127.0.0.1/zentao/www/", "admin", "xxxxxx")
    z.get_zentaosid()
    # z.get_bugs()
    # z.create_bug()
    z.bugs_lists()
