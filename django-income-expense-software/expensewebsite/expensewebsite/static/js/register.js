const usernameField = document.querySelector("#usernamefield");
const emailField = document.querySelector("#emailfield");
const passwordField = document.querySelector("#passwordfield");
const feedbackArea = document.querySelector("#invalid-feedback");
const emailfeedbackArea = document.querySelector("#email-feedback");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

/*
*Password validation
*/
handleToggleInput=(e) => {
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}

showPasswordToggle.addEventListener("click", handleToggleInput);


/*
*Email validation
*/
emailField.addEventListener("keyup", (e) =>{
    const emailVal = e.target.value;
    
    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display = "none";

    if (emailVal.length > 0){
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal }),
            method: "POST",
        }).then((res) => res.json())
            .then((data) => {
                if(data.email_error){
                    console.log("Error: ",data.email_error);
                    emailField.classList.add("is-invalid");
                    emailfeedbackArea.style.display = "block";
                    emailfeedbackArea.classList.add("text-danger");
                    emailfeedbackArea.innerHTML = data.email_error;
                    submitBtn.disabled = true;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});



/*
 *User validation
 */
usernameField.addEventListener("keyup", (e) =>{
    const usernameVal = e.target.value;
    
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";

    if (usernameVal.length > 0){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal }),
            method: "POST",
        }).then((res) => res.json())
            .then((data) => {
                if(data.username_error){
                    submitBtn.disabled = true;
                    console.log("Error: ",data.username_error);
                    usernameField.classList.add("is-invalid");
                    feedbackArea.style.display = "block";
                    feedbackArea.classList.add("text-danger");
                    feedbackArea.innerHTML = data.username_error;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});