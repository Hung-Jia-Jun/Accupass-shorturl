function getBaseURL()
{
	BaseURL = window.location.href;
	BaseURL = BaseURL.split("/")[2];
	console.log(BaseURL);
	return BaseURL
}
function getTextValue() {
	userTypeUrl = (document.getElementById("url").value);
	
	$.get("/UserShortUrl",
		{url : userTypeUrl},
		function(data) {
			if (data=="URL錯誤，請輸入正確的網址")
			{
				document.getElementById("response").innerText = data;
			}
			else
			{
				BaseURL = getBaseURL()
				completeURL = BaseURL + "/" + data
				document.getElementById("response").innerText = completeURL;
				$("#response").attr("href",data); 
			}
		}
	);
}
$(document).ready(function(){
	document.getElementById("confirm").addEventListener("click", getTextValue);
});