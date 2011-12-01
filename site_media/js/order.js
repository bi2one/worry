jQuery(function($) {
    var search_text_obj = $("#search-text");
    var search_submit_obj = $("#search-submit");
    search_text_obj.Watermark("찾고자 하는 읍/면/동을 입력하세요.");
    search_text_obj.keypress(function(e) {
	if (e.which == 13) {
	    onAddressSearchClick();
	}
    });
    search_submit_obj.click(function() {
	    onAddressSearchClick();
    });
    $("#id_receiver_address_number").click(function() {
	onOpenLayerClick();
    });
    onCloseLayerClick();

    if(typeof String.prototype.trim !== 'function') {
	String.prototype.trim = function() {
	    return this.replace(/^\s+|\s+$/g, ''); 
	}
    }
});

    function onAddressSearchClick() {
	var url = "/order/ajax_address_number/";
	var search_text = $("#search-text").val();
	var address_box = $("#layer-address");
	
        $.ajax({
		type: "POST",
		    url: url,
		    dataType: "json",
		    data: ({"search-text": search_text}),
		    success: function(data) {
		    $(".addr-field").remove();
		    $.each(data, function() {
			    address_box.append('<tr class="addr-field"><td class="zipcode"><a onClick="javascript:onAddressNumberClick('
				       + "'" + this.ZIPCODE + "',"
				       + "'" + this.address.trim() + "'"
			    	       + ');">'
			    	       + this.ZIPCODE
			    	       + "</a></td>"
			    	       + '<td class="address">'
			    	       + this.address
			    	       + '</td></tr>');
			});
		}
	    })
	    }
    
    function onAddressNumberClick(addr_number, addr) {
	$("#id_receiver_address_number").val(addr_number);
	$("#id_receiver_address").val(addr)
	    $("#id_receiver_detail_address").focus();
	onCloseLayerClick();
    }
    
    function onOpenLayerClick() {
	$("#address_layer").fadeIn();
    }
    
    function onCloseLayerClick() {
	$("#address_layer").fadeOut();
    }
