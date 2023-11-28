def nome_mes(mes):
    nome_mes = ''
    if mes == 1 or mes == '1':
        nome_mes = 'Janeiro'
    elif mes == 2 or mes == '2':
        nome_mes = 'Fevereiro'
    elif mes == 3 or mes == '3':
        nome_mes = 'Março'
    elif mes == 4 or mes == '4':
        nome_mes = 'Abril'
    elif mes == 5 or mes == '5':
        nome_mes = 'Maio'
    elif mes == 6 or mes == '6':
        nome_mes = 'Junho'
    elif mes == 7 or mes == '7':
        nome_mes = 'Julho'
    elif mes == 8 or mes == '8':
        nome_mes = 'Agosto'
    elif mes == 9 or mes == '9':
        nome_mes = 'Setembro'
    elif mes == 10 or mes == '10':
        nome_mes = 'Outubro'
    elif mes == 11 or mes == '11':
        nome_mes = 'Novembro'
    elif mes == 12 or mes == '12':
        nome_mes = 'Dezembro'
    else: 
        nome_mes = 'None'

    return nome_mes