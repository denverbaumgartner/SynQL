"""
API REQUEST BATCH PROCESSOR

OpenAI now supports batch processing of API requests. This file is intended to provide an easy interface for building, 
sending, and receiving batch requests.

## Preparing a Batch File

A batch file is a JSONL file that contains a list of JSON objects. Each object represents a single request. Note the need for a unique identifier for each request.

```jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
```

## Uploading a Batch File

```python
from openai import OpenAI
client = OpenAI()

batch_input_file = client.files.create(
  file=open("batchinput.jsonl", "rb"),
  purpose="batch"
)
```

## Creating the batch request

```python
batch_input_file_id = batch_input_file.id

client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)
```

## Batch Object 

The batch object results in a JSON object as follows:

```json
{
  "id": "batch_abc123",
  "object": "batch",
  "endpoint": "/v1/chat/completions",
  "errors": null,
  "input_file_id": "file-abc123",
  "completion_window": "24h",
  "status": "validating",
  "output_file_id": null,
  "error_file_id": null,
  "created_at": 1714508499,
  "in_progress_at": null,
  "expires_at": 1714536634,
  "completed_at": null,
  "failed_at": null,
  "expired_at": null,
  "request_counts": {
    "total": 0,
    "completed": 0,
    "failed": 0
  },
  "metadata": null
}
```
"""

# system packages
import json
from typing import Optional

# external packages
from openai import OpenAI

# internal packages

# client = OpenAI()

def prepare_batch_request_file(
        input_file_path: str,
        output_file_path: str,
): 
    """We are going to have this be specific to our current use case, and then can make it extensible later.
    
    We assume a jsonl file that looks like the following: 
    {
        "model": "gpt-4",
        "messages": "[
            {"role": "system", "content": "hello world!"},
            {"role": "user", "content": "hello world!"},
        ]",
        "temperature": 0.7,
    }
    """
    with open(input_file_path, 'r') as f: 
        reqs = [json.loads(line) for line in f]
    

    id = 0
    update_reqs = []
    for req in reqs: 
        update_req = {}
        update_req["custom_id"] = f"request-{id}"
        id += 1
        update_req["method"] = "POST"
        update_req["url"] = "/v1/chat/completions"
        update_req["body"] = {
            "model": req["model"],
            "temperature": req["temperature"],
            "messages": req["messages"],
        }
        update_reqs.append(update_req)

    with open(output_file_path, 'w') as f:
        for req in update_reqs: 
            f.write(json.dumps(req) + '\n')
        
def upload_batch_request_file(
        client: OpenAI,
        upload_file_path: str,
        # save_object: bool = False,
        # save_path: str = None,
):
    """Takes the local path to a batch request file and uploads it to OpenAI. Returns the file id."""
    batch_input_file = client.files.create(
        file=open(upload_file_path, "rb"),
        purpose="batch"
    )
    return batch_input_file.id

def create_batch_request(
        client: OpenAI,
        upload_file_path: str,
        description: str,
        save_path: Optional[str] = None,
        endpoint: Optional[str] = "/v1/chat/completions",
        completion_window: Optional[str] = "24h",   
):
    file_id = upload_batch_request_file(
        client=client,
        upload_file_path=upload_file_path
    )
    batch = client.batches.create(
        input_file_id=file_id,
        endpoint=endpoint,
        completion_window=completion_window,
        metadata={
            "description": description
        }
    )
    if save_path:
        with open(save_path, 'w') as f:
            f.write(json.dumps(batch))
    return batch