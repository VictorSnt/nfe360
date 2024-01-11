var originalButton;
        function openModal(event) {
          originalButton = event;  
          document.getElementById('modal').style.display = 'flex';
        }
      
        
        function closeModal() {
          document.getElementById('modal').style.display = 'none';
        }
      
        
        function checkPassword() {
          var password = document.getElementById('passwordInput').value;

          if (password === '6430') {
            console.log('Senha correta!');
            closeModal();
            let form = originalButton.closest('form');
            if (form) {
                
                form.submit();
                
            } else {
                console.error('Formulário não encontrado.');
            }
          } else {
            alert('Senha incorreta. Tente novamente.');
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