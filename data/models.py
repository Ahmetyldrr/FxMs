from django.db import models
from django.utils import timezone

class Tournament(models.Model):  

    season_id = models.IntegerField(verbose_name="Sezon ID")
    tournament_id = models.IntegerField(verbose_name="Turnuva ID")
    country_name = models.CharField(max_length=100, verbose_name="Ülke Adı")
    tournament_name = models.CharField(max_length=100, verbose_name="Turnuva Adı")
    season_name = models.CharField(max_length=100, verbose_name="Sezon Adı")
    season_year = models.CharField(max_length=10, verbose_name="Sezon Yılı")
    hasGlobalHighlights = models.BooleanField(default=False, verbose_name="Global Öne Çıkanlar Var mı?")
    hasEventPlayerStatistics = models.BooleanField(default=False, verbose_name="Oyuncu İstatistikleri Var mı?")
    hasEventPlayerHeatMap = models.BooleanField(default=False, verbose_name="Oyuncu Isı Haritası Var mı?")

    def __str__(self):
        return f"{self.tournament_name} ({self.season_year})"

    class Meta:
         constraints = [
             models.UniqueConstraint(fields=['season_id', 'tournament_id','tournament_name'
                                        ], name='unique_season_tournament')
         ]


class RoundinfoModel(models.Model):
    round = models.IntegerField()  # Sıra numarası (round)
    name = models.CharField(max_length=255, blank=True, null=True)  # Adı (opsiyonel)
    slug = models.SlugField(max_length=255, blank=True, null=True)  # Slug (opsiyonel)
    prefix = models.CharField(max_length=255, blank=True, null=True)  # Ön ek (opsiyonel)
    current = models.IntegerField()  # Geçerli haftanın numarası
    week = models.CharField(max_length=50)  # Hafta durumu: Biten, Devam, Baslamadı
    last = models.IntegerField()  # Ligdeki son hafta numarası
    tournament_id = models.IntegerField()  # Turnuva kimliği
    season_id = models.IntegerField()  # Sezon kimliği
    UpdateTime = models.DateTimeField(default=timezone.now)  # Güncelleme zamanı (otomatik)

    def __str__(self):
        return f"Round {self.round} - {self.week}"
    
    class Meta:
         constraints = [
             models.UniqueConstraint(fields=['round','season_id', 'tournament_id'
                                        ], name='unique_week_tournament')
         ]




class MatchInfo(models.Model):

    idx = models.BigIntegerField()  # Büyük tam sayı (id)
    startTimestamp = models.BigIntegerField()  # UNIX zaman damgası
    tournament_name = models.CharField(max_length=255)  # Turnuva adı
    tournament_category_name = models.CharField(max_length=255)  # Turnuva kategorisi
    tournament_category_id = models.IntegerField()  # Turnuva kategorisi ID
    tournament_uniqueTournament_name = models.CharField(max_length=255)  # Özgün turnuva adı
    tournament_uniqueTournament_id = models.IntegerField()  # Özgün turnuva ID
    season_name = models.CharField(max_length=255)  # Sezon adı
    season_year = models.CharField(max_length=20)  # Sezon yılı
    season_id = models.IntegerField()  # Sezon ID
    roundInfo_round = models.IntegerField()  # Tur bilgisi (round)
    status_type = models.CharField(max_length=50)  # Maç durumu (finished, ongoing)
    homeTeam_name = models.CharField(max_length=255)  # Ev sahibi takım adı
    homeTeam_nameCode = models.CharField(max_length=10)  # Ev sahibi takım kısa adı
    homeTeam_id = models.IntegerField()  # Ev sahibi takım ID
    awayTeam_name = models.CharField(max_length=255)  # Deplasman takımı adı
    awayTeam_nameCode = models.CharField(max_length=10)  # Deplasman takımı kısa adı
    awayTeam_id = models.IntegerField()  # Deplasman takımı ID
    homeScore_period1 = models.IntegerField(null=True, blank=True)  # Ev sahibi takım ilk yarı skoru (Null olabilir)
    homeScore_period2 = models.IntegerField(null=True, blank=True)  # Ev sahibi takım ikinci yarı skoru (Null olabilir)
    homeScore_normaltime = models.IntegerField(null=True, blank=True)  # Ev sahibi takım normal süre skoru (Null olabilir)
    awayScore_period1 = models.IntegerField(null=True, blank=True)  # Deplasman takımı ilk yarı skoru (Null olabilir)
    awayScore_period2 = models.IntegerField(null=True, blank=True)  # Deplasman takımı ikinci yarı skoru (Null olabilir)
    awayScore_normaltime = models.IntegerField(null=True, blank=True)  # Deplasman takımı normal süre skoru (Null olabilir)
    UpdateTime = models.DateTimeField(default=timezone.now)  # Güncelleme zamanı (otomatik)

    def __str__(self):
        return f"{self.homeTeam_name} vs {self.awayTeam_name} - {self.tournament_name} (Round {self.roundInfo_round})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['idx', 'season_id'], name='match_unique')
        ]

class RoundinfoErrorLog(models.Model):
    tournament_id = models.IntegerField()  # Hangi turnuvada hata oluştu
    season_id = models.IntegerField()  # Hangi sezonda hata oluştu
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hatanın oluşma zamanı

    def __str__(self):
        return f"Error in Tournament {self.tournament_id}, Season {self.season_id} - {self.created_at}"



from django.db import models
from django.utils import timezone

class MatchDataError(models.Model):
    tournament_id = models.IntegerField()  # Hangi turnuvada hata oluştu
    season_id = models.IntegerField()  # Hangi sezonda hata oluştu
    round_num = models.IntegerField()  # Tur numarası
    slug = models.CharField(max_length=255, blank=True, null=True)  # Slug (opsiyonel)
    prefix = models.CharField(max_length=255, blank=True, null=True)  # Ön ek (opsiyonel)
    error_message = models.TextField()  # Hata mesajı
    created_at = models.DateTimeField(auto_now_add=True)  # Hatanın oluşma zamanı (otomatik)

    def __str__(self):
        return f"Error in Tournament {self.tournament_id}, Season {self.season_id}, Round {self.round_num} - {self.created_at}"
# models.py
from django.db import models

class ErrorLog(models.Model):
    """
    Genel hata günlüğü tutmak için kullanılacak model.
    """
    tournament_id = models.IntegerField(null=True, blank=True)
    season_id = models.IntegerField(null=True, blank=True)
    round_num = models.IntegerField(null=True, blank=True)
    error_message = models.TextField()  # Hata mesajını saklayacak alan
    created_at = models.DateTimeField(auto_now_add=True)  # Hata zamanı

    def __str__(self):
        return f"ErrorLog: {self.error_message} ({self.created_at})"
