const currentChannel = localStorage.getItem('currentChannel');
// Chaning URL 
function changeChannel(newPath ,newChannel) {
  localStorage.setItem('currentChannel', newChannel);
  window.history.pushState({channel: newPath}, `Kanał - ${newPath}`, `${newPath}`);
}

// Async Fun to load chat from view
let initialHeightTextareaInput;
async function loadChatinDiv(chatUrl){

  try{
    const response = await fetch(chatUrl);
    if(response.ok){
      
      const data = await response.json();
      document.getElementById("loadChat").innerHTML = data.chat_content;
  
      const scrollBarChat = document.querySelector(".main-chat");
      window.onload = scrollBarChat.scrollTop = scrollBarChat.scrollHeight;
      
      const inputForm = document.getElementById('chat-message-input');
      inputForm.focus();
      initialHeightTextareaInput = inputForm.scrollHeight;
      
      inputForm.addEventListener('input', function(){
        autoResizeTextarea(inputForm)
      });

      inputForm.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          document.getElementById('chat-message-submit').click();
        }
      });
      
      searchInput.innerHTML="";
    }else{
      console.error('Request failed');
    } 
  
  }catch(error){
    console.error(error)
  }

  };

// fun to return list of users in specific room
function users(){
  const onlineUsers = document.getElementById("idOnlineUsers");
  const listItems = Array.from(onlineUsers.querySelectorAll('li'));
  return listItems
};


// Chats items 
let listItemsLi = document.querySelectorAll('.list-unstyled li');
let previousChat = null;
listItemsLi.forEach(item => {
  if (item.textContent.trim() === currentChannel) {
      createSocket(item);
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

const sockets = [];
const user = JSON.parse(document.getElementById('request-user').textContent);

// Sockets to handle chats/directmessages
async function createSocket(e){
      let typeSocket;
      let chatSocket;
      
      if(e.getAttribute('class').includes("friends")){

        const chosedUser = e.textContent.trim();
        const clickedUserValue = e.dataset.value;
    
        //changeChannel(chosedUser);
        changeChannel("/chats/"+ chosedUser, chosedUser)

        const clickedUser = "/directmessage/" + clickedUserValue + "/";
        
        await loadChatinDiv(clickedUser);
        const idBar = document.getElementById("friend-bar").textContent = chosedUser;
    
        chatSocket = new WebSocket( 'ws://'+ window.location.host + '/ws'+ clickedUser );
        sockets.push(chatSocket)
        typeSocket = 0; // For directmessages
      }else{

        let clickedChat = '';
        clickedChat = "/chat/" + e.textContent.trim();

        changeChannel("/chats/"+ e.textContent.trim(), e.textContent.trim())

        await loadChatinDiv(clickedChat);
        chatSocket = new WebSocket( 'ws://'+ window.location.host+ '/ws'+ clickedChat + '/');
        sockets.push(chatSocket)
        typeSocket = 1; // For chats
      }
      

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

        if(typeSocket == 1){
          const onlineUsers = document.getElementById("idOnlineUsers");
          let listOfUsers = users();
          let elementToRemove = listOfUsers.find(item => item.textContent === data.user_online);
          
          
          if(data.message == "user_connected"){ 
            if(!(elementToRemove)){
                onlineUsers.insertAdjacentHTML("beforeend", "<li><i class='p-1 bi bi-chat-square-fill '></i>" + data.user_online + "</li>");
            }
          }
          else if(data.message == "user_disconnected"){
              if (elementToRemove) {
                elementToRemove.remove(); 
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


        }else{

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
        }

      };
      
      
      chatSocket.onclose = function(e) {
          console.log('Chat socket closed unexpectedly');
      };
  };

// Eventlistener to handle click on textarea chat
document.body.addEventListener("click", function(event) {

  if (event.target.id == "chat-message-submit") {

        const messageInputDom = document.getElementById('chat-message-input');
        let message = messageInputDom.value.trim();
        const parentDiv = document.getElementById('chat-footer');
        console.log("wysyłam po kliknieciu przycisku nazwe usera");
          if(message != "" ){
              sockets[0].send(JSON.stringify({
              'username': user,
              'message': message
              }));
              messageInputDom.value = '';
              messageInputDom.style.height = '15%';
              parentDiv.style.height = '15%';
          }else{
              alert("Pusta wiadomość!")
          }
    }
}); 

// Resizing
let tmp;

function autoResizeTextarea(textarea) {  
  const parentDiv = document.getElementById('chat-footer');
  const scrollBarChat = document.querySelector(".main-chat");

  const originalHeight = textarea.clientHeight;
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight +1) + 'px'; 
  const newHeight = textarea.clientHeight;

  
  if (newHeight > originalHeight) {
    const heightDifference = newHeight - originalHeight;
    parentDiv.style.height = (parentDiv.clientHeight + heightDifference) + 'px';

    const maxHeightThreshold = 200; 
    if (textarea.clientHeight > maxHeightThreshold) {
      textarea.style.overflowY = 'auto';
    }
    
  }else if(newHeight < originalHeight){
    parentDiv.style.height = '15%';
  }
  window.onload = scrollBarChat.scrollTop = scrollBarChat.scrollHeight;

}

