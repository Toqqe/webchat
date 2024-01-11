const searchInput = document.getElementById("search-friend");

function SearchUsersOnChat(){

  const searchResults = document.getElementById('search-results');
  const searchForm = document.getElementById("search-form");

  document.addEventListener("click", function() { 
    searchInput.value = "";
    searchResults.style.display = 'none';
    
  });

  searchForm.addEventListener("input", async(event) => { 

    const query = document.querySelector("#search-friend").value;
    
    if(query != ""){
      const response = await fetch(`/search/${query}/`);
      let delayTimer;
      if(response.ok){
          const data = await response.json();
          clearTimeout(delayTimer);

          delayTimer = setTimeout(function() {

          searchResults.style.display = 'block';
          searchResults.innerHTML = "";

          if( data.users_list == ""){
            searchResults.innerHTML += "<li class='text-center p-2' style='background-color:transparent; opacity:100%;'>No results!</li>";
          }
          data.users_list.forEach((result) => { // w socketach ma isc direct message
            searchResults.innerHTML += "<li class='mx-1 p-1'><img class='rounded-circle mx-1' src=" + result.user_img + " width=30 height=24 /><a onclick='addToFriend(this);'>"+ result.users +
            "</a><span class='badge badge-success text-dark'>Start direct message!</span></li>";
          }); }, 300);

      }else{
        searchResults.style.display = 'none';
      }
    }
  });
}



function SearchUsers(){
  const roomName = JSON.parse(document.getElementById('current-room-name').textContent);

  const searchInput = document.getElementById("add-friend");
  const searchResults = document.getElementById('add-results');
  const searchForm = document.getElementById("add-to-channel-user");
  
  document.addEventListener("click", function() { 
    searchInput.value = "";
    searchResults.style.display = 'none';
    
  });
  
  searchForm.addEventListener("input", async(event) => { 
  
    const query = document.querySelector("#add-friend").value;

    let url;

    if(query != ""){
      url = `/search-channel/${roomName}/${query}/`
    }else{
      url = `/search-channel/${roomName}/${query}`
    }

    const response = await fetch(url);

    let delayTimer;
  
    if(response.ok){
        const data = await response.json();
        clearTimeout(delayTimer);
  
        delayTimer = setTimeout(function() {
        searchResults.style.display = 'block';
        searchResults.innerHTML = "";
        if( data.users_not_in_room == ""){
          searchResults.innerHTML += "<li class='text-center p-2' style='background-color:transparent; opacity:100%;'>No results!</li>";
        }
  //              "<p class='mx-1 p-2 mt-auto bd-highlight message text-break' data-bs-toggle='tooltip' data-bs-placement='top' title='" + data.message_timestamp +"'>" + data.message + "</p>" +

        data.room_users.forEach((result) => { 

          if(result.added == true){
            searchResults.innerHTML += 
            `<li class='d-flex bd-highlight mx-1 p-1'><img class='rounded-circle mx-1 bd-highlight' src=${result.user_img} width=30 height=24 /><a class="bd-highlight" type='button' data-value="add" onclick='addToChannel(this);' data-bs-toggle='tooltip' data-bs-placement='top' title="Add to channel!"'>${result.users}
              </a><i class="bi bi-plus bd-highlight ms-auto"></i></li>`;
          }else{
            searchResults.innerHTML += 
            `<li class='d-flex bd-highlight mx-1 p-1'><img class='rounded-circle mx-1 bd-highlight' src=${result.user_img} width=30 height=24 /><a class="bd-highlight" type='button' data-value="remove" onclick='addToChannel(this);' data-bs-toggle='tooltip' data-bs-placement='top' title="Add to channel!"'>${result.users}
              </a><i class="bi bi-dash bd-highlight ms-auto"></i></li>`; // do naprawy` 
          }


        }); 
      }, 300);
  
    }else{
      searchResults.style.display = 'none';
    }
  });
}

function addToChannel(e){

  if(e.dataset.value == "add"){

    const roomName = JSON.parse(document.getElementById('current-room-name').textContent);
    const modal = document.getElementById('addUsersToChannel');
    const modalToHide = bootstrap.Modal.getInstance(modal);  
  
    const response = fetch('/operations-to-channel/'+ roomName + '/' + e.textContent, {
      method:'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
    });
    if(response.ok){
      const data = response.json();
      modalToHide.hide();
      };

  }else if(e.dataset.value == "remove"){
    const roomName = JSON.parse(document.getElementById('current-room-name').textContent);
    const modal = document.getElementById('addUsersToChannel');
    const modalToHide = bootstrap.Modal.getInstance(modal);  
  
    const response = fetch('/operations-to-channel/'+ roomName + '/' + e.textContent, {
      method:'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
    });
    if(response.ok){
      const data = response.json();
      modalToHide.hide();
      };
  }

};

