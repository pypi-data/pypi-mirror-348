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
 * Interface for a Person
 */
interface Person {
    firstName: string;
    lastName: string;
    age: number;
    address?: Address;
    email?: string;
}

/**
 * Creates a person object
 * @param firstName The first name
 * @param lastName The last name
 * @param age The age
 * @param email Optional email address
 * @returns A Person object
 */
function createPerson(firstName: string, lastName: string, age: number, email?: string): Person {
    return {
        firstName,
        lastName,
        age,
        email
    };
}

/**
 * Formats a person's full name
 * @param person The person object
 * @returns Formatted full name
 */
function formatName(person: Person): string {
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

// Create a person
const john = createPerson("John", "Doe", 30, "john.doe@example.com");

// Add an address to the person
john.address = createAddress("123 Main St", "Anytown", "12345", "USA");

// Log person details
console.log(`Name: ${formatName(john)}`);
console.log(`Age: ${john.age}`);
console.log(`Email: ${john.email}`);
console.log(`Address: ${john.address?.street}, ${john.address?.city}, ${john.address?.zipCode}, ${john.address?.country}`);
