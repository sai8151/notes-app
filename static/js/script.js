document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // You can add more advanced validation and authentication logic here
        alert(`Username: ${username}\nPassword: ${password}`);
    });
