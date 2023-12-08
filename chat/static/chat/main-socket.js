const userButton = document.getElementById('user-status');
//const currUser = 'user-status-icon-' + user;

const userID = JSON.parse(document.getElementById('request-user-id').textContent);
let userCurrentStatus = document.getElementById("user-current-status").textContent.toLowerCase();

userCurrentStatus = (userCurrentStatus === 'true');

const userStatus = document.getElementById('user-status-icon');

updateElement(userCurrentStatus);
 

const mainSocket = new WebSocket( 'ws://'+ window.location.host + '/ws/general/');



mainSocket.onmessage = function(e){                 // mainSocket.onmessage = (e) =>{
    const data = JSON.parse(e.data);

    if(user != data.user){
        updateElementFriend(data.user ,data.status);         // data.username też trzeba 
    }else{
        updateElement(data.status);
    }
    //console.log(data)
};
mainSocket.onclose = function(e) {
    console.log('Chat socket closed unexpectedly');
};

userButton.addEventListener('click', ()=>{
    console.log("wysyłam status");

    mainSocket.send(JSON.stringify({
        'username': user,
        'status': userCurrentStatus    // F - offline, T - online 
        }));
    if(userCurrentStatus){
        userCurrentStatus = false
    }else{
        userCurrentStatus = true
    }
});


function updateElementFriend(users, usersStatus){
    let userStatusFriend = document.getElementById('user-status-icon-' + users);

    //usersStatus = (usersStatus === 'true');

    if(usersStatus){
        userStatusFriend.style.color = "green";
    }else{
        userStatusFriend.style.color = "black";
    }
}

function updateElement(userCurrentStatus){
    
    if(userCurrentStatus){
        userStatus.style.color = "green";
        userButton.innerText = 'Set status Offline'
    }else{
        userStatus.style.color = "black";
        userButton.innerText = 'Set status Online'
    }
}



// async function sendUserStatus(){
//     const csrfToken = await getCSRFToken();

//     const requestOptions = {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrfToken,
//         }
//     }

//     const response = await fetch('update/' + userID, requestOptions);
//     if(response.ok){
//         const data = await response.json();
//         console.log(data)
//         updateElement(data.user_status);
//     }

// };







// async function sendUserStatus(){
//     const csrfToken = await getCSRFToken();

//     const requestOptions = {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrfToken,
//         }
//     }

//     const response = await fetch('update/' + userID, requestOptions);
//     if(response.ok){
//         const data = await response.json();
//         console.log(data)
//         updateElement(data.user_status);

//         //userButton.innerText = data.is_active ? 'Set status Offline' : 'Set status Online';
//         // if(data.user_status){
//         //     userStatus.style.color = "green";
//         //     userButton.innerText = 'Set status Offline'
//         // }else{
//         //     userStatus.style.color = "black";
//         //     userButton.innerText = 'Set status Online'
//         // }

//     }
//     // const response = await fetch('update/' + userID, { same as above
//     //     method: 'POST',
//     //     headers: {
//     //         'X-CSRFToken': csrfToken,
//     //     }
//     // })
//     // .then((response) => {
//     //     const data = response.json()
//     //     return data;
//     // })
//     // .then( data => {
//     //     console.log(data)
//     // } )
//     // .catch(error => {
//     //     console.error('Wystąpił błąd:', error);
//     // });

// };

