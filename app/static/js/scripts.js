document.addEventListener("DOMContentLoaded", function () {

    const loader = document.getElementById("loader");
    const form = document.getElementById("form");
    const table = document.getElementById("table");
    const result = document.getElementById("result");
    const alert = document.getElementById("alert");

    const productName = document.getElementById("productName");
    const facebook_chk = document.getElementById("fchk");
    const twitter_chk = document.getElementById("tchk");
    const amazon_chk = document.getElementById("achk");

    document.getElementById("scrapeBtn").addEventListener('click', function () {

        if (productName.value === '') {
            addAlert("Please fill product name field :(", "alert-danger");
            return;
        }
        if (!facebook_chk.checked && !twitter_chk.checked && !amazon_chk.checked) {
            addAlert("Please select at least one source to scrape :(", "alert-warning");
            return;
        }

        alert.innerHTML = '';

        form.hidden = true;
        loader.hidden = false;
        table.hidden = true;

        const request = new XMLHttpRequest();
        request.open('POST', '/test/result');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            result.innerHTML = ' ';
            for (var i = 0; i < data.length; i++) {
                var row = document.createElement('tr');
                var cell1 = document.createElement('td');
                var cell2 = document.createElement('td');
                var cell3 = document.createElement('td');
                cell1.innerHTML = (i + 1);
                cell2.innerHTML = data[i].text;
                cell3.innerHTML = '<span class="badge badge-primary badge-pill">' + data[i].source + '</span>';
                row.appendChild(cell1);
                row.appendChild(cell2);
                row.appendChild(cell3);
                result.appendChild(row);
            }
            form.hidden = false;
            loader.hidden = true;
            table.hidden = false;
        };

        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status != 200) {
                form.hidden = false;
                loader.hidden = true;
                addAlert(`Error: ${this.statusText} :(`, "alert-danger");
            }
          };

        const data = new FormData();
        data.append("productName", productName.value)
        if (facebook_chk.checked)
            data.append("facebookCheck", "on");
        if (twitter_chk.checked)
            data.append("twitterCheck", "on");
        if (amazon_chk.checked)
            data.append("amazonCheck", "on");
        request.send(data);

    });


    function addAlert(msg, type) {
        var div = document.createElement("div");
        var btn = document.createElement("button");
        var span = document.createElement("span");
        
        div.className = "alert alert-dismissible fade show "
        div.className += type;
        div.setAttribute("role","alert");
        btn.className = "close";
        btn.setAttribute("data-dismiss", "alert");
        btn.setAttribute("aria-label", "close");
        btn.setAttribute("type", "button");
        span.setAttribute("arie-hidden", true);
        div.innerHTML = msg;
        span.innerHTML = "&times;";

        btn.appendChild(span);
        div.appendChild(btn);
        alert.appendChild(div);
    };


});