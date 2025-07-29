/**
 * Sample JavaScript file for testing patches with both additions and removals.
 * Modified version with both added and removed lines.
 */

// Configuration object
const config = {
  apiUrl: 'https://api.example.com/v2',
  timeout: 10000,
  retryAttempts: 5,
  debug: true,
  version: '2.0.0',
  authType: 'oauth2',
  maxConnections: 10
};

// User class
class User {
  constructor(id, name, email, role = 'user') {
    this.id = id;
    this.name = name;
    this.email = email;
    this.role = role;
    this.createdAt = new Date();
    this.isActive = true;
    this.lastLogin = null;
    this.preferences = {
      theme: 'light',
      notifications: true
    };
  }

  deactivate() {
    this.isActive = false;
    console.log(`User ${this.name} has been deactivated.`);
    return true;
  }

  updateEmail(newEmail) {
    this.email = newEmail;
    console.log(`Email updated to ${newEmail} for user ${this.name}.`);
    return true;
  }

  updateRole(newRole) {
    this.role = newRole;
    console.log(`Role updated to ${newRole} for user ${this.name}.`);
    return true;
  }

  login() {
    this.lastLogin = new Date();
    console.log(`User ${this.name} logged in at ${this.lastLogin}.`);
    return true;
  }

  updatePreferences(preferences) {
    this.preferences = { ...this.preferences, ...preferences };
    console.log(`Preferences updated for user ${this.name}.`);
    return true;
  }

  getInfo() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      role: this.role,
      createdAt: this.createdAt,
      isActive: this.isActive,
      lastLogin: this.lastLogin,
      preferences: this.preferences
    };
  }

  toString() {
    return `User: ${this.name} (${this.email}) - ${this.role}`;
  }
}

// Helper functions
function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

function formatDateTime(date) {
  if (!date) return 'Never';
  return new Date(date).toLocaleString();
}

// Main application
function main() {
  console.log('Starting application...');
  console.log(`API URL: ${config.apiUrl}`);
  console.log(`Version: ${config.version}`);
  console.log(`Auth Type: ${config.authType}`);

  // Create some users
  const users = [
    new User(generateId(), 'John Doe', 'john@example.com', 'admin'),
    new User(generateId(), 'Jane Smith', 'jane@example.com', 'editor'),
    new User(generateId(), 'Bob Johnson', 'bob@example.com')
  ];

  // Simulate user logins
  users.forEach(user => {
    user.login();
  });

  // Update user preferences
  users[0].updatePreferences({ theme: 'dark', notifications: false });

  // Display user information
  console.log('\nUser List:');
  users.forEach(user => {
    console.log(`- ${user.toString()} (Last login: ${formatDateTime(user.lastLogin)})`);
  });

  // Update a user's role
  const userToUpdate = users[1];
  userToUpdate.updateRole('manager');

  // Deactivate a user
  const userToDeactivate = users[2];
  userToDeactivate.deactivate();

  // Display final user status
  console.log('\nFinal User Status:');
  users.forEach(user => {
    const status = user.isActive ? 'Active' : 'Inactive';
    console.log(`- ${user.name} (${user.role}): ${status}`);
  });

  console.log('\nApplication finished.');
}

// Run the application
main();
