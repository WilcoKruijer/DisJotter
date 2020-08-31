define(["require"], function (require) {
    "use strict";

    return {
        jsonRequest: (method, url, data=null, query=null) => {
            if (typeof query === 'object' && query) {
                url += '?' + new URLSearchParams(query);
            }
        
            return fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: data ? JSON.stringify(data) : undefined
            });
        }
    }
});
