
function calculateDelta() {
  let daysElement = document.querySelector(".events .revenge-for-brother .days-remaining");
  let button = document.querySelector(".events .revenge-for-brother a");
  let now = new Date();
  let eventEnd = new Date(2024, 0, 1);

  daysDelta = Math.floor((eventEnd - now) / 1000 / 60 / 60 / 24);
  if (daysDelta > 0) {
    daysElement.textContent = `До конца события: ${daysDelta} д.`;
  } else {
    daysElement.textContent = "Событие завершилось!";
    button.remove()
  };
};

window.onload = calculateDelta();
