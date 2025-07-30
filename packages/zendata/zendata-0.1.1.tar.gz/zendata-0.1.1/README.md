
# Zendata

## 📦 Zendata Framework

A lightweight Python library that standardizes **input and output data** handling across data processing pipelines. It provides a clean structure for defining **tasks** and **services** using [Pydantic](https://docs.pydantic.dev/) to validate both input and output data types at runtime.

---

### ✨ Features

* ✅ Enforces strict typing and validation using `pydantic`
* ⚙️ Separates business logic from data structure
* 🔁 Reusable services with runtime checks
* 🧪 Simple to test and extend

---

### 📚 Why Use This?

When working with data pipelines, it's common to pass data between stages without validating it — leading to subtle bugs or type mismatches.
This framework provides a standard way to wrap each step in a **Task** that holds both input and output, and a **Service** that processes data while validating contracts.

---

### 🚀 Quick Start

#### 1. Define a Task

```python
from zendata.tasks.base import BaseTask, TaskStatus

task_definition = BaseTask(
    name="Task",
    input=int,
    output=int,
)
```

#### 2. Create a Service

```python
from zendata.tasks.service import Service, 
from zendata.tasks.task import Task, TaskStatus

class MyService(Service):
    def apply(self, task: Task) -> Task:
        # Your core logic
        task.output_data = task.input_data * 2
        return task
```

#### 3. Run the Service

```python
service = MyService(task_definition=task_definition, name="MultiplyByTwo")

result_task: Task = service.run(123)  # Will raise if types mismatch
print(result_task.output_data)
```

---

### 📦 Install

```bash
uv sync
```

---

### 🧪 Testing

```bash
make test
```
