from django.db import models

class Result(models.Model):
    # Temel Bilgiler
    
    tarih = models.CharField(max_length=50)
    custom_id = models.CharField(max_length=50)  # customId
    match_id = models.BigIntegerField(primary_key=True)
    start_timestamp = models.BigIntegerField()  # startTimestamp (Unix zaman damgası)
    
    # Turnuva ve Sezon Bilgileri
    tournament_name = models.CharField(max_length=255)  # Turnuva adı
    tournament_category_name = models.CharField(max_length=100)  # Turnuva kategorisi
    season_name = models.CharField(max_length=100)  # Sezon adı
    season_year = models.CharField(max_length=10)  # Sezon yılı
    tournament_unique_tournament_id = models.IntegerField()  # Benzersiz turnuva ID'si
    season_id = models.BigIntegerField()  # Sezon ID'si
    
    # Maç Detayları
    round_info_round = models.IntegerField()  # Maçın round'u (tur)
    status_type = models.CharField(max_length=50)  # Maç durumu (örneğin: finished)
    
    # Ev Sahibi Takım Bilgileri
    home_team_name = models.CharField(max_length=100)  # Ev sahibi takım adı
    home_team_name_code = models.CharField(max_length=10)  # Ev sahibi takım kodu (kısaltması)
    home_team_id = models.IntegerField()  # Ev sahibi takım ID'si
    home_score_display = models.IntegerField()  # Ev sahibi takımın toplam skoru
    home_score_period1 = models.IntegerField()  # Ev sahibi takımın ilk yarı skoru
    home_score_period2 = models.IntegerField()  # Ev sahibi takımın ikinci yarı skoru
    
    # Deplasman Takım Bilgileri
    away_team_name = models.CharField(max_length=100)  # Deplasman takımı adı
    away_team_name_code = models.CharField(max_length=10)  # Deplasman takım kodu (kısaltması)
    away_team_id = models.IntegerField()  # Deplasman takım ID'si
    away_score_display = models.IntegerField()  # Deplasman takımının toplam skoru
    away_score_period1 = models.IntegerField()  # Deplasman takımının ilk yarı skoru
    away_score_period2 = models.IntegerField()  # Deplasman takımının ikinci yarı skoru
    
    def __str__(self):
        return f"{self.tournament_name}: {self.home_team_name} vs {self.away_team_name} - {self.home_score_display}:{self.away_score_display}"


 
class GoalTime(models.Model):
    time = models.IntegerField()  # Olayın meydana geldiği dakika
    incident_type = models.CharField(max_length=50)  # Olay türü (örn. gol, faul, vb.)
    is_home = models.BooleanField()  # Ev sahibi takım olayı mı? (True: Doğru, False: Yanlış)
    incident_class = models.CharField(max_length=50)  # Olay sınıfı (örn. penaltı, regular vb.)
    player_name = models.CharField(max_length=100)  # Olayı gerçekleştiren oyuncu adı
    assist1_name = models.CharField(max_length=100, blank=True, null=True)  # Asist yapan oyuncu adı (opsiyonel)
    match_id = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return f"{self.player_name} - {self.incident_type} @ {self.time}'"
 
 
class MacBaskisi(models.Model):
    minute = models.IntegerField()  # Baskı değerinin kaydedildiği dakika
    value = models.IntegerField()   # Baskı değeri (Örneğin: -9, -31)
    match_id = models.BigIntegerField(primary_key=True)
    
    def __str__(self):
        return f"Minute {self.minute}: Value {self.value}"
 
