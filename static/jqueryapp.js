/**
 * New node file
 */

$(document).ready(function() {

	var listElements;

	var articleItems;

	var nav;

	var articleList, h1, kids, parents;

	var featuredArticle;

	var article2, article3;

	var navList, firstItem, link;

	listElements = $('li');

	articleItems = $('.article-item');

	articleItems.css('font-size', '20px');

	nav = $('#nav');

	articleList = $('.article-list');

	h1 = articleList.siblings('h1');

	if (true) {
		kids = articleList.children();
	} else {
		kids = articleList.find('*');
	}

	parents = articleList.parents('div');

	//featuredArticle = $('.featured');
	//featuredArticle.toggleClass('featured');

	article2 = $('.featured');
	article3 = $('.featured').next();

	article2.toggleClass('featured');
	article3.toggleClass('featured');

	navList = $('.nav-list');

	firstItem = navList.children().first();

	link = firstItem.find('a');

	link.attr('href', '#1');

	$('#input').on('change', function() {
	    var val = $(this).val();
	    $('.articles').find('h1').text(val);
	});

	item = articleList.children().first().find('ul');
	item.remove();

	buildTree();

	count();

	$('img').attr('src', 'http://placekitten.com/350/150');
});

/*
 * '#family2' should be a sibling of and come after '#family1'. '#bruce' should be the only immediate child
 * of '#family2'. '#bruce' should have two <div>s as children, '#madison' and '#hunter'.
 */
function buildTree() {

	var f2 = $('<div></div>', {id : "family2"}).append($('<h1></h1>').text("Family2")),

	br = $('<div></div>', {id : "bruce"}).append($('<h2></h2>').text("Bruce")),

	ma = $('<div></div>', {id : "madison"}).append($('<h3></h3>').text("Madison")),

	ht = $('<div></div>', {id : "hunter"}).append($('<h3></h3>').text("Hunter"));

	br.append(ma).append(ht);
	f2.append(br);
	$('#family1').parent().append(f2);
};

/*
 *
 */
function count() {

	$('p').each(function () {
		t = $(this).text();
		$(this).text(t + " " + t.length);
	});
}
