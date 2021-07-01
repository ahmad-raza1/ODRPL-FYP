$(document).ready(() => {

	console.log("DOM ready!");
	const loader = $('#preloader');

	$( () => {
		$('#main-form').submit( (event) => {
			//event.preventDefault();
			loader.show();
			$.ajax({
			url: "{% url 'abstracts' %}",
			//data: $(this).serialize(),
			method: 'post',
			//dataType: 'JSON'
			}).done(function(resp) {
			loader.hide();
			//alert(resp.status);
			});
		});
	});

	$("#search-for-full-papers").submit( (event) => {
		if ($("input[name=check]:checked").length === 0) {
			event.preventDefault();
			alert('Please select atleast one checkbox!');
			return false;
		}
	});

	$('#select-all').click(function(event) {   
		if (this.checked) {
			$(':checkbox').each(function() {
				this.checked = true;                        
			});
		} else {
			$(':checkbox').each(function() {
				this.checked = false;                       
			});
		}
	});

	$('input[name=check]').click(function() {
		$("#select-all").prop("checked", false);
	});

	$('#selection').click(function() {
		$(this).text(function(i, text){
			if (text === "Search For Full Papers") {
				$('.with-selection').css("display", "block");
				$('.without-selection').css("display", "none");
			} else {
				$('.with-selection').css("display", "none");
				$('.without-selection').css("display", "block");
			}
			return text === "Exit Selection Mode" ? "Search For Full Papers" : "Exit Selection Mode";
		})
	});

});

