import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

# .env dosyasından token'ı yükle
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Kullanıcı verilerini yükle
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

# Kullanıcı verilerini kaydet
def save_users(users_data):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

# Veritabanı
RECIPES = {
    # Ana Yemekler
    'makarna': {
        'title': 'Soslu Makarna',
        'ingredients': ['500g makarna', '2 yemek kaşığı zeytinyağı', '2 diş sarımsak', 'Tuz', '1 yemek kaşığı tereyağı', 'Rendelenmiş parmesan peyniri'],
        'instructions': [
            'Makarnayı kaynar suda haşlayın',
            'Sarımsakları ince ince doğrayın',
            'Zeytinyağında sarımsakları kavurun',
            'Haşlanmış makarnayı ekleyip karıştırın',
            'Tereyağı ve parmesan peyniri ekleyip servis yapın'
        ],
        'category': 'ana_yemek',
        'prep_time': '10 dakika',
        'cook_time': '15 dakika',
        'servings': '4 kişilik'
    },
    'pizza': {
        'title': 'Ev Yapımı Pizza',
        'ingredients': ['2 su bardağı un', '1 paket maya', '1 su bardağı ılık su', '1 yemek kaşığı zeytinyağı', 'Tuz', 'Domates sosu', 'Mozzarella peyniri', 'Sucuk', 'Mantar', 'Biber'],
        'instructions': [
            'Maya ılık suda eritilir',
            'Un, tuz ve zeytinyağı eklenir',
            'Hamur yoğrulur',
            '1 saat mayalanmaya bırakılır',
            'Hamur açılır ve tepsiye yerleştirilir',
            'Domates sosu sürülür',
            'Malzemeler yerleştirilir',
            '200 derece fırında 20 dakika pişirilir'
        ],
        'category': 'ana_yemek',
        'prep_time': '20 dakika',
        'cook_time': '20 dakika',
        'servings': '4 kişilik'
    },
    'köfte': {
        'title': 'Izgara Köfte',
        'ingredients': ['500g kıyma', '1 adet soğan', '1 yumurta', '2 dilim bayat ekmek', 'Tuz, karabiber', 'Kimyon', 'Pul biber'],
        'instructions': [
            'Soğan rendelenir',
            'Bayat ekmek ıslatılıp sıkılır',
            'Tüm malzemeler karıştırılır',
            'Köfteler şekillendirilir',
            'Izgarada veya tavada pişirilir',
            'Yanında pilav ve salata ile servis yapılır'
        ],
        'category': 'ana_yemek',
        'prep_time': '15 dakika',
        'cook_time': '15 dakika',
        'servings': '4 kişilik'
    },
    'karniyarik': {
        'title': 'Karnıyarık',
        'ingredients': ['6 adet patlıcan', '300g kıyma', '2 adet soğan', '2 adet domates', '2 adet biber', 'Sarımsak', 'Zeytinyağı', 'Tuz, karabiber'],
        'instructions': [
            'Patlıcanlar alacalı soyulur',
            'Kızgın yağda kızartılır',
            'Kıyma, soğan ve sarımsak kavrulur',
            'Domates ve biber eklenir',
            'Patlıcanlar ortadan yarılır',
            'İçine kıymalı harç doldurulur',
            'Fırında pişirilir'
        ],
        'category': 'ana_yemek',
        'prep_time': '20 dakika',
        'cook_time': '30 dakika',
        'servings': '6 kişilik'
    },
    'musakka': {
        'title': 'Patlıcan Musakka',
        'ingredients': ['6 adet patlıcan', '300g kıyma', '2 adet soğan', '2 adet domates', '2 adet biber', 'Sarımsak', 'Zeytinyağı', 'Tuz, karabiber'],
        'instructions': [
            'Patlıcanlar alacalı soyulur',
            'Kızgın yağda kızartılır',
            'Kıyma, soğan ve sarımsak kavrulur',
            'Domates ve biber eklenir',
            'Patlıcanlar dilimlenir',
            'Tepsiye dizilir',
            'Üzerine kıymalı harç dökülür',
            'Fırında pişirilir'
        ],
        'category': 'ana_yemek',
        'prep_time': '20 dakika',
        'cook_time': '30 dakika',
        'servings': '6 kişilik'
    },
    
    # Çorbalar
    'mercimek': {
        'title': 'Mercimek Çorbası',
        'ingredients': ['1 su bardağı kırmızı mercimek', '1 adet soğan', '1 adet havuç', '1 adet patates', '2 yemek kaşığı un', 'Tereyağı', 'Tuz, karabiber', 'Kırmızı biber'],
        'instructions': [
            'Mercimek yıkanır',
            'Soğan, havuç ve patates doğranır',
            'Tereyağında soğan kavrulur',
            'Un eklenip kavrulur',
            'Mercimek ve sebzeler eklenir',
            'Su eklenip pişirilir',
            'Blenderdan geçirilir',
            'Üzerine kırmızı biberli yağ gezdirilir'
        ],
        'category': 'corba',
        'prep_time': '10 dakika',
        'cook_time': '30 dakika',
        'servings': '6 kişilik'
    },
    'ezogelin': {
        'title': 'Ezogelin Çorbası',
        'ingredients': ['1 su bardağı kırmızı mercimek', '1/2 su bardağı pirinç', '1 adet soğan', '2 yemek kaşığı salça', 'Tereyağı', 'Nane', 'Tuz, karabiber'],
        'instructions': [
            'Mercimek ve pirinç yıkanır',
            'Soğan doğranır',
            'Tereyağında soğan kavrulur',
            'Salça eklenir',
            'Mercimek ve pirinç eklenir',
            'Su eklenip pişirilir',
            'Nane eklenir'
        ],
        'category': 'corba',
        'prep_time': '10 dakika',
        'cook_time': '30 dakika',
        'servings': '6 kişilik'
    },
    'yayla': {
        'title': 'Yayla Çorbası',
        'ingredients': ['1 su bardağı pirinç', '1 su bardağı yoğurt', '1 yumurta', '2 yemek kaşığı un', 'Tereyağı', 'Nane', 'Tuz'],
        'instructions': [
            'Pirinç yıkanıp haşlanır',
            'Yoğurt, yumurta ve un çırpılır',
            'Haşlanmış pirince eklenir',
            'Tereyağında nane kavrulur',
            'Üzerine dökülür'
        ],
        'category': 'corba',
        'prep_time': '10 dakika',
        'cook_time': '20 dakika',
        'servings': '6 kişilik'
    },
    'tarhana': {
        'title': 'Tarhana Çorbası',
        'ingredients': ['1 su bardağı tarhana', '1 yemek kaşığı salça', 'Tereyağı', 'Nane', 'Tuz'],
        'instructions': [
            'Tarhana ılık suda ıslatılır',
            'Tereyağında salça kavrulur',
            'Tarhana eklenir',
            'Su eklenip pişirilir',
            'Nane eklenir'
        ],
        'category': 'corba',
        'prep_time': '5 dakika',
        'cook_time': '15 dakika',
        'servings': '6 kişilik'
    },
    'domates': {
        'title': 'Domates Çorbası',
        'ingredients': ['4 adet domates', '1 adet soğan', '2 yemek kaşığı un', 'Tereyağı', 'Karabiber', 'Tuz'],
        'instructions': [
            'Domatesler rendelenir',
            'Soğan doğranır',
            'Tereyağında soğan kavrulur',
            'Un eklenip kavrulur',
            'Domates eklenir',
            'Su eklenip pişirilir',
            'Blenderdan geçirilir'
        ],
        'category': 'corba',
        'prep_time': '10 dakika',
        'cook_time': '20 dakika',
        'servings': '6 kişilik'
    },
    
    # Salatalar
    'sezar': {
        'title': 'Sezar Salata',
        'ingredients': ['1 adet marul', '1 su bardağı kruton', 'Parmesan peyniri', 'Sezar sos', 'Tavuk göğsü', 'Tuz, karabiber'],
        'instructions': [
            'Marul yıkanıp doğranır',
            'Tavuk göğsü ızgara yapılır',
            'Marul, kruton ve tavuk karıştırılır',
            'Sezar sos eklenir',
            'Üzerine parmesan rendelenir'
        ],
        'category': 'salata',
        'prep_time': '15 dakika',
        'cook_time': '10 dakika',
        'servings': '2 kişilik'
    },
    'coban': {
        'title': 'Çoban Salata',
        'ingredients': ['2 adet domates', '2 adet salatalık', '1 adet soğan', '2 adet biber', 'Zeytinyağı', 'Limon suyu', 'Tuz'],
        'instructions': [
            'Tüm sebzeler küp küp doğranır',
            'Soğan ince ince doğranır',
            'Malzemeler karıştırılır',
            'Zeytinyağı ve limon suyu eklenir',
            'Tuz ile tatlandırılır'
        ],
        'category': 'salata',
        'prep_time': '10 dakika',
        'cook_time': '0 dakika',
        'servings': '4 kişilik'
    },
    'rus': {
        'title': 'Rus Salatası',
        'ingredients': ['2 adet havuç', '2 adet patates', '1 kutu bezelye', '1 kutu mısır', 'Mayonez', 'Tuz'],
        'instructions': [
            'Havuç ve patates haşlanır',
            'Küp küp doğranır',
            'Bezelye ve mısır eklenir',
            'Mayonez ile karıştırılır',
            'Tuz ile tatlandırılır'
        ],
        'category': 'salata',
        'prep_time': '15 dakika',
        'cook_time': '20 dakika',
        'servings': '6 kişilik'
    },
    'akdeniz': {
        'title': 'Akdeniz Salatası',
        'ingredients': ['1 adet marul', '1 adet domates', '1 adet salatalık', 'Zeytin', 'Peynir', 'Zeytinyağı', 'Limon suyu', 'Tuz'],
        'instructions': [
            'Marul yıkanıp doğranır',
            'Domates ve salatalık doğranır',
            'Zeytin ve peynir eklenir',
            'Zeytinyağı ve limon suyu eklenir',
            'Tuz ile tatlandırılır'
        ],
        'category': 'salata',
        'prep_time': '10 dakika',
        'cook_time': '0 dakika',
        'servings': '4 kişilik'
    },
    'mevsim': {
        'title': 'Mevsim Salatası',
        'ingredients': ['1 adet marul', '1 adet domates', '1 adet salatalık', '1 adet havuç', '1 adet turp', 'Zeytinyağı', 'Limon suyu', 'Tuz'],
        'instructions': [
            'Tüm sebzeler yıkanır',
            'İnce ince doğranır',
            'Malzemeler karıştırılır',
            'Zeytinyağı ve limon suyu eklenir',
            'Tuz ile tatlandırılır'
        ],
        'category': 'salata',
        'prep_time': '15 dakika',
        'cook_time': '0 dakika',
        'servings': '4 kişilik'
    },
    
    # Tatlılar
    'künefe': {
        'title': 'Künefe',
        'ingredients': ['500g kadayıf', '250g taze peynir', '250g tereyağı', 'Şerbet için: 2 su bardağı şeker, 1 su bardağı su', 'Antep fıstığı'],
        'instructions': [
            'Kadayıf tereyağı ile yağlanır',
            'Yarısı tepsiye serilir',
            'Peynir eklenir',
            'Diğer yarısı kapatılır',
            'Fırında kızartılır',
            'Şerbet dökülür',
            'Antep fıstığı ile süslenir'
        ],
        'category': 'tatli',
        'prep_time': '20 dakika',
        'cook_time': '20 dakika',
        'servings': '6 kişilik'
    },
    'sütlaç': {
        'title': 'Sütlaç',
        'ingredients': ['1 litre süt', '1 su bardağı pirinç', '1 su bardağı şeker', '1 yemek kaşığı nişasta', 'Vanilya'],
        'instructions': [
            'Pirinç yıkanıp haşlanır',
            'Süt eklenir',
            'Şeker ve vanilya eklenir',
            'Nişasta sulandırılıp eklenir',
            'Kıvam alana kadar pişirilir',
            'Fırında üzeri kızartılır'
        ],
        'category': 'tatli',
        'prep_time': '10 dakika',
        'cook_time': '30 dakika',
        'servings': '6 kişilik'
    },
    'revani': {
        'title': 'Revani',
        'ingredients': ['3 adet yumurta', '1 su bardağı şeker', '1 su bardağı yoğurt', '1 su bardağı irmik', '1 su bardağı un', '1 paket kabartma tozu', 'Şerbet için: 2 su bardağı şeker, 2 su bardağı su'],
        'instructions': [
            'Yumurta ve şeker çırpılır',
            'Yoğurt eklenir',
            'İrmik, un ve kabartma tozu eklenir',
            'Fırında pişirilir',
            'Şerbet dökülür'
        ],
        'category': 'tatli',
        'prep_time': '15 dakika',
        'cook_time': '30 dakika',
        'servings': '8 kişilik'
    },
    'irmik': {
        'title': 'İrmik Helvası',
        'ingredients': ['2 su bardağı irmik', '1 su bardağı şeker', '1 su bardağı süt', '100g tereyağı', 'Antep fıstığı'],
        'instructions': [
            'İrmik tereyağında kavrulur',
            'Şeker ve süt eklenir',
            'Kıvam alana kadar pişirilir',
            'Antep fıstığı ile süslenir'
        ],
        'category': 'tatli',
        'prep_time': '10 dakika',
        'cook_time': '20 dakika',
        'servings': '6 kişilik'
    },
    'kadayif': {
        'title': 'Kadayıf Dolması',
        'ingredients': ['500g kadayıf', '250g ceviz', '250g tereyağı', 'Şerbet için: 2 su bardağı şeker, 1 su bardağı su'],
        'instructions': [
            'Kadayıf tereyağı ile yağlanır',
            'Ceviz içi serpilir',
            'Rulo şeklinde sarılır',
            'Fırında kızartılır',
            'Şerbet dökülür'
        ],
        'category': 'tatli',
        'prep_time': '20 dakika',
        'cook_time': '20 dakika',
        'servings': '8 kişilik'
    }
}

