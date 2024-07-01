const start_loading = () => {
    let spinner = document.querySelector('.spinner')
    spinner.classList.remove('d-none')
}

const end_loading = () => {
    let spinner = document.querySelector('.spinner')
    spinner.classList.add('d-none')
}


function setError(element, message) {
    let nxtElement = element.nextElementSibling
    nxtElement.textContent = message
    nxtElement.classList.add('d-block')
    element.classList.add('is-invalid')
    element.classList.remove('is-valid')
    nxtElement.classList.add('text-danger')
    nxtElement.classList.remove('text-success')
}

function setSuccess(element) {
    let nxtElement = element.nextElementSibling
    nxtElement.classList.remove('d-block')
    element.classList.add('is-valid')
    element.classList.remove('is-invalid')
}

function titleValidation(element) {
    if (element.value.trim().length == 0) {
        setError(element, 'Title field is must required.')
        return false;
    }
    return true;
}

function ajax_function(url, data, element) {
    $.ajax({
        method: 'post',
        url: url,
        data: data,
        dataType: 'json',
        success: function (res) {
            if (res.status == 'valid') {
                setSuccess(element)
            }
            if (res.status == 'invalid') {
                setError(element, res.message)
            }
        },
        error: function (err) {
            console.log('Error : ', err)
            alert('Error occurred.')
        }
    })
}


// // Check whether the email format is valid or not
function emailFormatvalidation(val) {
    // Valid Email Format
    let mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
    
    if (val.match(mailFormat)) {
        return true;
    } else {
        return false;
    }
}

// Custom validation functions
// Username Field Validaton
function usernameValidation(element) {
    let data = element.value.trim()
    let url = 'validate/username'

    if (data.length == 0) {
        return setError(element, 'Usernname is required.')
    }

    if (data.length < 5) {
        return setError(element, 'Must contains above 4 characters.')
    }

    if (data.search(' ') != -1) {
        return setError(element, 'Space chacter is not supported in username.')
    }

    ajax_function(url, { "username": data }, element)
}

// Email Field Validaton
function emailValidation(element) {
    let data = element.value.trim()
    let url = 'validate/email'

    if (data.length == 0) {
        return setError(element, 'Email address is reequired.')
    }

    if (!emailFormatvalidation(data)) {
        return setError(element, 'Email is not valid.')
    }

    ajax_function(url, { "email": data }, element)
}

// password Field Validaton
function passwordValidation(element) {
    let data = element.value.trim()

    if (data.length == 0) {
        return setError(element, 'Password is required.')
    }

    if (data.search(' ') != -1) {
        return setError(element, "Password can't contain space.")
    }

    if (data.length != 6) {
        return setError(element, 'Password have must only 6 characters.')
    }
    
    return setSuccess(element)
}
