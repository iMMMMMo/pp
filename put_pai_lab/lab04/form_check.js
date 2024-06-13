function isWhiteSpaceOrEmpty(str) {
    return /^[\s\t\r\n]*$/.test(str);
}

function checkStringAndFocus(obj, msg) {
    let str = obj.value;
    let errorFieldName = "e_" + obj.name.substr(2, obj.name.length);
    if (isWhiteSpaceOrEmpty(str)) {
        document.getElementById(errorFieldName).innerHTML = msg;
        obj.focus();
        return false;
    } else {
        document.getElementById(errorFieldName).innerHTML = "";
        return true;
    }
}

function isEmailInvalid(str) {
    let email = /^[a-zA-Z_0-9\.]+@[a-zA-Z_0-9\.]+\.[a-zA-Z][a-zA-Z]+$/;
    return !email.test(str);
}

function validate(form) {
    if (!checkStringAndFocus(form.elements["f_imie"], "Podaj imię!")) return false;
    if (!checkStringAndFocus(form.elements["f_nazwisko"], "Podaj nazwisko!")) return false;
    if (!checkStringAndFocus(form.elements["f_kod"], "Podaj kod!")) return false;
    if (!checkStringAndFocus(form.elements["f_ulica"], "Podaj ulicę!")) return false;
    if (!checkStringAndFocus(form.elements["f_miasto"], "Podaj miasto!")) return false;
    if (isEmailInvalid(form.elements["f_email"].value)) {
        document.getElementById("e_email").innerHTML = "Podaj właściwy e-mail";
        form.elements["f_email"].focus();
        return false;
    } else {
        document.getElementById("e_email").innerHTML = "";
    }
    return true;
}

function cnt(form, msg, maxSize) {
    if (form.value.length > maxSize)
        form.value = form.value.substring(0, maxSize);
    else
        msg.innerHTML = maxSize - form.value.length;
}

function showElement(e) {
    document.getElementById(e).style.visibility = 'visible';
}

function hideElement(e) {
    document.getElementById(e).style.visibility = 'hidden';
}

function alterRows(i, e) {
    if (e) {
        if (i % 2 == 1) {
            e.setAttribute("style", "background-color: Aqua;");
        }
        e = e.nextSibling;
        while (e && e.nodeType != 1) {
            e = e.nextSibling;
        }
        alterRows(++i, e);
    }
}

function nextNode(e) {
    while (e && e.nodeType != 1) {
        e = e.nextSibling;
    }
    return e;
}

function prevNode(e) {
    while (e && e.nodeType != 1) {
        e = e.previousSibling;
    }
    return e;
}

function swapRows(b) {
    let tab = prevNode(b.previousSibling);
    let tBody = nextNode(tab.firstChild);
    let lastNode = prevNode(tBody.lastChild);
    tBody.removeChild(lastNode);
    let firstNode = nextNode(tBody.firstChild);
    tBody.insertBefore(lastNode, firstNode);
}

window.onload = function() {
    alterRows(1, document.getElementsByTagName("tbody")[0].firstChild);
}
