function subject_toggle() {
    element_toggle('subject');
}

function contents_toggle() {
    element_toggle('contents');
}

function name_toggle() {
    element_toggle('name');
}

function element_toggle(sElementName) {
    var sCheckboxId = sElementName + '-checkbox';
    var sNextClass = '';
    var sClassPrefix = sElementName + '-checkbox-pic';
    var sCommonClass = "checkbox-toggle";
    var oCheckboxElement = document.getElementById(sCheckboxId);
    var sChecked = oCheckboxElement.checked;
    var oTargetPicClass = null;
    var oNextPicClass = null;
    
    if (sChecked) {
	oTargetPicClass = $("." + sClassPrefix + "-clicked")[0];
	oNextPicClass = $("." + sClassPrefix)[0];
	oCheckboxElement.checked = false;
    } else {
	oTargetPicClass = $("." + sClassPrefix)[0];
	oNextPicClass = $("." + sClassPrefix + "-clicked")[0];
	oCheckboxElement.checked = true;
    }
    oTargetPicClass.style.display = "none";
    oNextPicClass.style.display = "block";
}

function searchCheckBoxValidation() {
    // var oFrm = document.forms["search_area_form"];
    // if(!oFrm.name.checked && !oFrm.title.checked && !oFrm.content.checked) {
    // 	sfm_show_error_msg('적어도 한개의 항목에 체크해야 합니다.', oFrm.query);
    // 	return false;
    // } else {
    // 	return true;
    // }
    return true;
}


function submitenter(myfield,e)
{
    var keycode;
    if (window.event) keycode = window.event.keyCode;
    else if (e) keycode = e.which;
    else return true;

    if (keycode == 13)
    {
	search_submit($("#search_area"));
	return false;
    }
    else
	return true;
}


function search_submit(oForm) {
    if ($("#name-check").hasClass('name-check')) $("#name-checkbox").attr("checked", "checked");
    if ($("#subject-check").hasClass('subject-check')) $("#subject-checkbox").attr("checked", "checked");
    if ($("#content-check").hasClass('content-check'))  $("#content-checkbox").attr("checked", "checked");

    $(oForm).submit();
}

$(document).ready( function() {
	//var oFrmvalidator = new Validator("search_area_form");
	//oFrmvalidator.setAddnlValidationFunction("searchCheckBoxValidation");
	//    oFrmvalidator.addValidation("query", "req", "내용을 입력해주세요.");
	//    oFrmvalidator.searchCheckBoxValidation;
    $("#name-check, #name-check-label").click( function(obj) {
	var sCheckboxId = 'name-checkbox';
	var oCheckboxElement = document.getElementById(sCheckboxId);
	if ($("#name-check").hasClass('name-check')) {
	    $("#name-check").attr('src', '/site_media/images/search_name_checkbox.gif');
	    oCheckboxElement.checked = false;
	} else {
	    $("#name-check").attr('src', '/site_media/images/search_name_checkbox_selected.gif');
	    oCheckboxElement.checked = true;
	}
	$("#name-check").toggleClass("name-check");
    });

    $("#content-check,#content-check-label").click( function(obj) {
	var sCheckboxId = 'contents-checkbox';
	var oCheckboxElement = document.getElementById(sCheckboxId);
	if ($("#content-check").hasClass('content-check')) {
	    $("#content-check").attr('src', '/site_media/images/search_content_checkbox.gif');
	    oCheckboxElement.checked = false;
	} else {
	    $("#content-check").attr('src', '/site_media/images/search_content_checkbox_selected.gif');
	    oCheckboxElement.checked = true;
	}
	$("#content-check").toggleClass("content-check");
    });

    $("#subject-check,#subject-check-label").click( function(obj) {
	var sCheckboxId = 'subject-checkbox';
	var oCheckboxElement = document.getElementById(sCheckboxId);
	if ($("#subject-check").hasClass('subject-check')) {
	    $("#subject-check").attr('src', '/site_media/images/search_subject_checkbox.gif');
	    oCheckboxElement.checked = false;
	} else {
	    $("#subject-check").attr('src', '/site_media/images/search_subject_checkbox_selected.gif');
	    oCheckboxElement.checked = true;
	}
	$("#subject-check").toggleClass("subject-check");
    });

});