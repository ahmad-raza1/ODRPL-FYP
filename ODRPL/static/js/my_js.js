$(document).ready(() => {

	console.log("DOM ready!");

	/*$('#select-all').click(() => {
		$("#select-all").toggle();
	});*/

	//onClick="toggle(this)



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

	/*function readmore(value) {

		var dots = document.getElementById("dots"+value);
		var moreText = document.getElementById("more"+value);
		var btnText = document.getElementById("myBtn"+value);

		if (dots.style.display === "none") {
			dots.style.display = "inline";
			btnText.innerHTML = "Read more"; 
			moreText.style.display = "none";
		} else {
			dots.style.display = "none";
			btnText.innerHTML = "Read less"; 
			moreText.style.display = "inline";
		}

	}*/

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

