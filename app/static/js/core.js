function queryParams(params) {
    return Object.keys(params)
        .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(params[k])}`)
        .join("&");
}

function apiCall(method, endpoint, data, onSuccess, onFailure) {
    options = {
        credentials: "same-origin",
        method: method,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: queryParams(data)
    }
    return fetch(endpoint, options).then(function(response) {
        if (!response.ok) {
            return response.json().then(function(json) {
                return Promise.reject(new Error(json.message || response.statusText));
            });
        }
        return response
    })
        .then(function(response) {
            return response.json()
        })
        .then(onSuccess)
        .catch(function(error) {
            $.notify(`${error.message}`, "error");
            onFailure(error);
    });
}
