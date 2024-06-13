import React from 'react';
import Task from './Task';

function ToDoList({ tasks, showCompleted, toggleTaskCompleted }) {
  return (
    <div>
      {tasks.length === 0 ? (
        <p>No tasks to display</p>
      ) : (
        <ul>
          {tasks
            .filter((task) => showCompleted || !task.completed)
            .map((task) => (
              <Task key={task.id} task={task} toggleTaskCompleted={toggleTaskCompleted} />
            ))}
        </ul>
      )}
    </div>
  );
}

export default ToDoList;
