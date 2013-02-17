var news;
$(function(){
	$.ajax({
		url: '/get_results',
		type: 'GET',
		success: function(response) {
			news = JSON.parse(response);
		},
		error: function(response) {
			alert('failed to load todays news');
		},
		complete: function() {
			display('delhi');
		}
	});
});

$(function () {
	$('.cities').click(function(){
		$('.cities').removeClass('active');
		$(this).closest('li').addClass('active');
		$('#content').empty();
		display(this.id);
	});
});

var fontSize = d3.scale.log().range([10, 100]);
var fill = d3.scale.category20();

function display(city) {
	d3.layout.cloud().size([700,700])
	.words(Object.keys(news.data[city]).map(function(d) {
		return {text: d, size: 2*news.data[city][d] };
	}))
	.rotate(function() { return ~~(Math.random() * 2) * 90; })
	.font("Impact")
	.fontSize(function(d) { return d.size; })
	.on("end", draw)
	.start();
}

function draw(words) {
	d3.select("#content").append("svg")
	.attr("width", 960)
	.attr("height", 600)
	.append("g")
	.attr("transform", "translate(480,300)")
	.selectAll("text")
	.data(words)
	.enter().append("text")
	.style("font-size", function(d) { return d.size + "px"; })
	.style("font-family", "Impact")
	.style("fill", function(d, i) { return fill(i); })
	.attr("text-anchor", "middle")
	.attr("transform", function(d) {
		return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	})
	.text(function(d) { return d.text; });
}