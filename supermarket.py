import uuid
import re
from datetime import datetime

class Card:
    def __init__(self, seria, password, balance):
        self.seria = seria
        self.password = password
        self.balance = float(balance) if balance else 0.0

class PurchaseHistory: # tarix uchun
    def __init__(self, user, product, count, total_price, date):
        self.id = str(uuid.uuid4())
        self.user = user
        self.product = product
        self.count = count
        self.total_price = total_price
        self.date = date
        self.purchased = False

class User:
    def __init__(self, username, password, phone, is_admin, is_user):
        self.username = username
        self.password = password
        self.phone = phone
        self.is_admin = is_admin
        self.is_user = is_user
        self.cards = []
        self.cart = []
        self.purchase_history = []

    def add_card(self):
        while True:
            try:
                seria = input("Karta seriyasini kiriting (masalan, 1234-5678): ")
                if not re.match(r"^\d{4}-\d{4}$", seria):
                    print("Noto'g'ri seriya formati! XXXX-XXXX dan foydalaning.")
                    continue
                password = input("Karta parolini kiriting (kamida 4 ta belgi): ")
                if len(password) < 4:
                    print("Parol kamida 4 ta belgi bo'lishi kerak!")
                    continue
                balance = input("Karta balansini kiriting (raqamli): ")
                balance = float(balance)
                if balance < 0:
                    print("Balans salbiy bo'lmasligi kerak!")
                    continue
                card = Card(seria, password, balance)
                self.cards.append(card)
                print(f"{seria} kartasi muvaffaqiyatli qo'shildi!")
                break
            except ValueError:
                print("Noto'g'ri kirish! Balans uchun to'g'ri raqam kiriting.")
            except Exception as e:
                print(f"Xato yuz berdi: {e}. Qayta urinib ko'ring.")

class Product:
    def __init__(self, title, price, count):
        self.id = str(uuid.uuid4())
        self.title = title
        self.price = float(price) if price else 0.0
        self.count = int(count) if count else 0

