const searchInput = document.getElementById("search-friend");
const searchResults = document.getElementById('search-results');
const searchForm = document.getElementById("search-form");

document.addEventListener("click", function() { 
  searchInput.value = "";
  searchResults.style.display = 'none';
  
});

searchForm.addEventListener("input", async(event) => { 

  const query = document.querySelector("#search-friend").value;
  const response = await fetch('/search/'+query);
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
        "</a><span class='badge badge-success'>Click to add friend!</span></li>";
      }); }, 300);

  }else{
    searchResults.style.display = 'none';
  }

});



function SearchUsers(){

  const searchInput = document.getElementById("add-friend");
  const searchResults = document.getElementById('add-results');
  const searchForm = document.getElementById("add-to-channel-user");
  
  document.addEventListener("click", function() { 
    searchInput.value = "";
    searchResults.style.display = 'none';
    
  });
  
  searchForm.addEventListener("input", async(event) => { 
  
    const query = document.querySelector("#add-friend").value;
    const response = await fetch('/search/'+query);
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
          searchResults.innerHTML += "<li class='mx-1 p-1'><img class='rounded-circle mx-1' src=" + result.user_img + " width=30 height=24 /><a type='button' onclick='addToChannel(this);'>"+ result.users +
          "</a><span class='badge badge-success'>Add to channel!</span></li>";
        }); }, 300);
  
    }else{
      searchResults.style.display = 'none';
    }
  
  });
  
}

function addToChannel(e){
  const roomName = JSON.parse(document.getElementById('current-room-name').textContent);
  const modal = document.getElementById('addUsersToChannel');
  const modalToHide = bootstrap.Modal.getInstance(modal);  
  const response = fetch('/add-to-channel/'+ roomName + '/' + e.textContent );

  modalToHide.hide();

//   fetch('/' + roomName + '/' + e.textContent, {
//     method: 'POST',
//     body: formData,
// })

}