import {
  CellData,
  CellType,
  CellOutput,
  StreamOutput,
  DisplayDataOutput,
  ExecutionResultOutput,
  ErrorOutput
} from '@jovyan/client';

// Re-export CellData
export { CellData };

import { Cell, CodeCellModel } from '@jupyterlab/cells';
import { IMimeBundle } from '@jupyterlab/nbformat';

export const convertCellToCellData = (cell: Cell): CellData => {
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
