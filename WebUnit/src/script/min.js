$(document).ready(function () {
	
	var cache = {store : []};
	
	$("#imap").click(function() {
		$("#imap").fadeOut(1000, function () {
			$("#imap").show(1000);
		});
	});
	
	$("#initbutton").click(function () {
		if (cache.on && cache.on > $.now()) {
			$("div.feed").empty();
			$("div.feed").addClass("map");
			$("div.feed").append("<p align='right' style='font-style:italic; color:#B8B894;'>" + cache.d + "</p>");
			$.each(cache.store, function (index, value) {
				$("div.feed").append("<p>" + value + "</p>");
			});
			return;
		} else {
			cache.store.length = 0;
		}
		$.getJSON("/news", function (data) {
			$("h2").text("NY Times International News Feed");
			$("#imap").hide();
			$("div.feed").empty();
			$("div.feed").addClass("map");
			$("div.feed").append("<p align='right' style='font-style:italic'>" + data.date + "</p>");
			cache.d = data.date;
			$.each(data.items, function (index, value) {
				cache.store.push(this['title']);
				$("div.feed").append("<p>" + this['title'] + "</p>");
			});
			cache.on = $.now() + ((1000) * 60 * 5);
		});
	});
});