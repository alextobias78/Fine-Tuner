let messageCounter = 0;

document.addEventListener('DOMContentLoaded', function() {
    const systemContentInput = document.getElementById('system_content');
    const saveSystemPromptBtn = document.getElementById('saveSystemPrompt');
    const chatTypeInputs = document.querySelectorAll('input[name="chat_type"]');
    const singleTurnInputs = document.getElementById('single-turn-inputs');
    const multiTurnInputs = document.getElementById('multi-turn-inputs');
    const addMessageBtn = document.getElementById('add-message');
    const datasetForm = document.getElementById('datasetForm');
    const entriesContainer = document.getElementById('entries');
    const resultNotification = document.getElementById('result');

    // Load saved system prompt from localStorage
    const savedSystemPrompt = localStorage.getItem('savedSystemPrompt');
    if (savedSystemPrompt) {
        systemContentInput.value = savedSystemPrompt;
    }

    saveSystemPromptBtn.addEventListener('click', function() {
        localStorage.setItem('savedSystemPrompt', systemContentInput.value);
        showNotification('System prompt saved!', 'success');
    });

    // Update localStorage when system prompt changes
    systemContentInput.addEventListener('input', function() {
        localStorage.setItem('savedSystemPrompt', this.value);
    });

    // Ensure the system prompt is always up to date
    datasetForm.addEventListener('submit', function(e) {
        const currentSystemPrompt = systemContentInput.value;
        localStorage.setItem('savedSystemPrompt', currentSystemPrompt);
    });

    chatTypeInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'single') {
                singleTurnInputs.style.display = 'block';
                multiTurnInputs.style.display = 'none';
            } else {
                singleTurnInputs.style.display = 'none';
                multiTurnInputs.style.display = 'block';
            }
        });
    });

    addMessageBtn.addEventListener('click', addMessageInput);

    datasetForm.addEventListener('submit', handleFormSubmit);

    // Initial dataset load
    fetchDatasetEntries();
});

function addMessageInput() {
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
}

function handleFormSubmit(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const currentSystemPrompt = document.getElementById('system_content').value;
    formData.set('system_content', currentSystemPrompt);

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
    .then(response => response.json())
    .then(data => {
        showNotification('Entry added successfully!', 'success');
        addEntryToPreview(data);
        resetForm();
    })
    .catch(error => {
        showNotification('Error adding entry. Please try again.', 'error');
        console.error('Error:', error);
    });
}

function showNotification(message, type) {
    const notification = document.getElementById('result');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

function addEntryToPreview(entry) {
    const entryElement = document.createElement('div');
    entryElement.className = 'entry';
    entryElement.innerHTML = `<pre>${JSON.stringify(entry, null, 2)}</pre>`;
    document.getElementById('entries').prepend(entryElement);
}

function resetForm() {
    document.getElementById('datasetForm').reset();
    document.getElementById('multi-turn-messages').innerHTML = '';
}


function fetchDatasetEntries() {
    fetch('/get_entries')
    .then(response => response.json())
    .then(entries => {
        const entriesContainer = document.getElementById('entries');
        entriesContainer.innerHTML = '';
        entries.forEach(entry => addEntryToPreview(entry));
    })
    .catch(error => {
        console.error('Error fetching entries:', error);
        showNotification('Error loading dataset entries.', 'error');
    });
}
