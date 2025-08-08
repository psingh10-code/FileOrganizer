from flask import Flask, render_template, request, flash, redirect, url_for
import os
import webbrowser
from threading import Timer
from organizer import organize_folder

# Initialize the Flask application
app = Flask(__name__)

# A secret key is needed to show messages (flash) to the user.
# It's better to load this from an environment variable for security.
# For development, you can fall back to a default key.
app.secret_key = os.environ.get('SECRET_KEY', 'a-random-secret-key-for-your-app')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_path = request.form.get('folder_path')

        # Validate the input path
        if not folder_path or not os.path.isdir(folder_path):
            flash('Error: Please enter a valid and existing folder path.', 'error')
            return redirect(url_for('index'))
        
        try:
            # Run the organizer and get the results
            messages = organize_folder(folder_path)
            if messages:
                flash(f"Successfully organized {len(messages)} file(s) in '{folder_path}'.", 'success')
            else:
                flash('No files were moved. The folder might be empty or already organized.', 'info')
        except Exception as e:
            flash(f'An unexpected error occurred: {e}', 'error')

        return redirect(url_for('index'))

    # For a GET request, just show the page
    return render_template('index.html')

def open_browser():
    """
    Opens the default web browser to the application's URL.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Wait for 1 second before opening the browser to give the server time to start.
    Timer(1, open_browser).start()
    # Run the app. For production, consider setting debug=False.
    app.run(debug=True, port=5000)