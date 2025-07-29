--- data/input/sample2.ts	2025-05-08 10:08:45
+++ data/input/sample2_modified1.ts	2025-05-08 10:14:50
@@ -1,10 +1,22 @@
 /**
+ * Interface for an Address
+ */
+interface Address {
+    street: string;
+    city: string;
+    zipCode: string;
+    country: string;
+}
+
+/**
  * Interface for a Person
  */
 interface Person {
     firstName: string;
     lastName: string;
     age: number;
+    address?: Address;
+    email?: string;
 }
 
 /**
@@ -12,13 +24,15 @@
  * @param firstName The first name
  * @param lastName The last name
  * @param age The age
+ * @param email Optional email address
  * @returns A Person object
  */
-function createPerson(firstName: string, lastName: string, age: number): Person {
+function createPerson(firstName: string, lastName: string, age: number, email?: string): Person {
     return {
         firstName,
         lastName,
-        age
+        age,
+        email
     };
 }
 
@@ -31,9 +45,31 @@
     return `${person.firstName} ${person.lastName}`;
 }
 
+/**
+ * Creates an address object
+ * @param street The street
+ * @param city The city
+ * @param zipCode The zip code
+ * @param country The country
+ * @returns An Address object
+ */
+function createAddress(street: string, city: string, zipCode: string, country: string): Address {
+    return {
+        street,
+        city,
+        zipCode,
+        country
+    };
+}
+
 // Create a person
-const john = createPerson("John", "Doe", 30);
+const john = createPerson("John", "Doe", 30, "john.doe@example.com");
 
+// Add an address to the person
+john.address = createAddress("123 Main St", "Anytown", "12345", "USA");
+
 // Log person details
 console.log(`Name: ${formatName(john)}`);
 console.log(`Age: ${john.age}`);
+console.log(`Email: ${john.email}`);
+console.log(`Address: ${john.address?.street}, ${john.address?.city}, ${john.address?.zipCode}, ${john.address?.country}`);
