import { setupCodeGenerationStream } from '../handleCodeGeneration';
import { Cell, CodeCellModel, MarkdownCellModel } from '@jupyterlab/cells';
import { NotebookModel } from '@jupyterlab/notebook';
import * as jovyanClientModule from '../jovyanClient'; // Import the module

// Mock the JovyanClient
// Define the shape of the mock client instance
const mockJovyanClientInstance = {
  connect: jest.fn().mockResolvedValue(undefined),
  generateCodeStream: jest.fn().mockImplementation((options, callback) => {
    // Store the options for verification
    (mockJovyanClientInstance as any).lastOptions = options;

    // Simulate streaming some tokens
    callback('def ');
    callback('hello_world():\n');
    callback('    print("Hello, World!")');
    return Promise.resolve();
  }),
  // Add other methods/properties if needed by getJovyanClient checks
  isConnected: true // Assuming getJovyanClient might check this
};

// Mock the getJovyanClient function from the module
jest.spyOn(jovyanClientModule, 'getJovyanClient').mockImplementation(() => {
  // Clear last options when the mock client is requested
  (mockJovyanClientInstance as any).lastOptions = null;
  return mockJovyanClientInstance as any; // Return the mock instance
});

describe('handleCodeGeneration', () => {
  let notebookModel: NotebookModel;

  beforeEach(() => {
    // Create a new notebook model for each test
    notebookModel = new NotebookModel();
  });

  const createCell = (
    type: 'code' | 'markdown',
    source: string,
    outputs?: any[],
    metadata?: any // Keep metadata optional
  ): Cell => {
    // Return type matches original expectation via cast
    // Prepare the initial cell data as a plain object
    const cellData: any = {
      cell_type: type,
      source: source,
      metadata: metadata || {}
    };
    if (type === 'code') {
      // Add outputs only for code cells
      cellData.outputs = outputs || [];
    }

    // Perform the insertion within a transaction
    notebookModel.sharedModel.transact(() => {
      notebookModel.sharedModel.insertCell(0, cellData);
      // DO NOT try to get the model here immediately
    });

    // Retrieve the cell model *after* the transaction
    // This allows Yjs and the NotebookModel to synchronize
    const cellModel = notebookModel.cells.get(0);

    // Check if model retrieval was successful
    if (!cellModel) {
      throw new Error('Cell model could not be retrieved after insertion.');
    }

    // Basic type check after retrieval (optional but good practice)
    if (
      (type === 'code' && !(cellModel instanceof CodeCellModel)) ||
      (type === 'markdown' && !(cellModel instanceof MarkdownCellModel))
    ) {
      throw new Error(
        `Retrieved cell model type mismatch. Expected ${type}, got ${cellModel.type || 'unknown'}`
      );
    }

    // Return the structure expected by the tests using the original cast
    return { model: cellModel } as unknown as Cell;
  };

  test('correctly converts code cell with execution result', async () => {
    const cell = createCell('code', 'print("Hello")', [
      {
        output_type: 'execute_result',
        data: { 'text/plain': 'Hello' }
      }
    ]);

    const stream = await setupCodeGenerationStream({
      currentCell: cell,
      previousCells: [],
      nextCells: [],
      userInput: 'test',
      language: 'python'
    });

    const tokens = [];
    for await (const token of stream) {
      tokens.push(token);
    }

    expect(tokens).toEqual([
      'def ',
      'hello_world():\n',
      '    print("Hello, World!")'
    ]);

    // Verify the data sent to JovyanClient
    const lastOptions = (mockJovyanClientInstance as any).lastOptions;
    expect(lastOptions).toBeDefined();
    expect(lastOptions.currentCell).toEqual({
      cell_type: 'code',
      source: 'print("Hello")',
      outputs: [
        {
          output_type: 'execute_result',
          data: { 'text/plain': 'Hello' }
        }
      ]
    });
    expect(lastOptions.previousCells).toEqual([]);
    expect(lastOptions.nextCells).toEqual([]);
    expect(lastOptions.prompt).toBe('test');
    expect(lastOptions.language).toBe('python');
    expect(lastOptions.stream).toBe(true);
  });

  test('correctly converts code cell with stream output', async () => {
    const cell = createCell('code', 'print("Hello")', [
      {
        output_type: 'stream',
        name: 'stdout',
        text: 'Hello'
      }
    ]);

    const stream = await setupCodeGenerationStream({
      currentCell: cell,
      previousCells: [],
      nextCells: [],
      userInput: 'test',
      language: 'python'
    });

    const tokens = [];
    for await (const token of stream) {
      tokens.push(token);
    }

    expect(tokens).toEqual([
      'def ',
      'hello_world():\n',
      '    print("Hello, World!")'
    ]);

    // Verify the data sent to JovyanClient
    const lastOptions = (mockJovyanClientInstance as any).lastOptions;
    expect(lastOptions.currentCell).toEqual({
      cell_type: 'code',
      source: 'print("Hello")',
      outputs: [
        {
          output_type: 'stream',
          name: 'stdout',
          text: ['Hello']
        }
      ]
    });
  });

  test('correctly converts code cell with error output', async () => {
    const cell = createCell('code', 'print("Hello")', [
      {
        output_type: 'error',
        ename: 'NameError',
        evalue: 'name is not defined',
        traceback: [
          '<ipython-input-1-1> in <module>',
          'NameError: name is not defined'
        ]
      }
    ]);

    const stream = await setupCodeGenerationStream({
      currentCell: cell,
      previousCells: [],
      nextCells: [],
      userInput: 'test',
      language: 'python'
    });

    const tokens = [];
    for await (const token of stream) {
      tokens.push(token);
    }

    expect(tokens).toEqual([
      'def ',
      'hello_world():\n',
      '    print("Hello, World!")'
    ]);

    // Verify the data sent to JovyanClient
    const lastOptions = (mockJovyanClientInstance as any).lastOptions;
    expect(lastOptions.currentCell).toEqual({
      cell_type: 'code',
      source: 'print("Hello")',
      outputs: [
        {
          output_type: 'error',
          ename: 'NameError',
          evalue: 'name is not defined',
          traceback: [
            '<ipython-input-1-1> in <module>',
            'NameError: name is not defined'
          ]
        }
      ]
    });
  });

  test('correctly handles multiple cells in context', async () => {
    const previousCell = createCell('code', 'x = 42');
    const currentCell = createCell('code', 'print(x)');
    const nextCell = createCell('code', 'y = x + 1');

    const stream = await setupCodeGenerationStream({
      currentCell,
      previousCells: [previousCell],
      nextCells: [nextCell],
      userInput: 'test',
      language: 'python'
    });

    const tokens = [];
    for await (const token of stream) {
      tokens.push(token);
    }

    expect(tokens).toEqual([
      'def ',
      'hello_world():\n',
      '    print("Hello, World!")'
    ]);

    // Verify the data sent to JovyanClient
    const lastOptions = (mockJovyanClientInstance as any).lastOptions;
    expect(lastOptions.previousCells).toEqual([
      {
        cell_type: 'code',
        source: 'x = 42',
        outputs: []
      }
    ]);
    expect(lastOptions.currentCell).toEqual({
      cell_type: 'code',
      source: 'print(x)',
      outputs: []
    });
    expect(lastOptions.nextCells).toEqual([
      {
        cell_type: 'code',
        source: 'y = x + 1',
        outputs: []
      }
    ]);
  });

  test('correctly handles markdown cells', async () => {
    const markdownCell = createCell('markdown', '# Title\nSome text');
    const codeCell = createCell('code', 'print("Hello")');

    const stream = await setupCodeGenerationStream({
      currentCell: codeCell,
      previousCells: [markdownCell],
      nextCells: [],
      userInput: 'test',
      language: 'python'
    });

    const tokens = [];
    for await (const token of stream) {
      tokens.push(token);
    }

    expect(tokens).toEqual([
      'def ',
      'hello_world():\n',
      '    print("Hello, World!")'
    ]);

    // Verify the data sent to JovyanClient
    const lastOptions = (mockJovyanClientInstance as any).lastOptions;
    expect(lastOptions.previousCells).toEqual([
      {
        cell_type: 'markdown',
        source: '# Title\nSome text',
        outputs: []
      }
    ]);
    expect(lastOptions.currentCell).toEqual({
      cell_type: 'code',
      source: 'print("Hello")',
      outputs: []
    });
  });
});
