import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user's input and system prompt
        user_input = request.form.get("user_input")
        system_prompt = request.form.get("system_prompt")

        # TODO: Implement fine-tuning logic here using user_input and system_prompt

        # For now, just return a dummy response
        response_lines = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": "This is a dummy response. Fine-tuning logic needs to be implemented."}
        ]
        response_jsonl = "\n".join([json.dumps(line) for line in response_lines])
        return response_jsonl
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
