document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append('username', form.login.value);
        formData.append('password', form.password.value);
        formData.append('gender', form.gender.value);
        formData.append('avatar', form.avatar.files[0]);

        const csrftoken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1] || '';

        const response = await fetch('/register/', {
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
