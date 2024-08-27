import json

def create_dataset_entry(system_content, user_content, assistant_content):
    entry = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    return entry

def save_to_file(entry, filename="dataset.jsonl"):
    with open(filename, "a") as f:
        f.write(json.dumps(entry) + "\n")
