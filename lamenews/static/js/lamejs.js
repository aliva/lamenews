function vote(url, id, value, id_prefix){
	var xmlhttp;
	if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}	
	xmlhttp.open("GET",url, false);
	xmlhttp.send();
	
	if (xmlhttp.responseText== 'done'){
		counter = document.getElementById(id_prefix + '-' + value+'-counter-'+id);
		if (counter){
			count = Math.abs(parseInt(counter.textContent))+ 1;
			if (value == 'up')
				count = '+' + count;
			else
				count = '-' + count;
			counter.textContent = count 
		}
		else{
			alert('errr');
		}
	}
	else{
		alert(xmlhttp.responseText);
	}
	return false;
}
