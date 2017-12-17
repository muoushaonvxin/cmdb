"""monitoring_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from users.view.views import LoginView, LogoutView
from users.view.views import IndexView
from monitor import urls as monitor_url
from cmdb import urls as cmdb_url
from webchat import urls as webchat_url


urlpatterns = [
    # django admin 管理后台页面
    url(r'^admin/', admin.site.urls),

    # 默认首页是登录界面
    url(r'^$', TemplateView.as_view(template_name="login.html"), name="login"),

    # 登录成功之后,跳转到主界面
    url(r'^index/$', IndexView.as_view(), name="index"),

    # 用户登录方法
    url(r'^user_login/$', LoginView.as_view(), name="user_login"),

    # 用户登出方法
    url(r'^user_logout/$', LogoutView.as_view(), name="user_logout"),

    # cmdb 资产管理
    url(r'^cmdb/', include(cmdb_url), name="cmdb"),

    # 监控url
    url(r'^monitor/', include(monitor_url), name="monitor"),

    # 聊天功能
    url(r'^webchat/', include(webchat_url), name="webchat"),
]






























