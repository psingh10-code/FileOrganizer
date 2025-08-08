from flask import Flask, render_template, request, flash, redirect, url_for
import os
import webbrowser
from threading import Timer
from organizer import organize_folder, search_for_file

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
    return render_template('index.html', search_form_data={'folder_path': '', 'file_name': ''})

@app.route('/search', methods=['POST'])
def search():
    folder_path = request.form.get('folder_path')
    file_name = request.form.get('file_name')

    # This dictionary helps repopulate the form after submission
    search_form_data = {'folder_path': folder_path, 'file_name': file_name}

    if not folder_path or not os.path.isdir(folder_path):
        flash('Error: Please enter a valid folder path for searching.', 'error')
        return render_template('index.html', search_form_data=search_form_data)
    
    if not file_name:
        flash('Error: Please enter a file name to search for.', 'error')
        return render_template('index.html', search_form_data=search_form_data)

    try:
        results = search_for_file(folder_path, file_name)
        
        if results:
            flash(f"Found {len(results)} match(es) for '{file_name}'.", 'success')
        else:
            flash(f"No files found matching '{file_name}' in '{folder_path}'.", 'info')
        
        # Render the template directly to show results
        return render_template('index.html', search_results=results, search_form_data=search_form_data)

    except Exception as e:
        flash(f'An error occurred during search: {e}', 'error')
        return render_template('index.html', search_form_data=search_form_data)

def open_browser():
    """
    Opens the default web browser to the application's URL.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # The reloader will run this script twice. We only want to open the browser
    # in the main process, not the reloader's child process.
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        Timer(1, open_browser).start()
    # Run the app. For production, consider setting debug=False.
    app.run(debug=True, port=5000)