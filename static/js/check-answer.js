let validAnswerContainer = document.querySelector("main > .task .valid");
let answers = document.querySelectorAll("main > .task .answer");
let button = document.querySelector("main > .task form > .button");
let solution = document.querySelector("main > .task .solution");


function checkAnswer() {
  button.remove()
  solution.style.display = "block";
  validAnswerContainer.classList.add("answered");

  answers.forEach((element) => {
    if (element.querySelector("input").checked == true && !element.classList.contains("answered")) {
      element.classList.add("invalid");
    };

    element.querySelector("input").checked = false;
    element.querySelector("input").disabled = true;
  });
};
