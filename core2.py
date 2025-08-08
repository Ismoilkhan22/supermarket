class Card:
    def __init__(self, seria, password, balans):
        self.seria = seria
        self.password = password
        self.balans = balans


class User:
    def __init__(self, username, password, phone, is_admin, is_user):
        self.username = username
        self.password = password
        self.phone = phone
        self.cards = []
        self.products = []
        self.is_admin = is_admin
        self.is_user = is_user

    def add_card(self):
        seria = input("seria:")
        password = input("password:")
        balans = input("balans:")
        card = Card(seria, password, balans)
        self.cards.append(card)


class Products:
    def __init__(self, title, price, count):
        self.title = title
        self.price = price
        self.count = count


class Market:
    def __init__(self, title, ):
        self.title = title
        self.balans = 0
        self.user = []
        self.product = []

    def add_user(self):
        username = input("username: ")
        password = input("password: ")
        phone = input("phone: ")
        user = User(username, password, phone, False, True)
        self.user.append(user)
        return user

    def login(self, username, password):
        for item in self.user:
            if item.username == username and item.password == password:
                return True
        return False


market = Market("b1")
pro1 = Products('olma', "10000", '100')
pro2 = Products('olcha', "12000", '100')
pro3 = Products('kartoshka', "7000", '100')
pro4 = Products('pamidor', "5000", '100')
market.product.append(pro1)
market.product.append(pro2)
market.product.append(pro3)
market.product.append(pro4)
user1 = User("admin", "123", "12345675432", True, False)
user2 = User("ali", "123", "12345675432", False, True)
user3 = User("vali", "123", "12345675432", False, True)
market.user.append(user1)
market.user.append(user2)
market.user.append(user3)


def manager_market(market1: Market):
    while True:
        kod1 = input(" 1. Register \n 2. Login \n 3. Logout :")
        if kod1 == "1":
           user = market1.add_user()
           user.add_card()
        elif kod1 == "2":
            username = input("username: ")
            password = input("password: ")

            if market1.login(username, password):
                activ_user = None
                for item in market1.user:
                    if item.username and item.password:
                        activ_user = item
                        break
                print("==============",activ_user.is_admin,activ_user.username)
                if activ_user.is_admin:
                    pass
                else:
                    while True:
                        kod2 = input("TO'XTA")
            else:
                print("======= username yoki password xato =======")
        else:
            print("Rahmat!")
            break


if __name__=="__main__":
    manager_market(market)
