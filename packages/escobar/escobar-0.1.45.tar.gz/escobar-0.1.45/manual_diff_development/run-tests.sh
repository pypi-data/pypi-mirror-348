#!/bin/bash

# Script to run all framework tests

echo "Running tests for all patch application frameworks"
echo "=================================================="
echo ""

# First run PatchCraft (our custom hybrid framework)
echo "Running tests for PatchCraft (hybrid framework)..."
echo "---------------------------------"
node frameworks/patchcraft/test.js
echo ""
echo "Test completed for PatchCraft"
echo "=================================================="
echo ""

# Then run the other frameworks
for dir in frameworks/*; do
  if [ -d "$dir" ] && [ "$(basename $dir)" != "patchcraft" ]; then
    framework=$(basename $dir)
    echo "Running tests for $framework..."
    echo "---------------------------------"
    node $dir/test.js
    echo ""
    echo "Test completed for $framework"
    echo "=================================================="
    echo ""
  fi
done

echo "All tests completed!"
echo ""
echo "Summary: PatchCraft combines parse-diff (for parsing unified diff format)"
echo "with diff-match-patch (for robust patch application) to provide the best"
echo "of both worlds."
