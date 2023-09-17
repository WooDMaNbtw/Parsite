//function updateTime() {
//            // Создаем объект Date для получения текущего времени
//            var currentTime = new Date();
//
//            // Получаем часы, минуты и секунды
//            var hours = currentTime.getHours();
//            var minutes = currentTime.getMinutes();
//            var seconds = currentTime.getSeconds();
//
//            // Форматируем время в строку в формате HH:MM:SS
//            var timeString = hours + ':' + minutes + ':' + seconds;
//
//            // Получаем элемент div с id="time" и обновляем его содержимое
//            document.getElementById('time').innerHTML = timeString;
//        }
//
//        // Обновляем время каждую секунду, вызывая функцию updateTime
//        setInterval(updateTime, 1000);
//
//        // Вызываем функцию updateTime сразу после загрузки страницы
//        updateTime();





const login_open = document.querySelector("#open-login").addEventListener("click", OpenLogin);
const login_close = document.getElementById("close-login").addEventListener("click", CloseLogin);

function OpenLogin(err){
  err.preventDefault()
  let option = document.getElementById("popup-bg")
  option.style.opacity = "1";
  option.style.visibility = "visible";
  option.style.transition = "0.6s"
}

function CloseLogin(){
  let option = document.getElementById("popup-bg")
  option.style.opacity = "0";
  option.style.visibility = "hidden";
  option.style.transition = "0.6s"
};
