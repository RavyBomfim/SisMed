"""from datetime import datetime, timedelta

class AgendaMedico:
    def __init__(self, medico, periodo_inicial, periodo_final):
        self.medico = medico
        self.periodo_inicial = periodo_inicial
        self.periodo_final = periodo_final
        self.agenda = []

    def gerar_agenda(self):
        intervalo_de_tempo = timedelta(minutes=30)  # Intervalo de 30 minutos.
        data_atual = self.periodo_inicial

        while data_atual <= self.periodo_final:
            dia_semana = data_atual.weekday() + 1

            horarios_atendimento = HorarioMedico.objects.filter(
                medico=self.medico,
                dia_semana=dia_semana
            ).first()

            if horarios_atendimento:
                if horarios_atendimento.horario_inicio_manha:
                    horario_atual_manha = datetime(
                        data_atual.year, data_atual.month, data_atual.day,
                        horarios_atendimento.horario_inicio_manha.hour, horarios_atendimento.horario_inicio_manha.minute
                    )

                    while horario_atual_manha.time() < horarios_atendimento.horario_fim_manha:
                        # Crie um registro na model HorarioAgenda para este horário com disponível como True.
                        horario_agenda = HorarioAgenda(
                            medico=self.medico,
                            data=data_atual.date(),
                            horario=horario_atual_manha.time(),
                            disponivel=True
                        )
                        horario_agenda.save()
                        horario_atual_manha += intervalo_de_tempo

                if horarios_atendimento.horario_inicio_tarde:
                    horario_atual_tarde = datetime(
                        data_atual.year, data_atual.month, data_atual.day,
                        horarios_atendimento.horario_inicio_tarde.hour, horarios_atendimento.horario_inicio_tarde.minute
                    )

                    while horario_atual_tarde.time() < horarios_atendimento.horario_fim_tarde:
                        # Crie um registro na model HorarioAgenda para este horário com disponível como True.
                        horario_agenda = HorarioAgenda(
                            medico=self.medico,
                            data=data_atual.date(),
                            horario=horario_atual_tarde.time(),
                            disponivel=True
                        )
                        horario_agenda.save()
                        horario_atual_tarde += intervalo_de_tempo

            data_atual += timedelta(days=1)  # Avança para a próxima data.
"""