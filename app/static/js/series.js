document.addEventListener("DOMContentLoaded", function () {

    var url_string = window.location.href;
    var url = new URL(url_string);
    var link = url.searchParams.get("link");
    console.log(link);

    url = "/api/v1/series?link=" + link

    var container = document.getElementById("all");
    const request = new XMLHttpRequest();
    request.open('GET', url);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        console.log(data);
        for (var i = 0; i < data.length; i += 1) {

            const div = document.createElement("div");
            div.className = "col-sm-3";

            const a = document.createElement('a');
            a.className = "thumbnail fg-orange";
            a.href = "episode?link=" + (data[i].link);

            const img = document.createElement('img');
            img.src = data[i].thumbnail;
            img.alt = data[i].title;

            const h = document.createElement("h3");
            h.innerHTML = data[i].title;

            //a.append(img);
            a.append(h);
            div.append(a);
    

            container.append(div);
        }
    };
    request.send();


});