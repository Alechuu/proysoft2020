document.addEventListener('DOMContentLoaded', function () {
  function crea_query_string() {
    var id_centro = document.getElementById("centro_id")
    return encodeURIComponent(id_centro.value);
  }

  function formatear_fecha(fecha) {
    //Formato YYYY-MM-DD para parsear fecha en servidor de taco
    var dia = fecha.getDate() < 10 ? ('0' + fecha.getDate().toString()) : fecha.getDate().toString();
    var mes = (fecha.getMonth() + 1).toString();
    var year = fecha.getFullYear().toString();
    return year + '-' + mes + '-' + dia;
  }

  var calendarEl = document.getElementById('calendar');

  var calendar = obtenerCalendario(calendarEl);

  function obtenerCalendario(calendarEl) {
    return new FullCalendar.Calendar(calendarEl, {
      locale: 'es',
      headerToolbar: {
        start: 'prev,next today',
        center: 'title',
        end: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      slotLabelFormat: {
        hour: 'numeric',
        minute: '2-digit',
        omitZeroMinute: true,
        meridiem: 'short'
      },
      allDaySlot: false,
      navLinks: true, // can click day/week names to navigate views
      editable: true,
      dayMaxEvents: true, // allow "more" link when too many events
      nowIndicator: true,
      businessHours: [ // specify an array instead
        {
          daysOfWeek: [1, 2, 3, 4, 5], // Lunes a viernes
          startTime: '09:00', // 9am
          endTime: '18:00' // 6pm
        }
      ],
      events: function (info, successCallback, failureCallback) {
        axios.get('/api/centros/turnos_tomados', {
          params: {
            id_centro: crea_query_string(),
            //Mandamos las fechas en isoformat(YYYY-MM-DD)
            fecha_ini_calendario: formatear_fecha(info.start),
            fecha_fin_calendario: formatear_fecha(info.end)
          }
        })
          .then(function (response) {
            console.log(response);
            var turnos = [];
            var result = response.data.body.atributos;
            for (var i = 0; i < result.length; i++) {
              turnos.push(
                {
                  id_turno: result[i].id,
                  title: result[i].email_visitante,
                  start: result[i].hora_inicio,
                  end: result[i].hora_fin,
                  telefono: result[i].telefono_visitante,
                  editable: false//para evitar resize y arrastre
                }
              );
            }
            successCallback(turnos);

          })
          .catch(function (error) {
            console.log(error);
            failureCallback(error);
          })
          .then(function () {
            // always executed
          });
      },

      eventClick: function (info) {

        var fecha = info.event.start;
        var dia = fecha.getDate() < 10 ? '0' + fecha.getDate().toString() : fecha.getDate().toString();
        var mes = (fecha.getMonth() + 1).toString();
        var year = fecha.getFullYear().toString();
        var correo = info.event.title;

        var h = info.event.start.getHours() < 10 ? '0' + (info.event.start.getHours().toString()) : info.event.start.getHours().toString();
        var m = info.event.start.getMinutes() == 0 ? info.event.start.getMinutes().toString() + '0' : info.event.start.getMinutes().toString();
        var h_inicio = h + ':' + m;

        h = info.event.end.getHours() < 10 ? '0' + (info.event.end.getHours().toString()) : info.event.end.getHours().toString();
        m = info.event.end.getMinutes() == 0 ? info.event.end.getMinutes().toString() + '0' : info.event.end.getMinutes().toString();
        var h_fin = h + ':' + m;

        $('#hora_inicio').val(h_inicio);
        $('#hora_fin').val(h_fin);
        $("#email").val(correo);
        $("#fecha_turno").val(year + '-' + mes + '-' + dia);
        $('#telefono').val(info.event.extendedProps.telefono);
        $('#id_turno').val(info.event.extendedProps.id_turno);
        $("#fecha_turno").prop("disabled", true);
        //La hora de fin es informativa, se la calculo yo
        $("#hora_fin").prop("disabled", true);
        $("#hora_fin_button").prop("disabled", true);
        //no permito la edici??n ni el guardado si el evento es pasado al momento actual
        //dejo el formulario no editable y el bot??n de guardar desabilitado      
        var diaActual = new Date();
        if (fecha < diaActual) {
          $("#hora_inicio").prop("disabled", true);
          $("#hora_inicio_button").prop("disabled", true);
          $("#email").prop("disabled", true);          
          $("#telefono").prop("disabled", true);
          $("#guardar").prop("disabled", true);
          $("#borrar").hide();
        } else {
          $("#borrar").show();
        }
        $("#exampleModal").modal("show");
      },

      dateClick: function (info) {
        var d = info.date.getDate() < 10 ? '0' + info.date.getDate().toString() : info.date.getDate().toString();
        var mes = (info.date.getMonth() + 1).toString();
        var y = info.date.getFullYear().toString();


        //Si hizo click en una grilla horaria, le completo la hora de inicio y fin
        if (info.view.type == "timeGridDay" || info.view.type == "timeGridWeek") {
          //solo voy a mostrar el di??logo si est?? a partir de ahora(para que no pueda crear un turno pasado)
          var ahora = new Date();
          if (info.date > ahora) {
            var h_inicio, h_fin, m, h;
            if (info.date.getHours() > 0) {
              h = info.date.getHours() < 10 ? '0' + (info.date.getHours().toString()) : info.date.getHours().toString();
              if (info.date.getMinutes() == 0) {
                m = info.date.getMinutes().toString() + '0';
                h_inicio = h + ':' + m;
                h_fin = h + ':30';
              } else {
                //los minutos son 30. Calculo los horarios
                h_inicio = h + ':' + info.date.getMinutes().toString();
                if ((info.date.getHours() + 1) == 24) {
                  h_fin = '23:59';
                } else {
                  h = info.date.getHours() + 1;
                  h = h < 10 ? '0' + h.toString() : h.toString();
                  h_fin = h + ':00';
                }
              }
            } else {
              //son las 12 de la noche
              if (info.date.getMinutes() == 0) {
                h_inicio = "00:00";
                h_fin = "00:30";
              } else {
                h_inicio = "00:30";
                h_fin = "01:00";
              }
            }
            //Completo los horarios y deshabilito su edici??n
            $('#hora_inicio').val(h_inicio);
            $('#hora_fin').val(h_fin);
            $("#hora_inicio").prop("disabled", true);
            $("#hora_inicio_button").prop("disabled", true);
            $("#hora_fin").prop("disabled", true);
            $("#hora_fin_button").prop("disabled", true);

            //no importa sobre qu?? vista se de click, la fecha queda no editable.
            $("#fecha_turno").val(y + '-' + mes + '-' + d);
            $("#fecha_turno").prop("disabled", true);
            $("#borrar").hide();
            $("#exampleModal").modal("show");
          }
        } else {
          //hizo click en la vista de mes. Puede editar el inicio de la hora. La hora de fin
          //la calculo media hora hacia adelante seg??n regla de negocio.
          $("#hora_fin").prop("disabled", true);
          $("#hora_fin_button").prop("disabled", true);

          //no importa sobre qu?? vista se de click, la fecha queda no editable.
          $("#fecha_turno").val(y + '-' + mes + '-' + d);
          $("#fecha_turno").prop("disabled", true);
          $("#borrar").hide();
          $("#exampleModal").modal("show");
        }
      }
    });
  }

  calendar.render();

  $("#cerrar").click(cerrarVentanaTurno());

  $("#guardar").click(function () {
    //valido que los campos est??n completos
    if ($('#hora_inicio').val() == "" ||
      $('#hora_fin').val() == "" ||
      $("#fecha_turno").val() == "" ||
      $("#email").val() == "" ||
      $('#telefono').val() == "") {
      showAlertModalTurno("Debe completar todos los campos del formulario")
    } else {
      //Todos los datos completos. Listos para el post
      const formData = new FormData();
      formData.append('hora_inicio', $('#hora_inicio').val());
      formData.append('hora_fin', $('#hora_fin').val());
      formData.append('fecha', $("#fecha_turno").val());
      formData.append('email_visitante', $("#email").val());
      formData.append('telefono_visitante', $('#telefono').val());

      //pregunto por el id del turno si existe para determinar si es nuevo turno o edici??n de uno
      if ($('#id_turno').val() != '') {
        //********* EDICION DE TURNO **********/
        formData.append('id_turno', $('#id_turno').val());
        axios.post('/api/centros/' + crea_query_string() + '/modificar-reserva', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(function (response) {
          console.log(response);
          if (response.data.status == "400" || response.data.status == "500") {
            showAlertModalTurno(response.data.details)
          } else {
            showAlert(response.data.details)
            var calendarEl = document.getElementById('calendar');
            var calendar = obtenerCalendario(calendarEl);
            calendar.render();
            //Cierro y limpio la  ventana modal
            $('#exampleModal').modal('hide');
            $('#id_turno').val("");
            $('#hora_inicio').val("");
            $('#hora_fin').val("");
            $("#email").val("");
            $("#fecha_turno").val("");
            $('#telefono').val("");

            $("#hora_inicio").prop("disabled", false);
            $("#hora_inicio_button").prop("disabled", false);
            $("#hora_fin").prop("disabled", false);
            $("#hora_fin_button").prop("disabled", false);
            $("#email").prop("disabled", false);
            $("#fecha_turno").prop("disabled", false);
            $("#telefono").prop("disabled", false);
            $("#guardar").prop("disabled", false);
            $("#guardar").prop("disabled", false);
          }
        }).catch(function (error) {
          console.log(error);
        });
      } else {//********* NUEVO TURNO **********/
        axios.post('/api/centros/' + crea_query_string() + '/reserva', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(function (response) {
          console.log(response);
          if (response.data.status == "400" || response.data.status == "500") {
            showAlertModalTurno(response.data.details)
          } else {
            showAlert(response.data.details)
            var calendarEl = document.getElementById('calendar');
            var calendar = obtenerCalendario(calendarEl);
            calendar.render();
            //Cierro y limpio la  ventana modal
            $('#exampleModal').modal('hide');
            $('#id_turno').val("");
            $('#hora_inicio').val("");
            $('#hora_fin').val("");
            $("#email").val("");
            $("#fecha_turno").val("");
            $('#telefono').val("");

            $("#hora_inicio").prop("disabled", false);
            $("#hora_inicio_button").prop("disabled", false);
            $("#hora_fin").prop("disabled", false);
            $("#hora_fin_button").prop("disabled", false);
            $("#email").prop("disabled", false);
            $("#fecha_turno").prop("disabled", false);
            $("#telefono").prop("disabled", false);
            $("#guardar").prop("disabled", false);
            $("#guardar").prop("disabled", false);
          }
        }).catch(function (error) {
          console.log(error);
        });
      }
    }
  });

  $("#borrar").click(function () {
    var formData = new FormData();
    formData.append('id_turno', $('#id_turno').val());
    axios.post('/turno/borrar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRF-TOKEN': $('#csrf_token').val()
      }
    }).then(function (response) {
      console.log(response);
      showAlert(response.data)
      var calendarEl = document.getElementById('calendar');
      var calendar = obtenerCalendario(calendarEl);
      calendar.render();
      //Cierro y limpio la  ventana modal
      $('#exampleModal').modal('hide');
      $('#id_turno').val("");
      $('#hora_inicio').val("");
      $('#hora_fin').val("");
      $("#email").val("");
      $("#fecha_turno").val("");
      $('#telefono').val("");

      $("#hora_inicio").prop("disabled", false);
      $("#hora_inicio_button").prop("disabled", false);
      $("#hora_fin").prop("disabled", false);
      $("#hora_fin_button").prop("disabled", false);
      $("#email").prop("disabled", false);
      $("#fecha_turno").prop("disabled", false);
      $("#telefono").prop("disabled", false);
      $("#guardar").prop("disabled", false);
      $("#guardar").prop("disabled", false);
    })
      .catch(function (error) {
        console.log(error);
      });
  });

  //calculo y completo la hora de fin cuando ponen la hora de inicio.
  $("#hora_inicio").change(function () {
    var horaInicio = $("#hora_inicio").val();
    if (horaInicio != "") {
      //hora y minutos son enteros(necesarios para poder sumar)
      var hora = parseInt(horaInicio.substring(0, 2), 10);
      var minutos = parseInt(horaInicio.substring(3, 5), 10);

      //h y m son string que me van a formar el horario en formato hh:mm
      var h, m;

      if (hora > 0) {
        h = hora < 10 ? '0' + (hora.toString()) : hora.toString();
        if (minutos == 0) {
          h_fin = h + ':30';
        } else {
          //los minutos son 30. Calculo la hora de fin(no los minutos porque s?? que son 00)
          if ((hora + 1) == 24) {
            h_fin = '23:59';
          } else {
            h = hora + 1;
            h = h < 10 ? '0' + h.toString() : h.toString();
            h_fin = h + ':00';
          }
        }
      } else {
        //son las 12 de la noche
        if (minutos == 0) {
          h_fin = "00:30";
        } else {
          h_fin = "01:00";
        }
      }
      $("#hora_fin").val(h_fin);
    }
  });

});

function cerrarVentanaTurno() {
  return function () {
    $('#id_turno').val("");
    $('#hora_inicio').val("");
    $('#hora_fin').val("");
    $("#email").val("");
    $("#fecha_turno").val("");
    $('#telefono').val("");

    $("#hora_inicio").prop("disabled", false);
    $("#hora_inicio_button").prop("disabled", false);
    $("#hora_fin").prop("disabled", false);
    $("#hora_fin_button").prop("disabled", false);
    $("#email").prop("disabled", false);
    $("#fecha_turno").prop("disabled", false);
    $("#telefono").prop("disabled", false);
    $("#guardar").prop("disabled", false);
    $("#guardar").prop("disabled", false);
  };
}

function showAlert(mensaje) {
  // aqui dibujo el alert      
  $('#notificacion-global').html("").append(
    '<a href="#" class="close" data-hide="alert">&times;</a>'
  )
    .addClass("alert alert-success fade in")
    .append(mensaje).show();
  $("[data-hide]").on("click", function () {
    $(this).closest("." + $(this).attr("data-hide")).hide();
  });
}

function showAlertModalTurno(mensaje) {
  // aqui dibujo el alert      
  $('#bloque-notificacion').html("").append(
    '<a href="#" class="close" data-hide="alert">&times;</a>'
  )
    .addClass("alert alert-danger fade in")
    .append(mensaje).show();
  $("[data-hide]").on("click", function () {
    $(this).closest("." + $(this).attr("data-hide")).hide();
  });
}
