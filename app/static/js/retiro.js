const audio = document.getElementById("audio");
let interval;
let time = 300; // 5 minutos
let prayer_time = '';

$('#time_pray').on('change', function () {
  let timeVal = $(this).val();
  if (timeVal === "0") {
    $('.obs').removeClass('hidden');
  } else {
    $('.obs').addClass('hidden');
  }
});

function startPrayer() {

  let timeVal = $('#time_pray').val();

  // ENTRAR EM TELA CHEIA
  if (document.documentElement.requestFullscreen) {

    document.documentElement
      .requestFullscreen()
      .then(() => {

        console.log("Tela cheia ativada");

      })
      .catch(err => {

        console.log(err);

      });
  }

  $("#modalPrayer").removeClass("hidden");

  audio.play();
  audio.volume = 0.5;
  document.body.classList.add("locked");


  if (timeVal === "0") {
    time = 0;

    interval = setInterval(() => {
      time++;

      let minutes = Math.floor(time / 60);
      let seconds = time % 60;

      if ($(document).keypress(function () {
        prayer_time = `${String(minutes).padStart(2, '0')}m:${String(seconds).padStart(2, '0')}s`;
        document.getElementById("timer").innerHTML =
          `<p style="font-size: 36px;">Um tempo de oração de ${String(minutes).padStart(2, '0')} minutos e ${String(seconds).padStart(2, '0')} segundos! <br>✨ Continue buscando com Intensidade e Foco!</p>`;
        audio.pause();
        setTimeout(() => {
          clearInterval(interval);


          if (document.fullscreenElement) {

            document.exitFullscreen()
              .then(() => {

                console.log("Saiu da tela cheia");

              })
              .catch(err => {

                console.log(err);

              });
          }

          $("#modalPrayer").addClass("hidden");
          document.body.classList.remove("locked");
        }, 5000);
      }));
      if (clearInterval(interval)) {
        registarOracao(prayer_time);
      }
    }, 1000);



    $('#timer').html('<i class="fa-solid fa-infinity" style="font-size: 200px; font-style: italic"></i><p style="font-size: 24px; font-weight: bold; text-align: center;">Seu tempo de oração será revelado quando terminar! <br> <p style="font-size: 18px;">(Aperte Qualquer Tecla Para Encerrar ✨)</p></p>');
  } else if (timeVal != "0") {
    time = parseInt(timeVal);
    $('#timer').text(`${String(Math.floor(time / 60)).padStart(2, '0')}m:${String(time % 60).padStart(2, '0')}s`);
    prayer_time = `${String(Math.floor(time / 60)).padStart(2, '0')}m:${String(time % 60).padStart(2, '0')}s`;

    interval = setInterval(() => {
      time--;

      let minutes = Math.floor(time / 60);
      let seconds = time % 60;

      document.getElementById("timer").innerText =
        `${String(minutes).padStart(2, '0')}m:${String(seconds).padStart(2, '0')}s`;

      if (time <= 0) {
        endPrayer(prayer_time);
      }
    }, 1000);
  }
}

function endPrayer(duracao) {
  clearInterval(interval);
  $('#timer').text('')

  registarOracao(duracao);

  if (document.fullscreenElement) {

    document.exitFullscreen()
      .then(() => {

        console.log("Saiu da tela cheia");

      })
      .catch(err => {

        console.log(err);

      });
  }

  audio.pause();
  $("#modalPrayer").addClass("hidden");
  document.body.classList.remove("locked");

  time = 300;
}

function registarOracao(duracao) {
  fetch('/api/registrar_oracao', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      duracao: duracao
    })
  })
    .then(res => res.json())
    .then(data => {
      icone = document.getElementById('icone-fav' + id);


      if (data.status === 'adicionado') {
        icone.classList.remove('fa-regular');
        icone.classList.add('fa-solid');
        icone.style.color = '#ff0000';
      } else if (data.status === 'removido') {
        icone.classList.remove('fa-solid');
        icone.classList.add('fa-regular');
        icone.style.color = '#f8fafc';
      } else if (data.status === 'Não Logado!') {
        document.getElementById('liveToastBtn').click();
        document.querySelector('.text-toast').textContent = 'Faça login para salvar versículos!';
      }
    })
}

