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
			if (data.message=="URL錯誤，請輸入正確的網址")
			{
				document.getElementById("response").innerText = data.message;
			}
			else
			{
				BaseURL = getBaseURL()
				completeURL = BaseURL + "/" + data.url
				document.getElementById("response").innerText = completeURL;
				$("#response").attr("href",data.url); 
				$("#previewImg").attr("src",data.image); 
				document.getElementById("paragraph").innerText = data.paragraph;
			}
		}
	);
}
$(document).ready(function(){
	document.getElementById("confirm").addEventListener("click", getTextValue);
});