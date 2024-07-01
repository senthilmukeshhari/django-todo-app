let usernameEl = document.getElementById('username')
let emailEl = document.getElementById('email')
let passwordEl = document.getElementById('password')
let profileImg = document.getElementById('profile-pic')

// Form Validation
$('form[name=signupForm]').submit((e) => {
    start_loading()
    if ($('.is-valid').length < 3) {
        e.preventDefault();
        end_loading()
    }
    usernameValidation(usernameEl)
    emailValidation(emailEl)
    passwordValidation(passwordEl)
})

// When entering in the username field, perform username validation.
$('#username').keyup((e) => {
    usernameValidation(e.target)
})

// When entering in the email field, perform email validation.
$('#email').keyup((e) => {
    emailValidation(e.target)
})

// When entering in the password field, perform password validation.
$('#password').keyup((e) => {
    passwordValidation(e.target)
})

// When upload a image file, the image will be changed.
$('#input-img-file').change((e) => {
    profileImg.src = URL.createObjectURL(e.target.files[0])
})
