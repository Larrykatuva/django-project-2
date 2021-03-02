const usernameField = document.querySelector("#usernamefield");
const passwordField = document.querySelector("#passwordfield");
const feedbackArea = document.querySelector("#invalid-feedback");
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