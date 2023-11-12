$(document).ready(function() {

    const horario_select = $('#id_horario');
    var medicos_iniciais = $('#id_medico').html();
    var medico_select = $('#id_medico');
    var procedimento_select = $('#id_procedimento');
    var tipo_agendamento = $('#id_tipo_agendamneto');
    var procedimento = '';
    var valor_procedimento = 0.0;
    var valor_agendamento = $('#id_valor');

    console.log(procedimento);
    $('.select').find("option:first").prop("disabled", true);
    $('.select').formSelect();

    horario_select.append('<option value="" selected disabled>Horário</option>');
    if (type_view === 'UpdateView') {
        horario_select.append($("<option>", {value: horario_inicial, text: horario_inicial, selected:true}));
        tipo_agendamento = $('input[name="tipo_agendamento"]:checked').val();
        if (tipo_agendamento === 'Procedimento') {
            $('#retorno_select').css('display', 'none');
            $('#procedimento_select').css('display', 'block');
            procedimento_select.val(procedimento_id);
            procedimento_select.formSelect();
        } else {
            $('#procedimento_select').css('display', 'none');
            $('#retorno_select').css('display', 'block');
        }
    }
    horario_select.formSelect();

    $('.radio-label').change(function() {
        var valor_radio = $('input[name="tipo_agendamento"]:checked').val();

        if (valor_radio === 'Procedimento') {
            $('#procedimento_select').css('display', 'block');
            $('#retorno_select').css('display', 'none');
            $("#id_procedimento").val("");
            //
            medico_select.empty();
            medico_select.append('<option value="" selected disabled>Selecionar Médico/Especialidade</option>');
            medico_select.formSelect();
        } else {
            $('#procedimento_select').css('display', 'none');
            $('#retorno_select').css('display', 'block');
            $("#id_procedimento").val("");
            $("#id_procedimento").formSelect();
            //
            medico_select.append('<option value="" selected disabled>Selecionar Médico/Especialidade</option>');
            medico_select.html(medicos_iniciais)
            medico_select.formSelect();

        }

        valor = valor_agendamento.val();
        if(valor) {
            valor_agendamento.val('');
        }

    });


    $('#id_procedimento').on('change', function() {
        procedimento = $(this).val();
        medico_select.empty();
        medico_select.append('<option value="" selected disabled>Selecionar Médico/Especialidade</option>');
        medico_select.formSelect();

        if (procedimento) {
          $.ajax({
                url: '/medico_responsavel/' + procedimento + '/',
                success: function(data) {
                    for (var i = 0; i < data.medicos.length; i++) {
                        var option = $('<option>', {
                            value: data.medicos[i].id,
                            text: data.medicos[i].nome_completo + ' - ' + data.medicos[i].especialidade
                        });
                        $('#id_medico').append(option);
                    }
                    $('#id_medico').formSelect();
                    valor_procedimento = data.valor_procedimento
                    valor_agendamento.val(valor_procedimento);
                    valor_agendamento.focus(); valor_agendamento.blur();
                },
                error: function() {
                    console.log('Erro ao obter médicos associados ao procedimento.');
                }
            });
        }
    });

    $('#id_medico, #id_data').change(function () {

        var medico_id = $('#id_medico').val();
        var data_agend = $('#id_data').val();
        horario_select.empty();
        horario_select.append('<option value="" selected disabled>Horário</option>');

        console.log('Data agend: ' + data_agend);

        var dataSelecionada = new Date(data_agend);
        var dataAtual = new Date();

        if (dataSelecionada + 1 < dataAtual) {
            $('#erro-data').css('display', 'block');
            horario_select.empty();
            horario_select.append('<option value="" selected disabled>Horário</option>');
            horario_select.formSelect();
        } else {
            $('#erro-data').css('display', 'none');
            if (medico_id && data_agend) {
                var csrfToken = $("[name=csrfmiddlewaretoken]").val();
                // Solicitação AJAX para obter os horários disponíveis
                var dados = {
                    medico_id: medico_id,
                    data_agend: data_agend,
                }

                $.ajax({
                    url: '/retornar-horarios',
                    method: 'POST',
                    data: JSON.stringify(dados),
                    contentType: 'application/json',
                    dataType: 'json',
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    success: function (data) {
                        console.log('Dado recebido: ', data.horarios_disponiveis);
                        if (data.horarios_disponiveis.length === 0) {                     
                            horario_select.append($("<option>", {
                                value: '',
                                text: data.aviso
                            }));
                        } else {
                            $.each(data.horarios_disponiveis, function(index, horario) {
                                horario_select.append($("<option>", {
                                    value: horario,
                                    text: horario
                                }));
                            });
                        }
                        horario_select.formSelect();
                        dados_horariosJson = data;
                    },
                    error: function (xhr, status, error) {
                        console.log('Erro na requisição AJAX:', status);
                        console.log('Erro: ', error);
                        // Verifique a resposta completa para obter mais detalhes, se disponível
                        console.log('Resposta completa:', xhr.responseText);
                    }
                });
            };
        }
    });

    $('#id_medico, #id_retorno, #procedimento_select').change(function () {
        var valor_radio = $('input[name="tipo_agendamento"]:checked').val();
        console.log(valor_radio);
        var medico_id = $('#id_medico').val();
        var retorno = $('#id_retorno').val();

        if (valor_radio === 'Consulta') {
            if (retorno == 'True') {
                valor_agendamento.val('0.00');
                valor_agendamento.focus(); valor_agendamento.blur();
            } else if (medico_id && retorno) {
                var csrfToken = $("[name=csrfmiddlewaretoken]").val();
                var dados = {
                    medico_id: medico_id,
                }
                $.ajax({
                    url: '/valor-consulta',
                    method: 'POST',
                    data: JSON.stringify(dados),
                    contentType: 'application/json',
                    dataType: 'json',
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    success: function (data) {
                        valor_agendamento.val(data.valor_consulta);
                        valor_agendamento.focus(); valor_agendamento.blur();
                    },
                    error: function (xhr, status, error) {
                        console.log('Erro na requisição AJAX:', status);
                        console.log('Erro: ', error);
                        // Verifique a resposta completa para obter mais detalhes, se disponível
                        console.log('Resposta completa:', xhr.responseText);
                    }
                });
            } else {
                valor_agendamento.val('');
            }
        }
    });

});