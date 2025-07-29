/**
 * Test file for fast-json-patch framework
 * 
 * This framework implements JSON-Patch (RFC-6902) and is designed for
 * working with JSON data, not text files. We'll demonstrate how to use
 * it with our JSON-like data.
 */

const fs = require('fs');
const path = require('path');
const fsExtra = require('fs-extra');
const jsonpatch = require('fast-json-patch');

// Function to read a file
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error.message);
    return null;
  }
}

// Function to write to a file
function writeFile(filePath, content) {
  try {
    // Ensure directory exists
    fsExtra.ensureDirSync(path.dirname(filePath));
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  } catch (error) {
    console.error(`Error writing to file ${filePath}:`, error.message);
    return false;
  }
}

// Function to safely parse JSON
function parseJSON(content) {
  try {
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

// Function to generate and apply a JSON patch
function applyJSONPatch(originalFilePath, modifiedFilePath, outputFilePath) {
  try {
    // Read the original and modified files
    const originalContent = readFile(originalFilePath);
    const modifiedContent = readFile(modifiedFilePath);
    
    if (!originalContent || !modifiedContent) {
      return false;
    }
    
    // Try to parse as JSON
    const originalJSON = parseJSON(originalContent);
    const modifiedJSON = parseJSON(modifiedContent);
    
    if (!originalJSON || !modifiedJSON) {
      console.log(`\nSkipping ${originalFilePath} - Not valid JSON`);
      return false;
    }
    
    console.log(`\nGenerating and applying JSON patch`);
    console.log(`Original file: ${originalFilePath}`);
    console.log(`Modified file: ${modifiedFilePath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log('='.repeat(50));
    
    // Generate a patch
    const patch = jsonpatch.compare(originalJSON, modifiedJSON);
    
    // Display the patch
    console.log('Generated JSON Patch:');
    console.log(JSON.stringify(patch, null, 2));
    
    // Apply the patch
    const patchedJSON = jsonpatch.applyPatch(originalJSON, patch).newDocument;
    
    // Write the patched content to the output file
    const success = writeFile(outputFilePath, JSON.stringify(patchedJSON, null, 2));
    
    if (success) {
      console.log('Patch applied successfully!');
      
      // Compare with expected result
      if (JSON.stringify(modifiedJSON) === JSON.stringify(patchedJSON)) {
        console.log('✅ Output matches modified content!');
      } else {
        console.log('❌ Output does not match modified content!');
      }
    }
    
    console.log('-'.repeat(50));
    
    return success;
  } catch (error) {
    console.error(`Error applying JSON patch:`, error.message);
    return false;
  }
}

// Function to create a simple JSON file for testing
function createJSONTestFiles() {
  const testDir = path.resolve(__dirname, 'test-data');
  fsExtra.ensureDirSync(testDir);
  
  // Create original JSON file
  const originalJSON = {
    name: "Sample Project",
    version: "1.0.0",
    description: "A sample project for testing JSON patches",
    dependencies: {
      "react": "^17.0.2",
      "lodash": "^4.17.21"
    },
    scripts: {
      "start": "node index.js",
      "test": "jest"
    },
    author: "Test User",
    license: "MIT"
  };
  
  // Create modified JSON file (version 1)
  const modifiedJSON1 = {
    name: "Sample Project",
    version: "1.1.0",
    description: "A sample project for testing JSON patches",
    dependencies: {
      "react": "^17.0.2",
      "lodash": "^4.17.21",
      "express": "^4.17.1"
    },
    scripts: {
      "start": "node index.js",
      "test": "jest",
      "dev": "nodemon index.js"
    },
    author: "Test User",
    license: "MIT",
    repository: {
      "type": "git",
      "url": "https://github.com/user/sample-project"
    }
  };
  
  // Create modified JSON file (version 2)
  const modifiedJSON2 = {
    name: "Sample Project",
    version: "2.0.0",
    description: "An enhanced sample project for testing JSON patches",
    dependencies: {
      "react": "^18.0.0",
      "lodash": "^4.17.21",
      "express": "^4.17.1",
      "mongoose": "^6.0.0"
    },
    scripts: {
      "start": "node index.js",
      "test": "jest",
      "dev": "nodemon index.js",
      "build": "webpack"
    },
    author: {
      "name": "Test User",
      "email": "test@example.com"
    },
    license: "MIT",
    repository: {
      "type": "git",
      "url": "https://github.com/user/sample-project"
    },
    engines: {
      "node": ">=14.0.0"
    }
  };
  
  // Write the files
  writeFile(path.join(testDir, 'original.json'), JSON.stringify(originalJSON, null, 2));
  writeFile(path.join(testDir, 'modified1.json'), JSON.stringify(modifiedJSON1, null, 2));
  writeFile(path.join(testDir, 'modified2.json'), JSON.stringify(modifiedJSON2, null, 2));
  
  return {
    original: path.join(testDir, 'original.json'),
    modified1: path.join(testDir, 'modified1.json'),
    modified2: path.join(testDir, 'modified2.json')
  };
}

// Main function to test the framework
function main() {
  console.log('Testing fast-json-patch framework\n');
  
  // Create output directory
  const outputDir = path.resolve(__dirname, 'output');
  fsExtra.ensureDirSync(outputDir);
  
  // Create JSON test files
  console.log('Creating JSON test files...');
  const jsonFiles = createJSONTestFiles();
  
  // Define the test cases
  const testCases = [
    {
      original: jsonFiles.original,
      modified: jsonFiles.modified1,
      output: path.join(outputDir, 'patched1.json')
    },
    {
      original: jsonFiles.modified1,
      modified: jsonFiles.modified2,
      output: path.join(outputDir, 'patched2.json')
    }
  ];
  
  // Apply patches for each test case
  testCases.forEach(testCase => {
    applyJSONPatch(testCase.original, testCase.modified, testCase.output);
  });
  
  // Try to apply JSON patch to our sample files (will likely fail as they're not JSON)
  console.log('\nAttempting to apply JSON patch to non-JSON files (for demonstration)');
  
  const sampleFiles = [
    {
      original: '../../data/input/sample3.js',
      modified: '../../data/input/sample3_modified1.js',
      output: path.join(outputDir, 'sample3_1.js')
    }
  ];
  
  sampleFiles.forEach(testCase => {
    applyJSONPatch(
      path.resolve(__dirname, testCase.original),
      path.resolve(__dirname, testCase.modified),
      testCase.output
    );
  });
  
  console.log('\nNote: fast-json-patch is designed for JSON data, not text files.');
  console.log('It implements the JSON Patch standard (RFC-6902).');
  console.log('It is not suitable for patching source code or text files directly.');
}

// Run the main function
main();
