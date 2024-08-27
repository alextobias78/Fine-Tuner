let savedSystemPrompt = '';
let messageCounter = 0;

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('saveSystemPrompt').addEventListener('click', function() {
        savedSystemPrompt = document.getElementById('system_content').value;
        alert('System prompt saved!');
    });

    document.getElementById('chat_type').addEventListener('change', function() {
        const singleTurnInputs = document.getElementById('single-turn-inputs');
        const multiTurnInputs = document.getElementById('multi-turn-inputs');
        if (this.value === 'single') {
            singleTurnInputs.style.display = 'block';
            multiTurnInputs.style.display = 'none';
        } else {
            singleTurnInputs.style.display = 'none';
            multiTurnInputs.style.display = 'block';
        }
    });

    document.getElementById('add-message').addEventListener('click', function() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message-input';
        messageDiv.innerHTML = `
            <select name="role_${messageCounter}">
                <option value="user">User</option>
                <option value="assistant">Assistant</option>
            </select>
            <textarea name="content_${messageCounter}" placeholder="Message content"></textarea>
            <input type="number" name="weight_${messageCounter}" min="0" max="1" step="1" value="1" placeholder="Weight (0 or 1)">
            <button type="button" class="remove-message">Remove</button>
        `;
        document.getElementById('multi-turn-messages').appendChild(messageDiv);
        messageCounter++;

        messageDiv.querySelector('.remove-message').addEventListener('click', function() {
            messageDiv.remove();
        });
    });

    document.getElementById('datasetForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        if (savedSystemPrompt) {
            formData.set('system_content', savedSystemPrompt);
        }

        if (formData.get('chat_type') === 'multi') {
            const messages = [];
            document.querySelectorAll('.message-input').forEach((messageDiv, index) => {
                const role = messageDiv.querySelector(`select[name="role_${index}"]`).value;
                const content = messageDiv.querySelector(`textarea[name="content_${index}"]`).value;
                const weight = parseInt(messageDiv.querySelector(`input[name="weight_${index}"]`).value);
                messages.push({role, content, weight});
            });
            formData.set('messages', JSON.stringify(messages));
        }

        fetch('/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            const notification = document.getElementById('result');
            notification.textContent = 'Entry added successfully!';
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
            
            document.getElementById('entries').innerHTML = `<pre>${data}</pre>` + document.getElementById('entries').innerHTML;
            document.getElementById('user_content').value = '';
            document.getElementById('assistant_content').value = '';
            document.getElementById('multi-turn-messages').innerHTML = '';
        });
    });
});
