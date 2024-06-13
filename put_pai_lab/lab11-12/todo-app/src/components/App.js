import React, { useState } from 'react';
import Filter from './Filter';
import ToDoList from './ToDoList';
import NewTask from './NewTask';

function App() {
  const [tasks, setTasks] = useState([]);
  const [showCompleted, setShowCompleted] = useState(true);

  const addTask = (task) => {
    setTasks([...tasks, { id: Date.now(), text: task, completed: false }]);
  };

  const toggleTaskCompleted = (taskId) => {
    setTasks(
      tasks.map((task) =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const toggleShowCompleted = () => {
    setShowCompleted(!showCompleted);
  };

  return (
    <div className="app">
      <h1>To-Do List</h1>
      <Filter showCompleted={showCompleted} toggleShowCompleted={toggleShowCompleted} />
      <NewTask addTask={addTask} />
      <ToDoList tasks={tasks} showCompleted={showCompleted} toggleTaskCompleted={toggleTaskCompleted} />
    </div>
  );
}

export default App;
