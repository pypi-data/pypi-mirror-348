# Api examples

Run example 
```bash
uv run uvicorn examples.api.main:app --reload
```
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from zendata.data.ml.generation.text import Conversation, Message
from zendata.tasks.service import Service
from zendata.tasks.task import BaseTask, Task
from zendata.api.health import Health


class LLMService(Service):
    def apply(self, task: Task) -> Task:
        # Your core logic
        task.output_data = Message(user_id="system", message="Noting to add")
        return task


llm_task_definition = BaseTask(input=Message, output=Message)

llm_service = LLMService(task_definition=llm_task_definition, name="fake_llm")

fake_conversation_db: dict[str, Conversation] = {}

app = FastAPI()


@app.post("/conversation/{conversation_id}/message", response_model=Conversation)
def send_message(conversation_id: str, message: Message):
    if conversation_id not in fake_conversation_db:
        fake_conversation_db[conversation_id] = Conversation(
            conversation_id=conversation_id, messages=[]
        )
    fake_conversation_db[conversation_id].messages.append(message)
    task = llm_service.run(input_data=message)
    fake_conversation_db[conversation_id].messages.append(task.output_data)

    return fake_conversation_db[conversation_id]


@app.get("/conversation/{conversation_id}", response_model=Conversation)
def get_conversation(conversation_id: str):
    if conversation_id not in fake_conversation_db:
        fake_conversation_db[conversation_id] = Conversation(
            conversation_id=conversation_id, messages=[]
        )
    return fake_conversation_db[conversation_id]


health = Health(
    status="healthy",
    name="service-main",
    status_code=200,
    error=None,
    dependencies=[
        Health(
            name="service-second",
            status_code=500,
            status="unhealthy",
            error="Bad request",
        )
    ],
)


@app.get("/health/", response_model=Health)
def get_conversation():
    return JSONResponse(content=health.model_dump(), status_code=health.status_code)

```