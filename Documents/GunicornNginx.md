
Ubuntu üzerinde çalışan Django projen için Gunicorn ve Nginx ayarlarını yapabilmen için aşağıdaki adımları izleyebilirsin.

Adım 1: Gunicorn Kurulumu ve Yapılandırılması
Öncelikle Gunicorn'u proje sanal ortamına kurmamız gerekiyor.


# Sanal ortamı aktif et
    cd /home/ahmety/Masaüstü/myenv/
    source myenv/bin/activate

# Gunicorn'u kur
    pip install gunicorn

# Proje dizinine geç
    cd /home/ahmety/Masaüstü/DjangoPro/sofa

# Gunicorn'u çalıştır ve projenin düzgün çalıştığını kontrol et

    gunicorn --bind 0.0.0.0:8000 futbolprojesi.wsgi

Eğer herhangi bir hata almıyorsan, Gunicorn başarılı bir şekilde çalışıyordur. Şimdi Gunicorn için bir systemd servisi oluşturacağız, böylece uygulama sistem açıldığında otomatik olarak başlayacak.

Adım 2: Gunicorn için Systemd Servisi Oluşturma

Bir systemd servisi oluşturarak Gunicorn'u arka planda çalıştırabiliriz:


# Yeni bir systemd servis dosyası oluştur

    sudo nano /etc/systemd/system/gunicorn.service

Servis dosyasının içeriğini aşağıdaki gibi yapılandırın:

    [Unit]
    Description=Gunicorn Daemon for Django Project
    After=network.target
    
    [Service]
    User=ahmet
    Group=www-data
    WorkingDirectory=/home/ahmet/sofa
    ExecStart=/home/ahmet/myenv/bin/gunicorn --workers 3 --bind unix:/home/ahmet/sofa/gunicorn.sock sofa.wsgi:application
    
    [Install]
    WantedBy=multi-user.target



    
    Açıklamalar:

User ve Group: Projeyi çalıştıracak kullanıcı (ahmety) ve grup (www-data).
WorkingDirectory: Projenin dizinini belirtiyor.
ExecStart: Gunicorn'un çalıştırma komutunu içeriyor.
Servis dosyasını kaydedip kapattıktan sonra şu komutlarla servisi etkinleştirin ve başlatın:


# Servisi yeniden yükle

    sudo systemctl daemon-reload

# Gunicorn servisini başlat

    sudo systemctl start gunicorn

# Servisin sistem açılışında başlamasını sağla

    sudo systemctl enable gunicorn

# Gunicorn servisi durumunu kontrol et

    sudo systemctl status gunicorn

Adım 3: Nginx Yapılandırması
Nginx'i ters proxy olarak ayarlayacağız. Öncelikle Nginx'i kuralım:

# Nginx'i kur
    sudo apt install nginx -y

# Nginx servisini başlat

    sudo systemctl start nginx

Daha sonra, Nginx için bir konfigürasyon dosyası oluşturacağız:


# Yeni bir Nginx konfigürasyon dosyası oluştur

    sudo nano /etc/nginx/sites-available/sofa

# Konfigürasyon dosyasının içeriği
    server {
        listen 80;
        server_name _;
    
        location / {
            proxy_pass http://unix:/home/ahmety/Masaüstü/DjangoPro/sofa/gunicorn.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    
        location /static/ {
            alias /home/ahmety/Masaüstü/DjangoPro/sofa/static/;
        }
    
        location /media/ {
            alias /home/ahmety/Masaüstü/DjangoPro/sofa/media/;
        }
    }
    
Açıklamalar:

server_name _; ifadesi, tüm gelen talepleri kabul eder.
proxy_pass direktifi ile Nginx, Gunicorn'un Unix soketine bağlanır.
location /static/ ve location /media/ kısımları, statik ve medya dosyalarını sunar.
Konfigürasyon dosyasını kaydedip kapattıktan sonra şu komutları çalıştırın:


# Konfigürasyon dosyasını etkinleştir

    sudo ln -s /etc/nginx/sites-available/sofa /etc/nginx/sites-enabled

# Varsayılan Nginx konfigürasyon dosyasını kaldır
    sudo rm /etc/nginx/sites-enabled/default

# Nginx yapılandırmasını test et
    sudo nginx -t

# Nginx'i yeniden başlat
    
    sudo systemctl restart nginx

Adım 4: Güvenlik Duvarı Ayarları (Opsiyonel)
Eğer bir güvenlik duvarı (ufw) kullanıyorsanız, Nginx'in HTTP ve HTTPS bağlantılarını kabul etmesini sağlamalısınız:


# Nginx için gerekli izinleri ekle
    
    sudo ufw allow 'Nginx Full'
    
Adım 5: Hata Ayıklama ve Log Kontrolü
Eğer herhangi bir sorun yaşarsanız aşağıdaki komutlarla log dosyalarını kontrol edebilirsiniz:

# Gunicorn log dosyasını kontrol et

    journalctl -u gunicorn

# Nginx hata ve erişim loglarını kontrol et
    sudo tail -f /var/log/nginx/error.log
    sudo tail -f /var/log/nginx/access.log
