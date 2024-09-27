
# Celery - CeleryBeat and Flower Kurulum

## 1. Gerekli Bağımlılıkların Yüklenmesi
Celery'yi kullanmak için önce Ubuntu üzerinde gerekli bağımlılıkları yüklemeniz gerekiyor. Redis, Celery'nin sıklıkla kullanılan bir mesaj broker'ıdır.

Redis Yüklenmesi:

    sudo apt update
    sudo apt install redis-server
    
Redis sunucusunu başlatın:

    sudo systemctl enable redis-server
    sudo systemctl start redis-server
    
Proje dizininde sanal bir Python ortamı oluşturarak Celery'yi kurabilirsiniz.


    sudo apt install python3-venv
    python3 -m venv myenv  
    source myenv/bin/activate 


## 2. Celery Yapılandırılması (celery.py)
Projenizin kök dizininde celery.py adlı bir dosya oluşturun ve aşağıdaki yapılandırmayı ekleyin:

### proje_adi/celery.py
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
## 3. settings.py Dosyasına Celery Ayarlarının Eklenmesi
Celery'nin ayarlarını settings.py dosyasına ekleyin:


### Celery Ayarları
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Europe/Istanbul'

### Celery Beat için periyodik görevler (isteğe bağlı)

    CELERY_BEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'myapp.tasks.my_periodic_task',
            'schedule': 30.0,
        },
    }
    
## 4. tasks.py Dosyası
Bir görev oluşturmak için myapp/tasks.py adlı bir dosya ekleyin ve Celery görevini tanımlayın:


    from celery import shared_task
    import time
    
    @shared_task
    def my_periodic_task():
        time.sleep(10)
        print("30 saniyede bir çalışıyor.")

    
## 5. Celery Worker Servis Dosyasını Oluşturma (celery.service)
Ubuntu'da Celery'nin servis olarak çalışması için aşağıdaki adımları takip edin.


    sudo nano /etc/systemd/system/celery.service
    
İçerisine şu kodları ekleyin:

    [Unit]
    Description=Celery Service
    After=network.target
    [Service]
    User=ahmety  # Kullanıcı adınızı girin
    Group=www-data
    WorkingDirectory=/home/ahmety/Masaüstü/DjangoPro  # Proje dizininizi girin
    ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi worker --loglevel=info
    
    [Install]
    WantedBy=multi-user.target
    
## 6. Celery Beat Servis Dosyasını Oluşturma (celerybeat.service)

Celery Beat'i servis olarak çalıştırmak için benzer şekilde bir servis dosyası oluşturun:

    sudo nano /etc/systemd/system/celerybeat.service
    
Aşağıdaki yapılandırmayı ekleyin:

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


## 7. Servisleri Başlatma ve Etkinleştirme
Celery ve Celery Beat servislerini başlatmak ve her sistem açılışında otomatik çalıştırmak için şu komutları kullanın:

    sudo systemctl start celery
    sudo systemctl start celerybeat

### Otomatik başlatma için etkinleştir

    sudo systemctl enable celery
    sudo systemctl enable celerybeat
    
## 8. Servislerin Durumunu Kontrol Etme

Servislerin doğru bir şekilde çalışıp çalışmadığını kontrol etmek için şu komutları kullanabilirsiniz:

    sudo systemctl status celery
    sudo systemctl status celerybeat
## 9. Test Etme
Her şey kurulduktan sonra, Celery'nin görevleri doğru bir şekilde çalışıp çalışmadığını test etmek için:

    celery -A proje_adi worker --loglevel=info

Sonuç olarak, Django ile Celery ve Celery Beat'i Ubuntu'da bir servis olarak kurup, arka planda görevlerinizi çalıştırmaya başlamış olacaksınız.

