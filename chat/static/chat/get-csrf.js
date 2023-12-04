async function getCSRFToken() {
    const response = await fetch('/get-csrf-token/');
    const data = await response.json();
    return data.csrfToken;
};