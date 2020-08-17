document.addEventListener("DOMContentLoaded", function () {

    var url_string = window.location.href;
    var url = new URL(url_string);
    var link = url.searchParams.get("link");
    console.log(link);

    url = "/api/v1/episode?link=" + link

    var container = document.getElementById("all");
    const request = new XMLHttpRequest();
    request.open('GET', url);
    request.onload = () => {
        const data = JSON.parse(request.responseText);

        const video = document.createElement("video");
        video.className = "video-js vjs-default-skin vjs-big-play-centered embed-responsive-item";
        video.controls = "true";

        const src_720 = document.createElement("source");
        src_720.src = data["720p"];
        
        const src_480 = document.createElement("source");
        src_480.src = data["480p"];
        

        video.append(src_720);
        video.append(src_480);


        container.append(video);
    };
    request.send();


});