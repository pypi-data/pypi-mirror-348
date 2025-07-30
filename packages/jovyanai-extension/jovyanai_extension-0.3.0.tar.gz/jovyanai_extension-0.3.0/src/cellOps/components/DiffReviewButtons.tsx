import React, { useEffect, useState } from 'react';
// import posthog from 'posthog-js';

const ButtonWithTooltip: React.FC<{
  onClick: () => void;
  className: string;
  text: string;
  shortcut: string;
  tooltip: string;
}> = ({ onClick, className, text, shortcut, tooltip }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="jv-cell-diff-review-button-container">
      <button
        onClick={onClick}
        className={className}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        title={`${text} ${shortcut}`}
      >
        {text} <span style={{ fontSize: '0.7em' }}>{shortcut}</span>
      </button>
      {showTooltip && (
        <div className="tooltip">
          {tooltip}
          <br />
          Shortcut: <strong>{shortcut}</strong>
        </div>
      )}
    </div>
  );
};

interface IButtonsContainerProps {
  buttonsRef: React.RefObject<HTMLDivElement>;
  onAcceptAndRun: () => void;
  onAccept: () => void;
  onReject: () => void;
  onEditPrompt: () => void;
}

export const ButtonsContainer: React.FC<IButtonsContainerProps> = ({
  buttonsRef,
  onAcceptAndRun,
  onAccept,
  onReject
  // onEditPrompt
}) => {
  useEffect(() => {
    if (buttonsRef.current) {
      buttonsRef.current.focus({ preventScroll: true });
    }
  }, []);

  // const isMac = /Mac/i.test(navigator.userAgent);

  return (
    <div
      className="jv-diff-review-buttons-container"
      tabIndex={0}
      ref={buttonsRef}
      onKeyDown={event => {
        if (event.key === 'Enter') {
          event.preventDefault();
          if (!event.shiftKey && !(event.metaKey || event.ctrlKey)) {
            const acceptButton = document.querySelector(
              '.accept-button'
            ) as HTMLButtonElement;
            acceptButton.click();
          } else if (event.shiftKey) {
            const acceptAndRunButton = document.querySelector(
              '.accept-and-run-button'
            ) as HTMLButtonElement;
            acceptAndRunButton.click();
          }
        } else if (event.key === 'm' && (event.metaKey || event.ctrlKey)) {
          event.preventDefault();
          const editPromptButton = document.querySelector(
            '.edit-prompt-button'
          ) as HTMLButtonElement;
          editPromptButton.click();
        } else if (event.key === 'Escape') {
          event.preventDefault();
          const rejectButton = document.querySelector(
            '.reject-button'
          ) as HTMLButtonElement;
          rejectButton.click();
        }
      }}
      onBlur={() => {
        // Refocus the container when it loses focus
        if (buttonsRef.current) {
          buttonsRef.current.focus({ preventScroll: true });
        }
      }}
    >
      <ButtonWithTooltip
        onClick={onAcceptAndRun}
        className="accept-and-run-button"
        text="Accept & Run"
        shortcut="Shift + Enter"
        tooltip="Accept the changes and run the code in the current cell."
      />
      <ButtonWithTooltip
        onClick={onReject}
        className="reject-button"
        text="Reject"
        shortcut="Escape"
        tooltip="Reject the changes and revert to the original code."
      />
      <ButtonWithTooltip
        onClick={onAccept}
        className="accept-button"
        text="Accept"
        shortcut="Enter"
        tooltip="Accept the changes and keep the code in the current cell."
      />

      {/* <ButtonWithTooltip
                onClick={onEditPrompt}
                className="edit-prompt-button"
                text="Modify"
                shortcut={isMac ? "⌘ + M" : "Ctrl + M"}
                tooltip="Edit your last prompt."
            /> */}
    </div>
  );
};