class Market:
    def __init__(self, title):
        self.title = title
        self.balance = 0.0
        self.users = []
        self.products = []
        self.purchase_history = []

    def add_user(self):
        while True:
            try:
                username = input("Foydalanuvchi nomini kiriting (harf-raqam, 3-20 ta belgi): ")
                if not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
                    print("Foydalanuvchi nomi 3-20 ta harf-raqam bo'lishi kerak!")
                    continue
                if any(user.username == username for user in self.users):
                    print("Bunday foydalanuvchi nomi mavjud!")
                    continue
                password = input("Parolni kiriting (kamida 4 ta belgi): ")
                if len(password) < 4:
                    print("Parol kamida 4 ta belgi bo'lishi kerak!")
                    continue
                phone = input("Telefon raqamini kiriting (+998 va 9 ta raqam): ")
                if not re.match(r"^\+998\d{9}$", phone):
                    print("Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak!")
                    continue
                user = User(username, password, phone, False, True)
                self.users.append(user)
                print(f"{username} foydalanuvchisi muvaffaqiyatli ro'yxatdan o'tkazildi!")
                return user
            except Exception as e:
                print(f"Xato yuz berdi: {e}. Qayta urinib ko'ring.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def add_product(self, title, price, count):
        try:
            price = float(price)
            count = int(count)
            if price < 0 or count < 0:
                print("Narx va son salbiy bo'lmasligi kerak!")
                return
            product = Product(title, price, count)
            self.products.append(product)
            print(f"{title} mahsuloti muvaffaqiyatli qo'shildi!")
        except ValueError:
            print("Noto'g'ri narx yoki son! Raqamli qiymatlarni kiriting.")

    def update_product(self, product_id, title=None, price=None, count=None):
        for product in self.products:
            if product.id == product_id:
                try:
                    if title:
                        product.title = title
                    if price:
                        product.price = float(price)
                        if product.price < 0:
                            print("Narx salbiy bo'lmasligi kerak!")
                            return
                    if count:
                        product.count = int(count)
                        if product.count < 0:
                            print("Son salbiy bo'lmasligi kerak!")
                            return
                    print(f"{product.title} mahsuloti muvaffaqiyatli yangilandi!")
                    return
                except ValueError:
                    print("Noto'g'ri narx yoki son! Raqamli qiymatlarni kiriting.")
                    return
        print("Mahsulot topilmadi!")

    def display_products(self):
        if not self.products:
            print("Mahsulotlar yo'q!")
            return
        print("\nMavjud Mahsulotlar:")
        for product in self.products:
            print(f"ID: {product.id}, Nom: {product.title}, Narx: {product.price}, Son: {product.count}")

def admin_menu(market):
    while True:
        print("\nAdmin Menyusi:")
        print("1. Mahsulot qo'shish")
        print("2. Mahsulotni yangilash")
        print("3. Mahsulotlarni ko'rish")
        print("4. Do'kon balansini ko'rish")
        print("5. Barcha xarid tarixini ko'rish")
        print("6. Chiqish")
        choice = input("Tanlovni kiriting: ")
        if choice == "1":
            title = input("Mahsulot nomini kiriting: ")
            price = input("Mahsulot narxini kiriting: ")
            count = input("Mahsulot sonini kiriting: ")
            market.add_product(title, price, count)
        elif choice == "2":
            market.display_products()
            product_id = input("Yangilash uchun mahsulot ID sini kiriting: ")
            title = input("Yangi nomni kiriting (o'tkazib yuborish uchun Enter): ")
            price = input("Yangi narxni kiriting (o'tkazib yuborish uchun Enter): ")
            count = input("Yangi sonni kiriting (o'tkazib yuborish uchun Enter): ")
            market.update_product(product_id, title or None, price or None, count or None)
        elif choice == "3":
            market.display_products()
        elif choice == "4":
            print(f"Do'kon Balansi: {market.balance}")
        elif choice == "5":
            if not market.purchase_history:
                print("Xarid tarixi yo'q!")
            else:
                print("\nBarcha Xarid Tarixi:")
                for item in market.purchase_history:
                    status = "Sotib olingan" if item.purchased else "Kutilmoqda"
                    print(f"ID: {item.id}, Foydalanuvchi: {item.user.username}, Mahsulot: {item.product.title}, Son: {item.count}, Jami: {item.total_price}, Sana: {item.date}, Holat: {status}")
        elif choice == "6":
            print("Chiqildi!")
            break
        else:
            print("Noto'g'ri tanlov!")

def user_menu(market, user):
    while True:
        print("\nFoydalanuvchi Menyusi:")
        print("1. Karta qo'shish")
        print("2. Savatni ko'rish")
        print("3. Mahsulotni savatga qo'shish")
        print("4. Savatdan mahsulotni o'chirish")
        print("5. To'lov qilish")
        print("6. Xarid tarixini ko'rish")
        print("7. Kartalarni ko'rish")
        print("8. Chiqish")
        choice = input("Tanlovni kiriting: ")
        if choice == "1":
            user.add_card()
        elif choice == "2":
            if not user.cart:
                print("Savat bo'sh!")
            else:
                print("\nSavat Tarkibi:")
                for item in user.cart:
                    print(f"Mahsulot: {item.product.title}, Son: {item.count}, Jami: {item.total_price}")
        elif choice == "3":
            market.display_products()
            try:
                product_id = input("Savatga qo'shish uchun mahsulot ID sini kiriting: ")
                count = int(input("Miqdorni kiriting: "))
                if count <= 0:
                    print("Miqdor musbat bo'lishi kerak!")
                    continue
                for product in market.products:
                    if product.id == product_id:
                        if product.count >= count:
                            total_price = product.price * count
                            cart_item = PurchaseHistory(user, product, count, total_price, datetime.now())
                            user.cart.append(cart_item)
                            product.count -= count
                            print(f"{product.title} savatga qo'shildi!")
                        else:
                            print("Mahsulot zaxirasi yetarli emas!")
                        break
                else:
                    print("Mahsulot topilmadi!")
            except ValueError:
                print("Noto'g'ri miqdor! Raqamli qiymat kiriting.")
        elif choice == "4":
            if not user.cart:
                print("Savat bo'sh!")
            else:
                print("\nSavat Tarkibi:")
                for i, item in enumerate(user.cart, 1):
                    print(f"{i}. Mahsulot: {item.product.title}, Son: {item.count}")
                try:
                    index = int(input("O'chirish uchun element raqamini kiriting: ")) - 1
                    if 0 <= index < len(user.cart):
                        removed_item = user.cart.pop(index)
                        removed_item.product.count += removed_item.count
                        print(f"{removed_item.product.title} savatdan o'chirildi!")
                    else:
                        print("Noto'g'ri element raqami!")
                except ValueError:
                    print("Noto'g'ri kirish! Raqamli qiymat kiriting.")
        elif choice == "5":
            if not user.cart:
                print("Savat bo'sh!")
            else:
                print("\nSavat Tarkibi:")
                selected_items = []
                for i, item in enumerate(user.cart, 1):
                    print(f"{i}. Mahsulot: {item.product.title}, Son: {item.count}, Jami: {item.total_price}")
                    buy_choice = input("Bu mahsulotni sotib olasizmi? (ha/yo'q): ").strip().lower()
                    if buy_choice == "ha":
                        selected_items.append(item)
                if not selected_items:
                    print("Hech qanday mahsulot tanlanmadi!")
                else:
                    total = sum(item.total_price for item in selected_items)
                    if not user.cards:
                        print("Karta yo'q! Avval karta qo'shing.")
                    else:
                        print("Kartalar:")
                        for i, card in enumerate(user.cards, 1):
                            print(f"{i}. Seriya: {card.seria}, Balans: {card.balance}")
                        try:
                            card_choice = int(input("Qaysi kartadan to'lov qilasiz? (raqam): ")) - 1
                            if 0 <= card_choice < len(user.cards):
                                chosen_card = user.cards[card_choice]
                                if chosen_card.balance >= total:
                                    chosen_card.balance -= total
                                    market.balance += total
                                    for item in selected_items:
                                        item.purchased = True
                                        user.purchase_history.append(item)
                                        market.purchase_history.append(item)
                                        user.cart.remove(item)
                                    print("Tanlangan mahsulotlar xaridi muvaffaqiyatli! Savat yangilandi.")
                                else:
                                    print("Tanlangan kartada yetarli mablag' yo'q!")
                            else:
                                print("Noto'g'ri tanlov!")
                        except ValueError:
                            print("Noto'g'ri kirish! Raqamli qiymat kiriting.")
        elif choice == "6":
            if not user.purchase_history:
                print("Xarid tarixi yo'q!")
            else:
                print("\nXarid Tarixi:")
                for item in user.purchase_history:
                    status = "Sotib olingan" if item.purchased else "Kutilmoqda"
                    print(f"ID: {item.id}, Mahsulot: {item.product.title}, Son: {item.count}, Jami: {item.total_price}, Sana: {item.date}, Holat: {status}")
        elif choice == "7":
            if not user.cards:
                print("Kartalar yo'q!")
            else:
                print("\nKartalar:")
                for i, card in enumerate(user.cards, 1):
                    print(f"{i}. Seriya: {card.seria}, Balans: {card.balance}")
        elif choice == "8":
            print("Chiqildi!")
            break
        else:
            print("Noto'g'ri tanlov!")

def manager_market(market):
    while True:
        print("\nAsosiy Menyu:")
        print("1. Ro'yxatdan o'tish")
        print("2. Kirish")
        print("3. Chiqish")
        choice = input("Tanlovni kiriting: ")
        if choice == "1":
            user = market.add_user()
            if user:
                print("Hisobingizga karta qo'shing:")
                user.add_card()
        elif choice == "2":
            username = input("Foydalanuvchi nomini kiriting: ")
            password = input("Parolni kiriting: ")
            active_user = market.login(username, password)
            if active_user:
                print(f"Xush kelibsiz, {active_user.username}!")
                if active_user.is_admin:
                    admin_menu(market)
                else:
                    user_menu(market, active_user)
            else:
                print("Noto'g'ri foydalanuvchi nomi yoki parol!")
        elif choice == "3":
            print("Tashrif uchun rahmat!")
            break
        else:
            print("Noto'g'ri tanlov!")

if __name__ == "__main__":
    market = Market("B1 Supermarket")
    # Initial mahsulotlar
    market.add_product("Olma", 10000, 100)
    market.add_product("Olcha", 12000, 100)
    market.add_product("Kartoshka", 7000, 100)
    market.add_product("Pamidor", 5000, 100)
    # Default admin va foydalanuvchilar
    admin = User("admin", "admin123", "+998901234567", True, False)
    user1 = User("ali", "123", "+998901234568", False, True)
    user2 = User("vali", "123", "+998901234569", False, True)
    market.users.extend([admin, user1, user2])
    # Foydalanuvchilarga kartalar qo'shish
    user1.cards.append(Card("1111-5678", "pass1", 500000))
    user2.cards.append(Card("2222-5678", "pass2", 30000))
    manager_market(market)