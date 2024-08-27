from flask import Flask, request, render_template, jsonify
from dataset_handler import create_dataset_entry, save_to_file, get_dataset_entries

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        system_content = request.form['system_content']
        chat_type = request.form['chat_type']
        
        if chat_type == 'single':
            user_content = request.form['user_content']
            assistant_content = request.form['assistant_content']
            messages = [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
        else:  # multi-turn
            messages = json.loads(request.form['messages'])
        
        entry = create_dataset_entry(system_content, messages)
        save_to_file(entry)
        return jsonify(entry)
    
    return render_template('index.html', entries=get_dataset_entries())

if __name__ == '__main__':
    app.run(debug=True)
