/**
 * Test file for diff-match-patch framework
 * 
 * This framework provides robust algorithms to perform the operations required
 * for synchronizing plain text. It's based on Google's diff-match-patch library.
 */

const fs = require('fs');
const path = require('path');
const fsExtra = require('fs-extra');
const DiffMatchPatch = require('diff-match-patch');

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

// Function to apply a patch using diff-match-patch
function applyPatch(originalFilePath, modifiedFilePath, outputFilePath) {
  try {
    // Read the original and modified files
    const originalContent = readFile(originalFilePath);
    const modifiedContent = readFile(modifiedFilePath);
    
    if (!originalContent || !modifiedContent) {
      return false;
    }
    
    console.log(`\nGenerating and applying patch`);
    console.log(`Original file: ${originalFilePath}`);
    console.log(`Modified file: ${modifiedFilePath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log('='.repeat(50));
    
    // Create a new diff_match_patch object
    const dmp = new DiffMatchPatch();
    
    // Compute the diff between original and modified content
    const diffs = dmp.diff_main(originalContent, modifiedContent);
    
    // Make the diff more human-readable (optional)
    dmp.diff_cleanupSemantic(diffs);
    
    // Create patches from the diffs
    const patches = dmp.patch_make(originalContent, diffs);
    
    // Display patch information
    console.log(`Generated ${patches.length} patch(es)`);
    
    // Apply the patches to the original content
    const [patchedContent, results] = dmp.patch_apply(patches, originalContent);
    
    // Check if all patches were applied successfully
    const allSuccessful = results.every(result => result);
    console.log(`All patches applied successfully: ${allSuccessful}`);
    
    // Write the patched content to the output file
    const success = writeFile(outputFilePath, patchedContent);
    
    if (success) {
      console.log('Patched content written to output file!');
      
      // Compare with expected result
      if (modifiedContent === patchedContent) {
        console.log('✅ Output matches modified content!');
      } else {
        console.log('❌ Output does not match modified content!');
        
        // Calculate the similarity percentage
        const similarity = dmp.diff_levenshtein(dmp.diff_main(modifiedContent, patchedContent)) / modifiedContent.length;
        console.log(`Similarity: ${(100 - similarity * 100).toFixed(2)}%`);
      }
    }
    
    console.log('-'.repeat(50));
    
    return success;
  } catch (error) {
    console.error(`Error applying patch:`, error.message);
    return false;
  }
}

// Main function to test the framework
function main() {
  console.log('Testing diff-match-patch framework\n');
  
  // Create output directory
  const outputDir = path.resolve(__dirname, 'output');
  fsExtra.ensureDirSync(outputDir);
  
  // Define the test cases
  const testCases = [
    {
      original: '../../data/input/sample1.py',
      modified: '../../data/input/sample1_modified1.py',
      output: 'output/sample1_1.py'
    },
    {
      original: '../../data/input/sample1_modified1.py',
      modified: '../../data/input/sample1_modified2.py',
      output: 'output/sample1_2.py'
    },
    {
      original: '../../data/input/sample2.ts',
      modified: '../../data/input/sample2_modified1.ts',
      output: 'output/sample2_1.ts'
    },
    {
      original: '../../data/input/sample2_modified1.ts',
      modified: '../../data/input/sample2_modified2.ts',
      output: 'output/sample2_2.ts'
    },
    {
      original: '../../data/input/sample3.js',
      modified: '../../data/input/sample3_modified1.js',
      output: 'output/sample3_1.js'
    },
    {
      original: '../../data/input/sample3_modified1.js',
      modified: '../../data/input/sample3_modified2.js',
      output: 'output/sample3_2.js'
    },
    {
      original: '../../data/input/sample4.txt',
      modified: '../../data/input/sample4_modified1.txt',
      output: 'output/sample4_1.txt'
    },
    {
      original: '../../data/input/sample4_modified1.txt',
      modified: '../../data/input/sample4_modified2.txt',
      output: 'output/sample4_2.txt'
    },
    {
      original: '../../data/input/sample5.py',
      modified: '../../data/input/sample5_modified1.py',
      output: 'output/sample5_1.py'
    },
    {
      original: '../../data/input/sample6.js',
      modified: '../../data/input/sample6_modified1.js',
      output: 'output/sample6_1.js'
    },
    {
      original: '../../data/input/sample7.html',
      modified: '../../data/input/sample7_modified1.html',
      output: 'output/sample7_1.html'
    },
    {
      original: '../../data/input/sample8.json',
      modified: '../../data/input/sample8_modified1.json',
      output: 'output/sample8_1.json'
    }
  ];
  
  // Apply patches for each test case
  testCases.forEach(testCase => {
    applyPatch(
      path.resolve(__dirname, testCase.original),
      path.resolve(__dirname, testCase.modified),
      path.resolve(__dirname, testCase.output)
    );
  });
  
  console.log('\nNote: diff-match-patch is different from unified diff format.');
  console.log('It uses a different algorithm for computing and applying patches.');
  console.log('It is particularly good at handling text that has been moved around.');
}

// Run the main function
main();
