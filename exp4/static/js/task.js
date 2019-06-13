
/*

IDEA: Give people dot arrays using 1...N colors 
(where the number of colors C is manipulated). 
Have people estimate how many dots of one of the colors they saw.
Even in conditions where C colors are used, sometimes only show people
arrays with 1...(C-1) colors. D

 */



/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);

var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to


function shuffle_array(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
};

arrSum = function(arr){
  return arr.reduce(function(a,b){
    return a + b
  }, 0);
};


//var wait_for_digits = true;
var TRIAL_ID = 0;
var N_TRIALS = 2;
var CURR_TRIAL = 0;
var COLORS = ["red", "blue"];
var SIZES = [30,20];
var SHAPES = ["rect", "circle"];
var TEXTURES = ["solid", "unfilled"];
var CURR_STATE = "querying";

var ALL_OBJS = [['rect', 'red', 'big', 'solid'],['rect', 'red', 'big', 'unfilled'],
['rect', 'red', 'small', 'solid'],['rect', 'red', 'small', 'unfilled'],
['rect', 'blue', 'big', 'solid'],['rect', 'blue', 'big', 'unfilled'],
['rect', 'blue', 'small', 'solid'],['rect', 'blue', 'small', 'unfilled'],
['circle', 'red', 'big', 'solid'],['circle', 'red', 'big', 'unfilled'],
['circle', 'red', 'small', 'solid'],['circle', 'red', 'small', 'unfilled'],
['circle', 'blue', 'big', 'solid'],['circle', 'blue', 'big', 'unfilled'],
['circle', 'blue', 'small', 'solid'],['circle', 'blue', 'small', 'unfilled']];

var ORDERS = [[2, 13, 15, 9, 3, 7, 14, 0, 12, 6, 1, 5, 11, 10, 8, 4],
[0, 9, 8, 4, 15, 14, 13, 10, 5, 7, 11, 1, 6, 3, 12, 2],
[11, 8, 15, 0, 6, 10, 14, 5, 7, 2, 12, 3, 9, 4, 13, 1],
[5, 12, 0, 2, 7, 13, 11, 6, 4, 8, 14, 1, 3, 9, 10, 15]];


