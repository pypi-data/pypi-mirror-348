/**
 * Sample JavaScript file for testing patches with both additions and removals.
 */

// Configuration object
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
  retryAttempts: 3,
  debug: false,
  version: '1.0.0'
};

// User class
class User {
  constructor(id, name, email) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.createdAt = new Date();
    this.isActive = true;
  }

  deactivate() {
    this.isActive = false;
    console.log(`User ${this.name} has been deactivated.`);
  }

  updateEmail(newEmail) {
    this.email = newEmail;
    console.log(`Email updated to ${newEmail} for user ${this.name}.`);
  }

  getInfo() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      createdAt: this.createdAt,
      isActive: this.isActive
    };
  }

  toString() {
    return `User: ${this.name} (${this.email})`;
  }
}

// Helper functions
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

// Main application
function main() {
  console.log('Starting application...');
  console.log(`API URL: ${config.apiUrl}`);
  console.log(`Version: ${config.version}`);

  // Create some users
  const users = [
    new User(generateId(), 'John Doe', 'john@example.com'),
    new User(generateId(), 'Jane Smith', 'jane@example.com'),
    new User(generateId(), 'Bob Johnson', 'bob@example.com')
  ];

  // Display user information
  console.log('\nUser List:');
  users.forEach(user => {
    console.log(`- ${user.toString()} (Created: ${formatDate(user.createdAt)})`);
  });

  // Update a user's email
  const userToUpdate = users[1];
  userToUpdate.updateEmail('jane.smith@example.com');

  // Deactivate a user
  const userToDeactivate = users[2];
  userToDeactivate.deactivate();

  // Display final user status
  console.log('\nFinal User Status:');
  users.forEach(user => {
    const status = user.isActive ? 'Active' : 'Inactive';
    console.log(`- ${user.name}: ${status}`);
  });

  console.log('\nApplication finished.');
}

// Run the application
main();
