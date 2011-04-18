function id_check_submit() {
    var query = $("#id_username").val();
    $.ajax({
	type: 'POST',
	url: "/check_username/",
	data: { username: query },
	success:
	function(result){
	    id_check_result(result)
	}
    });
}

function id_check_result(result) {
    $("#id-check-result").html(result);
}

/* join validation */
function passwordConfirmValidation()
{
    var frm = document.forms["join_form"];
    if(frm.password.value != frm.password_confirm.value)
    {
	sfm_show_error_msg('비밀번호가 일치하지 않습니다.',frm.password);
	return false;
    }
    else
    {
	return true;
    }
}

window.onload = function() {
    var oFrmvalidator = new Validator("join_form");
    oFrmvalidator.setAddnlValidationFunction("passwordConfirmValidation");
    
    oFrmvalidator.addValidation("username", "req", "아이디를 입력해주세요.");
    oFrmvalidator.addValidation("username", "regexp=^[a-zA-Z][a-zA-Z0-9]*$", "부적절한 아이디 입니다.");
    
    oFrmvalidator.addValidation("password", "req", "비밀번호를 입력해주세요.");
    oFrmvalidator.passwordConfirmValidation;
    
    oFrmvalidator.addValidation("nick_name", "req", "닉네임을 입력해주세요.");
    oFrmvalidator.addValidation("email", "req", "이메일 주소를 입력해주세요.");
    oFrmvalidator.addValidation("email", "email", "올바른 이메일 주소를 입력해주세요.");
}