var CATEGORIES = [[0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0],[0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0],[1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0],[0,1,0,1,1,1,1,0,0,1,0,1,0,0,1,0],[1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0],[1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1],[1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1],[0,1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],[0,1,0,0,1,1,1,0,0,1,0,1,1,0,1,0],[0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0],
[0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0],[0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0],[0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],[0,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1],[0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
[0,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,1,0,0,1,1,1,0,0,1,0,1,0,0,0,0],[1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1],[1,0,1,1,0,0,0,1,1,0,1,0,0,1,0,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],[0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0],[1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1],[0,1,0,0,1,1,1,0,0,1,0,0,0,0,1,0],[1,0,1,1,0,0,0,1,1,0,1,0,1,1,1,1],[0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
[0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1],[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0],[0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0],[1,0,1,1,1,0,1,1,0,0,1,1,0,0,1,1],
[1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1],[1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],[1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0],[0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0], [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1], 
[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0], [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
[0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1]];

var CPLX = [5,5,3,3,5,3,15,3,5, 5,5,9,17,7,9,3,3,5,1,
5,1,13,5,17,3,1,5,11,5,3,13,13,3,7,3,5,3,5,9,5,5,5,15,5,3,1,1,1,1,1];
//var COND = ['EASY', 'MEDIUM','HARD'][Math.floor(Math.random()*3)];

/*
var CATEGORIES = [

[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1], [0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
[0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1], [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
[0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0], [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],[0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
[0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0], [0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1],[0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0], [1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0],[0,0,1,0,0,0,1,1,1,1,1,1,0,0,1,1]

]; */

//CATEGORIES = CATEGORIES.slice(0,1);

var PID = Math.round(Math.random()*10000000);


var ORDER = [];

for (var i=0; i < CATEGORIES.length;i++) {
	ORDER[i] = i;

}

ORDER = shuffle_array(ORDER);
ORDER = ORDER.slice(0,N_TRIALS);

var cat_tmp = [];
var cplx_tmp = [];
for (i=0; i<ORDER.length;i++) {
	cat_tmp[i] = CATEGORIES[ORDER[i]];
	cplx_tmp[i] = CPLX[ORDER[i]];

}

CATEGORIES = cat_tmp;
CPLX = cplx_tmp;

var COND = arrSum(CPLX)/CPLX.length;

var STR_CATEGORIES = [];

var tmp = "";
for(var i = 0; i < CATEGORIES.length; i += 1){
	tmp = "";
	for (var j = 0; j < CATEGORIES[i].length; j += 1){
    	tmp = tmp + String(CATEGORIES[i][j]);
    }
 
    STR_CATEGORIES[i] = tmp;

}

var pages = [
	//"instructions/instruct-1.html",
	//"instructions/instruct-2.html",
	"instructions/instruct-3.html",
	"instructions/instruct-ready.html",
	"stage.html",
	"postquestionnaire.html"
];

psiTurk.preloadPages(pages);

var instructionPages = [ // add as a list as many pages as you like
	//"instructions/instruct-1.html",
	//"instructions/instruct-2.html",
	"instructions/instruct-3.html",
	"instructions/instruct-ready.html"
];

/********************
* HTML manipulation
*
* All HTML files in the templates directory are requested 
* from the server when the PsiTurk object is created above. We
* need code to get those pages from the PsiTurk object and 
* insert them into the document.
*
********************/

/********************
UTILS */

var contains = function(a, obj) {
	//console.log(a);
    var i = a.length;
    while (i--) {
       if (a[i] === obj) {
           return true;
       }
    }
    return false;
};





var get_nums = function() {
	var l = [];
	var i_incr = (MAX_N - MIN_N)/TOTAL_N;
	for (i=MIN_N; i < MAX_N; i=i+i_incr) {
		l[l.length] = Math.floor(i + Math.random() * i_incr);
	}

	return(shuffle_array(l));

};

var make_grid = function(n, w, h,s_w,s_h) {
	var x = 0;
	var y = 0;
	var lst = [];
	for (i=1; i < n+1; i++) {
		for (j = 1; j < n+1; j++) {
			x = Math.round((j/(n+1)) * w) + s_w;
			y = Math.round((i/(n+1)) * h) + s_h;
			lst[lst.length] = [x,y];

		}
	}
	return(lst)
};


var assign_categories = function(objs, cats) {

	for (i=0; i<objs.length; i++) {
		//objs[i].category = Math.round(Math.random());
		objs[i].category = cats[i];
		//objs[i].unknown = ["A", "B"][1-cats[i]];
		objs[i].unknown =  ""; //["A", "B"][1-cats[i]];

	}
	return(objs);
	


};




var make_obj = function(shape,color,size,texture) {

	var o = new Object();
	o.shape=shape;
	o.color=color;
	o.size=size;
	o.texture=texture;
	o.unknown="?";

	return(o);

};


var make_white_obj = function() {

	var o = new Object();
	o.shape="rect";
	o.color="white";
	o.size=SIZES[0];
	o.texture="filled";
	o.unknown=false;

	return(o);

};


/*

var make_objs = function(cats) {
	var objs = [];
	for (a=0; a < COLORS.length; a++) {
		for (b=0;b<SIZES.length; b++) {
			for (c=0;c < SHAPES.length; c++) {
				for (d=0; d < TEXTURES.length; d++) {
					obj = make_obj(SHAPES[c], COLORS[a],SIZES[b], TEXTURES[d]);
					objs[objs.length] = obj;
				}

			}
		}

	}

	objs = assign_categories(objs, cats);
	return(objs);
};*/

var make_objs = function(cats) {
	var objs = [];
	var size = -1;
	for (var i = 0; i < ALL_OBJS.length; i++) {
		
		if (ALL_OBJS[i][2] == "small") {
			size = SIZES[0];

		} else {
			size = SIZES[1];
		}
		obj = make_obj(ALL_OBJS[i][0],ALL_OBJS[i][1],
						size,ALL_OBJS[i][3]);
		objs[i] = obj;
	}
	objs = assign_categories(objs, cats);
	return(objs);
};


var distance = function(o1,o2) {
	return(((o1[0] - o2[0])**2 + (o1[1] - o2[1])**2)**0.5)
};



var make_white = function(objs) {

	for (i=0; i < objs.length; i++) {
		obj= objs[i];
		obj.color="white";
	}

	return(objs);
};



var get_obj_identities = function(objs) {

	var ident = "";
	var obj;

	for (var i = 0; i < objs.length; i++) {
		obj = objs[i];
		shape = String(obj.shape).slice(0,1);
		color = String(obj.color).slice(0,1);
		size = String(obj.size).slice(0,1);
		texture=String(obj.texture).slice(0,1);
		ident = ident + shape+color+size+texture + "_"

	}

	return(ident)
};
/********************
UTILS */


var SEARCH_EXP = function() {

	var draw = function(ctx_which, grid_which, objs_which) {
		var pos_x;
		var pos_y;
		var obj;
		for (i=0; i < objs_which.length; i++) {
			pos_x = grid_which[i][0];
			pos_y = grid_which[i][1];
			obj = objs_which[i];
			ctx_which.fillStyle = obj.color;
			ctx_which.strokeStyle = obj.color;

        	ctx_which.beginPath();

			if (obj.shape == "rect") {
				if (obj.texture == "solid") {

					ctx_which.fillRect(pos_x-obj.size/2, pos_y-obj.size/2,
							obj.size,obj.size);
				} else {
					ctx_which.strokeRect(pos_x-obj.size/2,pos_y-obj.size/2, obj.size,obj.size);
				}

			} else {
					ctx_which.arc(pos_x, pos_y, obj.size/2, 0, Math.PI*2);
				if (obj.texture == "solid") {
					ctx_which.fill();


				} else {
					ctx_which.stroke();

				}

			}

			ctx_which.fillStyle = "black";

			ctx_which.font = "24px times";
			ctx_which.fillText(obj.unknown, pos_x-5, pos_y+10);

				//ctx_which.fillRect(pos_x, pos_y,obj.size,obj.size);

			//}
		}
	};

	var draw_middle = function() {


		pos_x = width/2;
		pos_y = height/2;

		console.log(objs_middle);
		obj = objs_middle[selected];
		ctx_middle.fillStyle = obj.color;
		ctx_middle.strokeStyle = obj.color;
		ctx_middle.beginPath();

		if (obj.shape == "rect") {
			if (obj.texture == "solid") {

				ctx_middle.fillRect(pos_x-obj.size/2, pos_y-obj.size/2,
						obj.size,obj.size);
			} else {
				ctx_middle.strokeRect(pos_x-obj.size/2,pos_y-obj.size/2, obj.size,obj.size);
			}

		} else {
				ctx_middle.arc(pos_x, pos_y, obj.size/2, 0, Math.PI*2);
			if (obj.texture == "solid") {
				ctx_middle.fill();


			} else {
				ctx_middle.stroke();

			}

		}

	};


	var draw_all = function() {
		clear_stimulus();


		//draw(ctx_middle, grid_middle,objs_middle);



		
		ctx_bottom.fillStyle = "#E8E8E8";
		ctx_top.fillStyle = "#E8E8E8";
		ctx_bottom.strokeStyle = "black";
		ctx_top.strokeStyle = "black";
		ctx_top.font = "20px times";
		ctx_bottom.font = "20px times";


		ctx_bottom.strokeRect(50,10,width-90, height-20);
		ctx_top.strokeRect(50,10, width-90, height-20);
		ctx_bottom.fillRect(50,10,width-90, height-20);
		ctx_top.fillRect(50,10,width-90, height-20);


		ctx_middle.strokeStyle = "black";
		ctx_middle.strokeRect(width+10,40, width*2/5, height/3);


		ctx_middle.fillStyle = "#E8E8E8";
		ctx_middle.font = "20px times";
		ctx_middle.fillRect(width+10,40, width*2/5, height/3);

		ctx_middle.fillStyle = "black";
		ctx_bottom.fillStyle = "black";
		ctx_top.fillStyle = "black";

		s1 = "Number correct: " + n_correct + "/" + n_query
		s2 = "Round bonus: $" + Math.round(money*100)*0.01

		ctx_middle.fillText(s1, width+85,height/2+60)
		ctx_middle.fillText(s2, width+90,height/2+85)



		ctx_middle.font = "18px times";

		ctx_middle.fillText("Is this object in category A or B?", width+40,72)
		ctx_middle.fillText("Use the up and down arrow keys to guess.", width+20,100)

		ctx_top.fillText("----Category A", width-10, height/2)
		ctx_bottom.fillText("----Category B", width-10, height/2)

		draw(ctx_top, grid_top,objs_top);
		draw(ctx_bottom, grid_bottom,objs_bottom);

		setTimeout(draw_middle, 200);

		//draw_middle();



	};





	var clear_stimulus = function() {
 		ctx_top.clearRect(0, 0, tot_width, height);
  		ctx_middle.clearRect(0, 0, tot_width, height);
 		ctx_bottom.clearRect(0, 0, tot_width, height);


	};











	var next = function() {
		CURR_STATE = "querying";

		//document.getElementById('ready').style.display = "block";
		money = 0.;
		n_correct = 0;
		n_query = 0;
		potential_money = 0.0;

		objs_remain = grid_middle.length;

		objs_middle = make_objs(CATEGORIES[TRIAL_ID]);
		obj_identities = get_obj_identities(objs_middle);


		objs_top = [];
		objs_bottom = [];

		listening = true;
		mouse_listening = false;		
		ORDER = ORDERS[Math.floor(Math.random() * ORDERS.length)];
		selected = ORDER[n_query];


		time = new Date().getTime();
		draw_all();

		};

	var show_feedback = function() {
		clear_stimulus();

		var mr = Math.round(money*100)*0.01;


		s5 = "You guessed " + n_correct + "/" + tot_objects;
		s5 = s5 + " objects correctly."

		ctx_top.fillStyle="black";

		ctx_top.font = "24px times";

		ctx_top.fillText(s5,tot_width/2-15,2*height/3 + 40)



		s1 = "So your bonus on that round was: $" + mr + ".";

		s2 = "Your total bonus so far is: $" + Math.round(total_money*100)*0.01 + ".";
		s3 = "Press ENTER to continue."


		ctx_middle.fillStyle="black";

		ctx_middle.font = "24px times";

		ctx_middle.fillText(s1, tot_width/2-40,20)
		ctx_middle.fillText(s2, tot_width/2,55)
		ctx_middle.fillText(s3, tot_width/2+30, 140);
		mouse_listening = false;
		TRIAL_ID = TRIAL_ID + 1;

		setTimeout(function() {
			listening = true;

		}, 1000);







	}

	
	var response_handler = function(e) {


		if (!listening) return;

		var keyCode = e.keyCode,
			response;



		console.log(objs_remain);
		console.log(CURR_STATE);




		if ((CURR_STATE == "feedback") && (keyCode == 13)) {
			psiTurk.saveData()

			if (TRIAL_ID == CATEGORIES.length) {
					finish();
				} else {
					next();

				}
		}  else if (CURR_STATE == "querying") {


		

	     	if (keyCode == 38 || keyCode == 40) {
		     	var o = Object.assign({},objs_middle[selected]);
		     	listening = false;
				ctx_middle.font = "24px times";

	    	    if (((o.category == 0) && (keyCode == 40)) ||
	         		 ((o.category == 1) && (keyCode == 38))) {
		         	 correct = 1;
		      	 	 n_correct = n_correct + 1;
		      	 	 money = money + 0.02;
		      	 	 total_money = total_money + 0.02;
		 			 ctx_middle.fillStyle="green";

					 ctx_middle.fillText("Correct!", width/2+25,height/2+10)

		        } else {
		        	ctx_middle.fillStyle="red";

		          	  correct = 0;
		      	 	 money = money - 0.02;
		      	 	 total_money = total_money - 0.02;
					 ctx_middle.fillText("Incorrect!", width/2+25,height/2+10)

		        }

				  rt = new Date().getTime() - time;
				  time = new Date().getTime()



			    psiTurk.recordTrialData({'phase':"TEST",
			                     'trial_id':TRIAL_ID,
			                     'CURR_STATE': CURR_STATE,
			                     'curr_trial':CURR_TRIAL,

			                     'CONDITION': COND,

			                     'pid': PID,
			                     'rt': rt,
			                     'trial_phase': "querying",
			                     'objs_remain':objs_remain,
			                     'obj_shape': o.shape,
			                     'obj_color':o.color,
			                     'obj_size':o.size,
			                     'obj_texture': o.texture,
			                     'obj_category': o.category,
			                     'money': Math.round(money*100)*0.01,
			                     'potential_money': Math.round(money*100)*0.01,
			                     'selected': selected, 
			                     'total_money': total_money,
			                   //  'bonus': total_money,

			                     'categories': STR_CATEGORIES[CURR_TRIAL],
			                     'cplx': CPLX[CURR_TRIAL],

			                     'objs': obj_identities,
			                     'correct_guess':correct,
			                     'n_query':n_query,
			                     'n_correct':n_correct
			                      });



		        setTimeout(function()  {



	          		if (o.category == 0) {
	          			objs_bottom[objs_bottom.length] = o;


	          		} else {
	           			objs_top[objs_top.length] = o;

	          		}


					n_query = n_query + 1;
					objs_remain = objs_remain - 1;

					if (objs_remain == 0) {
						CURR_STATE = "feedback";
						setTimeout(show_feedback, 250);

					} else {


						selected = ORDER[n_query];
						draw_all();
						listening = true;


					}


				}, 750);


	     	}

	     



		}





	};


	var finish = function() {
	    $("body").unbind("keydown", response_handler); // Unbind keys
	    currentview = new Questionnaire();
	};
	


	
	
	// Load the stage.html snippet into the body of the page
	psiTurk.showPage('stage.html');
	$("body").focus().keydown(response_handler); 

	// Start the test
	//var canvas = document.getElementById('canvas');
	//var grid = make_grid(4*3,width,height);

	//var ctx = canvas.getContext("2d");


	var canvas_top = document.getElementById('top');
	var canvas_middle = document.getElementById('middle');
	var canvas_bottom = document.getElementById('bottom');
	var ctx_top = canvas_top.getContext("2d");
	var ctx_middle = canvas_middle.getContext("2d");
	var ctx_bottom = canvas_bottom.getContext("2d");


	var tot_width = canvas_top.width;

	var width = canvas_top.width * 2/3;
	var height = canvas_top.height;

	var grid_top = make_grid(4, width, height, 0, 0);
	var grid_middle = make_grid(4,width, height,0,0);
	var grid_bottom = make_grid(4,width, height,0,0);

	var objs_middle = make_objs(CATEGORIES[TRIAL_ID]);
	var obj_identities = get_obj_identities(objs_middle);

	var tot_objects = objs_middle.length;

	var objs_top = [];
	var objs_bottom = [];
	var time = new Date().getTime();
	var rt = new Date().getTime() - time;
	ORDER = ORDERS[Math.floor(Math.random() * ORDERS.length)];



	//var selected = -1;
	var correct = -1;


	var closest_index = -1;
	var closest_distance = -1;
	var listening = true;
	var n_correct = 0;
	var n_query = 0;
	var selected = ORDER[n_query];
	//var querying = true;
	var money = 0.;
	var potential_money = grid_middle.length * 0.02;
	var total_money = 0.
	var objs_remain = grid_middle.length;

	//var objs_top = make_white(objs_middle.slice());
	//var objs_bottom =  make_white(objs_middle.slice());

	var mouse_listening = true;


	//document.getElementById('ready').addEventListener('click', ready);



	next();
	//show_feedback();


}
/****************
* Questionnaire *
****************/

var Questionnaire = function() {

	var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

	record_responses = function() {

		psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'submit'});

		$('textarea').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);
		});
		$('select').each( function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);		
		});

	};

	prompt_resubmit = function() {
		document.body.innerHTML = error_message;
		$("#resubmit").click(resubmit);
	};

	resubmit = function() {
		document.body.innerHTML = "<h1>Trying to resubmit...</h1>";
		reprompt = setTimeout(prompt_resubmit, 2000);
		
		psiTurk.saveData({
			success: function() {
			    clearInterval(reprompt); 
                psiTurk.computeBonus('compute_bonus', function(){
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 


			}, 
			error: prompt_resubmit
		});
	};

	// Load the questionnaire snippet 
	psiTurk.showPage('postquestionnaire.html');
	psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'begin'});
	
	$("#next").click(function () {
	    record_responses();
	    psiTurk.saveData({
            success: function(){
                psiTurk.computeBonus('compute_bonus', function() { 
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 
            }, 
            error: prompt_resubmit});
	});
    
	
};

// Task object to keep track of the current phase
var currentview;

/*******************
 * Run Task
 ******************/
$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { currentview = new SEARCH_EXP(); } // what you want to do when you are done with instructions
    );
});
