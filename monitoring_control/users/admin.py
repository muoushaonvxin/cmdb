from django.contrib import admin
from .models import UserProfile, EmailVerifyRecord, Banner
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



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
	fieldsets = (
		(None, {'fields': ('username', 'email', 'password', 'friends')}),
		('Personal info', {'fields': ()}),
		('API TOKEN info', {'fields': ('token',)}),
		('Permissions', {'fields': ('token',)}),
		('账户有效期', {'fields': ()}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'friends')}
		),
	)

	search_fields = ('email', 'username')
	ordering = ('email', 'username')
	filter_horizontal = ()

class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)