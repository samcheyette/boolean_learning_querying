var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to

// Task object to keep track of the current phase
var currentview;

psiTurk.preloadPages(["instructions.html",
					  "task.html",
			 		  "thanks.html",
			 		  "demographics.html"
					 ]);

var gender = "NA";
var race = "NA";
var ethnicity = "NA";

var removeBadCharacters = function(str)
{
	return str.split(',').join('').split('\n').join(' ');
}

var demographics = function()
{
	psiTurk.showPage("demographics.html");

	$("#next").click(function()
	{
		if ($('[name="gender"]').is(':checked') &&
			$('[name="race"]').is(':checked') &&
			$('[name="ethnicity"]').is(':checked'))
		{
			gender = $('[name="gender"]:checked').val();
			race = $('[name="race"]:checked').val();
			ethnicity = $('[name="ethnicity"]:checked').val();

			currentview = new instructions();
		}
		else
		{
			$("#error").animate({opacity: 1}, 500);
		}
	});
};

// Instructions
var instructions = function()
{
	psiTurk.showPage("instructions.html");

	$("#begin").on("click", $.proxy(function()
	{
		practiceInstructions();
	}));
};

var practiceStimuli = [
						"blackCat1.jpg",
						"dog1.jpg",
						"dog2.jpg",
						"blackCat3.jpg",
						"blackCat4.jpg",
						"dog3.jpg",
						"blackCat2.jpg",
						"dog4.jpg"
					  ];

var experimentStimuli = [
						 "red_square_small.jpg",
						 "red_square.jpg",
						 "red_triangle_small.jpg",
						 "green_triangle_small.jpg",
						 "green_square.jpg",
						 "red_triangle.jpg",
						 "green_square_small.jpg",
						 "green_triangle.jpg"
					   ];

// A = Red
// B = Small
// C = Square

// Cat
var practiceAnswers = [1, 0, 0, 1, 1, 0, 1, 0];

