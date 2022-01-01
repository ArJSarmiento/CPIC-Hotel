document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('login');
    const signupBtn = document.getElementById('signup');
    const submitButtonLogin = document.getElementById('loginSubmit');
    const submitButtonSignup = document.getElementById('signupSubmit');
    const LoginInputs = document.querySelectorAll('#loginForm input');
    const SignupInputs  = document.querySelectorAll('#signupForm input');

    submitButtonLogin.disabled=true;
    submitButtonSignup.disabled=true;

    function disableButton(inputs, button) {
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].value === '') {
                button.disabled = true;
                return;
            }
        }
        button.disabled = false;
    }

    LoginInputs.forEach(LoginInput => {
        LoginInput.addEventListener('keyup', ()  => {
            disableButton(LoginInputs, submitButtonLogin);
            console.log(submitButtonLogin.disabled);
        })
    });

    SignupInputs.forEach(SignupInput => {
        SignupInput.addEventListener('keyup', ()  => {   
            disableButton(SignupInputs, submitButtonSignup);
            console.log(submitButtonSignup.disabled);
        })
    });

    loginBtn.addEventListener('click', (e) => {
        let parent = e.target.parentNode.parentNode;
        Array.from(e.target.parentNode.parentNode.classList).find((element) => {
            if (element !== "slide-up") {
                parent.classList.add('slide-up')
            } else {
                signupBtn.parentNode.classList.add('slide-up')
                parent.classList.remove('slide-up')
            }
        });
    });

    signupBtn.addEventListener('click', (e) => {
        let parent = e.target.parentNode;
        Array.from(e.target.parentNode.classList).find((element) => {
            if (element !== "slide-up") {
                parent.classList.add('slide-up')
            } else {
                loginBtn.parentNode.parentNode.classList.add('slide-up')
                parent.classList.remove('slide-up')
            }
        });
    });
})