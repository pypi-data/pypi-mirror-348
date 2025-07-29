# Unified Diff Format Patch Testing Environment

This project provides a comprehensive testing environment for exploring and comparing various patch application frameworks, with a focus on the Unified Diff Format.

## Project Structure

- **data/**: Contains test data for patch application
  - **input/**: Original and modified source files
  - **patch/**: Patch files in unified diff format
  - **result/**: Results of applying patches to original files

- **frameworks/**: Contains test implementations for various patch application frameworks
  - **patchcraft/**: A hybrid framework combining parse-diff and diff-match-patch
  - **parse-diff/**: Tests for the parse-diff npm package
  - **unidiff/**: Tests for the unidiff npm package
  - **diffparser/**: Tests for the diffparser npm package
  - **diff-match-patch/**: Tests for the diff-match-patch npm package
  - **fast-json-patch/**: Tests for the fast-json-patch npm package
  - **just-diff-apply/**: Tests for the just-diff-apply npm package

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Run the tests:
   ```
   ./run-tests.sh
   ```

## Test Data

The test data includes:

- Python files (.py)
- TypeScript files (.ts)
- JavaScript files (.js)
- Text files (.txt)

Each file has:
- An original version
- Two modified versions
- Two patch files (in unified diff format)
- Two result files (from applying the patches)

## Patch Application Frameworks

This project explores several npm packages for patch application:

1. **PatchCraft**: A hybrid framework combining parse-diff and diff-match-patch
2. **parse-diff**: Parses unified diff format into a structured object
3. **unidiff**: Parses and applies unified diff format patches
4. **diffparser**: Alternative parser for unified diff format
5. **diff-match-patch**: Google's algorithm for robust text synchronization
6. **fast-json-patch**: Implements JSON-Patch (RFC-6902) for JSON data
7. **just-diff-apply**: Applies diffs to JavaScript objects

For more details on each framework, see the [frameworks README](frameworks/README.md).

## Documentation

- **notes.txt**: Describes the file and folder naming logic and provides instructions for generating more samples
- **frameworks/README.md**: Provides details on each framework and how to use them

## Running Individual Tests

To run tests for a specific framework:

```
node frameworks/<framework-name>/test.js
```

For example:

```
node frameworks/unidiff/test.js
```

## License

MIT
