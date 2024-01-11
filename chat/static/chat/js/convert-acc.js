const formButton = document.getElementById("convert-from-button");
const form = document.getElementById("convert-form");

// formButton.addEventListener('click', () => {
//     const form = document.getElementById("convert-form");

form.addEventListener('submit', (event) =>{
    event.preventDefault();

    const formData = new FormData(form);
    const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = fetch('/convert',{
        method:"POST",
        headers:{
            //'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        body:formData
    })
    .then( response => response.json() )
    .then( data =>{
        if (data.status == 'success') {
            console.log('Formularz został pomyślnie przesłany!');
        }else{
            console.log("failed") 
            const errorsObject = JSON.parse(data.errors);

            for (let field in errorsObject) {
                console.log(field)
                if (errorsObject.hasOwnProperty(field)) {
                    const errors = errorsObject[field];
            
                    for (const error of errors) {

                        const errorMessage = error.message;
                        const errorElement = document.getElementById(`id_${field}`);
                        const errorElementText = document.getElementById(`${field}_error`);

                        if (errorElement) {
                            errorElement.classList.add('error-from');
                            errorElementText.textContent = errorMessage;
                        }

                        //console.log(`Field: ${field}, Message: ${errorMessage}`);
                    }
                }
            }

            
        };
    })

});
// });

//     const csrfToken = await getCSRFToken();

//     const requestOptions = {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrfToken,
//         }
//     }