class OyuncuPerformans(models.Model):
       
    # Temel Bilgiler
    bs_team = models.CharField(max_length=10)  # 'home' veya 'away' bilgisi
    bs_name = models.CharField(max_length=100)  # Oyuncunun tam adı
    bs_shortName = models.CharField(max_length=50)  # Kısa adı
    bs_position = models.CharField(max_length=2)  # Pozisyon (örn. G, D, M, A)
    bs_jerseyNumber = models.IntegerField()  # Forma numarası
    bs_country = models.CharField(max_length=100)  # Ülke adı
    bs_userCount = models.IntegerField()  # Kullanıcı sayısı (oylayan veya beğenen)
    bs_marketValueCurrency = models.CharField(max_length=3)  # Para birimi (örn. EUR)
    bs_minutesPlayed = models.IntegerField()  # Oynanan dakika
    bs_rating = models.FloatField()  # Oyuncunun performans puanı

    # Atak Verileri
    at_totalPass = models.IntegerField()  # Toplam pas
    at_accuratePass = models.IntegerField()  # Doğru pas
    at_goalAssist = models.IntegerField()  # Asist sayısı
    at_shotOffTarget = models.IntegerField()  # Kaleyi bulmayan şut
    at_onTargetScoringAttempt = models.IntegerField()  # Kaleyi bulan şut
    at_bigChanceMissed = models.IntegerField()  # Kaçırılan büyük fırsatlar
    at_expectedGoals = models.FloatField()  # Beklenen gol (xG)
    at_expectedAssists = models.FloatField()  # Beklenen asist (xA)
    at_keyPass = models.IntegerField()  # Kilit paslar
    at_totalLongBalls = models.IntegerField()  # Uzun paslar
    at_accurateLongBalls = models.IntegerField()  # Doğru uzun paslar
    at_touches = models.IntegerField()  # Topla buluşmalar
    at_possessionLostCtrl = models.IntegerField()  # Top kaybı (kontrol kaybı)

    # Defans Verileri
    de_aerialWon = models.IntegerField()  # Hava topu kazanma
    de_duelLost = models.IntegerField()  # Kaybedilen ikili mücadele
    de_duelWon = models.IntegerField()  # Kazanılan ikili mücadele
    de_challengeLost = models.IntegerField()  # Kaybedilen mücadele
    de_dispossessed = models.IntegerField()  # Top kaptırma
    de_totalContest = models.IntegerField()  # Toplam mücadele
    de_wonContest = models.IntegerField()  # Kazanılan mücadele
    de_outfielderBlock = models.IntegerField()  # Oyuncu blokajı
    de_totalTackle = models.IntegerField()  # Toplam müdahale
    de_fouls = models.IntegerField()  # Faul
    de_interceptionWon = models.IntegerField()  # Top kapma
    de_totalClearance = models.IntegerField()  # Top uzaklaştırma

    # Kaleci Verileri
    go_saves = models.IntegerField()  # Kurtarış
    go_goalsPrevented = models.FloatField()  # Önlenen goller (negatif olabilir)
    go_penaltySave = models.IntegerField()  # Penaltı kurtarma

    # Takım Formasyonları
    home_formation = models.CharField(max_length=10)  # Ev sahibi formasyonu
    away_formation = models.CharField(max_length=10)  # Deplasman formasyonu

    # Maç İlişkisi
    match_id = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return f"{self.bs_name} - {self.match}"


class MacIstatistik(models.Model):
    # İstatistik Bilgileri
    name = models.CharField(max_length=100)  # İstatistik adı (örn. "Ball possession", "Expected goals")
    home = models.CharField(max_length=50, blank=True, null=True)  # Ev sahibi takım değeri (örn. 32% veya 0.73)
    away = models.CharField(max_length=50, blank=True, null=True)  # Deplasman takım değeri (örn. 68% veya 3.00)
    compareCode = models.IntegerField()  # Karşılaştırma kodu (örn. 2)
    statisticsType = models.CharField(max_length=50)  # İstatistik türü (örn. "positive")
    valueType = models.CharField(max_length=50)  # Değer tipi (örn. "event")
    homeValue = models.FloatField()  # Ev sahibi takım için numerik değer
    awayValue = models.FloatField()  # Deplasman takımı için numerik değer
    renderType = models.IntegerField()  # Render tipi (örn. 1 veya 2)
    key = models.CharField(max_length=50)  # İstatistik anahtarı (örn. "ballPossession", "expectedGoals")
    period = models.CharField(max_length=50)  # İstatistik periyodu (örn. "ALL")
    groupName = models.CharField(max_length=100)  # İstatistiğin ait olduğu grup (örn. "Match overview")

    match_id = models.BigIntegerField(primary_key=True)
    # Toplam Bilgiler (Eğer boş bırakılabiliyorsa null ve blank kullanılabilir)
    homeTotal = models.FloatField(blank=True, null=True)  # Ev sahibi takım için toplam değer
    awayTotal = models.FloatField(blank=True, null=True)  # Deplasman takımı için toplam değer

    def __str__(self):
        return f"{self.name} - {self.match}"


