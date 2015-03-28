$(function() {
  function isValidEmail(email) {
    var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    return re.test(email);
  }

  function isValidPassword(pwd) {
    // at least one number, one lowercase, one uppercase letter, one special symbol
    // at least nine characters
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[?!_#%^&@-]).{9,}/;
    return re.test(pwd);
  }

  function isValidPhone(phone) {
    // phone must be all digits
    var re = /^\d*$/;
    return re.test(phone);
  }
  
  function isEqual(pwd, pwdcf) {
    // passwords entered must be equal
    return (pwd==pwdcf);
  }

  $('#user-add-form').on('submit', function(event) { // form id

    var email = $('#user-email-input').val(); // input id
    var pwd = $('#user-password-input').val(); // input id
    var pwdcf = $('#user-confirm-password-input').val(); //input id
    var phone = $('#user-phone-input').val(); // input id

    if(isValidEmail(email)) {
      $('#email-error').hide(); // div id
    } else {
      $('#email-error').text('Email must be in the correct format.').show();
      event.preventDefault();
    }

    if(isValidPassword(pwd)) {
      $('#password-error').hide(); // div id
    } else {
      $('#password-error').text('Password has to be 9 or more characters, and contain at least 1 upper case, 1 lower case, 1 number, and 1 symbol.').show();
      event.preventDefault();
    }

    if(isEqual(pwd, pwdcf)) {
      $('#confirm-password-error').hide();
    } else {
      $('#confirm-password-error').text('Passwords entered must be the same.').show();
      event.preventDefault();
    }

    if(isValidPhone(phone)) {
      $('#phone-error').hide(); // div id
    } else {
      $('#phone-error').text('Phone must be all digits.').show();
      event.preventDefault();
    }

  });
});