CATEGORIES = {
    'ana_yemek': 'Ana Yemek',
    'corba': 'Çorba',
    'tatli': 'Tatlı',
    'salata': 'Salata'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users_data = load_users()
    
    # Kullanıcıyı kaydet
    if str(user.id) not in users_data['users']:
        users_data['users'][str(user.id)] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'join_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'favorites': []
        }
        save_users(users_data)
    
    keyboard = [
        [InlineKeyboardButton("Yemek Tarifleri", callback_data='recipes')],
        [InlineKeyboardButton("Kategoriler", callback_data='categories')],
        [InlineKeyboardButton("Favorilerim", callback_data='favorites')],
        [InlineKeyboardButton("Yardım", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Merhaba {user.first_name}! 👋\n"
        "Ben yemek tarifleri botuyum. Size nasıl yardımcı olabilirim?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'recipes':
        keyboard = []
        for recipe_id, recipe in RECIPES.items():
            keyboard.append([InlineKeyboardButton(recipe['title'], callback_data=f'recipe_{recipe_id}')])
        keyboard.append([InlineKeyboardButton("Geri", callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Mevcut tarifler:", reply_markup=reply_markup)
    
    elif query.data == 'categories':
        keyboard = []
        for cat_id, cat_name in CATEGORIES.items():
            keyboard.append([InlineKeyboardButton(cat_name, callback_data=f'category_{cat_id}')])
        keyboard.append([InlineKeyboardButton("Geri", callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Kategoriler:", reply_markup=reply_markup)
    
    elif query.data.startswith('category_'):
        category_id = query.data.split('_')[1]
        if category_id in CATEGORIES:
            keyboard = []
            for recipe_id, recipe in RECIPES.items():
                if recipe['category'] == category_id:
                    keyboard.append([InlineKeyboardButton(recipe['title'], callback_data=f'recipe_{recipe_id}')])
            keyboard.append([InlineKeyboardButton("Geri", callback_data='categories')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"{CATEGORIES[category_id]} kategorisindeki tarifler:", reply_markup=reply_markup)
    
    elif query.data == 'favorites':
        users_data = load_users()
        user_id = str(update.effective_user.id)
        if user_id in users_data['users'] and users_data['users'][user_id]['favorites']:
            keyboard = []
            for recipe_id in users_data['users'][user_id]['favorites']:
                if recipe_id in RECIPES:
                    keyboard.append([InlineKeyboardButton(RECIPES[recipe_id]['title'], callback_data=f'recipe_{recipe_id}')])
            keyboard.append([InlineKeyboardButton("Geri", callback_data='main_menu')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Favori tarifleriniz:", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("Geri", callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Henüz favori tarifiniz yok.", reply_markup=reply_markup)
    
    elif query.data == 'help':
        help_text = (
            "🤖 Bot Komutları:\n\n"
            "/start - Botu başlat\n"
            "/help - Yardım menüsü\n"
            "/categories - Kategorileri göster\n"
            "/recipes - Tüm tarifleri göster\n\n"
            "Bot özellikleri:\n"
            "• Yemek tarifleri\n"
            "• Kategori bazlı arama\n"
            "• Favori tarifler\n"
            "• Detaylı malzeme listesi\n"
            "• Adım adım yapılış\n"
            "• Hazırlama ve pişirme süreleri\n"
            "• Kişi sayısı bilgisi"
        )
        keyboard = [[InlineKeyboardButton("Geri", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(help_text, reply_markup=reply_markup)
    
    elif query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("Yemek Tarifleri", callback_data='recipes')],
            [InlineKeyboardButton("Kategoriler", callback_data='categories')],
            [InlineKeyboardButton("Favorilerim", callback_data='favorites')],
            [InlineKeyboardButton("Yardım", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ana menü:", reply_markup=reply_markup)
    
    elif query.data.startswith('recipe_'):
        recipe_id = query.data.split('_')[1]
        if recipe_id in RECIPES:
            recipe = RECIPES[recipe_id]
            text = (
                f"🍳 {recipe['title']}\n\n"
                f"⏱️ Hazırlama: {recipe['prep_time']}\n"
                f"🔥 Pişirme: {recipe['cook_time']}\n"
                f"👥 {recipe['servings']}\n\n"
                f"📋 Malzemeler:\n" + "\n".join(f"• {ing}" for ing in recipe['ingredients']) + "\n\n"
                f"👨‍🍳 Yapılışı:\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe['instructions']))
            )
            
            keyboard = [
                [InlineKeyboardButton("Favorilere Ekle", callback_data=f'add_fav_{recipe_id}')],
                [InlineKeyboardButton("Geri", callback_data='recipes')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
    
    elif query.data.startswith('add_fav_'):
        recipe_id = query.data.split('_')[2]
        users_data = load_users()
        user_id = str(update.effective_user.id)
        
        if user_id in users_data['users']:
            if recipe_id not in users_data['users'][user_id]['favorites']:
                users_data['users'][user_id]['favorites'].append(recipe_id)
                save_users(users_data)
                await query.answer("Tarif favorilere eklendi! ✅")
            else:
                await query.answer("Bu tarif zaten favorilerinizde! ⚠️")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    # Bot uygulamasını başlat
    application = Application.builder().token(TOKEN).build()

    # Komut işleyicileri
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Botu başlat
    application.run_polling()

if __name__ == '__main__':
    main() 