const popularDomainZones = [
  ".com",
  ".org",
  ".net",
  ".gov",
  ".edu",
  ".mil",
  ".io",
  ".co",
  ".uk",
  ".de",
  ".jp",
  ".ru",
  ".fr",
  ".ca",
  ".au",
  ".br",
  ".cn",
  ".es",
  ".in",
  ".it",
];

function check_submit_form() {
    let email = document.querySelector("#email").value;
    let warning = document.querySelector("#warning");
    let count = 0;

    for (let el = 0; el < popularDomainZones.length; el++){
        if (email.includes(popularDomainZones[el])) {
            count++;
        }
    }

    if (!email.includes("@") || !Boolean(count)) {
        warning.textContent = "Email: Incorrect email address, please try again";
        warning.style.color = "red";
        warning.style.transition = "0.6s";
        return false
    }
    else {
        warning.textContent = "Email:";
        warning.style.color = "#333";
        warning.style.transition = "0.6s";
    }

    let password = document.querySelector("#password");
    let confirm = document.querySelector("#confirmation");
    let pass_str = document.querySelector("#pass-str");
    let conf_str = document.querySelector("#conf-str");

    if (password.value !== confirm.value) {
        pass_str.textContent = "Does not match!";
        pass_str.style.color = "red";
        pass_str.style.transition = "0.6s";
        conf_str.textContent = "Does not match!";
        conf_str.style.color = "red";
        conf_str.style.transition = "0.6s";
        return false
    }
    else {
        pass_str.textContent = "Password:";
        conf_str.textContent = "Confirm password";
        pass_str.style.color = "#333";
        pass_str.style.transition = "0.6s";
    }
    return true

}


document.querySelector("#show-password").addEventListener("click", function() {
  let value = document.querySelector("#password");
  if (value.type === "password"){
    value.type = "text";
    document.querySelector("#show-password").classList.add("active")
  } else {
    value.type = "password";
    document.querySelector("#show-password").classList.remove("active")
  }
});


