// FIDO2/WebAuthn ceremonies: the server sends options as JSON with binary
// fields in base64url; the browser needs ArrayBuffers, and back.

const base64url = {
    encode(buffer) {
        let binary = "";
        for (const byte of new Uint8Array(buffer)) {
            binary += String.fromCharCode(byte);
        }
        return btoa(binary)
            .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
    },
    decode(text) {
        const base64 = text.replace(/-/g, "+").replace(/_/g, "/");
        const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, "=");
        return Uint8Array.from(atob(padded), c => c.charCodeAt(0)).buffer;
    },
};

function withBinaryIds(descriptors) {
    return (descriptors || []).map(
        descriptor => ({...descriptor, id: base64url.decode(descriptor.id)})
    );
}

function creationOptions(options) {
    return {
        ...options,
        challenge: base64url.decode(options.challenge),
        user: {...options.user, id: base64url.decode(options.user.id)},
        excludeCredentials: withBinaryIds(options.excludeCredentials),
    };
}

function requestOptions(options) {
    return {
        ...options,
        challenge: base64url.decode(options.challenge),
        allowCredentials: withBinaryIds(options.allowCredentials),
    };
}

function credentialJson(credential) {
    const response = credential.response;
    const json = {
        id: credential.id,
        rawId: base64url.encode(credential.rawId),
        type: credential.type,
        authenticatorAttachment: credential.authenticatorAttachment,
        clientExtensionResults: credential.getClientExtensionResults(),
        response: {clientDataJSON: base64url.encode(response.clientDataJSON)},
    };
    if (response.attestationObject) {
        json.response.attestationObject =
            base64url.encode(response.attestationObject);
        json.response.transports =
            response.getTransports ? response.getTransports() : [];
    } else {
        json.response.authenticatorData =
            base64url.encode(response.authenticatorData);
        json.response.signature = base64url.encode(response.signature);
        json.response.userHandle = response.userHandle
            ? base64url.encode(response.userHandle) : null;
    }
    return json;
}

async function postJson(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    });
    const body = await response.json().catch(() => ({}));
    return {ok: response.ok, body};
}

function showMessage(text) {
    // textContent, never innerHTML: messages are not markup.
    document.getElementById("message").textContent = text;
}

async function ceremony(urls, login, useAuthenticator, failure) {
    showMessage("");
    const started = await postJson(urls.options, {login});
    if (!started.ok) {
        showMessage(started.body.error || failure);
        return;
    }
    let credential;
    try {
        credential = await useAuthenticator(started.body.publicKey);
    } catch (error) {
        showMessage(failure);
        return;
    }
    const finished = await postJson(urls.finish, {
        ceremony: started.body.ceremony,
        credential: credentialJson(credential),
    });
    if (finished.ok) {
        window.location.assign(finished.body.redirect);
    } else {
        showMessage(finished.body.error || failure);
    }
}

function signUp(login) {
    return ceremony(
        {options: "/passkeys/registration/options",
         finish: "/passkeys/registration"},
        login,
        options => navigator.credentials.create(
            {publicKey: creationOptions(options)}
        ),
        "Could not create the passkey."
    );
}

function signIn(login) {
    return ceremony(
        {options: "/passkeys/authentication/options",
         finish: "/passkeys/authentication"},
        login,
        options => navigator.credentials.get(
            {publicKey: requestOptions(options)}
        ),
        "Could not sign in."
    );
}

function onSubmit(formId, action) {
    document.getElementById(formId).addEventListener("submit", event => {
        event.preventDefault();
        action(new FormData(event.target).get("login"));
    });
}