var experimentAnswers = [[0, 0, 0, 0, 0, 0, 0, 0], 
						 [0, 0, 0, 0, 0, 0, 1, 0], 
						 [0, 0, 0, 0, 0, 1, 0, 0], 
						 [0, 0, 0, 0, 0, 1, 1, 0], 
						 [0, 0, 0, 0, 1, 0, 0, 0], 
						 [0, 0, 0, 0, 1, 0, 1, 0], 
						 [0, 0, 0, 0, 1, 1, 0, 0], 
						 [0, 0, 0, 0, 1, 1, 1, 0], 
						 [0, 0, 0, 1, 0, 0, 0, 0], 
						 [0, 0, 0, 1, 0, 0, 1, 0], 
						 [0, 0, 0, 1, 0, 1, 0, 0], 
						 [0, 0, 0, 1, 0, 1, 1, 0], 
						 [0, 0, 0, 1, 1, 0, 0, 0], 
						 [0, 0, 0, 1, 1, 0, 1, 0], 
						 [0, 0, 0, 1, 1, 1, 0, 0], 
						 [0, 0, 0, 1, 1, 1, 1, 0], 
						 [0, 0, 1, 0, 0, 0, 0, 0], 
						 [0, 0, 1, 0, 0, 0, 1, 0], 
						 [0, 0, 1, 0, 0, 1, 0, 0], 
						 [0, 0, 1, 0, 0, 1, 1, 0], 
						 [0, 0, 1, 0, 1, 0, 0, 0], 
						 [0, 0, 1, 0, 1, 0, 1, 0], 
						 [0, 0, 1, 0, 1, 1, 0, 0], 
						 [0, 0, 1, 0, 1, 1, 1, 0], 
						 [0, 0, 1, 1, 0, 0, 0, 0], 
						 [0, 0, 1, 1, 0, 0, 1, 0], 
						 [0, 0, 1, 1, 0, 1, 0, 0], 
						 [0, 0, 1, 1, 0, 1, 1, 0], 
						 [0, 0, 1, 1, 1, 0, 0, 0], 
						 [0, 0, 1, 1, 1, 0, 1, 0], 
						 [0, 0, 1, 1, 1, 1, 0, 0], 
						 [0, 0, 1, 1, 1, 1, 1, 0], 
						 [0, 1, 0, 0, 0, 0, 0, 0], 
						 [0, 1, 0, 0, 0, 0, 1, 0], 
						 [0, 1, 0, 0, 0, 1, 0, 0], 
						 [0, 1, 0, 0, 0, 1, 1, 0], 
						 [0, 1, 0, 0, 1, 0, 0, 0], 
						 [0, 1, 0, 0, 1, 0, 1, 0], 
						 [0, 1, 0, 0, 1, 1, 0, 0], 
						 [0, 1, 0, 0, 1, 1, 1, 0], 
						 [0, 1, 0, 1, 0, 0, 0, 0], 
						 [0, 1, 0, 1, 0, 0, 1, 0], 
						 [0, 1, 0, 1, 0, 1, 0, 0], 
						 [0, 1, 0, 1, 0, 1, 1, 0], 
						 [0, 1, 0, 1, 1, 0, 0, 0], 
						 [0, 1, 0, 1, 1, 0, 1, 0], 
						 [0, 1, 0, 1, 1, 1, 0, 0], 
						 [0, 1, 0, 1, 1, 1, 1, 0], 
						 [0, 1, 1, 0, 0, 0, 0, 0], 
						 [0, 1, 1, 0, 0, 0, 1, 0], 
						 [0, 1, 1, 0, 0, 1, 0, 0], 
						 [0, 1, 1, 0, 0, 1, 1, 0], 
						 [0, 1, 1, 0, 1, 0, 0, 0], 
						 [0, 1, 1, 0, 1, 0, 1, 0], 
						 [0, 1, 1, 0, 1, 1, 0, 0], 
						 [0, 1, 1, 0, 1, 1, 1, 0], 
						 [0, 1, 1, 1, 0, 0, 0, 0], 
						 [0, 1, 1, 1, 0, 0, 1, 0], 
						 [0, 1, 1, 1, 0, 1, 0, 0], 
						 [0, 1, 1, 1, 0, 1, 1, 0], 
						 [0, 1, 1, 1, 1, 0, 0, 0], 
						 [0, 1, 1, 1, 1, 0, 1, 0], 
						 [0, 1, 1, 1, 1, 1, 0, 0], 
						 [0, 1, 1, 1, 1, 1, 1, 0], 
						 [1, 0, 0, 0, 0, 0, 0, 0], 
						 [1, 0, 0, 0, 0, 0, 1, 0], 
						 [1, 0, 0, 0, 0, 1, 0, 0], 
						 [1, 0, 0, 0, 0, 1, 1, 0], 
						 [1, 0, 0, 0, 1, 0, 0, 0], 
						 [1, 0, 0, 0, 1, 0, 1, 0], 
						 [1, 0, 0, 0, 1, 1, 0, 0], 
						 [1, 0, 0, 0, 1, 1, 1, 0], 
						 [1, 0, 0, 1, 0, 0, 0, 0], 
						 [1, 0, 0, 1, 0, 0, 1, 0], 
						 [1, 0, 0, 1, 0, 1, 0, 0], 
						 [1, 0, 0, 1, 0, 1, 1, 0], 
						 [1, 0, 0, 1, 1, 0, 0, 0], 
						 [1, 0, 0, 1, 1, 0, 1, 0], 
						 [1, 0, 0, 1, 1, 1, 0, 0], 
						 [1, 0, 0, 1, 1, 1, 1, 0], 
						 [1, 0, 1, 0, 0, 0, 0, 0], 
						 [1, 0, 1, 0, 0, 0, 1, 0], 
						 [1, 0, 1, 0, 0, 1, 0, 0], 
						 [1, 0, 1, 0, 0, 1, 1, 0], 
						 [1, 0, 1, 0, 1, 0, 0, 0], 
						 [1, 0, 1, 0, 1, 0, 1, 0], 
						 [1, 0, 1, 0, 1, 1, 0, 0], 
						 [1, 0, 1, 0, 1, 1, 1, 0], 
						 [1, 0, 1, 1, 0, 0, 0, 0], 
						 [1, 0, 1, 1, 0, 0, 1, 0], 
						 [1, 0, 1, 1, 0, 1, 0, 0], 
						 [1, 0, 1, 1, 0, 1, 1, 0], 
						 [1, 0, 1, 1, 1, 0, 0, 0], 
						 [1, 0, 1, 1, 1, 0, 1, 0], 
						 [1, 0, 1, 1, 1, 1, 0, 0], 
						 [1, 0, 1, 1, 1, 1, 1, 0], 
						 [1, 1, 0, 0, 0, 0, 0, 0], 
						 [1, 1, 0, 0, 0, 0, 1, 0], 
						 [1, 1, 0, 0, 0, 1, 0, 0], 
						 [1, 1, 0, 0, 0, 1, 1, 0], 
						 [1, 1, 0, 0, 1, 0, 0, 0], 
						 [1, 1, 0, 0, 1, 0, 1, 0], 
						 [1, 1, 0, 0, 1, 1, 0, 0], 
						 [1, 1, 0, 0, 1, 1, 1, 0], 
						 [1, 1, 0, 1, 0, 0, 0, 0], 
						 [1, 1, 0, 1, 0, 0, 1, 0], 
						 [1, 1, 0, 1, 0, 1, 0, 0], 
						 [1, 1, 0, 1, 0, 1, 1, 0], 
						 [1, 1, 0, 1, 1, 0, 0, 0], 
						 [1, 1, 0, 1, 1, 0, 1, 0], 
						 [1, 1, 0, 1, 1, 1, 0, 0], 
						 [1, 1, 0, 1, 1, 1, 1, 0], 
						 [1, 1, 1, 0, 0, 0, 0, 0], 
						 [1, 1, 1, 0, 0, 0, 1, 0], 
						 [1, 1, 1, 0, 0, 1, 0, 0], 
						 [1, 1, 1, 0, 0, 1, 1, 0], 
						 [1, 1, 1, 0, 1, 0, 0, 0], 
						 [1, 1, 1, 0, 1, 0, 1, 0], 
						 [1, 1, 1, 0, 1, 1, 0, 0], 
						 [1, 1, 1, 0, 1, 1, 1, 0], 
						 [1, 1, 1, 1, 0, 0, 0, 0], 
						 [1, 1, 1, 1, 0, 0, 1, 0], 
						 [1, 1, 1, 1, 0, 1, 0, 0], 
						 [1, 1, 1, 1, 0, 1, 1, 0], 
						 [1, 1, 1, 1, 1, 0, 0, 0], 
						 [1, 1, 1, 1, 1, 0, 1, 0], 
						 [1, 1, 1, 1, 1, 1, 0, 0], 
						 [1, 1, 1, 1, 1, 1, 1, 0]];


