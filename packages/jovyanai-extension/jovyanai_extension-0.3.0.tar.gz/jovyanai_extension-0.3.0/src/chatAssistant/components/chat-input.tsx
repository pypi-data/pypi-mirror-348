'use client';

import React from 'react';
import { useState, useRef } from 'react';
import { ContextMenu } from './context-menu';
import '../../../style/chat-input.css';
import { IMessage } from '../types';
import { useChatContext } from '../ChatContextProvider';
import { clientIsConnected, getJovyanClient } from '../../jovyanClient';
import { showAuthReminderDialog } from '../../utils/authDialog';
import { useNotebookController } from '../../context/NotebookControllerContext';

interface IChatInputProps {
  onSendMessage: (message: IMessage) => Promise<void>;
  onCancel: () => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<IChatInputProps> = ({
  onSendMessage,
  onCancel,
  disabled = false
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const chatContext = useChatContext();
  const notebookController = useNotebookController();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || disabled) {
      return;
    }

    const client = await getJovyanClient();
    await client.connect();

    if (!clientIsConnected()) {
      console.debug(
        'Chat submit: Jovyan client not connected. Prompting for auth.'
      );
      const userCancelled = await showAuthReminderDialog(
        notebookController?.settingRegistry
      );
      if (userCancelled) {
        console.debug('Chat submit: Auth dialog cancelled by user.');
        return;
      }

      if (!clientIsConnected()) {
        console.warn(
          'Chat submit: Auth dialog closed but client still not connected.'
        );
        return;
      }
    }

    const userMessage: IMessage = {
      role: 'user',
      content: message.trim(),
      contexts: chatContext.activeContexts
    };

    await onSendMessage(userMessage);
    setMessage('');
    if (textareaRef.current) {
      textareaRef.current.style.height = '24px';
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    const textarea = e.target;
    textarea.style.height = '24px';
    const newHeight = Math.min(textarea.scrollHeight, 200);
    textarea.style.height = `${newHeight}px`;
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter without Shift
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (message.trim() && !disabled) {
        handleSubmit(e as unknown as React.FormEvent);
      }
    }

    // Cancel on Shift + Cmd/Ctrl + Backspace when disabled
    if (e.shiftKey && (e.metaKey || e.ctrlKey) && e.key === 'Backspace') {
      if (disabled) {
        e.preventDefault(); // Prevent default backspace behavior
        onCancel(); // Call the cancel function
      }
    }
  };

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-form">
        <ContextMenu disabled={disabled} />

        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-textarea"
            value={message}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask, learn, brainstorm"
            disabled={disabled}
          />
        </div>

        <div className="input-controls">
          <div className="send-container">
            <span className="model-name">gemini-2.5-pro</span>
            {disabled ? (
              <button
                type="button"
                className="chat-input-cancel-button"
                onClick={onCancel}
              >
                Cancel Run
              </button>
            ) : (
              <button
                type="submit"
                className="send-button"
                disabled={!message.trim()}
              >
                Send <span className="enter-icon">↵</span>
              </button>
            )}
          </div>
        </div>
      </form>
    </div>
  );
};
