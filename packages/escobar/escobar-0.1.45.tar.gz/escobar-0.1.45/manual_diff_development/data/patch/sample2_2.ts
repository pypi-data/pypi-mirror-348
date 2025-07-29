--- data/input/sample2_modified1.ts	2025-05-08 10:14:50
+++ data/input/sample2_modified2.ts	2025-05-08 10:15:12
@@ -9,6 +9,14 @@
 }
 
 /**
+ * Interface for a Contact
+ */
+interface Contact {
+    email: string;
+    phone?: string;
+}
+
+/**
  * Interface for a Person
  */
 interface Person {
@@ -16,7 +24,7 @@
     lastName: string;
     age: number;
     address?: Address;
-    email?: string;
+    contact?: Contact;
 }
 
 /**
@@ -24,24 +32,23 @@
  * @param firstName The first name
  * @param lastName The last name
  * @param age The age
- * @param email Optional email address
  * @returns A Person object
  */
-function createPerson(firstName: string, lastName: string, age: number, email?: string): Person {
+function createPerson(firstName: string, lastName: string, age: number): Person {
     return {
         firstName,
         lastName,
-        age,
-        email
+        age
     };
 }
 
 /**
  * Formats a person's full name
  * @param person The person object
+ * @param includeMiddle Include middle name if available
  * @returns Formatted full name
  */
-function formatName(person: Person): string {
+function formatName(person: Person, includeMiddle: boolean = false): string {
     return `${person.firstName} ${person.lastName}`;
 }
 
@@ -62,14 +69,42 @@
     };
 }
 
+/**
+ * Creates a contact object
+ * @param email The email address
+ * @param phone Optional phone number
+ * @returns A Contact object
+ */
+function createContact(email: string, phone?: string): Contact {
+    return {
+        email,
+        phone
+    };
+}
+
+/**
+ * Formats a person's address
+ * @param address The address object
+ * @returns Formatted address
+ */
+function formatAddress(address: Address): string {
+    return `${address.street}, ${address.city}, ${address.zipCode}, ${address.country}`;
+}
+
 // Create a person
-const john = createPerson("John", "Doe", 30, "john.doe@example.com");
+const john = createPerson("John", "Doe", 30);
 
 // Add an address to the person
 john.address = createAddress("123 Main St", "Anytown", "12345", "USA");
 
+// Add contact information
+john.contact = createContact("john.doe@example.com", "+1-555-123-4567");
+
 // Log person details
 console.log(`Name: ${formatName(john)}`);
 console.log(`Age: ${john.age}`);
-console.log(`Email: ${john.email}`);
-console.log(`Address: ${john.address?.street}, ${john.address?.city}, ${john.address?.zipCode}, ${john.address?.country}`);
+console.log(`Email: ${john.contact?.email}`);
+console.log(`Phone: ${john.contact?.phone}`);
+if (john.address) {
+    console.log(`Address: ${formatAddress(john.address)}`);
+}
