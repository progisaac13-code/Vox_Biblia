const audio = document.getElementById("audio");
let interval;
let time = 300; // 5 minutos

function startPrayer() {

  let timeVal = $('#time_pray').val();
  time = parseInt(timeVal);

  $("#modalPrayer").removeClass("hidden");
  audio.play();
  audio.volume = 0.5;
  document.body.classList.add("locked");

  $('#timer').text(`${String(Math.floor(time / 60)).padStart(2, '0')}:${String(time % 60).padStart(2, '0')}`);

  interval = setInterval(() => {
    time--;

    let minutes = Math.floor(time / 60);
    let seconds = time % 60;

    document.getElementById("timer").innerText =
      `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    if (time <= 0) {
      endPrayer();
    }

  }, 1000);
}

function endPrayer() {
  clearInterval(interval);

  audio.pause();
  $("#modalPrayer").addClass("hidden");
  document.body.classList.remove("locked");

  time = 300;
}