[celerypy_dosyası](https://github.com/Ahmetyldrr/SofaPro/blob/main/sofa/celery.py)


## Flower Task Takibi

Flower Kurulumu ve Yapılandırılması

### 1. Flower Kurulumu
Öncelikle Flower'ı projenizin sanal ortamında yükleyin:


    pip install flower
    
### 2. Flower'ı Başlatma

Flower'ı çalıştırmak için Celery ile birlikte aşağıdaki komutu kullanabilirsiniz:

    celery -A sofa flower
    
Bu komut, Flower'ı başlatacak ve varsayılan olarak http://localhost:5555/ adresinde çalıştıracaktır.

Eğer Flower'ı farklı bir port üzerinden çalıştırmak isterseniz, şu komutu kullanabilirsiniz:


    celery -A proje_adi flower --port=8080

### 3. Flower İçin Servis Dosyasını Oluşturma
Flower'ı Ubuntu'da bir servis olarak çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

Flower servis dosyasını oluşturun:

    sudo nano /etc/systemd/system/flower.service
    
Aşağıdaki yapılandırmayı servis dosyasına ekleyin:

    [Unit]
    Description=Flower Service for Celery Monitoring
    After=network.target
    
    [Service]
    User=ahmety  # Kullanıcı adınızı buraya girin
    Group=www-data
    WorkingDirectory=/home/ahmety/Masaüstü/DjangoPro/sofa  # Proje dizininizi girin
    ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi flower --port=5555 --loglevel=info
    Restart=always
    
    [Install]
    WantedBy=multi-user.target


Servisi başlatın ve etkinleştirin:

    sudo systemctl start flower
    sudo systemctl enable flower
    
### 4. Flower Servisinin Durumunu Kontrol Etme
Flower servisinin durumunu kontrol etmek ve çalıştığından emin olmak için:

    sudo systemctl status flower

Eğer servis başlamazsa ya da hata mesajları alırsanız, 

    journalctl -u flower.service 

komutunu kullanarak daha detaylı hata kayıtlarını görebilirsiniz.

### 5. Flower İçin Authentication (Kimlik Doğrulama) Ekleme

Flower'a kimlik doğrulama eklemek için flower.service dosyanızda ExecStart komutunu şu şekilde güncelleyebilirsiniz:

    ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi flower --port=5555 --basic_auth=username:password --loglevel=info

Burada username ve password değerlerini istediğiniz kimlik bilgileri ile değiştirin.

### 6. Flower'ı Dışarıdan Erişilebilir Yapmak
Flower'ı yalnızca localhost'ta değil, diğer bilgisayarlardan da erişilebilir yapmak istiyorsanız, flower.service dosyasındaki ExecStart komutunu şu şekilde düzenleyin:

    ExecStart=/home/ahmety/Masaüstü/myenv/bin/celery -A proje_adi flower --port=5555 --address=0.0.0.0 --basic_auth=username:password --loglevel=info

Bu şekilde Flower, ağdaki herhangi bir IP adresinden erişilebilir olacaktır.

### 7. Flower Loglarını Kontrol Etme

Flower servisinin loglarını kontrol etmek için aşağıdaki komutları kullanabilirsiniz:

    sudo journalctl -u flower.service
    
### 8. Flower ile Kullanılabilecek Diğer Parametreler



    --broker=redis://localhost:6379/0: Broker URL'sini belirtmek için.
    --address=0.0.0.0: Tüm IP adreslerinden erişim sağlamak için.
    --port=5555: Çalışacağı portu belirtmek için.
    --basic_auth=user:pass: Kimlik doğrulama eklemek için.
    --persistent: Flower oturum verilerini ve durumunu diske yazması için.

#### 9. Flower Arayüzüne Erişme
Flower arayüzüne erişmek için tarayıcınızdan şu URL'yi ziyaret edebilirsiniz:

    http://localhost:5555/
    
Eğer --address=0.0.0.0 parametresi ile çalıştırdıysanız, IP adresinizi ve portu kullanarak Flower'a erişebilirsiniz:

    http://sunucu_ip_adresi:5555/



