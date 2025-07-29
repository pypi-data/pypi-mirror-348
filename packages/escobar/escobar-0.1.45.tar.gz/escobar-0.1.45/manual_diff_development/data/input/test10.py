"""
Task management system
"""

class Task:
    def __init__(self, title, description="", due_date=None, priority="medium", status="pending"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.tags = []
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
    
    def mark_completed(self):
        self.status = "completed"
    
    def mark_pending(self):
        self.status = "pending"
    
    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "None"
        due_date_str = self.due_date if self.due_date else "None"
        return f"Task: {self.title} | Priority: {self.priority} | Status: {self.status} | Due: {due_date_str} | Tags: {tags_str}"

class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
        return len(self.tasks) - 1  # Return the index of the added task
    
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False
    
    def get_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None
    
    def get_all_tasks(self):
        return self.tasks
    
    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority == priority]
    
    def get_tasks_by_tag(self, tag):
        return [task for task in self.tasks if tag in task.tags]

def main():
    # Create a task manager
    manager = TaskManager()
    
    # Add some tasks
    task1 = Task("Complete project", "Finish the Python project", "2023-12-31", "high")
    task1.add_tag("work")
    task1.add_tag("python")
    
    task2 = Task("Buy groceries", "Milk, eggs, bread", "2023-11-15", "medium")
    task2.add_tag("personal")
    
    task3 = Task("Read book", "Clean Code by Robert C. Martin", "2023-12-15", "low")
    task3.add_tag("personal")
    task3.add_tag("learning")
    
    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)
    
    # Mark a task as completed
    task2.mark_completed()
    
    # Print all tasks
    print("All Tasks:")
    for i, task in enumerate(manager.get_all_tasks()):
        print(f"{i}: {task}")
    
    print("\nPending Tasks:")
    for task in manager.get_tasks_by_status("pending"):
        print(task)
    
    print("\nPersonal Tasks:")
    for task in manager.get_tasks_by_tag("personal"):
        print(task)

if __name__ == "__main__":
    main()
