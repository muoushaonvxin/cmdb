/**
 * Created by Selience on 2017/12/15.
 */


/**
 * 去除字符串当中的所有空格
 */

window.onload = function(){
    getUserFriend();

    /*
    // 定时接受消息
    var msgrefrasher = setInterval(function(){
        GetNewMsgs();
    }, 3000);
    */

    GetNewMsgs();

    // send msg
    $('body').delegate("textarea", "keydown", function(e){
        if(e.which == 13){
            var msg_text = $("textarea").val();
            if($.trim(msg_text).length > 0){
                console.log(msg_text);
                SendMsg(msg_text);
            }
            AddSendMsgIntoBox(msg_text);
            $("textarea").val('');
        }
    });

};


function trim(str){
    return str.replace(/(^\s+)|(\s+$)/g, "");
}


/**
 * 获取当前用户的好友
 */
function getUserFriend(){
    // 获取当前的用户
    var user = document.getElementById("friend").textContent;
    var current_user = trim(user);

    var url = "/webchat/logic/friend/";
    var data = {'email': current_user};
    var xmlHttp;
    if(window.ActiveXObject){
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }else{
        xmlHttp = new XMLHttpRequest();
    }
    xmlHttp.open("post", url);
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlHttp.send(JSON.stringify(data));
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                console.log(xmlHttp.responseText);

                /**
                 * 创建一个新的div标签并把原来的内容清空
                 */
                var content = JSON.parse(xmlHttp.responseText);
                document.getElementById("content").innerHTML = "";
                document.getElementById("content").innerHTML = '<div class="black-box1-content">' + '</div>';

                /**
                 * 自动创建当前的好友
                 */
                for(var i in content.friend){
                    var parents_node = document.getElementsByClassName("black-box1-content")[0];
                    var child_node1 = document.createElement('div');
                    var child_node2 = document.createElement('br');
                    parents_node.appendChild(child_node1);
                    child_node1.className = 'current-message-person';
                    child_node1.setAttribute("contact-id", i);
                    child_node1.setAttribute("contact-type", "single");
                    child_node1.innerHTML = '<span class="current-friend">' + content.friend[i] + '</span>' +
                                            '<span class="current-message">' + "14" + '</span>';
                    parents_node.appendChild(child_node2);
                }

                /**
                 * 设置点击事件自动获取当前好友的id和类型
                 */
                var current_person_friend = document.getElementsByClassName('current-message-person');
                for(var i in current_person_friend){
                    current_person_friend[i].onclick = function(){
                        var chat_title = document.getElementsByClassName('title-set')[0];
                        var title = "正在跟" + this.childNodes[0].innerText + "聊天";
                        chat_title.innerText = title;
                        chat_title.setAttribute("contact-id", this.getAttribute("contact-id"));
                        chat_title.setAttribute("contact-type", this.getAttribute("contact-type"));
                    };
                }
            }
        }
    }
}


/**
 * 给用户发送消息
 */
function SendMsg(msg_text){
    var chat_title = document.getElementsByClassName('title-set')[0];
    var contact_type = chat_title.getAttribute("contact-type");
    var contact_id = chat_title.getAttribute("contact-id");
    if(contact_type && contact_id){
        var url = "/webchat/logic/msghandler/";
        var data = {
            'from': trim(document.getElementById("id").textContent),
            'to': trim(contact_id),
            'type': trim(contact_type),
            'msg': trim(msg_text)
        };
        // 向后台发送消息
        var xmlHttp;
        if(window.ActiveXObject){
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        }else{
            xmlHttp = new XMLHttpRequest();
        }
        xmlHttp.open("post", url);
        xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xmlHttp.send(JSON.stringify(data));
        xmlHttp.onreadystatechange = function(){
            if(xmlHttp.readyState == 4) {
                if (xmlHttp.status == 200) {
                    console.log(xmlHttp.responseText);
                }
            }
        }
    }
}


/**
 *
 * @param msg_text
 * 添加消息到聊天页面
 */
function AddSendMsgIntoBox(msg_text){
    var username = document.getElementById("username").textContent;
    var new_msg_ele = '<div class="msg_item">' +
                           '<span>' + username + '</span>' +
                           '<span>' + new Date().toLocaleTimeString() + '</span>' +
                           '<div class="msg-text">' + msg_text + '</div>' +
                      '</div>';
    $('.dialog-set').append(new_msg_ele);

    // 让滚动条自动进行滚动
    $('.dialog-set').animate({
        scrollTop: $('.dialog-set')[0].scrollHeight
    }, 500);

}


/**
 * 获取新的消息
 */
function GetNewMsgs(){
    var url = "/webchat/logic/getnewmsgs/";
    var xmlHttp;
    if(window.ActiveXObject){
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }else{
        xmlHttp = new XMLHttpRequest();
    }
    xmlHttp.open("get", url);
    xmlHttp.send(null);
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                console.log(xmlHttp.responseText);
                return GetNewMsgs();
            }
        }
    }
}