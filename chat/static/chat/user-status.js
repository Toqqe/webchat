// const userButton = document.getElementById('user-status');
// const userID = JSON.parse(document.getElementById('request-user-id').textContent);
// let userCurrentStatus = document.getElementById('user-current-status').textContent.toLowerCase();
// userCurrentStatus = (userCurrentStatus === 'true');

// const userStatus = document.getElementById('user-status-icon');

// updateElement(userCurrentStatus);

// function updateElement(userCurrentStatus){

//     if(userCurrentStatus){
//         userStatus.style.color = "green";
//         userButton.innerText = 'Set status Offline'
//     }else{
//         userStatus.style.color = "black";
//         userButton.innerText = 'Set status Online'
//     }
// }



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

// userButton.addEventListener('click', ()=>{
//     //sendUserStatus();
// });

