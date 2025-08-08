import uuid
import datetime



class Product:
    def __init__(self, name,price, quantity):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}-${self.price:.2f} (stock: {self.quantity})"


class CartItem:
    def __init(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return f"{self.quantity}x{self.product.name} - ${self.get_total():.2f}"

class Cart:
    def __init__(self):
        self.items=[]

    def add_item(self, product, quantity):
        if quantity>product.quantity:
            print(f"Error: Only{product.quantity} {product.name} in stock")
            return False
        for item in self.items:
            if item.product.id == product.id:
                item.quantity +=quantity
                product.quantity-=quantity
                return True
        self.items.append(CartItem(product,quantity))
        product.quantity -=quantity
        return True

    def remove_item(self, product_id, quantity):
        for item in self.items:
            if item.product.id == product_id:
                if quantity>=item.quantity:
                    self.items.remove(item)
                    item.product.quantity += item.quantity
                else:
                    item.quantity -= quantity
                    item.product.quantity += quantity
                return True
        return False

    def get_total(self):
        if not self.items:
            return "cart is empty"
        return "\n".join(str(item) for item in self.items)+f"\nTotal:${self.get_total():.2f}"


class User:
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.cart = Cart()
        self.order_history = []

    def add_to_cart(self, product, quantity):
        return self.cart.add_item(product, quantity)

    def remove_from_cart(self, product_id, quantity):
        return self.cart.remove_item(product_id, quantity)

    def checkout(self, products):
        if not self.cart.items:
            print("Cart is empty. Cannot checkout.")
            return False
        order = {
            "order_id":str(uuid.uuid4()),
            "date":datetime.datetime.now(),
            "items": self.cart.items.copy(),
            "total": self.cart.get_total()
        }
        self.order_history.append(order)
        self.cart = Cart() # Clear cart after checkout
        print("Checkout successful!")
        return True

    def view_order_history(self):
        if not self.order_history:
            return "no orders yet"
        result = []
        for order in self.order_history:
            order_str = f"Order ID: {order['order_id']}\nDate: {order['date']}\nItems:\n"
            order_str+="\n".join(str(item) for item in order['items'])
            order_str+= f"\n Total: ${order['total']:.2f}\n"
            result.append(order_str)
        return "\n".join(result)


class OnlineShop:
    def __init__(self):
        self.products = []
        self.users = []

    def add_product(self, name, price, quantity):
        product = Product(name, price, quantity)
        self.products.append(product)
        return product

    def register_user(self, username, passwords):
        for user in self.users:
            if user.username == username:
                print("Username already exists")
                return None
        user = User(username, passwords)
        self.users.append(User)
        return user

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        print("invalid username or password")
        return None

    def display_products(self):
        if not self.products:
            return "No products available"
        return "\n".join(f"ID:{p.id[:8]} - {str(p)}" for p in self.products)


def main():
    shop = OnlineShop()
    shop.add_product("Apple", 0.50, 100)
    shop.add_product("Banana", 0.30, 150)
    shop.add_product("milk", 2.99, 50)

    current_user = None
    while True:
        print("\n=== Online Shop ===")
        if current_user:
            print(f"Logged in as:{current_user.username}")
            print("1. View Product")
            print("2. View Cart")
            print("3. add to Cart")
            print("4. Remove from cart")
            print("5. checkout")
            print("6. view order history")
            print("7. Logout")
        else:
            print("1. Register")
            print("2. Login")
            print("3. view products")
            print("4. Exit")
        choice = input("Enter choice (1-7):")

        if not current_user:
            if choice == "1":
                username = input("Enter username:")
                password = input("Enter password:")
                user = shop.register_user(username, password)
                if user:
                    print(f"User {username} registered successfully")
            elif choice == "2":
                username = input("Enter username: ")
                password = int(input("Enter password: "))
                user = shop.login(username, password)
                if user:
                    current_user = user
                    print(f"Welcome, {username}! ")

            elif choice == "3":
                print(shop.display_products())

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("invalid choice")

        else:
            if choice == "1":
                print(shop.display_products())

            elif choice == "2":
                print(current_user.cart)

            elif choice == "3":
                print(shop.display_products())
                product_id = input("Enter product ID: ")
                quantity = int(input("Enter quantity: "))
                for product in shop.products:
                    if product.id.startswith(product_id):
                        if current_user.add_to_cart(product, quantity):
                            print("Added to cart successfully")
                        break

                    else:
                        print("product not found")

            elif choice == "4":
                print(current_user.cart)
                product_id = input("Enter product Id: ")
                quantity = int(input("Enter quantity to remove: "))
                if current_user.remove_cart(product_id, quantity):
                    print("removed from cart successfully")
                else:
                    print("product not found in cart")

            elif choice == "5":
                print(current_user.cart)
                confirm = input("Proceed to checkout? (y/n): ")
                if confirm.lower() == 'y':
                    current_user.checkout(shop.products)

            elif choice == '6':
                print(current_user.view_order_history())

            elif choice == '7':
                current_user= None
                print("Logged out successfully")

            else:
                print("invalid choice")

if __name__ =="__main__":
    main()