/**
 * Class representing a simple shopping cart
 */
class ShoppingCart {
    /**
     * Create a shopping cart
     */
    constructor() {
        this.items = [];
        this.discountCode = null;
    }
    
    /**
     * Add an item to the cart
     * @param {string} name - The item name
     * @param {number} price - The item price
     * @param {number} quantity - The item quantity
     */
    addItem(name, price, quantity = 1) {
        this.items.push({
            name,
            price,
            quantity
        });
    }
    
    /**
     * Remove an item from the cart
     * @param {string} name - The item name to remove
     */
    removeItem(name) {
        this.items = this.items.filter(item => item.name !== name);
    }
    
    /**
     * Update the quantity of an item
     * @param {string} name - The item name
     * @param {number} quantity - The new quantity
     */
    updateQuantity(name, quantity) {
        const item = this.items.find(item => item.name === name);
        if (item) {
            item.quantity = quantity;
        }
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
     * Calculate the total price of items in the cart
     * @return {number} The total price
     */
    calculateTotal() {
        let total = this.items.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0);
        
        // Apply discount if available
        if (this.discountCode) {
            const discount = total * (this.discountCode.percentage / 100);
            total -= discount;
        }
        
        return total;
    }
}

// Create a new shopping cart
const cart = new ShoppingCart();

// Add some items
cart.addItem("Laptop", 999.99, 1);
cart.addItem("Mouse", 29.99, 1);
cart.addItem("Keyboard", 59.99, 1);

// Update quantity
cart.updateQuantity("Mouse", 2);

// Apply a discount
cart.applyDiscount("SUMMER10", 10);

// Calculate and display the total
console.log(`Total: $${cart.calculateTotal().toFixed(2)}`);
console.log(`Discount applied: ${cart.discountCode ? cart.discountCode.code : 'None'}`);
