--- data/input/sample3.js	2025-05-08 10:08:56
+++ data/input/sample3_modified1.js	2025-05-08 10:16:41
@@ -7,6 +7,7 @@
      */
     constructor() {
         this.items = [];
+        this.discountCode = null;
     }
     
     /**
@@ -32,13 +33,45 @@
     }
     
     /**
+     * Update the quantity of an item
+     * @param {string} name - The item name
+     * @param {number} quantity - The new quantity
+     */
+    updateQuantity(name, quantity) {
+        const item = this.items.find(item => item.name === name);
+        if (item) {
+            item.quantity = quantity;
+        }
+    }
+    
+    /**
+     * Apply a discount code to the cart
+     * @param {string} code - The discount code
+     * @param {number} percentage - The discount percentage (0-100)
+     */
+    applyDiscount(code, percentage) {
+        if (percentage < 0 || percentage > 100) {
+            throw new Error("Discount percentage must be between 0 and 100");
+        }
+        this.discountCode = { code, percentage };
+    }
+    
+    /**
      * Calculate the total price of items in the cart
      * @return {number} The total price
      */
     calculateTotal() {
-        return this.items.reduce((total, item) => {
+        let total = this.items.reduce((total, item) => {
             return total + (item.price * item.quantity);
         }, 0);
+        
+        // Apply discount if available
+        if (this.discountCode) {
+            const discount = total * (this.discountCode.percentage / 100);
+            total -= discount;
+        }
+        
+        return total;
     }
 }
 
@@ -50,5 +83,12 @@
 cart.addItem("Mouse", 29.99, 1);
 cart.addItem("Keyboard", 59.99, 1);
 
+// Update quantity
+cart.updateQuantity("Mouse", 2);
+
+// Apply a discount
+cart.applyDiscount("SUMMER10", 10);
+
 // Calculate and display the total
 console.log(`Total: $${cart.calculateTotal().toFixed(2)}`);
+console.log(`Discount applied: ${cart.discountCode ? cart.discountCode.code : 'None'}`);
