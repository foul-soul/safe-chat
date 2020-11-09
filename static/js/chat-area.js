var height = 0;
$('chat-box').each(function(i, value){
    height += parseInt($(this).height());
});

height += '';

$('chat-box').animate({scrollTop: height});