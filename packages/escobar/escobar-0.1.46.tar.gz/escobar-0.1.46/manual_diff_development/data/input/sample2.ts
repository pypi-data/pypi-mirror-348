/**
 * Interface for a Person
 */
interface Person {
    firstName: string;
    lastName: string;
    age: number;
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
 * @returns Formatted full name
 */
function formatName(person: Person): string {
    return `${person.firstName} ${person.lastName}`;
}

// Create a person
const john = createPerson("John", "Doe", 30);

// Log person details
console.log(`Name: ${formatName(john)}`);
console.log(`Age: ${john.age}`);
