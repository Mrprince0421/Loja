// loja/static/api.js

const API_BASE_URL = window.location.origin;

/**
 * Formata um objeto de erro para ser exibido de forma legível.
 * Se for uma lista de objetos, formata cada um.
 * @param {any} errorData O dado de erro vindo da API.
 * @returns {string} A mensagem de erro formatada.
 */
function formatError(errorData) {
    if (Array.isArray(errorData)) {
        return errorData.map(err => {
            const loc = err.loc ? err.loc.join(' -> ') : 'N/A';
            const msg = err.msg || 'Erro desconhecido';
            const type = err.type || 'N/A';
            return `Local: ${loc}\nMensagem: ${msg}\nTipo: ${type}`;
        }).join('\n\n');
    }
    if (typeof errorData === 'object' && errorData !== null) {
        return JSON.stringify(errorData, null, 2);
    }
    return String(errorData);
}

/**
 * Lida com a resposta de uma requisição e lança um erro se o status não for OK.
 * @param {Response} response A resposta da requisição.
 * @returns {Promise<any>} O JSON da resposta.
 */
async function handleResponse(response) {
    if (response.status === 204) {
        return { message: "Operação realizada com sucesso (Status 204 No Content)." };
    }
    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch {
            throw new Error(`Erro HTTP! status: ${response.status}`);
        }

        const error = new Error('Erro da API');
        error.detail = errorData.detail;
        throw error;
    }
    return response.json();
}

/**
 * Lida com a exibição de erros na interface.
 * @param {Error} error O objeto de erro.
 * @param {HTMLElement} outputElement Elemento para exibir o JSON.
 * @param {HTMLElement} alertElement Elemento para exibir a mensagem de alerta.
 */
function handleError(error, outputElement, alertElement) {
    console.error('Fetch error:', error);
    let errorMessage = `Erro: ${error.message}`;

    if (error.detail) {
        errorMessage = `Erro:\n\n${formatError(error.detail)}`;
    }

    alertElement.innerHTML = `<div class="alert alert-error">${errorMessage}</div>`;
    outputElement.textContent = '';
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