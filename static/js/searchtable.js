document.addEventListener("readystatechange", (event) => {
    if (event.target.readyState === "complete") {
      myFunction5();
    }
    });
    $(document).ready(function(){
      $("#SBar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#Tbl_1 tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
    }); 
  