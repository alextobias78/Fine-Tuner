import json
import os
import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# Generate a random filename for the JSONL file once
filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.jsonl'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user's input and system prompt
        user_input = request.form.get("user_input")
        system_prompt = request.form.get("system_prompt")

        # TODO: Implement fine-tuning logic here using user_input and system_prompt


        # Prepare the response lines
        response_lines = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": request.form.get("assistant_input") or ""}
        ]

        # Append the entries to the JSONL file
        with open(filename, 'a') as f:
            for line in response_lines:
                f.write(json.dumps(line) + '\n')

        return "Entries have been saved to " + filename
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