var practiceInstructions = function()
{
	psiTurk.showPage("task.html");

	$("#nextQuestion").one("click", $.proxy(function()
	{
		$("#practiceInstructions").hide();
		$("#experiment").show();
		practice();
	}));
};

var nextStimuli = function(currentQuestion, stimuli,
						   answers, path, label)
{
	$("#currentStimuli").prop("src", path + stimuli[currentQuestion]);

	if (answers[currentQuestion])
	{
		$("#label").html(label);
	}
	else
	{
		$("#label").html("not " + label);
	}
};

var practice = function()
{
	currentQuestion = 0;
	stimuli = practiceStimuli;
	answers = practiceAnswers;
	path = "static/images/Practice/";
	label = "blicky";

	nextStimuli(currentQuestion, stimuli, answers, path, label);

	$("#nextQuestion").on("click", $.proxy(function()
	{
		if ($('input[name="response"]:checked').val() == 0)
		{
			currentQuestion++;
			nextStimuli(currentQuestion % 8, stimuli, answers, path, label);
			$('[name="response"]:checked').attr("checked", false);
			$("#error").animate({opacity: 0}, 500);
		}
		else if ($('input[name="response"]:checked').val() == 1)
		{
			$('[name="response"]:checked').attr("checked", false);
			$("#error").animate({opacity: 0}, 500);
			practiceFinalQuestion();
		}
		else
		{
			$("#error").animate({opacity: 1}, 500);
		}
	}));
};

