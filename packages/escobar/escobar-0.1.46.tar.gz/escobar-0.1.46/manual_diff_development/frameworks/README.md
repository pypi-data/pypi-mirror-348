# Patch Application Frameworks

This directory contains test implementations for various npm packages that can be used for parsing and applying patches. Each subdirectory contains a test file that demonstrates how to use the corresponding framework with our test cases.

## Frameworks Overview

### 1. PatchCraft

**Purpose**: Hybrid framework that combines parse-diff and diff-match-patch.

**Features**:
- Parses unified diff format using parse-diff
- Converts parsed diffs to diff-match-patch format
- Applies patches using diff-match-patch
- Works with standard unified diff format
- Leverages the robust patch application of diff-match-patch

**Run the test**:
```
node patchcraft/test.js
```

### 2. parse-diff

**Purpose**: Parse unified diff format into a structured object.

**Features**:
- Parses unified diff format
- Extracts file information, chunk information, and changes
- Does not apply patches

**Run the test**:
```
node parse-diff/test.js
```

### 2. unidiff

**Purpose**: Parse and apply unified diff format patches.

**Features**:
- Parses unified diff format
- Applies patches to text content
- Works with standard unified diff format

**Run the test**:
```
node unidiff/test.js
```

### 3. diffparser

**Purpose**: Parse unified diff format into a structured object (alternative to parse-diff).

**Features**:
- Parses unified diff format
- Extracts file information, chunk information, and changes
- Does not apply patches
- Different output structure compared to parse-diff

**Run the test**:
```
node diffparser/test.js
```

### 4. diff-match-patch

**Purpose**: Robust algorithms for synchronizing plain text.

**Features**:
- Computes diffs between text content
- Creates patches from diffs
- Applies patches to text content
- Not based on unified diff format
- Good at handling text that has been moved around

**Run the test**:
```
node diff-match-patch/test.js
```

### 5. fast-json-patch

**Purpose**: Implements JSON-Patch (RFC-6902) for working with JSON data.

**Features**:
- Compares JSON objects to generate patches
- Applies patches to JSON objects
- Not suitable for text files or source code
- Follows the JSON Patch standard (RFC-6902)

**Run the test**:
```
node fast-json-patch/test.js
```

### 6. just-diff-apply

**Purpose**: Apply diffs to JavaScript objects.

**Features**:
- Generates diffs between JavaScript objects
- Applies diffs to JavaScript objects
- Not suitable for text files or source code
- Works well with JSON data structures

**Run the test**:
```
node just-diff-apply/test.js
```

## Comparison

| Framework | Parses Unified Diff | Applies Patches | Works with Text Files | Works with JSON | Notes |
|-----------|---------------------|-----------------|------------------------|----------------|-------|
| PatchCraft | ✅ | ✅ | ✅ | ❌ | Hybrid approach |
| parse-diff | ✅ | ❌ | ✅ | ❌ | Parsing only |
| unidiff | ✅ | ✅ | ✅ | ❌ | Full unified diff support |
| diffparser | ✅ | ❌ | ✅ | ❌ | Parsing only |
| diff-match-patch | ❌ | ✅ | ✅ | ❌ | Different patch format |
| fast-json-patch | ❌ | ✅ | ❌ | ✅ | JSON-specific |
| just-diff-apply | ❌ | ✅ | ❌ | ✅ | JavaScript objects only |

## Running All Tests

To run all tests, you can use the following command from the project root:

```
for dir in frameworks/*; do
  if [ -d "$dir" ]; then
    echo "Running tests for $(basename $dir)..."
    node $dir/test.js
    echo ""
  fi
done
```

## Conclusion

When choosing a framework for patch application, consider the following:

1. **For text files with unified diff format**:
   - Use `PatchCraft` for the best of both worlds (standard format + robust application)
   - Use `unidiff` for both parsing and applying patches
   - Use `parse-diff` or `diffparser` if you only need to parse the patches

2. **For plain text synchronization without unified diff format**:
   - Use `diff-match-patch` for robust text patching

3. **For JSON data**:
   - Use `fast-json-patch` for RFC-6902 compliant JSON patching
   - Use `just-diff-apply` for simpler JavaScript object patching
