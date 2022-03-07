const question = document.getElementById('question');   // Question
const choices = Array.from(document.getElementsByClassName("option-button"));   // Array of all button choices

const answer = "1";    // Answer will be given like this. A -> 1, B ->, etc.


function disableButtons(){      // Disabling buttons after selecting an answer
    var choiceAmount = choices.length;
    for(var i = 0; i<choiceAmount; i++){
        choices[i].disabled = true;
        choices[i].parentElement.classList.add("not-allowed");
    }
}

choices.forEach(choice => {     // Loop to give each option button an eventlistener
    choice.addEventListener("click", e => {
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset["number"];
        const classToApply = selectedAnswer == answer ? "correct" : "incorrect";
        selectedChoice.parentElement.classList.add(classToApply);
        disableButtons();
    })
})

