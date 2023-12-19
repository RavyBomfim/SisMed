// static/js/usuario_form.js
$(document).ready(function () {
    const tipoUsuarioField = $('#id_tipo_usuario');
    const usuarioAssociadoField = $('#id_usuario_associado');

    function updateUsuarioAssociadoOptions() {
        const selectedTipoUsuario = tipoUsuarioField.val();
        usuarioAssociadoField.html('<option value="">Associar cadastro</option>');

        if (selectedTipoUsuario === 'medico') {
            // Carregar opções para médicos
            const medicos = JSON.parse('{{ medicos_json|escapejs }}');
            $.each(medicos, function (index, medico) {
                usuarioAssociadoField.append($('<option>', {
                    value: medico.id,
                    text: medico.nome_completo
                }));
            });
        } else if (selectedTipoUsuario === 'funcionario') {
            // Carregar opções para funcionários
            const funcionarios = JSON.parse('{{ funcionarios_json|escapejs }}');
            $.each(funcionarios, function (index, funcionario) {
                usuarioAssociadoField.append($('<option>', {
                    value: funcionario.id,
                    text: funcionario.nome_completo
                }));
            });
        }
    }

    tipoUsuarioField.change(updateUsuarioAssociadoOptions);

    // Chamar a função uma vez para configurar as opções iniciais
    updateUsuarioAssociadoOptions();
});
