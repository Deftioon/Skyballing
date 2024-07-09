function retrieveUUID(username) {
    let uuid = null;
    let url = "https://api.mojang.com/users/profiles/minecraft/" + username;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            uuid = data.id;
        });
    return uuid;
}