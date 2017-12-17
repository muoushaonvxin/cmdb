from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

# Create your models here.

class UserProfile(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name=u"用户名")
    nick_name = models.CharField(max_length=50, verbose_name=u"名称", default="")
    email = models.EmailField(verbose_name=u"email address", max_length=255, unique=True)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"电话号码")
    weixin = models.CharField(max_length=64, blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(verbose_name=u"staff status", default=True, help_text=u"Designates whether the user can log into this admin site.")
    memo = models.TextField(verbose_name='备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u"个人图像")
    friends = models.ManyToManyField('self', related_name=u"my_friends", blank=True)
    user_type = models.IntegerField(default=0, verbose_name=u"用户类型", choices=((0, u"普通用户"), (1, u"管理员")), null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    def __str__(self):
        return self.username

    def has_perms(self, perm_list, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    objects = UserManager()

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0},({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

























