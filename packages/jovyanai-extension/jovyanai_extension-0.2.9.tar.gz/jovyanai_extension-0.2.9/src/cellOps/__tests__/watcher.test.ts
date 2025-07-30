// import { INotebookTracker } from '@jupyterlab/notebook';
// import { Cell } from '@jupyterlab/cells';
// import watchCellFocusAndShowActivateCellButton from '../watcher';

// describe('watchCellFocusAndShowActivateCellButton', () => {
//   let mockNotebookTracker: INotebookTracker;
//   let mockCell: Cell;
//   let mockCodeCell: Cell;

//   beforeEach(() => {
//     // Create mock notebook tracker
//     mockNotebookTracker = {
//       activeCellChanged: {
//         connect: jest.fn(),
//         disconnect: jest.fn()
//       }
//     } as any;

//     // Create mock cells
//     mockCell = {
//       node: document.createElement('div'),
//       model: {
//         type: 'markdown'
//       }
//     } as any;

//     mockCodeCell = {
//       node: document.createElement('div'),
//       model: {
//         type: 'code',
//         sharedModel: {
//           source: 'print("hello")'
//         }
//       }
//     } as any;
//   });

//   it('should connect to notebook tracker', () => {
//     watchCellFocusAndShowActivateCellButton(mockNotebookTracker);
//     expect(mockNotebookTracker.activeCellChanged.connect).toHaveBeenCalled();
//   });

//   it('should add button to markdown cell with correct text', () => {
//     watchCellFocusAndShowActivateCellButton(mockNotebookTracker);

//     // Get the callback that was registered
//     const connectCallback = (mockNotebookTracker.activeCellChanged.connect as jest.Mock).mock.calls[0][0];

//     // Simulate cell focus change
//     connectCallback(mockNotebookTracker, mockCell);

//     // Check that button was added with correct text
//     const button = mockCell.node.querySelector('.ask-ai-button-container');
//     expect(button).not.toBeNull();
//     if (button) {
//       expect(button.textContent).toContain('Generate code');
//     }
//   });

//   it('should add button to code cell with correct text', () => {
//     watchCellFocusAndShowActivateCellButton(mockNotebookTracker);

//     // Get the callback that was registered
//     const connectCallback = (mockNotebookTracker.activeCellChanged.connect as jest.Mock).mock.calls[0][0];

//     // Simulate cell focus change
//     connectCallback(mockNotebookTracker, mockCodeCell);

//     // Check that button was added with correct text
//     const button = mockCodeCell.node.querySelector('.ask-ai-button-container');
//     expect(button).not.toBeNull();
//     if (button) {
//       expect(button.textContent).toContain('Change code');
//     }
//   });

//   it('should remove existing buttons when changing cells', () => {
//     watchCellFocusAndShowActivateCellButton(mockNotebookTracker);

//     // Get the callback that was registered
//     const connectCallback = (mockNotebookTracker.activeCellChanged.connect as jest.Mock).mock.calls[0][0];

//     // Simulate first cell focus
//     connectCallback(mockNotebookTracker, mockCell);

//     // Simulate second cell focus
//     connectCallback(mockNotebookTracker, mockCodeCell);

//     // Check that only one button exists
//     const buttons = document.querySelectorAll('.ask-ai-button-container');
//     expect(buttons.length).toBe(1);
//   });
// });
