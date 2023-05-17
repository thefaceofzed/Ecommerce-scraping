// JavaScript
var pwd = document.getElementById('password1');
var eye = document.getElementById('eye');

eye.addEventListener('click', togglePass);

function togglePass() {
  eye.classList.toggle('active');
  pwd.type = (pwd.type === 'password') ? 'text' : 'password';
}

// Form Validation
function checkStuff() {
  var email = document.getElementById('email');
  var password = document.getElementById('password1');
  var msg = document.getElementById('msg');

  if (email.value === '') {
    msg.style.display = 'block';
    msg.innerHTML = 'Please enter your email';
    email.focus();
    return false;
  } else {
    msg.innerHTML = '';
  }

  if (password.value === '') {
    msg.innerHTML = 'Please enter your password';
    password.focus();
    return false;
  } else {
    msg.innerHTML = '';
  }

  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (!re.test(email.value)) {
    msg.innerHTML = 'Please enter a valid email';
    email.focus();
    return false;
  } else {
    msg.innerHTML = '';
  }
}
