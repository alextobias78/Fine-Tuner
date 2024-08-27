import json

def create_dataset_entry(system_content, user_content, assistant_content):
    entry = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    return json.dumps(entry)

def save_to_file(entry, filename="dataset.jsonl"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def get_dataset_entries(filename="dataset.jsonl"):
    entries = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                entries.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return entries
