/**
 * Test file for unidiff framework
 * 
 * This framework provides utilities for working with unified diff format,
 * including parsing and applying patches.
 */

const fs = require('fs');
const path = require('path');
const fsExtra = require('fs-extra');
const unidiff = require('unidiff');

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

// Function to apply a patch using unidiff
function applyPatch(originalFilePath, patchFilePath, outputFilePath) {
  try {
    // Read the original file and patch file
    const originalContent = readFile(originalFilePath);
    const patchContent = readFile(patchFilePath);
    
    if (!originalContent || !patchContent) {
      return false;
    }
    
    console.log(`\nApplying patch: ${patchFilePath}`);
    console.log(`Original file: ${originalFilePath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log('='.repeat(50));
    
    // Parse the patch
    const parsedPatch = unidiff.parse(patchContent);
    
    // Apply the patch
    const patchedContent = unidiff.apply(originalContent, parsedPatch);
    
    // Write the patched content to the output file
    const success = writeFile(outputFilePath, patchedContent);
    
    if (success) {
      console.log('Patch applied successfully!');
      
      // Compare with expected result
      const expectedFilePath = originalFilePath.replace('input', 'result').replace('.py', '_1.py').replace('.ts', '_1.ts').replace('.js', '_1.js').replace('.txt', '_1.txt');
      if (fs.existsSync(expectedFilePath)) {
        const expectedContent = readFile(expectedFilePath);
        const patchedContent = readFile(outputFilePath);
        
        if (expectedContent === patchedContent) {
          console.log('✅ Output matches expected result!');
        } else {
          console.log('❌ Output does not match expected result!');
        }
      }
    }
    
    console.log('-'.repeat(50));
    
    return success;
  } catch (error) {
    console.error(`Error applying patch ${patchFilePath}:`, error.message);
    return false;
  }
}

// Main function to test the framework
function main() {
  console.log('Testing unidiff framework\n');
  
  // Create output directory
  const outputDir = path.resolve(__dirname, 'output');
  fsExtra.ensureDirSync(outputDir);
  
  // Define the test cases
  const testCases = [
    {
      original: '../../data/input/sample1.py',
      patch: '../../data/patch/sample1_1.py',
      output: 'output/sample1_1.py'
    },
    {
      original: '../../data/input/sample2.ts',
      patch: '../../data/patch/sample2_1.ts',
      output: 'output/sample2_1.ts'
    },
    {
      original: '../../data/input/sample3.js',
      patch: '../../data/patch/sample3_1.js',
      output: 'output/sample3_1.js'
    },
    {
      original: '../../data/input/sample4.txt',
      patch: '../../data/patch/sample4_1.txt',
      output: 'output/sample4_1.txt'
    }
  ];
  
  // Apply patches for each test case
  testCases.forEach(testCase => {
    applyPatch(
      path.resolve(__dirname, testCase.original),
      path.resolve(__dirname, testCase.patch),
      path.resolve(__dirname, testCase.output)
    );
  });
  
  console.log('\nNote: unidiff provides utilities for parsing and applying patches in unified diff format.');
}

// Run the main function
main();
