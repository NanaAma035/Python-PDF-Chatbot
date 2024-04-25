 // Function to send user message to the server and get response
 function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return; // Controleer of de invoer leeg is
    appendMessage("user", userInput);
    document.getElementById("user-input").value = ""; // Wis het invoerveld na het verzenden van het bericht
    // Voeg hier code toe om het antwoord van de assistent te genereren en weer te geven

    // Send user message to server
    fetch('/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("assistant", data.response); // Append assistant response to chat box
    })
    .catch(error => console.error('Error:', error));
}

// Function to append message to chat box
function appendMessage(role, content) {
    var chatBox = document.getElementById("chat-box");
    var messageDiv = document.createElement("div");
    messageDiv.className = role;
    messageDiv.innerHTML = content;

    if (role === "user") {
        messageDiv.classList.add("user-message");
    } else if (role === "assistant") {
        messageDiv.classList.add("assistant-message");
    }

    chatBox.appendChild(messageDiv);  // Voeg het bericht toe aan de chatbox
 
    // Scroll naar beneden om het nieuwste bericht te tonen
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Add an event listener for the input field
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage(); // Call the sendMessage function when the Enter key is pressed
    }
});


function toggleNav() {
    var sidenav = document.getElementById("mySidenav");
    var chatContainer = document.getElementById("chat-container");
    if (sidenav.style.width === "250px") {
        sidenav.style.width = "0";
        chatContainer.style.marginLeft = "0";
    } else {
        sidenav.style.width = "250px";
        chatContainer.style.marginLeft = "250px";
    }
}

//JavaScript code for handling user input and file upload

$(document).ready(function() {
    // Submit user input form
    $('#user-input-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        var userInput = $('#user-input').val(); // Get user input
        sendMessage(userInput); // Send user message to server
        $('#user-input').val(''); // Clear input field
    });

    // Function to send user message to server
    function sendMessage(message) {
        $.ajax({
            type: 'POST',
            url: '/get-response',
            contentType: 'application/json',
            data: JSON.stringify({ 'message': message }),
            success: function(response) {
                displayMessage('You', message); // Display user message
                displayMessage('Assistant', response.response); // Display bot response
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    // Function to display messages in the chat box
    function displayMessage(sender, content) {
        $('#chat-box').append('<div><strong>' + sender + ':</strong> ' + content + '</div>');
    }
});


function resetChat() {
    fetch('/reset-chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('chat-box').innerHTML = ''; // Clear chat box
            console.log(data.message);
        } else {
            console.error('Failed to reset chat');
        }
    })
    .catch(error => console.error('Error:', error));
}

