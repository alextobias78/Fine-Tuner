const form = document.querySelector('form');
const responseDiv = document.getElementById('response');
const addPromptButton = document.getElementById('add-prompt');
const promptsContainer = document.getElementById('prompts-container');
const themeToggle = document.getElementById('theme-toggle');
const submitButton = document.getElementById('submit-btn');
const multiPromptModeCheckbox = document.getElementById('multi_prompt_mode');

function createPromptSet() {
    const promptSet = document.createElement('div');
    promptSet.className = 'prompt-set';
    promptSet.innerHTML = `
        <label for="user_input">User Input:</label><br>
        <textarea class="user-input" name="user_input[]" rows="4" cols="50"></textarea><br><br>

        <label for="assistant_input">Assistant Input:</label><br>
        <textarea class="assistant-input" name="assistant_input[]" rows="4" cols="50"></textarea><br><br>

        <div class="weight-container" style="display: none;">
            <label for="weight">Weight:</label>
            <select class="weight" name="weight[]">
                <option value="1">1</option>
                <option value="0">0</option>
            </select><br><br>
        </div>

        <button type="button" class="remove-prompt"><i class="fas fa-trash"></i> Remove Prompt</button><br><br>
    `;
    return promptSet;
}

addPromptButton.addEventListener('click', () => {
    const newPromptSet = createPromptSet();
    promptsContainer.appendChild(newPromptSet);
});

promptsContainer.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-prompt')) {
        event.target.closest('.prompt-set').remove();
    }
});

multiPromptModeCheckbox.addEventListener('change', () => {
    addPromptButton.style.display = multiPromptModeCheckbox.checked ? 'inline-block' : 'none';
    const promptSets = promptsContainer.querySelectorAll('.prompt-set');
    promptSets.forEach((set, index) => {
        if (index === 0) return;
        set.style.display = multiPromptModeCheckbox.checked ? 'block' : 'none';
    });
    document.querySelectorAll('.weight-container').forEach(container => {
        container.style.display = multiPromptModeCheckbox.checked ? 'block' : 'none';
    });
});

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const icon = themeToggle.querySelector('i');
    const transitionDuration = getComputedStyle(document.documentElement).getPropertyValue('--transition-duration');
    if (document.body.classList.contains('dark-theme')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        document.body.style.transition = `background-color ${transitionDuration} ease, color ${transitionDuration} ease`;
    }
});

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Show loading spinner
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    form.appendChild(spinner);
    submitButton.disabled = true;

    const formData = new FormData(form);
    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    // Hide loading spinner
    spinner.remove();
    submitButton.disabled = false;

    const text = await response.text();
    responseDiv.innerHTML = `<p class="response-text">${text}</p>`;

    // Clear the input fields
    form.querySelectorAll('.user-input, .assistant-input').forEach(input => input.value = '');
});

// Initialize the form
multiPromptModeCheckbox.checked = false;
addPromptButton.style.display = 'none';

document.body.classList.add('dark-theme');

// Add subtle animations for form interactions
const formInputs = document.querySelectorAll('textarea, select, button');
formInputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.style.transform = 'scale(1.02)';
        input.style.transition = 'transform 0.2s ease';
    });
    input.addEventListener('blur', () => {
        input.style.transform = 'scale(1)';
    });
});

// Smooth scroll to response
responseDiv.addEventListener('DOMNodeInserted', () => {
    responseDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
});
