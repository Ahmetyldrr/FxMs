Sanal Ortamın aktive edilmesi

    source myenv/bin/activate
    
Service dosyalarının tekrar başlatılması

    sudo systemctl restart flower
    sudo systemctl restart celery
    sudo systemctl restart celerybeat
    sudo systemctl restart redis-server

Log dosyalarının incelenmesi

    journalctl -u flower -n 5
    journalctl -u celery -n 5
    journalctl -u celerybeat -n 5
    journalctl -u redis-server -n 5

