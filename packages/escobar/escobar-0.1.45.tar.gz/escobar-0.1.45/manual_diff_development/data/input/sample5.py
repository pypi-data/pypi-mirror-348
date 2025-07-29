"""
Sample Python file for testing patches with both additions and removals.
"""

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.prices = {}
        self.quantities = {}
        self.discount = 0
    
    def add_item(self, item, price, quantity=1):
        """Add an item to the shopping cart."""
        if item in self.items:
            self.quantities[item] += quantity
        else:
            self.items.append(item)
            self.prices[item] = price
            self.quantities[item] = quantity
        
        print(f"Added {quantity} {item}(s) to cart.")
    
    def remove_item(self, item, quantity=1):
        """Remove an item from the shopping cart."""
        if item in self.items:
            if self.quantities[item] <= quantity:
                self.items.remove(item)
                del self.prices[item]
                del self.quantities[item]
                print(f"Removed {item} from cart.")
            else:
                self.quantities[item] -= quantity
                print(f"Removed {quantity} {item}(s) from cart.")
        else:
            print(f"{item} not in cart.")
    
    def apply_discount(self, percent):
        """Apply a discount to the cart."""
        self.discount = percent
        print(f"Applied {percent}% discount to cart.")
    
    def calculate_total(self):
        """Calculate the total price of items in the cart."""
        total = sum(self.prices[item] * self.quantities[item] for item in self.items)
        discounted_total = total * (1 - self.discount / 100)
        return round(discounted_total, 2)
    
    def display_cart(self):
        """Display the contents of the cart."""
        if not self.items:
            print("Cart is empty.")
            return
        
        print("Shopping Cart Contents:")
        print("-----------------------")
        for item in self.items:
            print(f"{item}: {self.quantities[item]} x ${self.prices[item]} = ${self.quantities[item] * self.prices[item]}")
        
        print("-----------------------")
        print(f"Subtotal: ${sum(self.prices[item] * self.quantities[item] for item in self.items)}")
        if self.discount > 0:
            print(f"Discount: {self.discount}%")
            print(f"Total: ${self.calculate_total()}")
        else:
            print(f"Total: ${self.calculate_total()}")


def main():
    # Create a new shopping cart
    cart = ShoppingCart()
    
    # Add some items
    cart.add_item("Apple", 0.99, 5)
    cart.add_item("Banana", 0.59, 3)
    cart.add_item("Orange", 0.79, 4)
    
    # Display the cart
    cart.display_cart()
    
    # Apply a discount
    cart.apply_discount(10)
    
    # Display the cart again
    cart.display_cart()
    
    # Remove some items
    cart.remove_item("Banana", 2)
    
    # Display the final cart
    cart.display_cart()


if __name__ == "__main__":
    main()
