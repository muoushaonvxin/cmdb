from django.db import models
from users.models import UserProfile
from datetime import datetime

# Create your models here.
# 监控的主机表
class Host(models.Model):
    # 主机名唯一
    name = models.CharField(max_length=32, verbose_name=u"主机名")
    # IP地址唯一
    ip_addr = models.GenericIPAddressField(verbose_name=u"IP地址")
    # 主机组
    host_groups = models.ManyToManyField('HostGroup', blank=True, verbose_name=u"主机组")
    # 默认模板
    templates = models.ManyToManyField('Template', blank=True, verbose_name=u"默认模板")

    monitored_by_choices = (
        ('agent', 'Agent'),
        ('snmp', 'SNMP'),
        ('wget', 'WGET'),
    )
    # 监控选择
    monitored_by = models.CharField(max_length=64, choices=monitored_by_choices, verbose_name=u"监控方式")

    host_alive_check_interval = models.IntegerField(default=30, verbose_name=u"主机存活状态检测间隔")

    status_choices = (
        (1, 'Online'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Offline'),
        (5, 'Problem'),
    )
    # 主机状态
    status = models.IntegerField(choices=status_choices, default=1, verbose_name=u"主机状态")
    # 备注信息
    memo = models.TextField(blank=True, null=True, verbose_name=u"备注信息")

    # class Meta:
    #     db_table = 'host'
    #     verbose_name = u'主机'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    # 主机组名
    name = models.CharField(max_length=64, unique=True, verbose_name=u"主机组名")
    # 主机组模板
    templates = models.ManyToManyField('Template', blank=True, verbose_name=u"主机组模板")
    # 备注信息
    memo = models.TextField(blank=True, null=True, verbose_name=u"备注信息")

    # class Meta:
    #     db_table = 'hostgroup'
    #     verbose_name = u'主机组'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 一个服务下面有多个指标, 指标表
class ServiceIndex(models.Model):
    # 指标名称
    name = models.CharField(max_length=64, verbose_name=u"指标名称")
    # 具体指标, 比如cpu下的idle值
    key = models.CharField(max_length=64)
    data_type_choices = (
        ('int', 'int'),
        ('float', 'float'),
        ('str', 'string'),
    )
    # 指标数据类型
    data_type = models.CharField(max_length=32, choices=data_type_choices, default='int', verbose_name=u"指标数据类型")
    # 备注
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    # class Meta:
    #     db_table = 'serviceindex'
    #     verbose_name = u'服务指标'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return "%s.%s" % (self.name, self.key)


# 服务表
class Service(models.Model):
    # 服务名称
    name = models.CharField(max_length=64, unique=True, verbose_name=u"服务名称")
    # 监控间隔
    interval = models.IntegerField(default=60, verbose_name=u"监控间隔")
    # 插件名, 比如cpu下有多个指标, 是一对多的关系
    plugin_name = models.CharField(verbose_name=u"插件名", max_length=64, default='n/a')
    items = models.ManyToManyField('ServiceIndex', blank=True, verbose_name=u"指标列表")
    # 子服务
    has_sub_service = models.BooleanField(default=False, help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡", verbose_name=u"子服务")
    # 备注
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    # class Meta:
    #     db_table = 'service'
    #     verbose_name = u'服务'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 模板表
class Template(models.Model):
    name = models.CharField(verbose_name=u"模板名称", max_length=64, unique=True)
    services = models.ManyToManyField('Service', blank=True, verbose_name=u"服务列表")
    triggers = models.ManyToManyField('Trigger', blank=True, verbose_name=u"触发器列表")

    # class Meta:
    #     db_table = 'template'
    #     verbose_name = u'模板'
    #     verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 触发一个报警，由多个指标来判断，触发关联表,一个表达式只能关联一个trigger
class TriggerExpression(models.Model):
    # 所需触发器
    trigger = models.ForeignKey('Trigger', verbose_name=u"所属触发器")
    # 关联服务
    service = models.ForeignKey('Service', verbose_name=u"关联服务")
    # 关联服务指标
    service_index = models.ForeignKey('ServiceIndex', verbose_name=u"关联服务指标")
    # 只能监控专门指定的指标key
    specified_index_key = models.CharField(verbose_name=u"只能监控专门指定的指标key", max_length=64, blank=True, null=True)

    operator_type_choices = (
        ('eq', '='),
        ('lt', '<'),
        ('gt', '>'),
    )
    # 运算符
    operator_type = models.CharField(verbose_name=u"运算符", choices=operator_type_choices, max_length=32)

    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'),
    )
    # 数据处理方式
    data_calc_func = models.CharField(choices=data_calc_type_choices, max_length=64, verbose_name=u"数据处理方式")
    # 函数传入参数
    data_calc_args = models.CharField(help_text=u"若是多个参数, 则用,号分开, 第一个值是时间", max_length=64, verbose_name=u"函数传入参数")
    # 阀值
    threshold = models.IntegerField(verbose_name=u"阀值")

    # 逻辑选择
    logic_type_choices = (
        ('or', 'OR'),
        ('and', 'AND'),
    )
    # 与另一个表达式的关系
    logic_type = models.CharField(choices=logic_type_choices, max_length=32, blank=True, null=True, verbose_name=u"与一个条件的逻辑关系")

    def __str__(self):
        return "%s %s(%s(%s))" % (self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

    # class Meta:
    #     db_table = 'triggerexpression'
    #     verbose_name = u'触发器表达式'
    #     verbose_name_plural = verbose_name


class Trigger(models.Model):
    # 触发器名称
    name = models.CharField(max_length=64, verbose_name=u"触发器名称")
    # expressions = models.ManyToManyField(TriggerExpression,verbose_name=u"条件表达式")
    serverity_choices = (
        (1, 'Information'),
        (2, 'Warning'),
        (3, 'Average'),
        (4, 'High'),
        (5, 'Diaster'),
    )
    # 告警级别
    serverity = models.IntegerField(choices=serverity_choices, verbose_name=u"告警级别")
    enabled = models.BooleanField(default=True)
    # 备注
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    def __str__(self):
        return "<service:%s, serverity:%s>" % (self.name, self.get_serverity_display())

    # class Meta:
    #     db_table = 'trigger'
    #     verbose_name = u'触发器'
    #     verbose_name_plural = verbose_name


# 触发报警后的动作类型
class Action(models.Model):
    # action名称
    name = models.CharField(max_length=64, unique=True, verbose_name=u"动作名称")
    # 关联哪个主机组
    host_groups = models.ManyToManyField('HostGroup', blank=True, verbose_name=u"主机组")
    # 关联哪个主机
    hosts = models.ManyToManyField('Host', blank=True, verbose_name=u"主机")
    # 告警条件
    conditions = models.TextField(verbose_name=u"告警条件")
    # 触发器
    triggers = models.ManyToManyField('Trigger', blank=True, help_text=u"想让哪些trigger出发当前报警动作", verbose_name=u"触发器")
    # 告警间隔
    interval = models.IntegerField(default=300, verbose_name=u"告警间隔(s)")
    # 关联别的动作
    operations = models.ManyToManyField('ActionOperation', verbose_name=u"ActionOperation")
    # 故障回复是否要通知
    recover_notice = models.BooleanField(verbose_name=u"故障回复后发送通知消息", default=True)
    # 恢复后通知的主题是什么
    recover_subject = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"通知主题")
    recover_message = models.TextField(blank=True, null=True, verbose_name=u"通知文本")
    # 是否停用
    enabled = models.BooleanField(default=True, verbose_name=u"是否停用")

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'action'
    #     verbose_name = u'动作'
    #     verbose_name_plural = verbose_name


# 触发器报警后的具体动作
class ActionOperation(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"告警升级")
    step = models.SmallIntegerField(verbose_name=u"第n次警告", default=1, help_text=u"当trigger触发次数小于这个值时就执行这条记录里报警方式")

    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    # 通过告警次数, 给告警级别升级, 并且指定动作类型
    action_type = models.CharField(verbose_name=u"动作类型", choices=action_type_choices, default='email', max_length=64)

    # 告警通知对象
    notifiers = models.ManyToManyField(UserProfile, blank=True, verbose_name=u"通知对象")
    _msg_format = '''Host({hostname}, {ip}) service({service_name}) has issue,msg:{msg}'''
    # 消息格式
    msg_format = models.TextField(verbose_name=u"消息格式", default=_msg_format)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'actionoperation'
    #     verbose_name = u'操作'
    #     verbose_name_plural = verbose_name


# 主机维护表
class Maintenance(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # 主机
    hosts = models.ManyToManyField('Host', verbose_name='主机', blank=True)
    # 主机组
    host_groups = models.ManyToManyField('HostGroup', blank=True, verbose_name=u"主机组")
    # 维护内容
    content = models.TextField(verbose_name=u"维护内容")
    # 开始时间
    start_time = models.DateTimeField(verbose_name=u"开始时间")
    # 结束时间
    end_time = models.DateTimeField(verbose_name=u"结束时间")

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'maintenance'
    #     verbose_name = u'主机维护'
    #     verbose_name_plural = verbose_name


class EventLog(models.Model):
    """存储报警及其它事件日志"""
    event_type_choices = ((0, u'报警事件'), (1, u'维护事件'))
    event_type = models.SmallIntegerField(choices=event_type_choices, default=0)
    host = models.ForeignKey('Host', verbose_name=u"主机")
    trigger = models.ForeignKey('Trigger', verbose_name=u"触发器", blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "host%s  %s" % (self.host, self.log)

    # class Meta:
    #     db_table = 'eventlog'
    #     verbose_name = u'事件日志'
    #     verbose_name_plural = verbose_name