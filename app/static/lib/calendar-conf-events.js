document.addEventListener('DOMContentLoaded', function() {
    /* initialize the calendar
     -----------------------------------------------------------------*/
     function crea_query_string() {        
        var id_centro = document.getElementById("centro_id")      
        return "parametro_id_centro=" + encodeURIComponent(id_centro.value);
      }

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right:'month,basicWeek,basicDay'
        },
		initialView: 'timeGridWeek',
        editable: true, 
        locale: 'es',       
        events: function (start, end, callback) {
            $.ajax({
                url: "/turno-ajax?",
                data: crea_query_string(),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                crossDomain:true,
               success: function (result) {
                   var turnos = [];
                   for (var i = 0; i < result.length; i++) {

                    turnos.push({

                           title: result[i].email_visitante + " " + result[i].hora_inicio.slice(10)+ " - " +result[i].hora_fin.slice(10),
                           start: result[i].hora_inicio,
                           end: result[i].hora_fin                     

                       })
                   }
                   callback(turnos);                      
                },

                error: function (err) {

                    alert('No funciona!!!');
                }                    
            });
        },
        eventClick: function(calEvent, jsEvent, view) {

            alert('Event: ' + calEvent.title);
            alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
            alert('View: ' + view.name);
        
            // change the border color just for fun
            $(this).css('border-color', 'red');
        
          },
          dayClick: function(date, allDay, jsEvent, view) {

            if (allDay) {
              alert('Clicked on the entire day: ' + date);
            }else{
              alert('Clicked on the slot: ' + date);
            }
        
            alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
        
            alert('Current view: ' + view.name);
            
            $("#exampleModal").modal("show");
        
          }
    });
});