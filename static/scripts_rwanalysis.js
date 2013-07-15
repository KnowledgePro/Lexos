$(function() {
	$(".minifilepreview").click(function() {
		$(this).siblings(".minifilepreview").removeClass('enabled');
		$(this).addClass('enabled');
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	$("#radioratio").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeIn(timeToToggle);
		$(".rollingsearchwordoptdiv").css('display', 'inline');
	});
	$("#radioaverage").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeOut(timeToToggle);
	});

	$("#radioinputletter").click(function() {
		var oldVal = $(".rollinginput").val();
		$(".rollinginput").val(oldVal.slice(0,1));
	});

	$("#radioinputword").click(function() {
		if ($("#windowletter").prop('checked')) {
			$("#windowword").click();
		}
	});
	$("#radiowindowletter").click(function() {
		if ($("#inputword").prop('checked')) {
			$("#rwasubmiterrormessage3").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	$(".rollinginput").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			if ($(this).val().length > 0 && $("#inputletter").prop('checked')) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});
	$("#rollingwindowsize").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			key = String.fromCharCode( key );
			var regex = /[0-9]|\./;
			if( !regex.test(key) ) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});

	$("form").submit(function() {
		var empty = $("input").filter(function() {
			return this.value == '' && (this.type == 'text' || this.type == 'number');
		});
		numEmpty = empty.length;
		if ($(".minifilepreview.enabled").length == 0) {
			$("#rwasubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if (numEmpty > 0 && !(numEmpty == 1 && empty[0].id == 'rollingsearchwordopt' && $("#rollingaverage").prop('checked')) ) {
			$("#rwasubmiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	function makeRWAGraph() {
		if ($("#rwagraphdiv").text() == 'True') {
			$("#rwagraphdiv").removeClass('hidden');
			$("#rwagraphdiv").text('');

			var xhr = new XMLHttpRequest();

			xhr.open("GET", document.URL+'_data', false);
			xhr.send();

			var dataArray = eval(xhr.response);

			var margin = {top: 20, right: 20, bottom: 30, left: 50},
				width = 940 - margin.left - margin.right,
				height = 500 - margin.top - margin.bottom;

			var x = d3.scale.linear()
				.range([0, width])
				.domain(d3.extent(dataArray, function(d) { return d[0] }));

			var y = d3.scale.linear()
				.range([height, 0])
				.domain(d3.extent(dataArray, function(d) { return d[1] }));

			var line = d3.svg.line()
				.x(function(d) { return x(d[0]); })
				.y(function(d) { return y(d[1]); });

			var zoom = d3.behavior.zoom()
				.x(x)
				.y(y)
				.on("zoom", zoomed);

			svg = d3.select('#rwagraphdiv')
			.append("svg:svg")
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom)
			.append("svg:g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				.call(zoom);

			svg.append("svg:rect")
				.attr("width", width)
				.attr("height", height)
				.attr("class", "plot");

			var make_x_axis = function () {
				return d3.svg.axis()
					.scale(x)
					.orient("bottom")
					.ticks(5);
			};

			var make_y_axis = function () {
				return d3.svg.axis()
					.scale(y)
					.orient("left")
					.ticks(5);
			};

			var xAxis = d3.svg.axis()
				.scale(x)
				.orient("bottom")
				.ticks(5);

			svg.append("svg:g")
				.attr("class", "x axis")
				.attr("transform", "translate(0, " + height + ")")
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(y)
				.orient("left")
				.ticks(5);

			svg.append("g")
				.attr("class", "y axis")
				.call(yAxis);

			svg.append("g")
				.attr("class", "x grid")
				.attr("transform", "translate(0," + height + ")")
				.call(make_x_axis()
				.tickSize(-height, 0, 0)
				.tickFormat(""));

			svg.append("g")
				.attr("class", "y grid")
				.call(make_y_axis()
				.tickSize(-width, 0, 0)
				.tickFormat(""));

			var clip = svg.append("svg:clipPath")
				.attr("id", "clip")
			.append("svg:rect")
				.attr("x", 0)
				.attr("y", 0)
				.attr("width", width)
				.attr("height", height);

			var chartBody = svg.append("g")
				.attr("clip-path", "url(#clip)");

			chartBody.append("svg:path")
				.datum(dataArray)
				.attr("class", "line")
				.attr("d", line);

			function zoomed() {
				console.log(d3.event.translate);
				console.log(d3.event.scale);
				svg.select(".x.axis").call(xAxis);
				svg.select(".y.axis").call(yAxis);
				svg.select(".x.grid")
					.call(make_x_axis()
					.tickSize(-height, 0, 0)
					.tickFormat(""));
				svg.select(".y.grid")
					.call(make_y_axis()
					.tickSize(-width, 0, 0)
					.tickFormat(""));
				svg.select(".line")
					.attr("class", "line")
					.attr("d", line);
			}


		}
	}

	makeRWAGraph();
});