var practiceFinalQuestion = function()
{
	$("#experiment").hide();
	$("#comments").hide();
	$("#freeResponse").show();
	$("#nextQuestion").unbind();

	$("#nextQuestion").on("click", $.proxy(function()
	{
		if (($("#meaning").val().length > 0) &&
			($('ul:not(:has(:radio:checked))').length) == 0)
		{
			$("#meaning").val('');
			$('input[type="radio"]').prop('checked', false); 
			experimentInstructions();
		}
		else
		{
			$("#error2").animate({opacity: 1}, 500);
		}
	}));
};

var experimentInstructions = function()
{
	$("#freeResponse").hide();
	$("#instructions").show();
	$("#nextQuestion").unbind();

	$("#nextQuestion").one("click", $.proxy(function()
	{
		startExperiment();
	}));
};

var startExperiment = function()
{
	$("#instructions").hide();
	$("#experiment").show();
	$("#first").html("Are you certain you know what \"daxxy\" means?");

	//start = performance.now();
	currentQuestion = 0;
	stimuli = experimentStimuli;
	answers = experimentAnswers[mycondition];
	path = "static/images/Experiment/";
	label = "daxxy";

	nextStimuli(currentQuestion, stimuli, answers, path, label);

	$("#nextQuestion").on("click", $.proxy(function()
	{
		if ($('input[name="response"]:checked').val() == 0)
		{
			//end = performance.now();
			currentQuestion++;
			nextStimuli(currentQuestion % 8, stimuli, answers, path, label);
			$('[name="response"]:checked').attr("checked", false);
			$("#error").animate({opacity: 0}, 500);
		}
		else if ($('input[name="response"]:checked').val() == 1)
		{
			psiTurk.recordUnstructuredData("trialsSeen", currentQuestion + 1);
			$("#error").animate({opacity: 0}, 500);
			finalQuestion();
		}
		else
		{
			$("#error").animate({opacity: 1}, 500);
		}
	}));
};

var finalQuestion = function()
{
	$("#freeResponseQuestion").html("What does \"daxxy\" mean?");
	$("#experiment").hide();
	$("#freeResponse").show();
	$("#nextQuestion").unbind();
	$("#comments").show();

	$("#nextQuestion").on("click", $.proxy(function()
	{
		if ($("#meaning").val().length > 0  &&
			($('ul:not(:has(:radio:checked))').length) == 0)
		{
			psiTurk.recordUnstructuredData("rule", removeBadCharacters($("#meaning").val()));
			psiTurk.recordUnstructuredData("rating", $('input[name=rating]:checked').val());
			psiTurk.recordUnstructuredData("comments", removeBadCharacters($("#comments").val()));

			psiTurk.saveData(
		    {
	            success: function()
	            {
	                psiTurk.completeHIT();
	               	psiTurk.showPage("thanks.html");
	            }
	        });
		}
		else
		{
			$("#error2").animate({opacity: 1}, 500);
		}
	}));
};

$(window).load(function()
{
	$.ajax(
	{
		//url: "FuzzyWords.csv",
		//url: "../static/images/Practice/",
		success: function(file_content)
		{
			//var data = $.csv.toArrays(file_content);
			currentview = new demographics();
			//$(data).find("a:contains(.jpg)").each(function()
     		//{
		    	//var files = document.querySelectorAll("a.icon.file");
    			//files.forEach(function(item){filenames.push(item.textContent)})
    			//console.log(data);
  			//});
  		}
	});
});