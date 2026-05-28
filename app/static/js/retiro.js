let interval;
let time = 300; // 5 minutos

function startPrayer() {
  document.getElementById("prayerMode").style.display = "flex";
  document.body.classList.add("locked");

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

  document.getElementById("prayerMode").style.display = "none";

  document.body.classList.remove("locked");

  time = 300;
}