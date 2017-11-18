from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from cmdb.models import Asset, Server, CPU, IDC, RAM, NIC, NetworkDevice, Software
from cmdb.models import NewAssetApprovalZone, Disk, RaidAdaptor, Manufactory
from cmdb.models import BusinessUnit, Contract, Tag, EventLog
from users.models import UserProfile

from django.contrib.auth import forms as auth_form


class BaseAdmin(object):

	choice_fields = []
	fk_fields = []
	dynamic_fk = None
	dynamic_list_display = []
	dynamic_choice_fields = []
	m2m_fields = []


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ('email', )

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(label="Password",
		help_text=("Raw password2 are not stored, so there is no way to see"
					"this user's password, but you can change the password"
					"using <a href=\"password/\">this form</a>."))

	class Meta:
		model = UserProfile
		fields = ('email', 'password', 'is_active', )


	def clean_password(self):
		return self.initial['password']


class UserProfileAdmin(UserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('id', 'email', 'is_active')
	# list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('department', 'tel', 'mobile', 'memo')}),
		('API TOKEN info', {'fields': ('token',)}),
		('Permissions', {'fields': ('valid_begin_time', 'valid_end_time')}),
		('账户有效期', {'fields': ('valid_begin_time', 'valid_end_time')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin')}
		),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


class ServerInline(admin.TabularInline):
	model = Server
	exclude = ('memo',)


class CPUInline(admin.TabularInline):
	model = CPU
	exclude = ('memo',)
	readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
	model = NIC
	exclude = ('memo',)
	readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
	model = RAM
	exclude = ('memo',)
	readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
	model = Disk
	exclude = ('memo',)
	readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
	list_display = ('id', 'asset_type', 'sn', 'name', 'manufactory', 'management_ip', 'idc', 'business_unit', 'trade_date')
	inlines = [ServerInline, CPUInline, RAMInline, DiskInline, NICInline]
	search_fields = ['sn',]	
	list_filter = ['idc', 'manufactory', 'business_unit', 'asset_type']
	choice_fields = ('asset_type', 'status')
	fk_fields = ('manufactory', 'idc', 'business_unit', 'admin')
	list_per_page = 10
	list_filter = ('asset_type', 'manufactory', 'idc', 'business_unit', 'admin', 'trade_date')
	dynamic_fk = 'asset_type'
	dynamic_list_display = ('model', 'sub_asset_type', 'os_type', 'os_distribution')
	dynamic_choice_fields = ('sub_asset_type',)
	m2m_fields = ('tags',)


class NicAdmin(admin.ModelAdmin):
	list_display = ('name', 'macaddress', 'ipaddress', 'netmask', 'bonding')
	search_fields = ('macaddress', 'ipaddress')


class EventLogAdmin(admin.ModelAdmin, BaseAdmin):
	list_display = ('name', 'colored_event_type', 'asset', 'component', 'detail', 'date', 'user')	
	search_fields = ('asset',)
	list_filter = ('event_type', 'component', 'date', 'user')


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
	list_display = ('sn', 'asset_type', 'manufactory', 'model', 'cpu_model', 'cpu_count', 'cpu_core_count', 'ram_size', 'os_distribution', 'os_release', 'date', 'approved', 'approved_by', 'approved_date')
	actions = ['approve_selected_objects']

	def approve_selected_objects(modeladmin, request, queryset):
		selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		ct = ContentType.objects.get_for_model(queryset.model)
		return HttpResponseRedirect("/cmdb/asset/new_asset/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
	approve_selected_objects.short_description = "批准入库"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Server)
admin.site.register(NetworkDevice)
admin.site.register(IDC)
admin.site.register(BusinessUnit)
admin.site.register(Contract)
admin.site.register(CPU)
admin.site.register(Disk)
admin.site.register(NIC, NicAdmin)
admin.site.register(RAM)
admin.site.register(Manufactory)
admin.site.register(Tag)
admin.site.register(Software)
admin.site.register(EventLog, EventLogAdmin)
admin.site.register(NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
