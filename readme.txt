Loyiha nomi: YouTube Download and Search API (Django REST Framework asosida)

=========================================
📌 Loyihaga qisqacha izoh:
Ushbu loyiha Django REST Framework yordamida tuzilgan bo‘lib, YouTube videolarini qidirish, formatlarini olish, audio/video shaklida yuklab olish imkonini beradigan API xizmatini taqdim etadi. Barcha asosiy API logikasi `api/views.py` faylida joylashgan.

API tashqi xizmat bilan quyidagi URL orqali ishlaydi:
http://4532381-xa58658.twc1.net/
➡ Ushbu URL'ni o‘zgartirish shart (quyida batafsil).

=========================================
🚀 O‘rnatish va ishga tushirish:

1. Loyihani yuklab oling:
   git clone https://github.com/AlijonovUz/youtube.git

2. Loyiha fayllarini "YouTube" nomli papkaga joylashtiring:
   Masalan:
   ~/Projects/YouTube/

3. Terminal yoki CMD orqali papkaga o‘ting:
   cd youtube_download_and_search

4. Virtual muhit yarating va faollashtiring:
   python -m venv venv
   Linux/macOS: source venv/bin/activate
   Windows: venv\Scripts\activate

5. Kutubxonalarni o‘rnating:
   pip install -r requirements.txt

6. Django migratsiyalarini bajaring:
   python manage.py migrate

7. Serverni ishga tushiring:
   python manage.py runserver

=========================================
🔄 Fon rejimida (background) ishga tushirish:

Linux/macOS tizimlarida:
   nohup python manage.py runserver 0.0.0.0:8000 &

Bu holatda server fon rejimida ishlaydi va chiqishlar `nohup.out` fayliga yoziladi.

Windows (PowerShell) uchun:
   Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py", "runserver"

=========================================
🛠️ API URL manzillarni o‘zgartirish:

`api/views.py` faylini oching va undagi quyidagi URL manzillarni:

   http://4532381-xa58658.twc1.net/

o‘rniga kerakli manzilingiz bilan almashtiring, masalan:
   http://localhost:9000/

Eslatma: bunday URL’lar bir nechta joyda ishlatilgan bo‘lishi mumkin, ularning barchasini topib, yangilab chiqing.

=========================================
📬 API Endpointlar (batafsil):

1. 🔎 Video qidirish:
   Endpoint: `GET /api/search/`
   Parametrlar:
     - `title`: qidirilayotgan video nomi (majburiy)
     - `page`: sahifa raqami (ixtiyoriy)
   Misol:
     `/api/search/?title=python+darslik&page=2`

2. 🎵 Faqat audio faylni yuklab olish:
   Endpoint: `POST /api/audio/`
   JSON parametrlari:
     - `url`: YouTube video havolasi (majburiy)
   Misol:
   ```json
   {
     "url": "https://www.youtube.com/watch?v=abc123"
   }
🎥 Video formatlar ro‘yxatini olish:
Endpoint: POST /api/video/formats/
JSON parametrlari:

url: YouTube video havolasi (majburiy)
Misol:

json
Copy
Edit
{
  "url": "https://www.youtube.com/watch?v=abc123"
}
📥 Video yuklab olish:
Endpoint: POST /api/video/download/
JSON parametrlari:

url: YouTube video havolasi (majburiy)

format_id: kerakli format ID (majburiy)
Misol:

json
Copy
Edit
{
  "url": "https://www.youtube.com/watch?v=abc123",
  "format_id": "18"
}
=========================================
📁 Papka tuzilmasi:

Loyiha quyidagicha tartibda saqlanishi tavsiya qilinadi:

https://example.uz/
└── YouTube/
├── api/
├── search/
├── manage.py
└── README.txt

Bu tartib loyiha ichidagi yo‘llar va importlarda xatolik bo‘lmasligi uchun zarurdir.

=========================================
🔒 Xavfsizlik tavsiyalari:

Agar loyihani internet orqali ochmoqchi bo‘lsangiz:

settings.py ichida DEBUG = False qiling

ALLOWED_HOSTS ro‘yxatiga domen nomini kiriting

Tashqi xizmatlar xavfsiz va autentifikatsiyalangan bo‘lishi lozim

Eslatma: media/ papkasiga yuklangan audio/video fayllar yuklangan vaqtdan boshlab, 1 daqiqa o'tgach avtomatik tarzda o'chirilib yuboriladi! Bu vaqtni o'zgartirish mumkin, lekin server to'lib ketmasligi uchun default holatda shunday qilib sozlangan.

=========================================
✅ TAYYOR!
Endi siz YouTube videolarini qidirish, formatlarini ko‘rish va yuklab olish imkoniyatiga ega API’dan foydalanishingiz mumkin!
