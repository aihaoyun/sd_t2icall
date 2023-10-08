setTimeout(function() {
    const t2icall = document.getElementById("tab_t2icall");
    const t2icall_div = document.createElement("div");
    t2icall_div.style = "height:700px";
    t2icall_div.innerHTML = '<iframe id="t2icallIframe" name="Frame" src="/t2icall/easy_ui.html" style="width: 100%; height: 100%;"></iframe>';
    t2icall.appendChild(t2icall_div);
},1000*25);
