/**
 * Test file for just-diff-apply framework
 * 
 * This framework is designed for applying diffs to JavaScript objects,
 * not text files. We'll demonstrate how to use it with our JSON-like data.
 */

const fs = require('fs');
const path = require('path');
const fsExtra = require('fs-extra');
const justDiff = require('just-diff');
const justDiffApply = require('just-diff-apply');

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

// Function to generate and apply a diff using just-diff and just-diff-apply
function applyObjectDiff(originalFilePath, modifiedFilePath, outputFilePath) {
  try {
    // Read the original and modified files
    const originalContent = readFile(originalFilePath);
    const modifiedContent = readFile(modifiedFilePath);
    
    if (!originalContent || !modifiedContent) {
      return false;
    }
    
    // Try to parse as JSON
    const originalObj = parseJSON(originalContent);
    const modifiedObj = parseJSON(modifiedContent);
    
    if (!originalObj || !modifiedObj) {
      console.log(`\nSkipping ${originalFilePath} - Not valid JSON`);
      return false;
    }
    
    console.log(`\nGenerating and applying diff`);
    console.log(`Original file: ${originalFilePath}`);
    console.log(`Modified file: ${modifiedFilePath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log('='.repeat(50));
    
    // Generate a diff
    const diff = justDiff(originalObj, modifiedObj);
    
    // Display the diff
    console.log('Generated Diff:');
    console.log(JSON.stringify(diff, null, 2));
    
    // Create a copy of the original object
    const patchedObj = JSON.parse(JSON.stringify(originalObj));
    
    // Apply the diff
    justDiffApply(patchedObj, diff);
    
    // Write the patched content to the output file
    const success = writeFile(outputFilePath, JSON.stringify(patchedObj, null, 2));
    
    if (success) {
      console.log('Diff applied successfully!');
      
      // Compare with expected result
      if (JSON.stringify(modifiedObj) === JSON.stringify(patchedObj)) {
        console.log('✅ Output matches modified content!');
      } else {
        console.log('❌ Output does not match modified content!');
      }
    }
    
    console.log('-'.repeat(50));
    
    return success;
  } catch (error) {
    console.error(`Error applying diff:`, error.message);
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
    description: "A sample project for testing diffs",
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
    description: "A sample project for testing diffs",
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
    description: "An enhanced sample project for testing diffs",
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
  console.log('Testing just-diff-apply framework\n');
  
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
  
  // Apply diffs for each test case
  testCases.forEach(testCase => {
    applyObjectDiff(testCase.original, testCase.modified, testCase.output);
  });
  
  // Try to apply diff to our sample files (will likely fail as they're not JSON)
  console.log('\nAttempting to apply diff to non-JSON files (for demonstration)');
  
  const sampleFiles = [
    {
      original: '../../data/input/sample3.js',
      modified: '../../data/input/sample3_modified1.js',
      output: path.join(outputDir, 'sample3_1.js')
    }
  ];
  
  sampleFiles.forEach(testCase => {
    applyObjectDiff(
      path.resolve(__dirname, testCase.original),
      path.resolve(__dirname, testCase.modified),
      testCase.output
    );
  });
  
  console.log('\nNote: just-diff-apply is designed for JavaScript objects, not text files.');
  console.log('It is not suitable for patching source code or text files directly.');
  console.log('It works well for JSON data structures and can optionally support JSON Patch format.');
}

// Run the main function
main();
