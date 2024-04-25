import os  # Importing the os module for interacting with the operating system
import secrets  # Importing the secrets module for generating cryptographically strong random numbers
import requests  # Importing the requests module for making HTTP requests
from flask import Flask, flash, render_template, request, jsonify, redirect, session, url_for  # Importing necessary classes and functions from Flask
from werkzeug.utils import secure_filename  # Importing the secure_filename function from werkzeug.utils for secure filename generation
from PyPDF2 import PdfReader  # Importing PdfReader class from PyPDF2 for reading PDF files
import openai  # Importing the openai module for using the OpenAI API

# Setting up constants
UPLOAD_FOLDER = 'uploads'  # Folder where uploaded files will be stored
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions

# Creating a Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generating a secret key for session management
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setting up OpenAI API key
openai.api_key = "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"

# List to store chat messages
messages = [{"role": "system", "content": " "}]  # Initial system message

# Route for the home page
@app.route('/')
def home():
    return render_template('bot.html')  # Rendering the bot.html template

# Route for receiving user input and getting AI response
@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json['message']  # Extracting the user's message from the request
    messages.append({"role": "user", "content": user_input})  # Adding the user's message to the chat history

    # Requesting AI response from OpenAI's Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    chatGPT_reply = response["choices"][0]["message"]["content"]  # Extracting the AI's response
    messages.append({"role": "assistant", "content": chatGPT_reply})  # Adding the AI's response to the chat history

    return jsonify({"response": chatGPT_reply})  # Returning the AI's response as JSON

# Route for resetting the chat
@app.route('/reset-chat', methods=['POST'])
def reset_chat():
    global messages  # Accessing the global messages variable
    messages = [{"role": "system", "content": "You are a financial expert "}]  # Resetting the chat history

# Deleting the uploaded PDF file if it exists
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.pdf')
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return jsonify({"status": "success", "message": "Chat reset successfully"})  # Returning a success message

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for uploading files
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']  # Getting the uploaded file from the request
        if file and allowed_file(file.filename):  # Checking if the file is allowed
            filename = secure_filename(file.filename)  # Generating a secure filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Constructing the file path
            file.save(file_path)  # Saving the uploaded file

            # Extracting text from uploaded PDF files
            if filename.endswith('.pdf'):
                reader = PdfReader(file_path)  # Creating a PdfReader object
                text = ""
                for page in reader.pages:
                    text += page.extract_text()  # Extracting text from each page
                # Asking a question about the uploaded document
                question = "What can you tell me about this document?"
                messages.append({"role": "user", "content": question})  # Adding the question to the chat history
                messages.append({"role": "user", "content": text})  # Adding the text from the document to the chat history
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )
                chatGPT_reply = response["choices"][0]["message"]["content"]  # Extracting the AI's response
                messages.append({"role": "assistant", "content": chatGPT_reply})  # Adding the AI's response to the chat history
                return jsonify({"response": chatGPT_reply})  # Returning the AI's response as JSON
    return render_template('bot.html')  # Rendering the bot.html template

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode


