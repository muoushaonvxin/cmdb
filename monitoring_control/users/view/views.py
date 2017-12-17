from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserProfile, Banner
from django.views import View
from users.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend, RemoteUserBackend
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.hashers import make_password
# Create your views here.

# 登录装饰检测

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录
class LoginView(View):
    """
        用户登录
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":u"用户未激活!"})
            else:
                return render(request, "login.html", {"msg":u"用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form":login_form})


# 用户登出
class LogoutView(View):
    """
        用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


# 跳转到用户登录首页
class IndexView(View):
    def get(self, request):
        return render(request, "index.html", {})