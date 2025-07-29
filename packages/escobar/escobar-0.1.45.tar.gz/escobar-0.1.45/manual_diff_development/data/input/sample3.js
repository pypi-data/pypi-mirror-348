/**
 * Class representing a simple shopping cart
 */
class ShoppingCart {
    /**
     * Create a shopping cart
     */
    constructor() {
        this.items = [];
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
     * Calculate the total price of items in the cart
     * @return {number} The total price
     */
    calculateTotal() {
        return this.items.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0);
    }
}

// Create a new shopping cart
const cart = new ShoppingCart();

// Add some items
cart.addItem("Laptop", 999.99, 1);
cart.addItem("Mouse", 29.99, 1);
cart.addItem("Keyboard", 59.99, 1);

// Calculate and display the total
console.log(`Total: $${cart.calculateTotal().toFixed(2)}`);
