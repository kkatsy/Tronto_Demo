/* ---------- CHAT BOT ENGINE JS ----------- */
/* original from: https://codepen.io/adamcjoiner/pen/ggxdJK */


$(function() {

	// chat aliases
	var you = 'You';
	var robot = 'Tronto Bot';

	// init next move
	var chat = $('.chat');
	$('.busy').text(robot + ' is typing...');

	// submit user input and get chat-bot's reply
	var submitChat = function() {

		var input = $('.input input').val();
		if(input == '') return;

		$('.input input').val('');
		updateChat(you, input);

		// get a reply to user input
		chatBot(input);
	}

// add a new line to the chat
var updateChat = function(party, text) {

	var style = 'you';
	if(party != you) {
		style = 'other';
	}

	var line = $('<div><span class="party"></span> <span class="text"></span></div>');
	line.find('.party').addClass(style).text(party + ':');
	line.find('.text').text(text);

	chat.append(line);

	chat.stop().animate({ scrollTop: chat.prop("scrollHeight")});

}

// get QA from server-side with lag
var chatBot = function(question) {
	// jsonify + encode user's question
	var json_query = JSON.stringify(question);
	json_query = encodeURIComponent(json_query);

	// get site route for app status func server-side
	var url = "/chatbot/" + json_query;

	// get request to get application's vuln status
	var http = new XMLHttpRequest();
	http.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {

			var response = this.responseText;
			if(response == "error"){
				console.log(response);
			} else {
				var reply = JSON.parse(response);
				console.log("answer: ", reply);

				// slow reply by 400 to 800 ms
				var delayStart = 400;
				var delayEnd = 800;
				var waiting = 0;
				var latency = Math.floor((Math.random() * (delayEnd - delayStart)) + delayStart);
				$('.busy').css('display', 'block');
				waiting++;
				setTimeout( function() {
					if(typeof reply === 'string') {
						updateChat(robot, reply);
					} else {
						for(var r in reply) {
							updateChat(robot, reply[r]);
						}
					}
					if(--waiting == 0) $('.busy').css('display', 'none');
				}, latency);
			}

		}
	}
	http.open("GET", url, true);
	http.send();
}


// event binding
$('.input').bind('keydown', function(e) {
	if(e.keyCode == 13) {
		submitChat();
	}
});
$('.input a').bind('click', submitChat);

// initial chat state
updateChat(robot, 'Hi there! Enter a question to learn more about your vulnerabilities!');

});
