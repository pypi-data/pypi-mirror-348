/**
 * Test file for PatchCraft framework with various diff examples
 * 
 * This test demonstrates applying patches with various diff scenarios:
 * 1. Adding and removing lines at the beginning of a file
 * 2. Adding and removing lines in the middle of a file
 * 3. Adding and removing lines at the end of a file
 * 4. Replacing a line with multiple lines
 * 5. Replacing multiple lines with a single line
 * 6. Moving a block of code from one place to another
 * 7. Indentation changes
 * 8. Adding and removing blank lines between functions
 * 9. Adding and removing comments
 * 10. Complex changes with multiple additions and removals
 */

const fs = require('fs');
const path = require('path');
const fsExtra = require('fs-extra');
const parseDiff = require('parse-diff');
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

/**
 * Apply a unified diff to content
 * 
 * @param {Array} chunks - Array of chunks from parse-diff
 * @param {string} originalContent - Original file content
 * @returns {string} - Modified content after applying the diff
 */
function applyUnifiedDiff(chunks, originalContent) {
  // Split the original content into lines for easier manipulation
  const originalLines = originalContent.split('\n');
  
  // Create a copy of the original lines that we'll modify
  let modifiedLines = [...originalLines];
  
  // Process chunks in reverse order to avoid line number changes
  // affecting subsequent chunks
  for (let i = chunks.length - 1; i >= 0; i--) {
    const chunk = chunks[i];
    
    // The line where changes start (0-based)
    const lineIndex = chunk.oldStart - 1;
    
    // Extract the changes
    const changes = chunk.changes;
    
    // Group consecutive additions and deletions
    const changeGroups = [];
    let currentGroup = null;
    
    for (const change of changes) {
      if (change.type === 'normal') {
        if (currentGroup) {
          changeGroups.push(currentGroup);
          currentGroup = null;
        }
      } else {
        if (!currentGroup || currentGroup.type !== change.type) {
          if (currentGroup) {
            changeGroups.push(currentGroup);
          }
          currentGroup = {
            type: change.type,
            changes: [change]
          };
        } else {
          currentGroup.changes.push(change);
        }
      }
    }
    
    if (currentGroup) {
      changeGroups.push(currentGroup);
    }
    
    // Apply change groups in reverse order
    for (let j = changeGroups.length - 1; j >= 0; j--) {
      const group = changeGroups[j];
      
      // Find the position of this group in the chunk
      let position = 0;
      for (const change of changes) {
        if (change === group.changes[0]) {
          break;
        }
        if (change.type === 'normal' || change.type === 'del') {
          position++;
        }
      }
      
      if (group.type === 'del') {
        // Remove lines
        modifiedLines.splice(lineIndex + position, group.changes.length);
      } else if (group.type === 'add') {
        // Add lines
        // Remove the '+' character from the beginning of added lines
        const linesToAdd = group.changes.map(change => {
          // If the content starts with '+', remove it
          if (change.content.startsWith('+')) {
            return change.content.substring(1);
          }
          return change.content;
        });
        modifiedLines.splice(lineIndex + position, 0, ...linesToAdd);
      }
    }
  }
  
  // Join the modified lines back into a string
  return modifiedLines.join('\n');
}

/**
 * Convert unified diff chunks to diff-match-patch format
 * 
 * @param {Array} chunks - Array of chunks from parse-diff
 * @param {string} originalContent - Original file content
 * @returns {Array} - Array of patches in diff-match-patch format
 */
function convertChunksToDMP(chunks, originalContent) {
  const dmp = new DiffMatchPatch();
  
  // Apply the unified diff to get the modified content
  const modifiedContent = applyUnifiedDiff(chunks, originalContent);
  
  // Let diff-match-patch create the patches by comparing original and modified content
  const diffs = dmp.diff_main(originalContent, modifiedContent);
  dmp.diff_cleanupSemantic(diffs);
  
  return dmp.patch_make(originalContent, diffs);
}

/**
 * Normalize content to handle whitespace consistently
 * 
 * @param {string} content - Content to normalize
 * @returns {string} - Normalized content
 */
function normalizeContent(content) {
  if (!content) return content;
  
  // Normalize line endings to LF
  content = content.replace(/\r\n/g, '\n');
  
  // Trim trailing whitespace on each line
  content = content.split('\n').map(line => line.trimRight()).join('\n');
  
  // Ensure file ends with exactly one newline
  if (!content.endsWith('\n')) {
    content += '\n';
  } else {
    content = content.replace(/\n+$/, '\n');
  }
  
  return content;
}

