document.addEventListener('DOMContentLoaded', function() {
    /* initialize the calendar
     -----------------------------------------------------------------*/
     function crea_query_string() {        
        var id_centro = document.getElementById("centro_id")      
        return  encodeURIComponent(id_centro.value);
      }

      function formatear_fecha(fecha){
          //Formato YYYY-MM-DD para parsear fecha en servidor de taco
            var dia = fecha.getDate() < 10 ? ('0'+fecha.getDate().toString()):fecha.getDate().toString();
            var mes = (fecha.getMonth() + 1).toString();
            var year = fecha.getFullYear().toString(); 
            return year+'-'+mes+'-'+dia;   
      }

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right:'month,basicWeek,basicDay'
        },
		initialView: 'monthView',
        editable: true, 
        locale: 'es',       
        events: function (start, end, callback) {
            $.ajax({
                url: "/turno-ajax?",
                data: {
                    parametro_id_centro: crea_query_string(),
                    //Mandamos las fechas en isoformat(YYYY-MM-DD)
                    fecha_ini_calendario: formatear_fecha(start),
                    fecha_fin_calendario: formatear_fecha(end)               
                },
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                crossDomain:true,
               success: function (result) {
                   var turnos = [];
                   for (var i = 0; i < result.length; i++) {

                    turnos.push(
                        {
                           title: result[i].email_visitante + " " + result[i].hora_inicio.slice(10)+ " - " +result[i].hora_fin.slice(10),
                           start: result[i].hora_inicio,
                           end: result[i].hora_fin,
                           telefono: result[i].telefono_visitante,                  
                           editable: false
                       }
                       );
                   }
                   callback(turnos);                      
                },

                error: function (err) {

                    alert('No funciona!!!');
                }                    
            });
        },
        eventClick: function(calEvent, jsEvent, view) {

            var fecha = calEvent.start;
            var dia = fecha.getDate() < 10 ? '0'+fecha.getDate().toString():fecha.getDate().toString();
            var mes = (fecha.getMonth() + 1).toString();
            var year = fecha.getFullYear().toString();
            var correo = calEvent.title.substring(0,calEvent.title.indexOf(' '))

            var h = calEvent.start.getHours() < 10 ? '0' + (calEvent.start.getHours().toString()) :calEvent.start.getHours().toString();
            var m = calEvent.start.getMinutes() == 0 ? calEvent.start.getMinutes().toString() + '0': calEvent.start.getMinutes().toString();
            var h_inicio = h + ':' + m; 
            
            h = calEvent.end.getHours() < 10 ? '0' + (calEvent.end.getHours().toString()) :calEvent.end.getHours().toString();
            m = calEvent.end.getMinutes() == 0 ? calEvent.end.getMinutes().toString() + '0': calEvent.end.getMinutes().toString();
            var h_fin = h + ':' + m;

            $('#hora_inicio').val(h_inicio);
            $('#hora_fin').val(h_fin);
            $("#email").val(correo)
            $("#fecha_turno").val(year+'-'+mes+'-'+dia)
            $('#telefono').val(calEvent.telefono);
            $("#exampleModal").modal("show");                     
          },
          dayClick: function(date, allDay, jsEvent, view) {            
            var d = date.getDate() < 10 ? '0'+date.getDate().toString():date.getDate().toString();
            var m = (date.getMonth() + 1).toString();
            var y = date.getFullYear().toString();
            $("#fecha_turno").val(y+'-'+m+'-'+d)
            $("#exampleModal").modal("show");                    
          }
    });

    $("#cerrar").click(function(){
        //Borro los datos de la ventana modal
        $('#hora_inicio').val("");
        $('#hora_fin').val("");
        $("#email").val("");
        $("#fecha_turno").val("");
        $('#telefono').val("");
    });

    $("#guardar").click(function(){

        const formData = new FormData();
        formData.append('hora_inicio', $('#hora_inicio').val());
        formData.append('hora_fin',  $('#hora_fin').val());
        formData.append('fecha', $("#fecha_turno").val());
        formData.append('email_visitante', $("#email").val());
        formData.append('telefono_visitante', $('#telefono').val());

        axios.post('/api/centros/'+crea_query_string()+'/reserva', formData,{
            headers: {
                'Content-Type': 'multipart/form-data'
              }
        }).then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });;
    });
});