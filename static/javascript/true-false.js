const question = document.getElementById('question');   // Question
const choices = Array.from(document.getElementsByClassName("option-button"));   // Array of all button choices

const answer = "1";    // Answer will be given like this. A -> 1, B ->, etc. 

//var selectedChoice;     // Element chosen
//var selectedAnswer;     // Number of chosen element

// var button = document.getElementsByClassName("btn");    // Button to submit

//function giveFeedback(){        // Method that shows correct or not
//    const classToApply = selectedAnswer == answer ? "correct" : "incorrect";
//    selectedChoice.parentElement.classList.add(classToApply);
//    disableButtons();
//}

// button[0].addEventListener("click", giveFeedback, false);


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


