
# Celery - CeleryBeat and Flower Kurulum

1. Gerekli Bağımlılıkların Yüklenmesi
Celery'yi kullanmak için önce Ubuntu üzerinde gerekli bağımlılıkları yüklemeniz gerekiyor. Redis, Celery'nin sıklıkla kullanılan bir mesaj broker'ıdır.

Redis Yüklenmesi:
bash
Kodu kopyala
sudo apt update
sudo apt install redis-server
Redis sunucusunu başlatın:

bash
Kodu kopyala
sudo systemctl enable redis-server
sudo systemctl start redis-server
Python Virtual Environment ve Celery Kurulumu:
Proje dizininde sanal bir Python ortamı oluşturarak Celery'yi kurabilirsiniz.

bash
Kodu kopyala
sudo apt install python3-venv  # Virtual environment için gerekli paket
python3 -m venv myenv  # Sanal ortam oluştur
source myenv/bin/activate  # Ortamı aktif et

pip install django celery redis  # Gerekli Python paketlerini yükleyin
2. Celery Yapılandırılması (celery.py)
Projenizin kök dizininde celery.py adlı bir dosya oluşturun ve aşağıdaki yapılandırmayı ekleyin:

python
Kodu kopyala
# proje_adi/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django ayarlarını celery'e tanıt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proje_adi.settings')

app = Celery('proje_adi')

# Django'nun settings.py dosyasındaki CELERY ile başlayan ayarları otomatik alır.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm uygulamalardaki tasks.py dosyalarını otomatik bulur.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
3. settings.py Dosyasına Celery Ayarlarının Eklenmesi
Celery'nin ayarlarını settings.py dosyasına ekleyin:

python
Kodu kopyala
# Celery Ayarları
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Istanbul'

# Celery Beat için periyodik görevler (isteğe bağlı)
CELERY_BEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'myapp.tasks.my_periodic_task',
        'schedule': 30.0,
    },
}
4. tasks.py Dosyası
Bir görev oluşturmak için myapp/tasks.py adlı bir dosya ekleyin ve Celery görevini tanımlayın:

python
Kodu kopyala
# myapp/tasks.py
from celery import shared_task
import time

@shared_task
def my_periodic_task():
    time.sleep(10)
    print("30 saniyede bir çalışıyor.")
5. Celery Worker Servis Dosyasını Oluşturma (celery.service)
Ubuntu'da Celery'nin servis olarak çalışması için aşağıdaki adımları takip edin.

Servis dosyasını oluşturun:

bash
Kodu kopyala
sudo nano /etc/systemd/system/celery.service
İçerisine şu kodları ekleyin:

ini
Kodu kopyala
[Unit]
Description=Celery Service
After=network.target

[Service]
User=ahmety  # Kullanıcı adınızı girin
Group=www-data
WorkingDirectory=/home/ahmety/Masaüstü/DjangoPro/sofa  # Proje dizininizi girin
ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi worker --loglevel=info

[Install]
WantedBy=multi-user.target
6. Celery Beat Servis Dosyasını Oluşturma (celerybeat.service)
Celery Beat'i servis olarak çalıştırmak için benzer şekilde bir servis dosyası oluşturun:

bash
Kodu kopyala
sudo nano /etc/systemd/system/celerybeat.service
Aşağıdaki yapılandırmayı ekleyin:

ini
Kodu kopyala
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
User=ahmety  # Kullanıcı adınızı girin
Group=www-data
WorkingDirectory=/home/ahmety/Masaüstü/DjangoPro/sofa  # Proje dizininizi girin
ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi beat --loglevel=info

[Install]
WantedBy=multi-user.target
7. Servisleri Başlatma ve Etkinleştirme
Celery ve Celery Beat servislerini başlatmak ve her sistem açılışında otomatik çalıştırmak için şu komutları kullanın:

bash
Kodu kopyala
# Servisleri başlat
sudo systemctl start celery
sudo systemctl start celerybeat

# Otomatik başlatma için etkinleştir
sudo systemctl enable celery
sudo systemctl enable celerybeat
8. Servislerin Durumunu Kontrol Etme
Servislerin doğru bir şekilde çalışıp çalışmadığını kontrol etmek için şu komutları kullanabilirsiniz:

bash
Kodu kopyala
sudo systemctl status celery
sudo systemctl status celerybeat
9. Test Etme
Her şey kurulduktan sonra, Celery'nin görevleri doğru bir şekilde çalışıp çalışmadığını test etmek için:

bash
Kodu kopyala
celery -A proje_adi worker --loglevel=info
Sonuç olarak, Django ile Celery ve Celery Beat'i Ubuntu'da bir servis olarak kurup, arka planda görevlerinizi çalıştırmaya başlamış olacaksınız.
