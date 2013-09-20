$(document).ready(function () {
	
	$("#imap").click(function() {
		$("#imap").fadeOut(1000, function () {
			$("#imap").show(1000);
		});
	});
	
	$("#initbutton").click(function () {
		$.getJSON("/news", function (data) {
			$("h2").text("NY Times News Feed");
			$("#imap").hide();
			$("div.feed").addClass("map");
			$.each(data.items, function () {
				$("div.feed").append("<p>" + this['title'] + "</p>");
			});
		});
	});
	
});