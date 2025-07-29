/**
 * Class representing a simple shopping cart
 */
class ShoppingCart {
    /**
     * Create a shopping cart
+     * @param {string} currency - The currency symbol to use (default: $)
     */
+    constructor(currency = '$') {
        this.items = [];
        this.discountCode = null;
+        this.currency = currency;
+        this.taxRate = 0;
    }

    /**
     * Add an item to the cart
     * @param {string} name - The item name
     * @param {number} price - The item price
     * @param {number} quantity - The item quantity
+     * @param {boolean} taxable - Whether the item is taxable
     */
+    addItem(name, price, quantity = 1, taxable = true) {
        this.items.push({
            name,
            price,
+            quantity,
+            taxable
        });
    }

    /**
     * Remove an item from the cart
     * @param {string} name - The item name to remove
+     * @returns {boolean} Whether the item was removed
     */
    removeItem(name) {
+        const initialLength = this.items.length;
        this.items = this.items.filter(item => item.name !== name);
+        return initialLength > this.items.length;
    }

    /**
     * Update the quantity of an item
     * @param {string} name - The item name
     * @param {number} quantity - The new quantity
+     * @returns {boolean} Whether the update was successful
     */
    updateQuantity(name, quantity) {
+        if (quantity < 1) {
+            return this.removeItem(name);
+        }
+
        const item = this.items.find(item => item.name === name);
        if (item) {
            item.quantity = quantity;
+            return true;
        }
+        return false;
    }

    /**
     * Apply a discount code to the cart
     * @param {string} code - The discount code
     * @param {number} percentage - The discount percentage (0-100)
     */
    applyDiscount(code, percentage) {
        if (percentage < 0 || percentage > 100) {
            throw new Error("Discount percentage must be between 0 and 100");
        }
        this.discountCode = { code, percentage };
    }

    /**
+     * Set the tax rate for the cart
+     * @param {number} rate - The tax rate percentage (0-100)
     */
+    setTaxRate(rate) {
+        if (rate < 0 || rate > 100) {
+            throw new Error("Tax rate must be between 0 and 100");
+        }
+        this.taxRate = rate;
+    }
+
+    /**
+     * Calculate the subtotal (before tax and discounts)
+     * @returns {number} The subtotal
+     */
+    calculateSubtotal() {
+        return this.items.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0);
+    }
+
+    /**
+     * Calculate the tax amount
+     * @returns {number} The tax amount
+     */
+    calculateTax() {
+        if (this.taxRate === 0) {
+            return 0;
+        }

+        const taxableAmount = this.items.reduce((total, item) => {
+            if (item.taxable) {
+                return total + (item.price * item.quantity);
+            }
+            return total;
+        }, 0);
+
+        return taxableAmount * (this.taxRate / 100);
+    }
+
+    /**
+     * Calculate the discount amount
+     * @returns {number} The discount amount
+     */
+    calculateDiscount() {
+        if (!this.discountCode) {
+            return 0;
        }

+        const subtotal = this.calculateSubtotal();
+        return subtotal * (this.discountCode.percentage / 100);
+    }
+
+    /**
+     * Calculate the total price of items in the cart
+     * @param {boolean} includeTax - Whether to include tax in the total
+     * @return {number} The total price
+     */
+    calculateTotal(includeTax = true) {
+        const subtotal = this.calculateSubtotal();
+        const discount = this.calculateDiscount();
+        let total = subtotal - discount;
+
+        if (includeTax) {
+            total += this.calculateTax();
+        }
+
        return total;
    }
+
+    /**
+     * Format a price with the currency symbol
+     * @param {number} price - The price to format
+     * @returns {string} The formatted price
+     */
+    formatPrice(price) {
+        return `${this.currency}${price.toFixed(2)}`;
+    }
+
+    /**
+     * Get a summary of the cart
+     * @returns {string} A summary of the cart
+     */
+    getSummary() {
+        const subtotal = this.calculateSubtotal();
+        const discount = this.calculateDiscount();
+        const tax = this.calculateTax();
+        const total = this.calculateTotal();
+
+        return `
+Cart Summary:
+-------------
+Subtotal: ${this.formatPrice(subtotal)}
+${this.discountCode ? `Discount (${this.discountCode.code}): -${this.formatPrice(discount)}` : ''}
+${this.taxRate > 0 ? `Tax (${this.taxRate}%): ${this.formatPrice(tax)}` : ''}
+Total: ${this.formatPrice(total)}
+`;
+    }
}

// Create a new shopping cart
+const cart = new ShoppingCart('€');

+// Set tax rate
+cart.setTaxRate(20); // 20% VAT
+
// Add some items
cart.addItem("Laptop", 999.99, 1);
+cart.addItem("Mouse", 29.99, 2);
cart.addItem("Keyboard", 59.99, 1);
+cart.addItem("Software License", 199.99, 1, false); // Non-taxable item

// Apply a discount
+cart.applyDiscount("SUMMER20", 20);

+// Display cart summary
+console.log(cart.getSummary());
