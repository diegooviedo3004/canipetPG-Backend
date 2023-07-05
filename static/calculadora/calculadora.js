$(document).ready(function() {
    var alert_input = document.querySelector("#alert-input");
    $('#inputGroupSelect02').prop('disabled', 'disabled');
    $('#inputGroupSelect03').prop('disabled', 'disabled');
    // var select = document.getElementById('inputGroupSelect02');
    // let seleccion1 =select.addEventListener('change', () => {
    //     console.log(select.value)

    // });
    function CalcularBARF(input1, NivelDeActividad) {
      
        let result = input1 / 100;
        result = result * parseFloat(NivelDeActividad);
        result = result * 1000;
        console.log(result.toFixed(2));
        document.getElementById("input-result").value = result.toFixed(2) + " g/dia";

    }


    $("#inputGroupSelect01").change(function() {
        if($("#inputGroupSelect01").val() == "0"){
            $('#inputGroupSelect02').prop('disabled', 'disabled');
            $('#inputGroupSelect03').prop('disabled', 'disabled');
          }
        if($("#inputGroupSelect01").val() == "1"){
          $('#inputGroupSelect02').prop('disabled', 'disabled');
          $('#inputGroupSelect03').prop('disabled', false);
        }
        if($("#inputGroupSelect01").val() == "2"){
          $('#inputGroupSelect03').prop('disabled', 'disabled');
          $('#inputGroupSelect02').prop('disabled', false);
        }
      });
      
    
    $("#calcular").bind( "click", () => {
        let input1 = document.querySelector("#input-kg").value
       if ($("#input-kg").val() == "") {
            alert_input.style.display = "block"
       }
       else {
            alert_input.style.display = "none";
            if ( document.getElementById('inputGroupSelect01').value == "1") {
                var NivelDeActividad =  document.getElementById('inputGroupSelect03').value;
                CalcularBARF(input1, NivelDeActividad);
            }

            else if ( document.getElementById('inputGroupSelect01').value == "2") {
                var NivelDeActividad =  document.getElementById('inputGroupSelect02').value;
                CalcularBARF(input1, NivelDeActividad);

            }
        }
    });
});


