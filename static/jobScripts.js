$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var xp13_received = [];
    var xp251_received = [];
    var wp01_received = [];
    var jm01_received = [];
    
    var cmc401_received = [];
    var cmc402_received = [];
    var cmcevo1_received = [];
    var cmcevo2_received = [];
    var cmceasy_received = [];
    var cmc250_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        if (msg.XP13){
            xp13_received.push(msg.XP13);
        }
        if (msg.XP251){
            xp251_received.push(msg.XP251);
        }
        if (msg.WP01){
            wp01_received.push(msg.WP01);
        }
        if (msg.JM01){
            jm01_received.push(msg.JM01);
        }
        
        if (msg.CMC401){
            cmc401_received.push(msg.CMC401);
        }
        if (msg.CMC402){
            cmc402_received.push(msg.CMC402);
        }
        if (msg.CMCEVO1){
            cmcevo1_received.push(msg.CMCEVO1);
        }
        if (msg.CMCEVO2){
            cmcevo2_received.push(msg.CMCEVO2);
        }
        if (msg.CMCEASY){
            cmceasy_received.push(msg.CMCEASY);
        }
        if (msg.CMC250){
            cmc250_received.push(msg.CMC250);
        }
        
        
        var numbers_string = '<tr><td>XP13B</td><td>XP251</td><td>WP01</td><td>JM01</td><td>CMC401</td><td>CMC402</td><td>CMC EVO 1</td><td>CMC EVO 2</td><td>CMC Easy</td><td>CMC 250</td></tr>'
        for (var i = 0; i < Math.max(xp13_received.length,xp251_received.length,wp01_received.length,jm01_received.length); i++){
            numbers_string += '<tr>';
            if(typeof xp13_received[i] !== "undefined"){
                numbers_string += '<td>' + xp13_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof xp251_received[i] !== "undefined"){
                numbers_string += '<td>' + xp251_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof wp01_received[i] !== "undefined"){
                numbers_string += '<td>' + wp01_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof jm01_received[i] !== "undefined"){
                numbers_string += '<td>' + jm01_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            
            if(typeof cmc401_received[i] !== "undefined"){
                numbers_string += '<td>' + cmc401_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof cmc402_received[i] !== "undefined"){
                numbers_string += '<td>' + cmc402_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof cmcevo1_received[i] !== "undefined"){
                numbers_string += '<td>' + cmcevo1_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof cmcevo2_received[i] !== "undefined"){
                numbers_string += '<td>' + cmcevo2_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof cmceasy_received[i] !== "undefined"){
                numbers_string += '<td>' + cmceasy_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            if(typeof cmc250_received[i] !== "undefined"){
                numbers_string += '<td>' + cmc250_received[i].toString() + '</td>';
            }
            else{
                numbers_string += '<td></td>'
            }
            numbers_string += '</tr>';
        }
        $('#log').html(numbers_string);
    });
    socket.on('jobs', function(jobg){
        var jobstring = ''
        $.each(jobg.jobgrouping, function(key1,value1){
            jobstring+= '<p>'+ key1 + ': '+value1['JobNum']+'</p>';
        });
        $('#job').html(jobstring);
    });
    socket.on('stringtest', function(msg){
        for (var i = 0; i < Math.max(xp13_received.length,xp251_received.length,wp01_received.length,jm01_received.length); i++){
            var jobstring = '';
            
        }
    });
});