'use client';

import React from 'react';
import { CodeBlock } from './code-block'; // Now we will use this again
import { InlineCode } from './inline-code'; // Import the new component
import '../../../style/chat-message.css';
import type { IMessage } from '../types';
import { useChatContext } from '../ChatContextProvider';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'; // Restore GFM

interface IChatMessageProps {
  message: IMessage;
  isThinking?: boolean; // Add the optional thinking prop
}

export const ChatMessage: React.FC<IChatMessageProps> = ({
  message,
  isThinking // Destructure the new prop
}) => {
  const chatContextController = useChatContext();

  // Render content using ReactMarkdown with custom component for code blocks
  const renderMarkdownContent = (content: string) => {
    return (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]} // Restore GFM
        components={{
          // Only override `code`. Differentiate based on className presence.
          code({ node, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');

            if (match) {
              // ClassName like "language-python" exists - render Block
              const codeContent = String(children).replace(/\n$/, '');
              const language = match[1];
              return <CodeBlock code={codeContent} language={language} />;
            } else {
              return <InlineCode {...props}>{children}</InlineCode>;
            }
          }
          // No `pre` override needed anymore
        }}
      >
        {content}
      </ReactMarkdown>
    );
  };

  // If isThinking is true, render a simple indicator
  if (isThinking) {
    return (
      <div className={'message assistant thinking'}>
        <div className="message-content">
          <div className="thinking-indicator">
            Thinking<span className="dot">.</span>
            <span className="dot">.</span>
            <span className="dot">.</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`message ${message.role}`}>
      {message.role === 'user' &&
        message.contexts &&
        message.contexts.length > 0 && (
          <div className="message-header">
            {message.contexts.map((context, index) => (
              <span key={index} className={`context-tag ${context.type}`}>
                @{chatContextController.getContextName(context)}
              </span>
            ))}
          </div>
        )}

      {/* Use the markdown renderer with custom code block handling */}
      <div className="message-content">
        {renderMarkdownContent(message.content)}
      </div>
    </div>
  );
};
