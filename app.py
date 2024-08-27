from flask import Flask, render_template, request, send_file, jsonify
import json
import io
import os
from datetime import datetime

app = Flask(__name__)

DATASETS_DIR = 'datasets'
os.makedirs(DATASETS_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        system_prompt = data.get('systemPrompt', '')
        conversations = json.loads(data.get('conversations', '[]'))
        
        dataset = []
        for conv in conversations:
            dataset.append({
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conv['userPrompt']},
                    {"role": "assistant", "content": conv['assistantResponse']}
                ]
            })
        
        jsonl_content = '\n'.join(json.dumps(item) for item in dataset)
        
        # Save the dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'dataset_{timestamp}.jsonl'
        filepath = os.path.join(DATASETS_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(jsonl_content)
        
        return jsonify({
            "message": "Dataset created successfully", 
            "filename": filename,
            "content": jsonl_content  # Return the content of the dataset
        })
    
    return render_template('index.html')

@app.route('/datasets', methods=['GET'])
def get_datasets():
    datasets = [f for f in os.listdir(DATASETS_DIR) if f.endswith('.jsonl')]
    return jsonify(datasets)

@app.route('/download/<filename>', methods=['GET'])
def download_dataset(filename):
    return send_file(os.path.join(DATASETS_DIR, filename), as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_dataset(filename):
    filepath = os.path.join(DATASETS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": f"Dataset {filename} deleted successfully"}), 200
    else:
        return jsonify({"message": f"Dataset {filename} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)