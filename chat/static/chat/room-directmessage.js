let friendsList = document.getElementById("friends")

async function addToFriend(e){

    const response = await fetch('/users/' + e.textContent.trim());
    if(response.ok){
        const data = await response.json();
        
        const newListFriendItem = document.createElement('li');
        newListFriendItem.className = 'chats-friends';
        newListFriendItem.dataset.value = data.friend_code;

        newListFriendItem.innerHTML = `
        <a id="room-name" class="room-link" class="d-flex justify-content-between" data-value="${data.friend_code}" onclick="return createSocketWithUser(this);">
            <div class="d-flex">
                <p class="mb-0 position-relative">
                    <img src="{{friends.friend.user_img.url}}" class="rounded-circle" width="32" height="32" alt="Avatar" loading="lazy" />
                    <i id="user-status-icon-{{friends.friend}}"   // poprawic
                    data-value-status="{{friends.friend.online}}" // poprawic
                    data-value-nickname="{{friends.friend}}" class="bi bi-chat-dots-fill position-absolute mt-4 bottom-0 end-0 rounded-circle"></i>
                    <p class="mx-2">${data.friend_added}</p>
                </p>
            </div>
        </a>`
        ;
        friendsList.appendChild(newListFriendItem);
        createSocketWithUser(newListFriendItem);

        if(previousChat){
            previousChat.classList.remove('active');
        };
        newListFriendItem.classList.add('active');
        previousChat = newListFriendItem;

        //scrollBarChats.scrollTo(0, scrollBarChats.scrollHeight);

        // friendsList.innerHTML += 
        // `<li class="chats-friends" data-value="${data.friend_code}" onclick="return createSocketWithUser(this);" >
        //     <a id="room-name" class="room-link" class="d-flex justify-content-between">
        //         <div class="d-flex justify-content-between">
        //             <p class="mb-0">${data.friends_list}</p>
        //         </div>
        //     </a>
        // </li>`;
    }
};

/////////////////////// TO DO: poprawienie dołączania do pokoju !! tworzy nowy nawet jeżeli taki jest
function createNewChannel(event){
    event.preventDefault();

    const createNewRoom = document.getElementById('create-new-channel');
    const modal = document.getElementById('createNewChannel');
    const modalToHide = bootstrap.Modal.getInstance(modal);   

    const scrollBarChats = document.getElementById("chat-lists");

    let chatList = document.getElementById('chat-list');
    let listItems = chatList.getElementsByTagName('li');

    const formData = new FormData(createNewRoom);
    const newChannel = document.querySelector('#id_channel_name').value;
    let newListItem;
    // Wyślij żądanie POST do serwera

    fetch('/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then((response) => {
        
        if(response.status == "exist"){
            modalToHide.hide();

            for(let i = 0; i<listItems.length; i++){
                let currentValue = listItems[i].getAttribute('data-value');
                if (currentValue === response.room) {
                    newListItem = listItems[i];
                }
            }
            createSocket(response.room);
        }else{

            newListItem = document.createElement('li');
            newListItem.className = 'chats';
            if(response.private){
                newListItem.innerHTML = `
                <a id="room-name" class="friend-link" class="d-flex justify-content-between" onclick="return createSocket(this);">
                    <div class="d-flex justify-content-between p-1 mx-1">
                    <p class="mb-0"><i class="bi bi-file-earmark-lock2 mx-2"></i>${newChannel}</p>
                    </div>
                </a>`;

            }else{
                newListItem.innerHTML = `
                <a id="room-name" class="friend-link" class="d-flex justify-content-between" onclick="return createSocket(this);">
                    <div class="d-flex justify-content-between p-1 mx-1">
                    <p class="mb-0"><i class="bi bi-chat-square-quote mx-2"></i>${newChannel}</p>
                    </div>
                </a>`;
            }
            chatList.appendChild(newListItem);

            createSocket(newChannel);
            modalToHide.hide();
        }

        if(previousChat){
            previousChat.classList.remove('active');
        };

        newListItem.classList.add('active');
        previousChat = newListItem;
        scrollBarChats.scrollTo(0, scrollBarChats.scrollHeight);

    })
    .catch(error => {
        console.error('Wystąpił błąd:', error);
    });

};


async function createSocketWithUser(e){

    const chosedUser = e.textContent.trim();
    const clickedUserValue = e.dataset.value;
    // const response = await fetch('/users/' + chosedUser);
    // if(response.ok){
    //     const data = await response.json();
    //     friendsList.innerHTML += data.friends_list;
    // }


    const clickedUser = "/directmessage/" + clickedUserValue + "/";
    await loadChatinDiv(clickedUser);
    const idBar = document.getElementById("friend-bar").textContent = chosedUser;

    const chatSocket = new WebSocket( 'ws://'+ window.location.host + '/ws'+ clickedUser );

    sockets.push(chatSocket)

     if(chatSocket != sockets[0]){
       console.log("TUU!");
       sockets[0].send(JSON.stringify({
         'close': "to_close",
         }));
         sockets[0].close();
         sockets[0] = chatSocket;
     }

     
     chatSocket.onmessage = function(e) {
       const data = JSON.parse(e.data);

       const scrollBarChat = document.querySelector(".main-chat");
   
       let user_message = 
           "<div id='chat-text' class='d-flex p-1'>" + 
               "<p class='bd-highlight mt-auto'>" +
                   "<img class='rounded-circle img-message mt-auto' src='" + data.user_online_img + "' alt='image'</img>"+
               "</p>"+
               "<p class='mx-1 p-2 mt-auto bd-highlight message text-break' data-bs-toggle='tooltip' data-bs-placement='top' title='" + data.message_timestamp +"'>" + data.message + "</p>" +
           "</div>"

       if(user != data.username){
           user_message =
           "<div id='chat-text' class='d-flex justify-content-end p-1'>" + 
               "<p class='mx-1 p-2 mt-auto bd-highlight message-opposed text-break' data-bs-toggle='tooltip' data-bs-placement='top' title='" + data.message_timestamp +"'>" + data.message + "</p>" +
               "<p class='bd-highlight mt-auto'>" +
                   "<img class='rounded-circle img-message mt-auto'  src='" + data.user_online_img + "'</img>" +
               "</p>" 
           "</div>"
       }
       document.getElementById('chat-text').insertAdjacentHTML("beforeend",user_message);
       scrollBarChat.scrollTo(0, scrollBarChat.scrollHeight);

     };

     
     chatSocket.onclose = function(e) {
         console.log('Chat socket closed unexpectedly');
     };
 };

