const usernameField = document.querySelector("#usernameField")
const feedbackField = document.querySelector(".invalid-feedback")
const emailField = document.querySelector("#emailField")
const emailFeedback = document.querySelector(".emailfeedback")
const phonenumberField = document.querySelector("#phonenumberField")
const phonenumberfeedback = document.querySelector(".phonenumberfeedback")
const showPasswordToggle = document.querySelector(".showPasswordToggle")
const passwordField = document.querySelector("#passwordField")
const submitBtn = document.queryCommandValue(".submit-btn")


const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent==="SHOW"){
        showPasswordToggle.textContent="HIDE"
        passwordField.setAttribute("type","password")
    }else{
        showPasswordToggle.textContent="SHOW"
        passwordField.setAttribute("type","text")

    }
}



showPasswordToggle.addEventListener("click",handleToggleInput)


phonenumberField.addEventListener("keyup",(e) => {
    const phonenumberVal = e.target.value;
    phonenumberField.classList.remove("is-invalid")
    phonenumberfeedback.style.display="none"

    if(phonenumberVal.length>0){

        fetch('/authentication/phonenumber_validation',{
            body:JSON.stringify({phonenumber:phonenumberVal}),
            method:"POST"
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data",data)
            if(data.phonenumber_error){
                submitBtn.disabled=true
                phonenumberField.classList.add("is-invalid")
                phonenumberfeedback.style.display="block"
                phonenumberfeedback.innerHTML=`<p>${data.phonenumber_error}</P>`

            }else{
                submitBtn.removeAttribute('disabled')
            }
            
        })
    }
})


emailField.addEventListener("keyup",(e) =>{
    const emailval = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedback.style.display="none"

    if(emailval.length>0){
        fetch('/authentication/email_validation',{
            body:JSON.stringify({email: emailval}),
            method:"POST"

        })
        .then((res)=>res.json())
        .then((data) => {
            
            if(data.email_error){
                submitBtn.disabled=true
                emailField.classList.add("is-invalid");
                emailFeedback.style.display="block"
       
                emailFeedback.innerHTML=`<p>${data.email_error}</P>`
            }else{
                submitBtn.removeAttribute("disabled")
            }

            
        })
    }

})

usernameField.addEventListener("keyup", (e) => {
    
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackField.style.display="none"

    if(usernameVal.length>0){
        fetch('/authentication/username_validation',{
            body:JSON.stringify({username:usernameVal}),
            method:"POST"
        })
        .then((res)=>res.json())
        .then(data => {
            console.log(data)
            if(data.username_error){
                submitBtn.disabled=true
                usernameField.classList.add("is-invalid");
                feedbackField.style.display="block"
       
                feedbackField.innerHTML=`<p>${data.username_error}</P>`
            }else{
                submitBtn.removeAttribute('disabled')
            }
        })

    }
})