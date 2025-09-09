// loja/static/api.js

const API_BASE_URL = window.location.origin;

/**
 * Mapeia códigos de status e mensagens de erro da API para mensagens amigáveis.
 * @param {object} errorData O objeto de erro vindo da API.
 * @param {number} status O status code da resposta HTTP.
 * @returns {string} Uma mensagem de erro amigável para o usuário.
 */
function getFriendlyErrorMessage(errorData, status) {
    if (status === 401) {
        if (errorData && errorData.detail === 'Incorrect username or password') {
            return 'Usuário ou senha incorretos.';
        }
        return 'Sessão expirada ou credenciais inválidas. Por favor, faça login novamente.';
    }

    if (status === 404) {
        return 'O recurso solicitado não foi encontrado.';
    }

    if (status === 409) {
        if (errorData && errorData.detail) {
             if (errorData.detail === 'Username already exists') {
                 return 'Nome de usuário já está em uso.';
             }
             if (errorData.detail === 'Email already exists') {
                 return 'E-mail já está em uso.';
             }
             if (errorData.detail === 'Username or Email already exists') {
                 return 'Nome de usuário ou e-mail já existe.';
             }
        }
        return 'Conflito de dados. Verifique as informações e tente novamente.';
    }

    // Para erros de validação (Unprocessable Entity - 422)
    if (status === 422 && errorData && errorData.detail && Array.isArray(errorData.detail)) {
        let validationErrors = errorData.detail.map(err => {
            const loc = err.loc ? err.loc[err.loc.length - 1] : 'campo';
            return `O campo '${loc}' ${err.msg}`;
        });
        return `Erro de validação:\n${validationErrors.join('\n')}`;
    }

    if (errorData && errorData.detail) {
        return `Erro da API: ${errorData.detail}`;
    }

    return `Ocorreu um erro inesperado (Status: ${status}).`;
}

/**
 * Lida com a resposta de uma requisição e lança um erro se o status não for OK.
 * @param {Response} response A resposta da requisição.
 * @returns {Promise<any>} O JSON da resposta.
 */
async function handleResponse(response) {
    if (response.status === 204) {
        return { message: "Operação realizada com sucesso." };
    }
    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch {
            throw new Error(`Erro HTTP! status: ${response.status}`);
        }

        const friendlyMessage = getFriendlyErrorMessage(errorData, response.status);
        const error = new Error(friendlyMessage);
        error.detail = errorData.detail;
        throw error;
    }
    return response.json();
}

/**
 * Lida com a exibição de erros na interface.
 * @param {Error} error O objeto de erro.
 * @param {HTMLElement} alertElement Elemento para exibir a mensagem de alerta.
 */
function handleError(error, alertElement) {
    console.error('Fetch error:', error);
    let errorMessage = `Erro: ${error.message}`;

    if (error.detail && typeof error.detail === 'string') {
        errorMessage = `Erro da API: ${error.detail}`;
    }

    alertElement.innerHTML = `<div class="alert alert-error">${errorMessage}</div>`;
}

/**
 * Função genérica para fazer uma requisição POST.
 * @param {string} endpoint O endpoint da API.
 * @param {Object | URLSearchParams} data O corpo da requisição.
 * @param {string} contentType O tipo de conteúdo da requisição.
 * @param {string} accessToken O token de acesso para autenticação.
 * @returns {Promise<any>} A resposta tratada da API.
 */
async function postData(endpoint, data, contentType = 'application/json', accessToken = null) {
    const headers = { 'Content-Type': contentType };
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    let body;
    if (data instanceof URLSearchParams) {
        body = data;
    } else if (contentType === 'application/json') {
        body = JSON.stringify(data);
    } else {
        body = data;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body,
    });
    return handleResponse(response);
}

/**
 * Função genérica para fazer uma requisição PUT.
 * @param {string} endpoint O endpoint da API.
 * @param {Object} data O corpo da requisição.
 * @param {string} accessToken O token de acesso para autenticação.
 * @returns {Promise<any>} A resposta tratada da API.
 */
async function putData(endpoint, data, accessToken) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data),
    });
    return handleResponse(response);
}

/**
 * Função genérica para fazer uma requisição DELETE.
 * @param {string} endpoint O endpoint da API.
 * @param {string} accessToken O token de acesso para autenticação.
 * @returns {Promise<any>} A resposta tratada da API.
 */
async function deleteData(endpoint, accessToken) {
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'DELETE',
        headers,
    });
    return handleResponse(response);
}

/**
 * Função para fazer uma requisição GET.
 * @param {string} endpoint O endpoint da API.
 * @param {URLSearchParams} params Parâmetros de busca.
 * @param {string} accessToken O token de acesso para autenticação.
 * @returns {Promise<any>} A resposta tratada da API.
 */
async function getData(endpoint, params, accessToken = null) {
    const queryString = params ? `?${params.toString()}` : '';
    const headers = {};
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}${queryString}`, {
        method: 'GET',
        headers,
    });
    return handleResponse(response);
}