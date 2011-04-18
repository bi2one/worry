var playing = false;

/*
preload_image_object = new Image();

image_url = new Array();
image_url[0] = "http://mydomain.com/image0.gif";
image_url[1] = "http://mydomain.com/image1.gif";
image_url[2] = "http://mydomain.com/image2.gif";
image_url[3] = "http://mydomain.com/image3.gif";

var i = 0;
for(i=0; i<=3; i++) 
    preload_image_object.src = image_url[i];
*/  

function getYTPlayer() {
    var obj = parent.top.document.getElementById('yt-player');
    if (obj == null)
	if (typeof (top.frames[0]) != "undefined")
	    obj = top.frames[0].document.getElementById('yt-player');
	else
	    obj = null;
    return obj;
}

function getPlayerState() {
	player = getYTPlayer();
	if (player == null)
	    return 0;
	state = player.getPlayerState();
	$("#playerState").attr('value', state);
	return state;
}

function setPlayerButton() {
    if (getPlayerState() == 1) {
	$('#music-on-off').css('background-image', 'url("/site_media/images/music_off_btn.png")');    
    } else {
	$('#music-on-off').css('background-image', 'url("/site_media/images/music_on_btn.png")');    
    }
}

function musicButtonOnOff(state) {
    if (state == 'off')
	$('#music-on-off').css('background-image', 'url("/site_media/images/music_off_btn.png")');
    else 
	$('#music-on-off').css('background-image', 'url("/site_media/images/music_on_btn.png")');
}

function moveToPage(page) {
    if (page == "main" )
	window.location.href='/intro/';
}

function musicToggle() {
    var ytplayer = getYTPlayer();
    if (playing) {
	ytplayer.stopVideo();
	musicButtonOnOff('on');
    } else {
	ytplayer.playVideo();
	musicButtonOnOff('off');
    }
    playing = !playing;
}


function title_focus(obj) {
    var title = $(obj).attr('title');
    var text = $(obj).attr('value');
    if (title == text) {
	$(obj).attr('value', '');
    }
}


function tag_click(obj) {
    var title = $(obj).attr('title');
    var text = $(obj).attr('value');
    if (title == text) {
	$(obj).attr('value', '');
    }
}

function moveWithConfirm(message, url) {
     var answer = confirm(message);
         if (answer){
           window.location.href = url;
        }
}