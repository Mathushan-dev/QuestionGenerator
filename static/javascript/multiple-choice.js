const question = document.getElementById('question');   // Question
const choices = Array.from(document.getElementsByClassName("option-button"));   // Array of all button choices

const answer = "1";    // Answer will be given like this. A -> 1, B ->, etc.
let tries = 1;


function disableButtons(questionId){      // Disabling buttons after selecting an answer
    var choiceAmount = choices.length;
    for(var i = 0; i<choiceAmount; i++){
        console.log(questionId, choices[i].getAttribute("questionid"))
        if (choices[i].getAttribute("questionid") == questionId) {
            choices[i].disabled = true;
            choices[i].parentElement.classList.add("not-allowed");
        }
    }
}

function postData(questionId){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/saveQuestionAttributes', true);
    xhr.setRequestHeader('content-Type', 'application/json');
    console.log(JSON.stringify({"questionid": questionId, "score": 1, "tries": tries}));
    xhr.send(JSON.stringify({"questionid": questionId, "score": 1, "tries": tries}));
}

choices.forEach(choice => {     // Loop to give each option button an eventlistener
    console.log(choice.dataset["questionid"])
    choice.setAttribute("questionid", choice.dataset["questionid"])
    choice.addEventListener("click", e => {
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset["number"];
        const questionId = selectedChoice.dataset["questionid"];
        const classToApply = selectedAnswer == answer ? "correct" : "incorrect";
        selectedChoice.parentElement.classList.add(classToApply);
        if (classToApply == "correct") {
            disableButtons(questionId);
            postData(questionId);
            tries = 1;
        }
        if (classToApply == "incorrect"){
            tries += 1;
            postData(questionId);
        }
    })
})

