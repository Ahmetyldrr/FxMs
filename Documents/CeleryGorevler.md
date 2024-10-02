# Celery Görevleri Nasıl Çalışır..

Bir celery modelinin çalışması için öncelikle bir modelimiz olmalıdır.
Ayırca celery nin settings.py de eklenmesi gerekmektedir.
Aşağıdaki kodlarda aşama aşama görevin nasıl çalıştığı incelenecektir.

## Modelin Kurulması(model.py)
  
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

bu modelimize otomatik api den veri göndermeye çalışacağız.
Öncelikle bu model için bir veri kaynağı olması lazım

## Veri Çekim Fonksiyonu(tasks.py or other.py)

Bu modelde iki parametre var , tournament_id ve season_id bu fonksiyona bu iki parametre verildiğinde model de bulunan sutunlar için verileri çekmektedir.
Bu fonksiyonu tasky.py de yada farklı bir python dosyasında yazıp import edebiliriz.


      def Roundinfo(t,s):
  
  
        """
        
            
            #https://www.sofascore.com/api/v1/unique-tournament/17015/season/61648/rounds
        #https://www.sofascore.com/api/v1/unique-tournament/13363/season/57319/rounds
        #52,63814
        #https://www.sofascore.com/api/v1/unique-tournament/804/season/61242/events/round/29/slug/final
        df = Roundinfo(804,61242)
        df
        #hafta_indices = df[df['week'] == 'Devam'].index
        #hafta = dict(df.iloc[hafta_indices[0]])
        #data = RoundData(hafta["tournament_id"],hafta["season_id"],hafta["round"],hafta["slug"],hafta["prefix"])
        #data.to_excel("Haftanın_Maçları.xlsx")
        #data
        bu fonksiyon ile ligin hangi haftada olduğu ve biten maçları alınır.
        ayrıca ilgili hafta yukarıda koda göre dizayn edilebilir.
        
            """
        conn = http.client.HTTPSConnection('www.sofascore.com')
        conn.request('GET', '/api/v1/unique-tournament/'+str(t)+'/season/'+str(s)+'/rounds')
        response = conn.getresponse()
        data = json.loads(response.read())
        all_round  = pd.DataFrame(data["rounds"])
        all_round["current"] = data["currentRound"]["round"]
        
        all_round["week"] = all_round.apply(
            lambda row: "Devam" if row["round"] == row["current"] 
            else "Biten" if row["round"] < row["current"] 
            else "Baslamadı", axis=1)
        
        # "last" sütununun eklenmesi (Ligin son haftası)
        all_round["last"] = len(all_round)
    
        all_round["tournament_id"] = t
        all_round[py"season_id"] = s
    
        columns_to_select = ['round', 'name', 'slug', 'prefix', 'current', 'week', 'last','tournament_id', 'season_id']
        
        for column in columns_to_select:
            if column not in all_round.columns:
                all_round[column] = ""  
                
        df = all_round[columns_to_select]
        
        #df["UpdateTime"] = datetime.now()
        
        devam_indices = df[df['week'] == 'Devam'].index
        if len(devam_indices) > 1:
            for i in range(devam_indices[0],devam_indices[1]):
                df.loc[i, 'week'] = 'Biten'
                
      
        df = df.fillna("")
        
        return df
  
## Celery ve Model Parametrelerinin Alınması(tasks.py)

Kodların celery de görünmesi içimn shared_task ile decoratöre bağlanması lazım.
burada tournaments modelimizde parametre almak için bu modeldeki verileri çağırıyoruz.
daha sonra bu modelden gelen tournament.id ve season.id bilgilerini Roundinfo fonskiyonuna veriyoruz.
Yapılan bu api çağrısından gelen veriler ise daha sonra for döngüsü ile tek tek RoundinfoModeline ekliyoruz.

    @shared_task
    def start_all_roundinfo_tasks():
    
        tournaments = Tournament.objects.all()  # Tüm turnuvaları alıyoruz
        
        for tournament in tournaments:
            print(tournament.tournament_id)
            time.sleep(1)
            try:
                df = Roundinfo(tournament.tournament_id, tournament.season_id)  # API'den veri çekme
                for _, row in df.iterrows():
                    RoundinfoModel.objects.update_or_create(
                        tournament_id=row['tournament_id'],  # Model alanı olan `tournament_id`
                        season_id=row['season_id'],  # Model alanı olan `season_id`
                        round=row['round'],
                        defaults={
                            'name': row['name'],
                            'slug': row['slug'],
                            'prefix': row['prefix'],
                            'current': row['current'],
                            'week': row['week'],
                            'last': row['last'],
                        
                        }
                    )
    
            except Exception as e:
                # Eğer bir hata olursa, ErrorLog modeline kaydediyoruz
                RoundinfoErrorLog.objects.create(
                    tournament_id=tournament.tournament_id,
                    season_id=tournament.season_id,
                    error_message=str(e)  # Hata mesajını kaydediyoruz
                )

## Modelin Admine Eklenmesi (Admin.py)

Modellerin adminde görünmesi için Roundinfomodeladmin adında bir class oluşturduktan sonra admin.site.register ile ekleme işlemi yapılır.

    class RoundinfoModelAdmin(admin.ModelAdmin):
        list_display = ('round', 'name', 'current', 'week', 'last', 'tournament_id', 'season_id', 'UpdateTime')  # Liste görünümü
        list_filter = ('week', 'current', 'last')  # Filtreleme
        search_fields = ('name', 'slug', 'tournament_id', 'season_id')  # Arama yapılacak alanlar
        ordering = ('-UpdateTime',)  # Güncelleme zamanına göre sıralama (en son güncellenenler önce)
        actions = [export_to_excel]
    
    admin.site.register(RoundinfoModel, RoundinfoModelAdmin)


## Modelin Admide Çalıştırılması

Bu işlemleri bitirdikten sonra admin sistemine giriş yapılır ve period_task ta bir görev oluşturulur ve sistem manuel olarak çalıştırılabilir.

## Örnek action kodu

bu kod actions = [export_to_excel] ile roundinfoadmin modeli için aktive edilmiştir.
    
    @admin.action(description="Seçilen Roundinfo verilerini Excel'e indir")
    def export_to_excel(modeladmin, request, queryset):
        # Queryset'ten alınan verileri bir DataFrame'e dönüştürüyoruz
        data = queryset.values(
            'tournament_id', 'season_id', 'round', 'name', 'slug', 'prefix', 'current', 'week', 'last', 'UpdateTime'
        )
        df = pd.DataFrame.from_records(data)
    
        # Zaman dilimi farkını kaldırıyoruz (Excel bunu desteklemediği için)
        if 'UpdateTime' in df.columns:
            df['UpdateTime'] = df['UpdateTime'].dt.tz_localize(None)
    
        # Excel dosyasına aktarmak için HTTP response oluşturuyoruz
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=roundinfo.xlsx'
    
        # DataFrame'i Excel dosyasına yazıyoruz
        df.to_excel(response, index=False, engine='openpyxl')
    
        return response



