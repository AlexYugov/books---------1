const API_URL = 'http://127.0.0.1:8000';

async function apiRequest(url, method = 'GET', data = null, token = null, contentType = 'application/json') {
    const headers = {};
    if (contentType) {
        headers['Content-Type'] = contentType;
    }
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const config = { method, headers };
    if (data) {
        if (contentType === 'application/x-www-form-urlencoded') {
            const formData = new URLSearchParams();
            for (const key in data) {
                formData.append(key, data[key]);
            }
            config.body = formData;
        } else {
            config.body = JSON.stringify(data);
        }
    }
    const response = await fetch(`${API_URL}${url}`, config);
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Ошибка запроса: ${response.status}`);
    }
    return response.status === 204 ? null : response.json();
}

// Аутентификация
function register(data) {
    return apiRequest('/register', 'POST', data);
}
function login(data) {
    return apiRequest('/token', 'POST', data, null, 'application/x-www-form-urlencoded');
}

// Книги
function getBooks(skip = 0, limit = 10, title = '', genre = '', city = '') {
    return apiRequest(`/books?skip=${skip}&limit=${limit}&title=${title}&genre=${genre}&city=${city}`);
}
function getBook(id) {
    return apiRequest(`/books/${id}`);
}
function createBook(data, token) {
    return apiRequest('/books', 'POST', data, token);
}
function updateBook(id, data, token) {
    return apiRequest(`/books/${id}`, 'PUT', data, token);
}
function deleteBook(id, token) {
    return apiRequest(`/books/${id}`, 'DELETE', null, token);
}
function getUserBooks(token) {
    return apiRequest('/users/me/books', 'GET', null, token);
}

// Пользователи
function getUser(id, token) {
    return apiRequest(`/users/${id}`, 'GET', null, token);
}
function getUserByLogin(login, token) {
    return apiRequest(`/users/by-login/${login}`, 'GET', null, token);
}
function updateUser(id, data, token) {
    return apiRequest(`/users/${id}`, 'PUT', data, token);
}
function deleteUser(id, token) {
    return apiRequest(`/users/${id}`, 'DELETE', null, token);
}
function getAllUsers(skip = 0, limit = 10, city = '', token) {
    return apiRequest(`/users?skip=${skip}&limit=${limit}&city=${city}`, 'GET', null, token);
}