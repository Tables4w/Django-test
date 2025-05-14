document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append('username', form.login.value);
        formData.append('password', form.password.value);

        const csrftoken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1] || '';

        const response = await fetch('/login/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const result = await response.json();
        document.getElementById('result').innerText = JSON.stringify(result);
    });
});
