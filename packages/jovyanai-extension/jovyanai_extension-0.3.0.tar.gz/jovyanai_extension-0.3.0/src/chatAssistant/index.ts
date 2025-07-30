import React from 'react';
import { ChatInterface } from './components/chat-interface';
import '../../style/chatAssistant.css';
import { JupyterFrontEnd, ILabShell } from '@jupyterlab/application';
import { Widget } from '@lumino/widgets';
import { createRoot } from 'react-dom/client';
import { WidgetTracker } from '@jupyterlab/apputils';
import { LabIcon } from '@jupyterlab/ui-components';
import logo from '../../style/icons/logo.svg';

// import { CellData } from '@jovyan/client';
import { NotebookController } from '../controller';
import { NotebookControllerContext } from '../context/NotebookControllerContext';
import { ChatContextProvider } from './ChatContextProvider';
interface IChatAssistantOptions {
  app: JupyterFrontEnd;
  notebookController: NotebookController;
}

export function attachChatAssistant(options: IChatAssistantOptions): void {
  const { app, notebookController } = options;

  // Initialize the chat assistant
  const content = document.createElement('div');
  content.id = 'jupyterlab-chat-extension-root';
  content.className = 'jupyterlab-chat-extension';

  // Create a JupyterLab widget
  const widget = new Widget({ node: content });
  widget.id = 'jupyterlab-chat-assistant-widget';
  const chatIcon = new LabIcon({
    name: 'jovyan::chat',
    svgstr: logo
  });
  widget.title.icon = chatIcon;
  widget.title.caption = 'Jovyan AI Chat Assistant';
  widget.title.closable = true;
  widget.title.className = 'jp-mod-opacity-50';
  const tracker = new WidgetTracker({
    namespace: 'jupyterlab-chat-extension'
  });
  tracker.add(widget);

  // Add the widget to the right area
  app.shell.add(widget, 'right', { activate: false });

  // Initialize React component
  const root = createRoot(content);
  // Wrap ChatInterface with the Provider
  root.render(
    React.createElement(
      NotebookControllerContext.Provider,
      { value: notebookController },
      React.createElement(ChatContextProvider, {
        children: React.createElement(ChatInterface)
      })
    )
  );

  // Register the command to activate and focus
  app.commands.addCommand('jovyanai:toggle-chat', {
    label: 'Toggle Chat Assistant',
    execute: () => {
      const labShell = app.shell as ILabShell;
      const sidePanel = Array.from(labShell.widgets('right')).find(
        widget => widget.id === 'jupyterlab-chat-assistant-widget'
      );
      const wasExpanded = sidePanel?.isVisible || false;

      const inputElement =
        widget.node.querySelector<HTMLInputElement>('#chat-input');

      if (wasExpanded) {
        labShell.collapseRight();
      } else {
        labShell.activateById(widget.id);
        requestAnimationFrame(() => {
          if (inputElement) {
            inputElement.focus();
          } else {
            console.warn(
              'Chat input element (#chat-input) not found for focusing after activation.'
            );
          }
        });
      }
      return null;
    }
  });

  // Add keyboard shortcut
  app.commands.addKeyBinding({
    command: 'jovyanai:toggle-chat',
    keys: ['Alt B'],
    selector: 'body'
  });

  // Register the command to add the current cell to context
  app.commands.addCommand('jovyanai:addCurrentCellContext', {
    label: 'Add Current Cell to Chat Context',
    execute: () => {
      const activeCell = notebookController.currentCell; // Use currentCell property
      if (activeCell) {
        // Check if the chat widget is visible, open if not
        if (!widget.isVisible) {
          console.debug('Chat panel not visible. Activating chat panel.');
          app.shell.activateById(widget.id);
        }

        console.debug(
          'Dispatching jovyanai:addCurrentCellContext event for cell:',
          activeCell.model.id
        );
        const event = new CustomEvent('jovyanai:addCurrentCellContext');
        document.body.dispatchEvent(event);
      } else {
        console.warn('No active cell found to add to context.');
      }
      return null;
    }
  });

  // Add keyboard shortcut for adding cell context
  app.commands.addKeyBinding({
    command: 'jovyanai:addCurrentCellContext',
    keys: ['Alt L'], // Changed from Alt B to Alt L
    selector: 'body'
  });
}
