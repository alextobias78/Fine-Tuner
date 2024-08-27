document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('datasetForm');
    const addConversationBtn = document.getElementById('addConversation');
    const systemPromptInput = document.getElementById('systemPrompt');
    const userPromptInput = document.getElementById('userPrompt');
    const assistantResponseInput = document.getElementById('assistantResponse');
    const datasetsContainer = document.getElementById('datasetsContainer');
    const previewContainer = document.getElementById('datasetPreview');

    let conversations = [];

    // Load saved system prompt
    const savedSystemPrompt = localStorage.getItem('systemPrompt');
    if (savedSystemPrompt) {
        systemPromptInput.value = savedSystemPrompt;
    }

    // Save system prompt when it changes
    systemPromptInput.addEventListener('input', function() {
        localStorage.setItem('systemPrompt', this.value);
        updateDatasetPreview();
    });

    addConversationBtn.addEventListener('click', function() {
        const userPrompt = userPromptInput.value.trim();
        const assistantResponse = assistantResponseInput.value.trim();

        if (userPrompt && assistantResponse) {
            conversations.push({
                userPrompt: userPrompt,
                assistantResponse: assistantResponse
            });

            // Clear input fields
            userPromptInput.value = '';
            assistantResponseInput.value = '';

            updateDatasetPreview();
        } else {
            alert('Please fill in both User Prompt and Assistant Response before adding a new conversation.');
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const systemPrompt = systemPromptInput.value;

        // Check if there's at least one conversation
        if (conversations.length === 0) {
            // If no conversations in the array, check if current fields are filled
            const currentUserPrompt = userPromptInput.value.trim();
            const currentAssistantResponse = assistantResponseInput.value.trim();
            if (currentUserPrompt && currentAssistantResponse) {
                conversations.push({
                    userPrompt: currentUserPrompt,
                    assistantResponse: currentAssistantResponse
                });
            } else {
                alert('Please add at least one conversation before generating the dataset.');
                return;
            }
        }

        const formData = new FormData();
        formData.append('systemPrompt', systemPrompt);
        formData.append('conversations', JSON.stringify(conversations));

        fetch('/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadDatasets();
            // Display the dataset content
            const datasetContent = document.getElementById('datasetContent');
            datasetContent.textContent = data.content;
            document.getElementById('datasetContentSection').style.display = 'block';

            // Clear inputs after successful submission
            systemPromptInput.value = '';
            userPromptInput.value = '';
            assistantResponseInput.value = '';
            conversations = [];
            updateDatasetPreview();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    function loadDatasets() {
        fetch('/datasets')
            .then(response => response.json())
            .then(datasets => {
                datasetsContainer.innerHTML = '';
                datasets.forEach(dataset => {
                    const datasetElement = document.createElement('div');
                    datasetElement.className = 'dataset-item card';
                    datasetElement.innerHTML = `
                        <div class="card-body">
                            <h5 class="card-title">${dataset}</h5>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-primary download-btn" data-filename="${dataset}">Download</button>
                                <button class="btn btn-sm btn-danger delete-btn" data-filename="${dataset}">Delete</button>
                            </div>
                        </div>
                    `;
                    datasetsContainer.appendChild(datasetElement);
                });
                addDownloadListeners();
                addDeleteListeners();
            });
    }

    function addDownloadListeners() {
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filename = this.getAttribute('data-filename');
                window.location.href = `/download/${filename}`;
            });
        });
    }

    function addDeleteListeners() {
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filename = this.getAttribute('data-filename');
                if (confirm(`Are you sure you want to delete ${filename}?`)) {
                    fetch(`/delete/${filename}`, { method: 'DELETE' })
                        .then(response => response.json())
                        .then(data => {
                            alert(data.message);
                            loadDatasets();
                        })
                        .catch(error => console.error('Error:', error));
                }
            });
        });
    }

    // Load datasets when the page loads
    loadDatasets();

    // Dark mode functionality
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Check for saved dark mode preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // Set initial dark mode state
    if (isDarkMode) {
        body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    // Toggle dark mode
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    });

    function updateDatasetPreview() {
        const systemPrompt = systemPromptInput.value;
        const currentUserPrompt = userPromptInput.value.trim();
        const currentAssistantResponse = assistantResponseInput.value.trim();

        let previewConversations = [...conversations];
        if (currentUserPrompt && currentAssistantResponse) {
            previewConversations.push({
                userPrompt: currentUserPrompt,
                assistantResponse: currentAssistantResponse
            });
        }

        if (previewConversations.length === 0) {
            previewContainer.textContent = "No conversations added yet. Add a conversation or fill in the current fields to see a preview.";
            return;
        }

        const dataset = previewConversations.map(conv => ({
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: conv.userPrompt },
                { role: "assistant", content: conv.assistantResponse }
            ]
        }));

        const jsonlContent = dataset.map(item => JSON.stringify(item)).join('\n');
        previewContainer.textContent = jsonlContent;
    }

    // Update preview when inputs change
    systemPromptInput.addEventListener('input', updateDatasetPreview);
    userPromptInput.addEventListener('input', updateDatasetPreview);
    assistantResponseInput.addEventListener('input', updateDatasetPreview);

    // Initial preview update
    updateDatasetPreview();
});
