const chat_socket = new WebSocket("ws://" + window.location.host + "/");
const msg_input = document.getElementById("msg-input");
const message_container = document.getElementById("message-container");
const overflow_anchor = document.getElementById("anchor");
const username = document.querySelector("meta[name='username']").content;
const pfp_path = document.querySelector("meta[name='pfp']").content
chat_socket.onopen = function (e) {
    console.log("Websocket initialised!");
}
chat_socket.onclose = function (e) {
    console.log("Error: Websocket closed.");
}
msg_input.focus();

msg_input.onkeyup = function (e) {
    if (e.keyCode == 13) { // Newline
        const message_contents = msg_input.value;
        // Ensure that the message isn't empty.
        if (message_contents != "") {
            chat_socket.send(JSON.stringify({ message: message_contents, username: username }));
            // Clear the input box.
            msg_input.value = "";
        }
    }
}
function get_message_inner_html(username, message) {
    // Returns the inner HTML for the message
    var outer_div = document.createElement("div");
    outer_div.classList.add("msg");

    var pfp = document.createElement("img");
    pfp.src = pfp_path;
    pfp.alt = username;
    pfp.classList.add("pfp");
    outer_div.appendChild(pfp);

    var inner_div = document.createElement("div")
    inner_div.classList.add("msg-inner");

    outer_div.appendChild(inner_div);

    var name_span = document.createElement("span");
    name_span.classList.add("name");
    console.log(username);
    name_span.innerText = username;
    inner_div.appendChild(name_span);

    var time_span = document.createElement("span");
    time_span.classList.add("time");
    time_span.innerText = "12:34";
    inner_div.appendChild(time_span);

    var msg_body = document.createElement("p");
    msg_body.classList.add("msg-contents");
    msg_body.innerText = message;
    inner_div.appendChild(msg_body);

    return outer_div;
}

chat_socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    var div = get_message_inner_html(data.username, data.message);
    message_container.insertBefore(div, anchor);
    if (data.username == username) {
        anchor.scrollIntoView({ behavior: "instant", block: "end" })
    }
}