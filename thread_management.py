import time

def generate_response(client, message_body, thread_id=None):
    if thread_id is None:
        # Create a new thread if no thread ID is provided
        thread = client.beta.threads.create()
        thread_id = thread.id
    # Add the message to the thread (new or existing)
    client.beta.threads.messages.create(
       thread_id=thread_id,
       role="user",
       content=message_body,
    )
    return thread_id


def run_assistant(client, assistant_id, thread_id):
    assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.retrieve(thread_id)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    for message in messages.data:
        if message.role == "assistant":
            assistant_response = message.content[0].text.value
            return assistant_response

    return "No response from the assistant."
