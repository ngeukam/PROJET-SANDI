from django.contrib import admin
from app_sandi.models.patient import Patient
from app_sandi.models.clinic import Clinic
from app_sandi.models.laboratoire import Laboratoire
from import_export.admin import ImportExportActionModelAdmin
from app_sandi.models.prescription import Prescription
from app_sandi.models.resultat import Resultat
from app_sandi.forms.login import CustomUserChangeForm, CustomUserCreationForm
from .models.login import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete=False
    verbose_plural_name="User Profile"
    fk_name = 'user'  
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = ['username']
    search_fields = ('username',)
    ordering = ('username',)
    inlines = (UserProfileInline,)
    list_display = ('username', 'is_doctor', 'is_active', 'is_superuser',)
    list_filter = ('username', 'is_doctor', 'is_active', 'is_superuser', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'username','user_type')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_doctor', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_doctor', 'is_active', 'user_type')}
         ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    
admin.site.register(User, CustomUserAdmin)

admin.site.register(Patient)
class PatientAdmin(ImportExportActionModelAdmin):
    pass
admin.site.register(Laboratoire)
class LaboratoireAdmin(ImportExportActionModelAdmin):
    pass
admin.site.register(Clinic)
class LaboratoireAdmin(ImportExportActionModelAdmin):
    pass
admin.site.register(Prescription)
class PrescriptionAdmin(ImportExportActionModelAdmin):
    pass
admin.site.register(Resultat)
class ResultatAdmin(ImportExportActionModelAdmin):
    pass