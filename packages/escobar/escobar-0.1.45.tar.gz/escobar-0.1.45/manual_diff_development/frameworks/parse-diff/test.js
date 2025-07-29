/**
 * Test file for parse-diff framework
 * 
 * This framework is primarily for parsing unified diff format,
 * not for applying patches. We'll demonstrate how to parse our
 * patch files and extract information from them.
 */

const fs = require('fs');
const path = require('path');
const parseDiff = require('parse-diff');

// Function to read a patch file and parse it
function parsePatchFile(patchFilePath) {
  try {
    // Read the patch file
    const patchContent = fs.readFileSync(patchFilePath, 'utf8');
    
    // Parse the diff
    const files = parseDiff(patchContent);
    
    console.log(`\nParsing patch file: ${patchFilePath}`);
    console.log('='.repeat(50));
    
    // Display information about each file in the diff
    files.forEach(file => {
      console.log(`File: ${file.to}`);
      console.log(`From: ${file.from}`);
      console.log(`Index: ${file.index || 'N/A'}`);
      console.log(`--- ${file.deletions} deletions`);
      console.log(`+++ ${file.additions} additions`);
      
      // Display chunks information
      console.log('\nChunks:');
      file.chunks.forEach((chunk, i) => {
        console.log(`  Chunk ${i + 1}:`);
        console.log(`    Old range: ${chunk.oldStart},${chunk.oldLines}`);
        console.log(`    New range: ${chunk.newStart},${chunk.newLines}`);
        
        // Display a sample of changes
        if (chunk.changes.length > 0) {
          console.log('    Sample changes:');
          const samplesToShow = Math.min(3, chunk.changes.length);
          for (let j = 0; j < samplesToShow; j++) {
            const change = chunk.changes[j];
            console.log(`      ${change.type} ${change.content.substring(0, 50)}${change.content.length > 50 ? '...' : ''}`);
          }
          if (chunk.changes.length > samplesToShow) {
            console.log(`      ... and ${chunk.changes.length - samplesToShow} more changes`);
          }
        }
      });
      
      console.log('-'.repeat(50));
    });
    
    return files;
  } catch (error) {
    console.error(`Error parsing patch file ${patchFilePath}:`, error.message);
    return null;
  }
}

// Main function to test the framework
function main() {
  console.log('Testing parse-diff framework\n');
  
  // Define the patch files to test
  const patchFiles = [
    '../../data/patch/sample1_1.py',
    '../../data/patch/sample1_2.py',
    '../../data/patch/sample2_1.ts',
    '../../data/patch/sample2_2.ts',
    '../../data/patch/sample3_1.js',
    '../../data/patch/sample3_2.js',
    '../../data/patch/sample4_1.txt',
    '../../data/patch/sample4_2.txt'
  ];
  
  // Parse each patch file
  patchFiles.forEach(patchFile => {
    parsePatchFile(path.resolve(__dirname, patchFile));
  });
  
  console.log('\nNote: parse-diff is a parsing library and does not apply patches.');
  console.log('It is useful for analyzing and understanding the structure of patch files.');
}

// Run the main function
main();
