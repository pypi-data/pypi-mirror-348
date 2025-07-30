'use client';

import React, { useState } from 'react';
import '../../../style/shared-popup.css';

interface IAddGitRepoPopupProps {
  onClose: () => void;
  onSubmit: (name: string, url: string) => void;
}

export const AddGitRepoPopup: React.FC<IAddGitRepoPopupProps> = ({
  onClose,
  onSubmit
}) => {
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  const handleSubmit = async () => {
    if (!name || !url) {
      return;
    }
    setIsLoading(true);
    setIsSuccess(false);
    try {
      await onSubmit(name, url);
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
            <p>Please wait while your repository is being processed.</p>
          </div>
        ) : isSuccess ? (
          <div className="popup-status">
            <h4>Success! ✅</h4>
            <p>Your repository has been added.</p>
          </div>
        ) : (
          <>
            <h4 className="popup-title">Add Git Repository</h4>
            <input
              type="text"
              placeholder="Repository Name (required)"
              value={name}
              onChange={e => setName(e.target.value)}
              disabled={isLoading}
              className="popup-input"
            />
            <input
              type="text"
              placeholder="Repository URL (required)"
              value={url}
              onChange={e => setUrl(e.target.value)}
              disabled={isLoading}
              className="popup-input"
            />
            <button
              onClick={handleSubmit}
              disabled={!name || !url || isLoading}
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
