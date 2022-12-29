from django.contrib import admin
from .models import BerkasPengguna, PengajuanJadwal, UserProfile, PengajuanJadwalReview

#from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

admin.site.site_header = 'LPPM UNDA'

@admin.register(BerkasPengguna)
class BerkasPenggunaAdmin(ImportExportModelAdmin):
    list_display = ('ID', 'NIDN_NPM', 'NAMA_BERKAS', 'JENIS_BERKAS', 'format_link_berkas', 'SUMBER_PENDANAAN')
    list_filter = ('JENIS_BERKAS', 'SUMBER_PENDANAAN')
    search_fields = ('NAMA_BERKAS', 'NIDN_NPM')
    raw_id_fields = ['NIDN_NPM']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'NIDN_NPM' and not request.user.is_superuser:
            kwargs['queryset'] = UserProfile.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(NIDN_NPM=request.user.userprofile.ID)
    
    def format_link_berkas(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.LINK_BERKAS,
            obj.LINK_BERKAS
        )
    format_link_berkas.allow_tags = True

    


@admin.register(PengajuanJadwal)
class PengajuanJadwalAdmin(ImportExportModelAdmin):
    list_display = ('ID', 'TGL_PENGAJUAN', 'JENIS_PENGAJUAN', 'NAMA_PRESENTER','JUDUL_BERKAS','LINK_BERKAS')
    list_filter = ('JENIS_PENGAJUAN', 'NAMA_PRESENTER')
    search_fields = ('JUDUL_BERKAS', 'NIDN_NPM__NIDN_NPM','NAMA_PRESENTER')
    raw_id_fields = ('NIDN_NPM', 'LINK_BERKAS',)
  

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('ID', 'NIDN_NPM', 'KATEGORI', 'PEJABAT_LPPM','REVIEWER',)
    search_fields = ('NIDN_NPM', 'PEJABAT_LPPM')
    list_filter = ('KATEGORI', 'PEJABAT_LPPM')
    raw_id_fields = ('user',)
    #resource_class = UserProfileResource
  
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Jika pengguna adalah superuser, tampilkan semua data
            return qs
        elif request.user.is_staff:
            # Jika pengguna adalah staff (status aktif), tampilkan data dari semua pengguna
            return qs.filter(user=request.user)
        else:
            # Jika pengguna bukan superuser atau staff (status aktif), tampilkan hanya data dari pengguna yang bersangkutan
            return qs.filter(user=request.user)


class CustomModelAdmin(ImportExportModelAdmin):
    list_display = ('ID', 'STATUS_PENGAJUAN', 'TGL_SEMINAR', 'KESIMPULAN')
    list_filter = ('STATUS_PENGAJUAN',)
    search_fields = ('NIDN_NPM__NIDN_NPM',)
    raw_id_fields = ('ID','REVIEWER1', 'REVIEWER2', 'REVIEWER3', 'PEJABAT_LPPM')
    # Override metode get_form untuk mengatur akses field pada form
    def get_form(self, request, obj=None, **kwargs):
        # Jika user bukan superuser, maka ubah akses field sesuai dengan kondisi yang ditentukan
        if not request.user.is_superuser:
            # Jika user memiliki REVIEWER = 'Ya', maka hanya bisa mengedit field CATATAN_REVIEWER1, CATATAN_REVIEWER2, CATATAN_REVIEWER3
            if request.user.userprofile.REVIEWER == 'Ya' and request.user.userprofile.PEJABAT_LPPM == 'Tidak':
                #self.readonly_fields = ('CATATAN_REVIEWER1', 'CATATAN_REVIEWER2', 'CATATAN_REVIEWER3')
                self.readonly_fields = ('ID', 'STATUS_PENGAJUAN','TGL_SEMINAR')
                self.exclude = ( 'PEJABAT_LPPM', 'TGL_SEMINAR')
            elif request.user.userprofile.PEJABAT_LPPM != 'Tidak':
                self.fields = ('ID', 'STATUS_PENGAJUAN', 'TGL_SEMINAR', 'STATUS_PENGAJUAN','REVIEWER1', 'REVIEWER2', 'REVIEWER3', 'PEJABAT_LPPM')
            elif request.user.userprofile.REVIEWER == 'Ya' and request.user.userprofile.PEJABAT_LPPM != 'Tidak':
                self.fields = ('ID', 'STATUS_PENGAJUAN','KESIMPULAN','REVIEWER1','REVIEWER2','REVIEWER3', 'PEJABAT_LPPM', 'TGL_SEMINAR', 'CATATAN_REVIEWER1', 'CATATAN_REVIEWER2', 'CATATAN_REVIEWER3')
            # Jika user memiliki REVIEWER = 'Tidak', maka seluruh field menjadi readonly            
            else:
                self.readonly_fields = ('ID', 'STATUS_PENGAJUAN','KESIMPULAN','REVIEWER1','REVIEWER2','REVIEWER3', 'PEJABAT_LPPM', 'TGL_SEMINAR', 'CATATAN_REVIEWER1', 'CATATAN_REVIEWER2', 'CATATAN_REVIEWER3')
        # Jika user adalah superuser, maka tidak ada batasan akses field
             
        else:
            self.readonly_fields = ()
            self.exclude = ()
        # Kembalikan form dengan akses field yang telah diatur
        return super(CustomModelAdmin, self).get_form(request, obj, **kwargs)

#class UserProfileInline(admin.StackedInline):
#    model = UserProfile
#    extra = 0

#class UserAdmin(admin.ModelAdmin):
#    inlines = [UserProfileInline]
#    fields = ['username', 'password', 'password_confirmation']
#    change_password_form = AdminPasswordChangeForm

#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
admin.site.register(PengajuanJadwalReview, CustomModelAdmin)
