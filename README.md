# 🍳 Yemek Tarifi Telegram Botu (v1.0.3)

Bu bot, kullanıcılara çeşitli yemek tarifleri sunan bir Telegram botudur. Kullanıcılar tarifleri kategorilere göre görüntüleyebilir, favorilerine ekleyebilir ve detaylı tarif bilgilerine ulaşabilirler.

## 🚀 Özellikler

- Ana yemek, çorba, tatlı ve salata kategorileri
- Her tarif için detaylı malzeme listesi
- Adım adım yapılış talimatları
- Hazırlama ve pişirme süreleri
- Porsiyon bilgisi
- Favori tarif kaydetme
- Kategori bazlı filtreleme

## 🔄 Gelecek Güncellemeler

Bot sürekli olarak geliştirilmektedir. İşte yakında eklenecek bazı özellikler:

- 📱 Resimli tarifler
- 🔍 Gelişmiş arama sistemi
- 📊 Kalori hesaplayıcı
- 🌍 Çoklu dil desteği
- 🏷️ Diyet etiketleri (Vejetaryen, Vegan, Glutensiz)
- 💬 Kullanıcı yorumları ve puanlama sistemi
- 📝 Kişisel tarif ekleme özelliği
- 🛒 Alışveriş listesi oluşturma
- 📺 Video tarif desteği
- ⚖️ Porsiyon hesaplayıcı

## 📋 Gereksinimler

- Python 3.8+
- python-telegram-bot
- python-dotenv

## ⚙️ Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/tahamhl/yemek-tarifi-bot.git
cd yemek-tarifi-bot
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
# Windows için
venv\Scripts\activate
# Linux/Mac için
source venv/bin/activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyası oluşturun ve Telegram Bot Token'ınızı ekleyin:
```
TELEGRAM_TOKEN=your_telegram_token_here
```

5. Botu çalıştırın:
```bash
python bot.py
```

## 🤖 Bot Komutları

- `/start` - Botu başlat
- `/help` - Yardım menüsü
- `/categories` - Kategorileri göster
- `/recipes` - Tüm tarifleri göster

## 🔧 Yapılandırma

Bot yapılandırması `bot.py` dosyasında bulunmaktadır. Tarif veritabanı aynı dosya içinde `RECIPES` sözlüğünde tutulmaktadır.

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniözellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: XYZ'`)
4. Branch'inizi push edin (`git push origin feature/yeniözellik`)
5. Pull Request oluşturun



## 👥 İletişim

Sorularınız için Issues bölümünü kullanabilir veya bana [Telegram](https://t.me/tahamhl) üzerinden ulaşabilirsiniz.

## 📝 Sürüm Geçmişi

### v1.0.3 (Güncel)
- Kategori sistemi iyileştirildi
- Favori tarif sistemi eklendi
- Performans optimizasyonları yapıldı

### v1.0.2
- Yeni tarifler eklendi
- Hata düzeltmeleri yapıldı

### v1.0.1
- İlk kararlı sürüm
- Temel bot fonksiyonları
- Basit tarif veritabanı

### v1.0.0
- İlk beta sürümü 