var originalButton;

function openModal(event) {

  originalButton = event;  
  document.getElementById('modal').style.display = 'flex';
  document.querySelector('.senha-input').focus();
  document.querySelector('.senha-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
          checkPassword();
      }
  });
}



function closeModal() {
  document.getElementById('modal').style.display = 'none';
}


function checkPassword() {
  var password = document.getElementById('passwordInput').value;

  if (password === '64303251') {
    closeModal();
    let form = originalButton.closest('form');
    if (form) {
        
        form.submit();
        
    } else {
        console.error('Formulário não encontrado.');
    }
  } else {
    alert('Senha incorreta. Tente novamente.');
    document.querySelector('.senha-input').value = '';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  let buttons = document.getElementsByClassName('openModal');
  Array.from(buttons).forEach(element => {
    element.addEventListener('click', function (event) {
      event.preventDefault();
      openModal(element);
    });
  });
});


