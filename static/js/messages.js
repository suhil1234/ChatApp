let input_message = $('#input-message')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()
let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()
        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id,
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    let sender_img = data['sender_img']
    let reciver_img = data['reciver_img']
    let count = data['count']
    let date = data['date_str']
    let time = data['time_str']
    newMessage(message, sent_by_id, thread_id,sender_img,reciver_img,date,time)
    updateMessageCount(count,thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


function newMessage(message, sent_by_id, thread_id,sender_img,reciver_img,date,time) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
	    message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send">${date}, ${time}</span>
				</div>
				<div class="img_cont_msg">
					<img src=${sender_img} class="rounded-circle user_img_msg">
				</div>
			</div>
	    `
    }
	else{
	    message_element = `
           <div class="d-flex mb-4 received">
              <div class="img_cont_msg">
                 <img src=${reciver_img} class="rounded-circle user_img_msg">
              </div>
              <div class="msg_cotainer">
                 ${message}
              <span class="msg_time">${date}, ${time}</span>
              </div>
           </div>
        `

    }
    let message_body = $('.messages-wrapper[chat-id="' + chat_id +'"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);

}



$('.contact-li').click(function() {
    // Remove active class from previously active list item
    $('.contact-li.active').removeClass('active');
    
    // Add active class to the clicked list item
    $(this).addClass('active');

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

    console.log(chat_id)

})

function updateMessageCount(count,thread_id) {
    $('.message-count#'+thread_id).text(count + ' messages');
        }

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}