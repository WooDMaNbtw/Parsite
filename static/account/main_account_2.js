//const popularDomainZones = [
//  ".com",
//  ".org",
//  ".net",
//  ".gov",
//  ".edu",
//  ".mil",
//  ".io",
//  ".co",
//  ".uk",
//  ".de",
//  ".jp",
//  ".ru",
//  ".fr",
//  ".ca",
//  ".au",
//  ".br",
//  ".cn",
//  ".es",
//  ".in",
//  ".it",
//];
//
//
//function check_submit_form() {
//    alert("ddsada")
//    let email = document.querySelector("#email").value;
//    let warning = document.querySelector("#warning");
//    let count = 0;
//
//    for (let el = 0; el < popularDomainZones.length; el++){
//        if (email.includes(popularDomainZones[el])) {
//            count++;
//        }
//    }
//
//    if (!email.includes("@") || !Boolean(count)) {
//        warning.textContent = "Email: Incorrect email address, please try again";
//        warning.style.color = "red";
//        warning.style.transition = "0.6s";
//        return false
//    }
//    else {
//        warning.textContent = "Email:";
//        warning.style.color = "#333";
//        warning.style.transition = "0.6s";
//    }