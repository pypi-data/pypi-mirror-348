// button in the top right corner of the cell to activate AI commands

import React, { useState } from 'react';

const ActivateCellButton = ({
  onClick,
  text
}: {
  onClick: () => void;
  text: string;
}) => {
  // Text is Generate code on new cell or Change code in cell with some existing code
  const [tooltipVisible, setTooltipVisible] = useState(false);

  // get shortcut keybinding by checking if Mac
  const isMac = /Mac/i.test(navigator.userAgent);
  const shortcut = isMac ? '⌘K' : '^K';
  const shortcutText = isMac ? 'Cmd+K' : 'Ctrl+K';

  return (
    <div className="jv-cell-ai-button-container">
      <button
        className="jv-cell-ai-button"
        title={`Generate code ${shortcut}`}
        onClick={onClick}
        onMouseEnter={() => setTooltipVisible(true)}
        onMouseLeave={() => setTooltipVisible(false)}
      >
        {text} <span style={{ fontSize: '0.8em' }}>{shortcut}</span>
      </button>
      {tooltipVisible && (
        <div className="jv-cell-ai-tooltip">
          Open the prompt box to instruct AI ({shortcutText})
        </div>
      )}
    </div>
  );
};

export default ActivateCellButton;
