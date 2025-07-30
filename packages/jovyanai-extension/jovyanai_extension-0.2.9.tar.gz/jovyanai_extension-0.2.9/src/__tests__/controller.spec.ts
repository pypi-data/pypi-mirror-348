import { Cell } from '@jupyterlab/cells';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { CommandRegistry } from '@lumino/commands';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { NotebookController } from '../controller';

describe('NotebookController', () => {
  let controller: NotebookController;
  let mockNotebookTracker: jest.Mocked<INotebookTracker>;
  let mockCommands: jest.Mocked<CommandRegistry>;
  let mockNotebookPanel: jest.Mocked<NotebookPanel>;
  let mockCell: jest.Mocked<Cell>;
  let mockSettingRegistry: jest.Mocked<ISettingRegistry>;

  beforeEach(() => {
    // Create mock cell
    mockCell = {
      node: document.createElement('div'),
      model: {
        sharedModel: {
          setSource: jest.fn()
        }
      }
    } as any;

    // Create mock notebook panel
    mockNotebookPanel = {
      content: {
        activeCell: mockCell,
        activeCellIndex: 0,
        widgets: [mockCell],
        model: {
          defaultKernelLanguage: 'python'
        }
      },
      model: {
        sharedModel: {
          insertCell: jest.fn()
        }
      }
    } as any;

    // Create mock notebook tracker
    mockNotebookTracker = {
      currentWidget: mockNotebookPanel
    } as any;

    // Create mock commands
    mockCommands = {
      execute: jest.fn()
    } as any;

    // Create mock setting registry
    mockSettingRegistry = {
      load: jest.fn(),
      get: jest.fn(),
      set: jest.fn()
    } as any;

    controller = new NotebookController(
      mockNotebookTracker,
      mockCommands,
      mockSettingRegistry
    );
  });

  describe('activeCell', () => {
    it('should return the active cell from the current notebook', () => {
      expect(controller.activeCell).toBe(mockCell);
    });

    it('should return undefined when no notebook is active', () => {
      (mockNotebookTracker as any).currentWidget = undefined;
      expect(controller.activeCell).toBeUndefined();
    });
  });

  describe('addElementAfterCellInput', () => {
    it('should add element after input area when it exists', () => {
      const element = document.createElement('div');
      const inputArea = document.createElement('div');
      inputArea.className = 'jp-Cell-inputWrapper';
      mockCell.node.appendChild(inputArea);

      controller.addElementAfterCellInput(mockCell, element);
      expect(inputArea.nextElementSibling).toBe(element);
    });

    it('should append element to cell node when input area does not exist', () => {
      const element = document.createElement('div');
      controller.addElementAfterCellInput(mockCell, element);
      expect(mockCell.node.lastElementChild).toBe(element);
    });
  });

  describe('addElementInCellChild', () => {
    it('should append element to cell node', () => {
      const element = document.createElement('div');
      controller.addElementInCellChild(mockCell, element);
      expect(mockCell.node.lastElementChild).toBe(element);
    });
  });

  describe('writeCodeInCell', () => {
    it('should set the cell source code', () => {
      const code = 'print("Hello")';
      controller.writeCodeInCell(mockCell, code);
      expect(mockCell.model.sharedModel.setSource).toHaveBeenCalledWith(code);
    });
  });

  describe('runCell', () => {
    it('should execute the run-cell command', () => {
      controller.runCell(mockCell);
      expect(mockCommands.execute).toHaveBeenCalledWith('notebook:run-cell');
    });
  });

  describe('insertCell', () => {
    it('should insert a new cell at the specified index', () => {
      const content = 'print("New cell")';
      const index = 1;
      controller.insertCell(index, content);
      expect(
        mockNotebookPanel.model?.sharedModel.insertCell
      ).toHaveBeenCalledWith(index, {
        cell_type: 'code',
        source: content
      });
    });
  });

  describe('currentCell', () => {
    it('should return the current active cell', () => {
      expect(controller.currentCell).toBe(mockCell);
    });
  });

  describe('currentCellIndex', () => {
    it('should return the current cell index', () => {
      expect(controller.currentCellIndex).toBe(0);
    });
  });

  describe('getPreviousCells', () => {
    it('should return cells before the current cell', () => {
      const previousCell = { ...mockCell };
      (mockNotebookPanel.content as any).widgets = [previousCell, mockCell];
      mockNotebookPanel.content.activeCellIndex = 1;

      const result = controller.getPreviousCells(mockCell);
      expect(result).toEqual([previousCell]);
    });
  });

  describe('getNextCells', () => {
    it('should return cells after the current cell', () => {
      const nextCell = { ...mockCell };
      (mockNotebookPanel.content as any).widgets = [mockCell, nextCell];
      mockNotebookPanel.content.activeCellIndex = 0;

      const result = controller.getNextCells(mockCell);
      expect(result).toEqual([nextCell]);
    });
  });

  describe('getLanguage', () => {
    it('should return the notebook kernel language', () => {
      expect(controller.getLanguage()).toBe('python');
    });

    it('should return python as default when no language is set', () => {
      (mockNotebookPanel.content as any).model = null;
      expect(controller.getLanguage()).toBe('python');
    });
  });

  describe('runCommand', () => {
    it('should execute the specified command', () => {
      const command = 'notebook:save';
      controller.runCommand(command);
      expect(mockCommands.execute).toHaveBeenCalledWith(command);
    });
  });
});
