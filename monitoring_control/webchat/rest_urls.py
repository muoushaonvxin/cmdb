# -*- encoding: utf-8 -*-
__author__ = "zhangyz"
__date__ = "2017/12/16 18:29"

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from webchat.view.views import GetUserFriend, MsgHandler, GetNewMsgs

urlpatterns = [
    url(r'^friend/$', GetUserFriend.as_view(), name="friend"),

    # 接受用户发送过来的消息
    url(r'^msghandler/$', MsgHandler.as_view(), name="msghandler"),

    # 获取新的消息
    url(r'^getnewmsgs/$', GetNewMsgs.as_view(), name="getnewmsgs"),
]
