'use client';

import React, { useState } from 'react';
import { Clipboard, Check } from 'lucide-react';
import '../../../style/inline-code.css'; // We will create this file next

interface IInlineCodeProps {
  children?: React.ReactNode;
}

export const InlineCode: React.FC<IInlineCodeProps> = ({ children }) => {
  const [isCopied, setIsCopied] = useState(false);

  const codeString = React.Children.toArray(children).join(''); // Extract text content

  const handleCopy = (event: React.MouseEvent) => {
    event.stopPropagation(); // Prevent potential parent handlers
    navigator.clipboard.writeText(codeString).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 1500); // Reset after 1.5 seconds
    });
  };

  return (
    <code className="inline-code-container">
      <span className="inline-code-text">{children}</span>
      <button
        onClick={handleCopy}
        className="inline-code-copy-button"
        title="Copy code"
      >
        {isCopied ? <Check size={12} /> : <Clipboard size={12} />}
      </button>
    </code>
  );
};
