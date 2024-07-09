import "./src/skyballing/requests.js";


register("command", (name) => {
    ChatLib.chat(`Hello, ${name}!`);
}).setName("hello").setAliases("hi", "hey");

register("command", (username) => {
    uuid = retrieveUUID(username);
    ChatLib.chat(`UUID: ${uuid}`);
}).setName("uuid").setAliases("uuid", "getuuid");