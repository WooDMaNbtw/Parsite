const imageInput = document.getElementById("imageInput");
const uploadedImage = document.getElementById("uploadedImage");

imageInput.addEventListener("change", function (event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = "block"; // Отображаем изображение
        };

        reader.readAsDataURL(file);
    }
});