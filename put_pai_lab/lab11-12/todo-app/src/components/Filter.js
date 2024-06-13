import React from 'react';

function Filter({ showCompleted, toggleShowCompleted }) {
  return (
    <div>
      <label>
        <input type="checkbox" checked={showCompleted} onChange={toggleShowCompleted} />
        Show Completed
      </label>
    </div>
  );
}

export default Filter;
