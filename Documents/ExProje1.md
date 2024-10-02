Adım 1: Gerekli Kütüphanelerin ve Ortamın Kurulumu
İlk olarak, Ubuntu üzerinde bir Python sanal ortamı oluşturup aktifleştirelim. Daha sonra gerekli kütüphaneleri kuracağız:

# Python ve venv paketini kur
    sudo apt update
    sudo apt install python3 python3-venv python3-pip -y

# Proje klasörüne git ve sanal ortamı oluştur
    mkdir futbol-projesi
    cd futbol-projesi
    python3 -m venv myenv

# Sanal ortamı aktif et
    source myenv/bin/activate

# Gerekli kütüphaneleri yükle
    pip install django djangorestframework 
    celery psycopg2-binary requests
Adım 2: PostgreSQL Kurulumu ve Yapılandırması
PostgreSQL veritabanını kurup yapılandıracağız. Bunun için bir kullanıcı ve veritabanı oluşturacağız:

# PostgreSQL'i kur
    sudo apt install postgresql postgresql-contrib -y

# PostgreSQL servislerini başlat
    sudo systemctl start postgresql
    sudo systemctl enable postgresql

# Postgres kullanıcısına geç
    sudo -i -u postgres

# Yeni bir veritabanı ve kullanıcı oluştur
    psql
    CREATE DATABASE futbol_db;
    CREATE USER futbol_user WITH PASSWORD 'sifre123';
    GRANT ALL PRIVILEGES ON DATABASE futbol_db TO futbol_user;

# PostgreSQL'den çık
    \q
    exit
    Adım 3: Django Projesinin ve Uygulamanın Oluşturulması
    Bir Django projesi oluşturup gerekli ayarları yapacağız:


# Django projesini oluştur
    django-admin startproject futbolprojesi

# Uygulamayı oluştur
    cd futbolprojesi
    django-admin startapp futbol

# Projeye futbol uygulamasını ekle
    nano futbolprojesi/settings.py
INSTALLED_APPS bölümüne futbol ve rest_framework ekleyin:
    
 
    INSTALLED_APPS = [
        ...
        'futbol',
        'rest_framework',
    ]
Veritabanı ayarlarını yapın (settings.py dosyasında):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'futbol_db',
            'USER': 'futbol_user',
            'PASSWORD': 'sifre123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
Adım 4: Futbol Modellerinin Oluşturulması
futbol/models.py dosyasına gidin ve modelleri oluşturun:


# futbol/models.py

    from django.db import models
    
    class Tournament(models.Model):
        name = models.CharField(max_length=255)
        season = models.CharField(max_length=50)
        tournament_id = models.IntegerField(unique=True)
        created_at = models.DateTimeField(auto_now_add=True)
    
        def __str__(self):
            return f"{self.name} - {self.season}"


    class MatchDetail(models.Model):
        tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
        match_id = models.IntegerField(unique=True)
        home_team = models.CharField(max_length=255)
        away_team = models.CharField(max_length=255)
        score = models.CharField(max_length=10)
        date = models.DateTimeField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.home_team} vs {self.away_team}"
            
Adım 5: Django Admin Ayarları ve Veritabanı Migrate
Modelleri Django admin panelinde görmek ve veritabanına yansıtmak için admin.py dosyasını düzenleyin ve ardından migrate işlemi yapın:

# futbol/admin.py

    from django.contrib import admin
    from .models import Tournament, MatchDetail
    
    admin.site.register(Tournament)
    admin.site.register(MatchDetail)

# Migrate işlemlerini yap
    python manage.py makemigrations
    python manage.py migrate

# Süper kullanıcı oluştur

    python manage.py createsuperuser

Adım 6: Celery Yapılandırması
Celery'yi projeye entegre edelim. futbolprojesi dizinine celery.py dosyası ekleyin:


# futbolprojesi/celery.py

    from __future__ import absolute_import, unicode_literals
    import os
    from celery import Celery
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futbolprojesi.settings')
    
    app = Celery('futbolprojesi')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    
    
    #Görevlerin otomatik olarak tanınmasını sağlar
    app.autodiscover_tasks()


settings.py dosyasına Celery yapılandırmasını ekleyin:


# futbolprojesi/settings.py

# Celery Ayarları

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


Adım 7: Celery Görevlerinin Oluşturulması
futbol uygulamasında tasks.py dosyasını oluşturun ve Celery görevlerini yazın:


# futbol/tasks.py

    from celery import shared_task
    import requests
    from .models import Tournament, MatchDetail
    
    @shared_task
    def fetch_tournament_data():
        url = "https://api.example.com/tournaments"
        response = requests.get(url)
        tournaments = response.json()
    
        for tournament in tournaments:
            Tournament.objects.update_or_create(
                tournament_id=tournament['id'],
                defaults={
                    'name': tournament['name'],
                    'season': tournament['season']
                }
            )

    @shared_task
    def fetch_match_data(tournament_id):
        url = f"https://api.example.com/tournaments/{tournament_id}/matches"
        response = requests.get(url)
        matches = response.json()
    
        tournament = Tournament.objects.get(tournament_id=tournament_id)
    
        for match in matches:
            MatchDetail.objects.update_or_create(
                match_id=match['id'],
                defaults={
                    'tournament': tournament,
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'score': match['score'],
                    'date': match['date']
                }
        )
        
Adım 8: Celery Servisinin Başlatılması
Redis sunucusunu başlatın ve Celery servisini çalıştırın:

# Redis kurulumu ve başlatılması
    sudo apt-get install redis-server -y
    sudo systemctl start redis
    sudo systemctl enable redis

# Celery çalıştırma
    celery -A futbolprojesi worker --loglevel=info
    celery -A futbolprojesi beat --loglevel=info

Adım 9: API'den Veri Çekme ve Güncelleme
Admin panelinden Tournament modeline bir turnuva ekleyin veya fetch_tournament_data görevini çalıştırarak verileri ekleyin:

# Django shell üzerinden çalıştırma
    python manage.py shell

from futbol.tasks import fetch_tournament_data, fetch_match_data
fetch_tournament_data.delay()

# Eklenen bir turnuva ID'si ile maç verilerini çekme
fetch_match_data.delay(tournament_id=1)
Bu adımları tamamladıktan sonra Django admin panelinden ve Celery görevlerini izleyerek verilerin otomatik olarak güncellendiğini görebilirsiniz.
