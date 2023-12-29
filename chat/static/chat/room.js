const currentChannel = localStorage.getItem('currentChannel');


if (currentChannel) {
  // Wyślij zapytanie lub wykonaj akcje związane z aktualnym kanałem
  console.log(`Użytkownik jest na kanale: ${currentChannel}`);
}

function changeChannel(newChannel) {
  localStorage.setItem('currentChannel', newChannel);

  window.history.pushState({channel: newChannel}, `Kanał - ${newChannel}`, `/${newChannel}`);
}


const liElements = document.querySelectorAll(".chats");
let tempValue, activeElement, test;
const sockets = [];
const user = JSON.parse(document.getElementById('request-user').textContent);

let previousChat = null;
const firstRoom = document.querySelector('.chats');

// if (firstRoom != null){
//   createSocket(firstRoom.textContent.trim());

//   firstRoom.classList.add('active');
//   previousChat = firstRoom;
// }


async function loadChatinDiv(chatUrl){

  try{
    const response = await fetch(chatUrl);
    if(response.ok){
      
      const data = await response.json();
      document.getElementById("loadChat").innerHTML = data.chat_content;

      const scrollBarChat = document.querySelector(".main-chat");
      function scrollToBottom() {
        scrollBarChat.scrollTop = scrollBarChat.scrollHeight;
      }

      window.onload = scrollToBottom();
      document.querySelector('#chat-message-input').focus();
      document.querySelector('#chat-message-input').onkeyup = function(e) {
          if (e.keyCode === 13) {  // enter, return
              document.querySelector('#chat-message-submit').click();
          }
      };
      searchInput.innerHTML="";
    }else{
      console.error('Request failed');
    } 
  
  }catch(error){
    console.error(error)
  }

  };

  
function users(){
  const onlineUsers = document.getElementById("idOnlineUsers");
  const listItems = Array.from(onlineUsers.querySelectorAll('li'));
  return listItems
};


let listItemsLi = document.querySelectorAll('.list-unstyled li');

listItemsLi.forEach(item => {
  if(item.getAttribute('class').includes("friends")){

  }

  if (item.textContent.trim() === currentChannel) {
      if(item.getAttribute('class').includes("friends")){
        createSocketWithUser(item)
      }else{
          createSocket(item.textContent.trim())
      }


      if (previousChat) {
        previousChat.classList.remove('active');
      }
      item.classList.add('active');
      previousChat = item;
  }
  
  item.addEventListener('click', function() {

    if (previousChat) {
      previousChat.classList.remove('active');
    }
    this.classList.add('active');
    previousChat = this;

  });
});


async function createSocket(e){
      let clickedChat = '';

      if (e.textContent == undefined){
        changeChannel(e)
        //window.history.replaceState({channel: e}, 'Nazwa Kanału', e);
        clickedChat = "/chat/" + e;
        
      }else{
        //window.history.replaceState({channel: e.textContent.trim()}, 'Nazwa Kanału', e.textContent.trim());
        changeChannel(e.textContent.trim())
        clickedChat = "/chat/" + e.textContent.trim();
      }
      await loadChatinDiv(clickedChat);

      const chatSocket = new WebSocket( 'ws://'+ window.location.host+ '/ws'+ clickedChat + '/');

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

        const onlineUsers = document.getElementById("idOnlineUsers");
        const scrollBarChat = document.querySelector(".main-chat");
        let listOfUsers = users()

        let elementToRemove = listOfUsers.find(item => item.textContent === data.user_online);

        if(data.message == "user_connected"){ 
            if(!(elementToRemove)){
                onlineUsers.insertAdjacentHTML("beforeend", "<li><i class='p-1 bi bi-chat-square-fill '></i>" + data.user_online + "</li>");
            }
        }
        else if(data.message == "user_disconnected"){
            if (elementToRemove) {
              elementToRemove.remove(); // Usuwa znaleziony element, jeśli istnieje.
            }
        }
        else{

            let user_message = `<div id='chat-text' class='d-flex'>
                    <p class='bd-highlight mt-auto'>
                        <img class='rounded-circle img-message mt-auto' src='${data.user_online_img}' alt='image'</img>
                    </p>
                    <p class='mx-1 p-2 mt-auto bd-highlight message text-break' data-bs-toggle='tooltip' data-bs-placement='top' title='${data.message_timestamp}'> ${data.message} </p>
                </div>`
            if(user != data.username){
                user_message = `<div id='chat-text' class='d-flex justify-content-end'>
                    <p class='mx-1 p-2 mt-auto bd-highlight message-opposed text-break' data-bs-toggle='tooltip' data-bs-placement='top' title='${data.message_timestamp}'> ${data.message} </p>
                    <p class='bd-highlight mt-auto'>
                        <img class='rounded-circle img-message mt-auto' src='${data.user_online_img}'</img>
                    </p>
                </div>`
            }
            document.getElementById('chat-text').insertAdjacentHTML("beforeend",user_message)
            scrollBarChat.scrollTo(0, scrollBarChat.scrollHeight);
        }
      };
      
      
      chatSocket.onclose = function(e) {
          console.log('Chat socket closed unexpectedly');
      };
  };

document.body.addEventListener("click", function(event) {

  if (event.target.id == "chat-message-submit") {

        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;

        console.log("wysyłam po kliknieciu przycisku nazwe usera");
          if(message != ""){

              sockets[0].send(JSON.stringify({
              'username': user,
              'message': message
              }));
              messageInputDom.value = '';
          }else{
              alert("Pusta wiadomość!")
          }
    }
}); 



