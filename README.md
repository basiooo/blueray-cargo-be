# Blueray cargo test

# Cara menjalankan aplikasi
 - Dengan docker
   - jalankan perintah ```docker-compose up```
   - buka browser dengan alamat ```localhost:8000```
 
 - Tanpa docker
   - install package yang diperlukan ```pip install -r requirements.txt```
   - sesuaikan konfigurasi database di ```blueray/settings.py```
   - migrate database dengan perintah ```python manage.py migrate```
   - jalankan server ```python manage.py runserver
   - buka browser dengan alamat ```localhost:8000```

# Menjalankan test
  - Dengan docker 
    - jalankan perintah ```docker-compose --profile test up```