/**
 * Apply a unified diff patch using PatchCraft
 * 
 * @param {string} originalFilePath - Path to the original file
 * @param {string} patchFilePath - Path to the patch file
 * @param {string} outputFilePath - Path to the output file
 * @returns {boolean} - Whether the patch was applied successfully
 */
function applyPatch(originalFilePath, patchFilePath, outputFilePath) {
  try {
    // Read the original file and patch file
    let originalContent = readFile(originalFilePath);
    const patchContent = readFile(patchFilePath);
    
    if (!originalContent || !patchContent) {
      return false;
    }
    
    // Normalize the original content
    originalContent = normalizeContent(originalContent);
    
    console.log(`\nApplying patch: ${patchFilePath}`);
    console.log(`Original file: ${originalFilePath}`);
    console.log(`Output file: ${outputFilePath}`);
    console.log('='.repeat(50));
    
    // Step 1: Parse the unified diff using parse-diff
    console.log('Step 1: Parsing unified diff with parse-diff');
    const files = parseDiff(patchContent);
    
    if (files.length === 0) {
      console.error('No valid patches found in the patch file');
      return false;
    }
    
    // Get the first file's chunks (we assume one file per patch for simplicity)
    const chunks = files[0].chunks;
    console.log(`Found ${chunks.length} chunks in the patch`);
    
    // Step 2: Convert the chunks to diff-match-patch format
    console.log('Step 2: Converting to diff-match-patch format');
    const dmp = new DiffMatchPatch();
    const patches = convertChunksToDMP(chunks, originalContent);
    console.log(`Generated ${patches.length} diff-match-patch patches`);
    
    // Step 3: Apply the patches using diff-match-patch
    console.log('Step 3: Applying patches with diff-match-patch');
    let [patchedContent, results] = dmp.patch_apply(patches, originalContent);
    
    // Check if all patches were applied successfully
    const allSuccessful = results.every(result => result);
    console.log(`All patches applied successfully: ${allSuccessful}`);
    
    // Normalize the patched content
    patchedContent = normalizeContent(patchedContent);
    
    // Step 4: Write the patched content to the output file
    console.log('Step 4: Writing patched content to output file');
    
    // Compare with expected result
    const expectedFilePath = originalFilePath.replace('test', 'test_modified');
    let expectedContent = null;
    
    if (fs.existsSync(expectedFilePath)) {
      expectedContent = readFile(expectedFilePath);
      console.log(`Comparing with expected result: ${expectedFilePath}`);
      
      if (expectedContent) {
        expectedContent = normalizeContent(expectedContent);
        if (expectedContent === patchedContent) {
          console.log('✅ Output matches expected result!');
        } else {
          console.log('❌ Output does not match expected result!');
          
          // Calculate the similarity percentage
          const similarity = dmp.diff_levenshtein(dmp.diff_main(expectedContent, patchedContent)) / Math.max(expectedContent.length, 1);
          console.log(`Similarity: ${(100 - similarity * 100).toFixed(2)}%`);
          
          // Log the first difference
          const diffs = dmp.diff_main(expectedContent, patchedContent);
          for (const [op, text] of diffs) {
            if (op !== 0) { // Not equal
              console.log(`First difference (${op === -1 ? 'expected' : 'actual'}): "${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"`);
              break;
            }
          }
        }
      }
    }
    
    const success = writeFile(outputFilePath, patchedContent);
    
    if (success) {
      console.log('Patch applied successfully!');
    }
    
    console.log('-'.repeat(50));
    
    return success;
  } catch (error) {
    console.error(`Error applying patch ${patchFilePath}:`, error.message);
    return false;
  }
}

// Main function to test the framework with various diff examples
function main() {
  console.log('Testing PatchCraft framework with various diff examples\n');
  
  // Create output directory
  const outputDir = path.resolve(__dirname, 'output_examples');
  fsExtra.ensureDirSync(outputDir);
  
  // Define the test cases
  const testCases = [];
  
  // Add test cases for each example
  for (let i = 1; i <= 10; i++) {
    testCases.push({
      original: `../../data/input/test${i}.py`,
      patch: `../../data/patch_test/test${i}_1.patch`,
      output: `output_examples/test${i}_result.py`
    });
  }
  
  // Apply patches for each test case
  testCases.forEach(testCase => {
    applyPatch(
      path.resolve(__dirname, testCase.original),
      path.resolve(__dirname, testCase.patch),
      path.resolve(__dirname, testCase.output)
    );
  });
  
  console.log('\nTest completed for all examples');
  console.log('These test cases demonstrate how PatchCraft handles various diff scenarios.');
}

// Run the main function
main();
