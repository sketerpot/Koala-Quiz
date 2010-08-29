// JavaScript code for viewing quizzes.

$(function() {
    $("#submit").button().click(function() {
	var answers = [];
	$("input:radio:checked").map(function() {
	    answers.push($(this).val());
	});

	if (answers.length !== number_of_questions) {
	    alert("You must answer all the questions! FIXME: change this.");
	    return false;
	}

	$("#answers-hidden").val(answers.join(' '));
    });
});

function show_answers() {
    $("div.quiz-question").map(function() {
	var given_answer = $(this).attr("given_answer");
	$("div.answers div", this).map(function() {
	    if ($("input:radio", this).attr("value") == given_answer) {
		$("label", this).addClass("answer-Chosen");
		if ($("label", this).hasClass("answer-False")) {
		    $("label", this).addClass("answer-Incorrect");
		}
	    }
	});
    });
}