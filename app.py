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
        system_prompt = request.form.get("system_prompt")
        multi_prompt_mode = request.form.get("multi_prompt_mode") == "on"

        user_inputs = request.form.getlist("user_input[]")
        assistant_inputs = request.form.getlist("assistant_input[]")
        weights = request.form.getlist("weight[]")

        messages = [{"role": "system", "content": system_prompt}]

        if multi_prompt_mode:
            for user_input, assistant_input, weight in zip(user_inputs, assistant_inputs, weights):
                if user_input:
                    messages.append({"role": "user", "content": user_input})
                if assistant_input:
                    messages.append({"role": "assistant", "content": assistant_input, "weight": int(weight)})
        else:
            if user_inputs[0]:
                messages.append({"role": "user", "content": user_inputs[0]})
            if assistant_inputs[0]:
                messages.append({"role": "assistant", "content": assistant_inputs[0]})

        response_data = {"messages": messages}

        # Append the entry to the JSONL file
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(response_data) + '\n')

        return f"Entries have been saved to {filename}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
