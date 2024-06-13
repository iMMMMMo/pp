import React from 'react';

function Task({ task, toggleTaskCompleted }) {
  return (
    <li>
      <label>
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => toggleTaskCompleted(task.id)}
        />
        {task.text}
      </label>
    </li>
  );
}

export default Task;
