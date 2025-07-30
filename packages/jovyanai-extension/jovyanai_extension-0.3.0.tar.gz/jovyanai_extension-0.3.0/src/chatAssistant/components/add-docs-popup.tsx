'use client';

import React, { useState } from 'react';
import '../../../style/shared-popup.css';

interface IAddDocPopupProps {
  onClose: () => void;
  onSubmit: (
    name: string,
    file: File | null,
    link: string | null
  ) => Promise<void>;
}

export const AddDocPopup: React.FC<IAddDocPopupProps> = ({
  onClose,
  onSubmit
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [link, setLink] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  const handleSubmit = async () => {
    if (!name || (!file && !link)) {
      return;
    }
    setIsLoading(true);
    setIsSuccess(false);
    try {
      await onSubmit(name, file, link);
      setIsLoading(false);
      setIsSuccess(true);
      setTimeout(() => {
        onClose();
        setIsSuccess(false);
      }, 1500);
    } catch (error) {
      console.error('Submission error:', error);
      setIsLoading(false);
      onClose();
    }
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <button onClick={onClose} className="popup-close-button">
          &times;
        </button>
        {isLoading ? (
          <div className="popup-status">
            <h4>Indexing... ⏳</h4>
            <p>Please wait while your document is being processed.</p>
          </div>
        ) : isSuccess ? (
          <div className="popup-status">
            <h4>Success! ✅</h4>
            <p>Your document has been added.</p>
          </div>
        ) : (
          <>
            <h4 className="popup-title">Add New Document</h4>
            <input
              type="text"
              placeholder="Document Name (required)"
              value={name}
              onChange={e => setName(e.target.value)}
              disabled={isLoading}
              className="popup-input"
            />

            <div className="popup-drop-area">
              <input
                type="file"
                id="file-upload"
                style={{ display: 'none' }}
                onChange={e => setFile(e.target.files?.[0] || null)}
                disabled={isLoading}
              />
              <label
                htmlFor="file-upload"
                style={{
                  cursor: isLoading ? 'not-allowed' : 'pointer',
                  opacity: isLoading ? 0.5 : 1
                }}
              >
                Drag & drop file here
                <br />
                or click to browse
              </label>
            </div>
            {file && <p>File: {file.name}</p>}
            <p className="popup-divider">or</p>
            <input
              type="text"
              placeholder="Add URL"
              value={link}
              onChange={e => setLink(e.target.value)}
              className="popup-input"
              disabled={isLoading}
            />
            <button
              onClick={handleSubmit}
              disabled={!name || (!file && !link) || isLoading}
              className="popup-submit-button"
            >
              Submit
            </button>
          </>
        )}
      </div>
    </div>
  );
};
