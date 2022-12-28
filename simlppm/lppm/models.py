from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    NIDN_NPM = models.CharField(max_length=13)

    KATEGORI_CHOICES = (
        ('Dosen', 'Dosen'),
        ('Mahasiswa', 'Mahasiswa'),
        ('Umum', 'Umum'),
    )
    KATEGORI = models.CharField(max_length=20, choices=KATEGORI_CHOICES)

    PEJABAT_LPPM_CHOICES = (
        ('Ketua LPPM', 'Ketua LPPM'),
        ('Anggota LPPM', 'Anggota LPPM'),
        ('Tidak', 'Tidak'),
    )
    PEJABAT_LPPM = models.CharField(max_length=20, choices=PEJABAT_LPPM_CHOICES)

    REVIEWER_CHOICES = (
        ('Ya', 'Ya'),
        ('Tidak', 'Tidak'),
    )
    REVIEWER = models.CharField(max_length=5, choices=REVIEWER_CHOICES)

    def __str__(self):
        return self.NIDN_NPM

    class Meta:
        verbose_name_plural = "Profil Pengguna"

class BerkasPengguna(models.Model):
    ID = models.AutoField(primary_key=True)
    NIDN_NPM = models.ForeignKey(UserProfile, related_name='berkas_pengguna', on_delete=models.CASCADE)
    NAMA_BERKAS = models.TextField(max_length=200)
    
    JENIS_BERKAS_CHOICES = (
        ('(Dosen) Proposal Penelitian', '(Dosen) Proposal Penelitian'),
        ('(Dosen) Laporan Akhir Penelitian', '(Dosen) Laporan Akhir Penelitian'),
        ('(Dosen) Pengabdian pada Masyarakat', '(Dosen) Pengabdian pada Masyarakat'),
        ('(Mahasiswa) Proposal Skripsi/TA', '(Mahasiswa) Proposal Skripsi/TA'),
        ('(Mahasiswa) Sidang Skripsi/TA', '(Mahasiswa) Sidang Skripsi/TA'),
        ('(Umum) Focus Group Discussion', '(Umum) Focus Group Discussion'),
        ('(Umum) Lainnya', '(Umum) Lainnya'),
    )    
    JENIS_BERKAS = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)
    LINK_BERKAS = models.CharField(max_length=300)

    SUMBER_PENDANAAN_CHOICES = (
        ('Internal', 'Internal'),
        ('External', 'External'),
        ('Hibah', 'Hibah'),
    )  
    SUMBER_PENDANAAN = models.CharField(max_length=25, choices=SUMBER_PENDANAAN_CHOICES)

    def __str__(self):
        return self.NAMA_BERKAS
    
    class Meta:
        verbose_name_plural = "Berkas Pengguna"

class PengajuanJadwal(models.Model):
    ID = models.AutoField(primary_key=True)
    NIDN_NPM = models.ManyToManyField(UserProfile, related_name='pengajuan_jadwal')
    NAMA_PRESENTER = models.CharField(max_length=80)
    LINK_BERKAS = models.ManyToManyField(BerkasPengguna, related_name='pengajuan_jadwal')
    TGL_PENGAJUAN = models.DateField()

    JENIS_PENGAJUAN_CHOICES = (
        ('(Dosen) Proposal Penelitian', '(Dosen) Proposal Penelitian'),
        ('(Dosen) Laporan Akhir Penelitian', '(Dosen) Laporan Akhir Penelitian'),
        ('(Dosen) Pengabdian pada Masyarakat', '(Dosen) Pengabdian pada Masyarakat'),
        ('(Mahasiswa) Proposal Skripsi/TA', '(Mahasiswa) Proposal Skripsi/TA'),
        ('(Mahasiswa) Sidang Skripsi/TA', '(Mahasiswa) Sidang Skripsi/TA'),
        ('(Umum) Focus Group Discussion', '(Umum) Focus Group Discussion'),
        ('(Umum) Lainnya', '(Umum) Lainnya'),
    )    

    JENIS_PENGAJUAN = models.CharField(max_length=100, choices=JENIS_PENGAJUAN_CHOICES)
    LINK_BERKAS = models.ForeignKey(BerkasPengguna, on_delete=models.CASCADE, related_name='pengajuan_jadwal')
    
    JUDUL_BERKAS = models.TextField(max_length=1000)
    

    def __str__(self):
        return self.JUDUL_BERKAS

    class Meta:
        verbose_name_plural = "Pengajuan Jadwal"


class PengajuanJadwalReview(models.Model):
    ID = models.OneToOneField(PengajuanJadwal, on_delete=models.CASCADE)
    TGL_SEMINAR = models.DateField()


    STATUS_PENGAJUAN_CHOICES = (
        ('Dijadwalkan', 'Dijadwalkan'),
        ('Ditolak', 'Ditolak'),
        ('Revisi', 'Revisi'),
        ('Selesai', 'Selesai'),
    )    

    #JENIS_PENGAJUAN = models.CharField(max_length=100, choices=JENIS_PENGAJUAN_CHOICES)
    STATUS_PENGAJUAN = models.CharField(max_length=11,choices=STATUS_PENGAJUAN_CHOICES)
    
    REVIEWER1 = models.ManyToManyField(UserProfile, related_name='reviewer1', limit_choices_to={'KATEGORI': 'Dosen','REVIEWER':'Ya'})
    REVIEWER2 = models.ManyToManyField(UserProfile, related_name='reviewer2', limit_choices_to={'KATEGORI': 'Dosen','REVIEWER':'Ya'})
    REVIEWER3 = models.ManyToManyField(UserProfile, related_name='reviewer3', limit_choices_to={'KATEGORI': 'Dosen','REVIEWER':'Ya'})
    
    PEJABAT_LPPM = models.ManyToManyField(UserProfile, related_name='pejabat_lppm', limit_choices_to={'PEJABAT_LPPM__in': ['Ketua LPPM', 'Anggota LPPM']})

    KESIMPULAN = models.TextField(max_length=1000,blank=True)
    CATATAN_REVIEWER1 = models.TextField(max_length=1000,blank=True)
    CATATAN_REVIEWER2 = models.TextField(max_length=1000,blank=True)
    CATATAN_REVIEWER3 = models.TextField(max_length=1000,blank=True)
    
    

    def __str__(self):
        return self.STATUS_PENGAJUAN

    class Meta:
        verbose_name_plural = "Info Seminar"
