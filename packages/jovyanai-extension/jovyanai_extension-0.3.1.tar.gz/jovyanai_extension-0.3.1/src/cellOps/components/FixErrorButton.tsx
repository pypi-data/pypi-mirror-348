// button in the top right corner of the cell to activate AI commands

import React, { useState } from 'react';

const FixErrorButton = ({
  onClick,
  text
}: {
  onClick: () => void;
  text: string;
}) => {
  // Text is Generate code on new cell or Change code in cell with some existing code
  const [tooltipVisible, setTooltipVisible] = useState(false);

  // get shortcut keybinding by checking if Mac
  //   const isMac = /Mac/i.test(navigator.userAgent);
  const shortcut = '⇧F';
  const shortcutText = 'Shift+F';

  return (
    <div className="jv-cell-fix-error-container">
      <button
        className="jv-cell-fix-error-button"
        title={`Fix Error ${shortcut}`}
        onClick={onClick}
        onMouseEnter={() => setTooltipVisible(true)}
        onMouseLeave={() => setTooltipVisible(false)}
      >
        {text} <span style={{ fontSize: '0.8em' }}>{shortcut}</span>
      </button>
      {tooltipVisible && (
        <div className="jv-cell-fix-error-tooltip">
          Fix this error with AI ({shortcutText})
        </div>
      )}
    </div>
  );
};

export default FixErrorButton;
