--- data/input/sample5.py	2025-05-08 12:08:07
+++ data/input/sample5_modified1.py	2025-05-08 12:08:25
@@ -1,5 +1,6 @@
 """
 Sample Python file for testing patches with both additions and removals.
+This is the modified version with both added and removed lines.
 """
 
 class ShoppingCart:
@@ -8,6 +9,7 @@
         self.prices = {}
         self.quantities = {}
         self.discount = 0
+        self.tax_rate = 0
     
     def add_item(self, item, price, quantity=1):
         """Add an item to the shopping cart."""
@@ -20,31 +22,32 @@
         
         print(f"Added {quantity} {item}(s) to cart.")
     
-    def remove_item(self, item, quantity=1):
-        """Remove an item from the shopping cart."""
-        if item in self.items:
-            if self.quantities[item] <= quantity:
-                self.items.remove(item)
-                del self.prices[item]
-                del self.quantities[item]
-                print(f"Removed {item} from cart.")
-            else:
-                self.quantities[item] -= quantity
-                print(f"Removed {quantity} {item}(s) from cart.")
-        else:
-            print(f"{item} not in cart.")
+    # The remove_item method has been removed in this version
     
     def apply_discount(self, percent):
         """Apply a discount to the cart."""
         self.discount = percent
         print(f"Applied {percent}% discount to cart.")
     
+    def apply_tax(self, rate):
+        """Apply a tax rate to the cart."""
+        self.tax_rate = rate
+        print(f"Applied {rate}% tax to cart.")
+    
     def calculate_total(self):
         """Calculate the total price of items in the cart."""
-        total = sum(self.prices[item] * self.quantities[item] for item in self.items)
-        discounted_total = total * (1 - self.discount / 100)
-        return round(discounted_total, 2)
+        subtotal = sum(self.prices[item] * self.quantities[item] for item in self.items)
+        discounted_total = subtotal * (1 - self.discount / 100)
+        final_total = discounted_total * (1 + self.tax_rate / 100)
+        return round(final_total, 2)
     
+    def clear_cart(self):
+        """Remove all items from the cart."""
+        self.items = []
+        self.prices = {}
+        self.quantities = {}
+        print("Cart has been cleared.")
+    
     def display_cart(self):
         """Display the contents of the cart."""
         if not self.items:
@@ -57,12 +60,22 @@
             print(f"{item}: {self.quantities[item]} x ${self.prices[item]} = ${self.quantities[item] * self.prices[item]}")
         
         print("-----------------------")
-        print(f"Subtotal: ${sum(self.prices[item] * self.quantities[item] for item in self.items)}")
+        subtotal = sum(self.prices[item] * self.quantities[item] for item in self.items)
+        print(f"Subtotal: ${subtotal}")
+        
         if self.discount > 0:
-            print(f"Discount: {self.discount}%")
-            print(f"Total: ${self.calculate_total()}")
+            discount_amount = subtotal * (self.discount / 100)
+            print(f"Discount: {self.discount}% (-${discount_amount:.2f})")
+            discounted_total = subtotal - discount_amount
+            print(f"Discounted subtotal: ${discounted_total:.2f}")
         else:
-            print(f"Total: ${self.calculate_total()}")
+            discounted_total = subtotal
+        
+        if self.tax_rate > 0:
+            tax_amount = discounted_total * (self.tax_rate / 100)
+            print(f"Tax: {self.tax_rate}% (+${tax_amount:.2f})")
+        
+        print(f"Total: ${self.calculate_total()}")
 
 
 def main():
@@ -73,19 +86,27 @@
     cart.add_item("Apple", 0.99, 5)
     cart.add_item("Banana", 0.59, 3)
     cart.add_item("Orange", 0.79, 4)
+    cart.add_item("Grapes", 2.99, 1)
     
     # Display the cart
     cart.display_cart()
     
     # Apply a discount
-    cart.apply_discount(10)
+    cart.apply_discount(15)
     
+    # Apply tax
+    cart.apply_tax(8)
+    
     # Display the cart again
     cart.display_cart()
     
-    # Remove some items
-    cart.remove_item("Banana", 2)
+    # Clear the cart
+    cart.clear_cart()
     
+    # Add new items
+    cart.add_item("Milk", 3.49, 1)
+    cart.add_item("Bread", 2.29, 2)
+    
     # Display the final cart
     cart.display_cart()
 
