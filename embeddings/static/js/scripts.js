$(document).ready(function () {

    document.addEventListener("DOMContentLoaded", function () {
        const hamburgerMenu = document.getElementById("hamburger-menu");
        const navLinks = document.getElementById("nav-links");
    
        hamburgerMenu.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });
    });
    $('#send-btn').on('click', function () {
        var userMessage = $('#user-message').val();
        //alert(userMessage);
        if (userMessage) {
            // Append user message to chat
            $('#chat-box').append('<div class="chat-message user">' + userMessage + '</div>');

            // Clear input field
            $('#user-message').val('');

            // Scroll to bottom of chat
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

            // Send message to backend
            $.ajax({
                url: '/search',
                method: 'POST',
                data: { query: userMessage },
                success: function (response) {
                    // Append bot response to chat
                    $('#chat-box').append('<div class="chat-message bot">' + response.prompt + '</div>');
                    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                },
                error: function () {
                    // Handle error
                    $('#chat-box').append('<div class="chat-message bot">Sorry, I couldn\'t process your request.</div>');
                    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                }
            });
        }
    });
});
