jQuery(document).ready(function(){
	if(jQuery('#main-content-inner').length > 0){
	
		jQuery('td #activity-progazer').mouseover(function(){
			jQuery(this).siblings('.table-input').hide();
		});
	}
	});
