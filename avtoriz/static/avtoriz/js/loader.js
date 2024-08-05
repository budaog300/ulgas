function showLoader() {
        // Показать лоадер
        var loader = document.getElementById("loader");
        loader.innerHTML = "<h1 style='margin-top:10%;color:white;'>Идет обновление данных, пожалуйста, подождите</h1>";
        loader.style.display = "block";

        // Скрыть лоадер через 10 секунд
        setTimeout(function() {
            document.getElementById("loader").style.display = "none";
            document.getElementById("logo").click();
        }, 10000);
    }