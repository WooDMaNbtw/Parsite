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