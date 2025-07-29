/**
 * Interface for an Address
 */
interface Address {
    street: string;
    city: string;
    zipCode: string;
    country: string;
}

/**
 * Interface for a Contact
 */
interface Contact {
    email: string;
    phone?: string;
}

/**
 * Interface for a Person
 */
interface Person {
    firstName: string;
    lastName: string;
    age: number;
    address?: Address;
    contact?: Contact;
}

/**
 * Creates a person object
 * @param firstName The first name
 * @param lastName The last name
 * @param age The age
 * @returns A Person object
 */
function createPerson(firstName: string, lastName: string, age: number): Person {
    return {
        firstName,
        lastName,
        age
    };
}

/**
 * Formats a person's full name
 * @param person The person object
 * @param includeMiddle Include middle name if available
 * @returns Formatted full name
 */
function formatName(person: Person, includeMiddle: boolean = false): string {
    return `${person.firstName} ${person.lastName}`;
}

/**
 * Creates an address object
 * @param street The street
 * @param city The city
 * @param zipCode The zip code
 * @param country The country
 * @returns An Address object
 */
function createAddress(street: string, city: string, zipCode: string, country: string): Address {
    return {
        street,
        city,
        zipCode,
        country
    };
}

/**
 * Creates a contact object
 * @param email The email address
 * @param phone Optional phone number
 * @returns A Contact object
 */
function createContact(email: string, phone?: string): Contact {
    return {
        email,
        phone
    };
}

/**
 * Formats a person's address
 * @param address The address object
 * @returns Formatted address
 */
function formatAddress(address: Address): string {
    return `${address.street}, ${address.city}, ${address.zipCode}, ${address.country}`;
}

// Create a person
const john = createPerson("John", "Doe", 30);

// Add an address to the person
john.address = createAddress("123 Main St", "Anytown", "12345", "USA");

// Add contact information
john.contact = createContact("john.doe@example.com", "+1-555-123-4567");

// Log person details
console.log(`Name: ${formatName(john)}`);
console.log(`Age: ${john.age}`);
console.log(`Email: ${john.contact?.email}`);
console.log(`Phone: ${john.contact?.phone}`);
if (john.address) {
    console.log(`Address: ${formatAddress(john.address)}`);
}
