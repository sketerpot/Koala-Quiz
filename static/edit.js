// JavaScript code for the quiz editor. Uses JQuery and JQuery-UI.

// When the page loads, set up the buttons.
$(function() {
    $("#addquestion").button().click(add_question);
});

// Random UUID generator function, taken from Robert Kieffer. This
// function is open source, as are any modified versions of it.
function randomUUID() {
    var s = [], itoh = '0123456789ABCDEF';

    // Make array of random hex digits. The UUID only has 32 digits in it, but we
    // allocate an extra items to make room for the '-'s we'll be inserting.
    for (var i = 0; i <36; i++) s[i] = Math.floor(Math.random()*0x10);

    // Conform to RFC-4122, section 4.4
    s[14] = 4;  // Set 4 high bits of time_high field to version
    s[19] = (s[19] & 0x3) | 0x8;  // Specify 2 high bits of clock sequence

    // Convert to hex chars
    for (var i = 0; i <36; i++) s[i] = itoh[s[i]];

    // Insert '-'s
    s[8] = s[13] = s[18] = s[23] = '-';

    return s.join('');
}

var question_html = '<div class="quiz-question" style="display: none"><div class="label">Question:</div><br /><textarea rows="1" cols="1"></textarea><br /><div class="label">Answers (check the right one):</div><br /><div class="answers"><input type="radio" name="FIXME" value="0" class="checkbox" checked="true"> <input type="text" class="answer"><br /><input type="radio" value="1" name="FIXME" class="checkbox"> <input type="text" class="answer"><br /><input type="radio" value="2" name="FIXME" class="checkbox"> <input type="text" class="answer"><br /><input type="radio" value="3" name="FIXME" class="checkbox"> <input type="text" class="answer"><br /></div></div>';

// Create a new question form and slide it in at the bottom.
function add_question() {
    var html = question_html.replace(/FIXME/g, randomUUID());
    $(html).appendTo($("#questions")).slideDown();
}

// Build the JSON document for this quiz, and return it.
function build_json() {
    var questions = [];

    // Iterate through each question, building its data structure,
    // then adding it to the list of questions.
    $(".quiz-question").each(function() {
	var current_question = {'question': $('textarea', this).val()};
	// Accumulate a list of [answer_text, correct?] pairs.
	var answers = [];
	$('.answers > input:text', this).each(function(i) {
	    answers[i] = [$(this).val(), false];
	});
	// Check the correct answer
	answers[$('.answers > input:radio:checked', this).val()][1] = true;
	// Eliminate blank answers
	current_question.answers = [];
	for (var i = 0; i < answers.length; i++)
	    if (answers[i][0] !== '')
		current_question.answers.push(answers[i]);
	// Add non-blank questions to the list
	if (current_question.question !== "")
	    questions.push(current_question);
    });

    return {'title': $("#title-input").val(),
	    'questions': questions};
}

// Create the JSON and put it in the hidden JSON field prior to form
// submission.
$(function() {
    $("input:submit").button().click(function() {
	$("#quiz-json").val(JSON.stringify(build_json()));
    });
});