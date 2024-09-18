# GPT-4 Fine-Tuner

## Introduction
This application allows users to create and save fine-tuning data for GPT-4 by providing system prompts alongside user and assistant inputs. It supports a "multi-prompt mode" that allows users to provide multiple sets of user and assistant inputs with optional weights.

## Features
- Generate fine-tuning data for GPT-4 models.
- Multi-prompt mode for advanced fine-tuning scenarios.
- Dark mode toggle for improved user experience.

## Technologies Used
- Python
- Flask
- HTML
- CSS
- JavaScript

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/alextobias78/Fine-Tuner.git
    cd Fine-Tuner
    ```

2. **Install the required packages:**
    ```bash
    pip install flask
    ```

## Running the Application

1. **Start the Flask server:**
    ```bash
    python app.py
    ```

2. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:5000/
    ```

## Usage

### Home Page
- Enter the `System Prompt` in the provided text area.
- Add user and assistant inputs by clicking the "Add Prompt" button.
- To enable multi-prompt mode, check the `Multi-Prompt Mode` checkbox.
  - When multi-prompt mode is enabled, you can provide weights for each set of inputs.
- Click the `Submit` button to save the entries.

### Toggle Dark Mode
- Click the moon/sun icon at the top to toggle between light and dark themes.

## File Structure

- `app.py`:
  - The main Flask application file.
  - Routes and logic for handling data submission and rendering the HTML template.

- `templates/index.html`:
  - The HTML template for the main interface.
  - Contains a form for entering system prompts, user inputs, assistant inputs, and a response area for displaying results.

- `static/script.js`:
  - Handles the front-end logic for the form submission.
  - Manages the dynamic addition and removal of prompt sets.
  - Toggles multi-prompt mode and dark mode.

- `static/styles.css`:
  - Contains styling for the application, including form elements and dark mode.

## Author
- Alex Tobias
## License
- This project is licensed under the MIT License.
