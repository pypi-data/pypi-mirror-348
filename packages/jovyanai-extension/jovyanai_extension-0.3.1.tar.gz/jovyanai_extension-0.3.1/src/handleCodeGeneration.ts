import {
  CellData,
  CellType,
  CellOutput,
  StreamOutput,
  DisplayDataOutput,
  ExecutionResultOutput,
  ErrorOutput
} from '@jovyan/client';
import { Cell, CodeCellModel } from '@jupyterlab/cells';
import { IMimeBundle } from '@jupyterlab/nbformat';
import { getJovyanClient } from './jovyanClient';
type GenerateCodeOptions = {
  userInput: string;
  currentCell: Cell;
  previousCells: Cell[];
  nextCells: Cell[];
  language: string;
};

const _convertCellToCellData = (cell: Cell): CellData => {
  const outputs: CellOutput[] = [];

  if (cell.model.type === 'code') {
    const codeCell = cell.model as CodeCellModel;
    const outputArea = codeCell.outputs;
    for (let i = 0; i < outputArea.length; i++) {
      const output = outputArea.get(i);
      if (output) {
        const outputData = output.toJSON();
        switch (outputData.output_type) {
          case 'execute_result': {
            const execOutput: ExecutionResultOutput = {
              output_type: 'execute_result',
              data: outputData.data as IMimeBundle
            };
            outputs.push(execOutput);
            break;
          }
          case 'stream': {
            const streamOutput: StreamOutput = {
              output_type: 'stream',
              name: String(outputData.name || 'stdout'),
              text: Array.isArray(outputData.text)
                ? outputData.text.map(String)
                : [String(outputData.text || '')]
            };
            outputs.push(streamOutput);
            break;
          }
          case 'display_data': {
            const displayOutput: DisplayDataOutput = {
              output_type: 'display_data',
              data: outputData.data as IMimeBundle
            };
            outputs.push(displayOutput);
            break;
          }
          case 'error': {
            const errorOutput: ErrorOutput = {
              output_type: 'error',
              ename: String(outputData.ename || 'Error'),
              evalue: String(outputData.evalue || 'Unknown error'),
              traceback: Array.isArray(outputData.traceback)
                ? outputData.traceback.map(String)
                : []
            };
            outputs.push(errorOutput);
            break;
          }
        }
      }
    }
  }

  return {
    cell_type: cell.model.type as CellType,
    source: cell.model.sharedModel.source,
    outputs: outputs
  };
};

export const setupCodeGenerationStream = async (
  options: GenerateCodeOptions
): Promise<AsyncGenerator<string, void, unknown>> => {
  const client = await getJovyanClient();

  // We'll store tokens here as they come in.
  let done = false;
  const chunks: string[] = [];
  client
    .generateCodeStream(
      {
        currentCell: _convertCellToCellData(options.currentCell),
        previousCells: options.previousCells.map(_convertCellToCellData),
        nextCells: options.nextCells.map(_convertCellToCellData),
        prompt: options.userInput,
        language: options.language,
        stream: true
      },
      chunk => {
        chunks.push(chunk);
      }
    )
    .then(() => {
      // Resolve the promise when the stream is finished
      done = true;
    })
    .catch(error => {
      // Handle errors here
      console.error('Error generating code stream:', error);
      throw error;
    });

  return (async function* () {
    while (!done || chunks.length > 0) {
      if (chunks.length > 0) {
        const nextToken = chunks.shift();
        if (nextToken) {
          yield nextToken;
        }
      } else {
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
  })();
};
