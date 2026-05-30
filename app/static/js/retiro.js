const audio = document.getElementById("audio");
let interval;
let time = 300; // 5 minutos

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
        document.getElementById("timer").innerHTML =
          `<p style="font-size: 36px;">Um tempo de oração de ${String(minutes).padStart(2, '0')} minutos e ${String(seconds).padStart(2, '0')} segundos! <br>✨ Continue buscando com Intensidade e Foco!</p>`;
        audio.pause();
        setTimeout(() => {

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

    }, 1000);


    $('#timer').html('<i class="fa-solid fa-infinity" style="font-size: 200px; font-style: italic"></i><p style="font-size: 24px; font-weight: bold; text-align: center;">Seu tempo de oração será revelado quando terminar! <br> <p style="font-size: 18px;">(Aperte Qualquer Tecla Para Encerrar ✨)</p></p>');
  } else if (timeVal != "0") {
    time = parseInt(timeVal);
    $('#timer').text(`${String(Math.floor(time / 60)).padStart(2, '0')}m:${String(time % 60).padStart(2, '0')}s`);

    interval = setInterval(() => {
      time--;

      let minutes = Math.floor(time / 60);
      let seconds = time % 60;

      document.getElementById("timer").innerText =
        `${String(minutes).padStart(2, '0')}m:${String(seconds).padStart(2, '0')}s`;

      if (time <= 0) {
        endPrayer();
      }

    }, 1000);
  }
}

function endPrayer() {
  clearInterval(interval);
  $('#timer').text('')
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

