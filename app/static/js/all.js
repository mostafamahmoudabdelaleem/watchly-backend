document.addEventListener("DOMContentLoaded", function () {

    var container = document.getElementById("all");
    const request = new XMLHttpRequest();
    request.open('GET', '/api/v1/all_series');
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        console.log(data);
        for (var i = 0; i < data.length; i += 1) {

            const div = document.createElement("div");
            div.className = "col-sm-3";

            const a = document.createElement('a');
            a.className = "thumbnail fg-orange";
            a.href = "series?link=" + (data[i].link);

            const img = document.createElement('img');
            img.src = data[i].img_link;
            img.alt = data[i].name;

            const h = document.createElement("h3");
            h.innerHTML = data[i].name;

            //a.append(img);
            a.append(h);
            div.append(a);
    

            container.append(div);
        }
    };
    request.send();

});