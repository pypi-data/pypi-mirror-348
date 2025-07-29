"""
Sample Python file for testing patches with both additions and removals.
This is the modified version with both added and removed lines.
"""

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.prices = {}
        self.quantities = {}
        self.discount = 0
        self.tax_rate = 0
    
    def add_item(self, item, price, quantity=1):
        """Add an item to the shopping cart."""
        if item in self.items:
            self.quantities[item] += quantity
        else:
            self.items.append(item)
            self.prices[item] = price
            self.quantities[item] = quantity
        
        print(f"Added {quantity} {item}(s) to cart.")
    
    # The remove_item method has been removed in this version
    
    def apply_discount(self, percent):
        """Apply a discount to the cart."""
        self.discount = percent
        print(f"Applied {percent}% discount to cart.")
    
    def apply_tax(self, rate):
        """Apply a tax rate to the cart."""
        self.tax_rate = rate
        print(f"Applied {rate}% tax to cart.")
    
    def calculate_total(self):
        """Calculate the total price of items in the cart."""
        subtotal = sum(self.prices[item] * self.quantities[item] for item in self.items)
        discounted_total = subtotal * (1 - self.discount / 100)
        final_total = discounted_total * (1 + self.tax_rate / 100)
        return round(final_total, 2)
    
    def clear_cart(self):
        """Remove all items from the cart."""
        self.items = []
        self.prices = {}
        self.quantities = {}
        print("Cart has been cleared.")
    
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
        subtotal = sum(self.prices[item] * self.quantities[item] for item in self.items)
        print(f"Subtotal: ${subtotal}")
        
        if self.discount > 0:
            discount_amount = subtotal * (self.discount / 100)
            print(f"Discount: {self.discount}% (-${discount_amount:.2f})")
            discounted_total = subtotal - discount_amount
            print(f"Discounted subtotal: ${discounted_total:.2f}")
        else:
            discounted_total = subtotal
        
        if self.tax_rate > 0:
            tax_amount = discounted_total * (self.tax_rate / 100)
            print(f"Tax: {self.tax_rate}% (+${tax_amount:.2f})")
        
        print(f"Total: ${self.calculate_total()}")


def main():
    # Create a new shopping cart
    cart = ShoppingCart()
    
    # Add some items
    cart.add_item("Apple", 0.99, 5)
    cart.add_item("Banana", 0.59, 3)
    cart.add_item("Orange", 0.79, 4)
    cart.add_item("Grapes", 2.99, 1)
    
    # Display the cart
    cart.display_cart()
    
    # Apply a discount
    cart.apply_discount(15)
    
    # Apply tax
    cart.apply_tax(8)
    
    # Display the cart again
    cart.display_cart()
    
    # Clear the cart
    cart.clear_cart()
    
    # Add new items
    cart.add_item("Milk", 3.49, 1)
    cart.add_item("Bread", 2.29, 2)
    
    # Display the final cart
    cart.display_cart()


if __name__ == "__main__":
    main()
