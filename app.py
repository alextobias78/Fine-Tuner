from flask import Flask, request, render_template, Response
from dataset_handler import create_dataset_entry, save_to_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        system_content = request.form['system_content']
        user_content = request.form['user_content']
        assistant_content = request.form['assistant_content']
        
        entry = create_dataset_entry(system_content, user_content, assistant_content)
        save_to_file(entry)
        return Response(entry, mimetype='application/json')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
