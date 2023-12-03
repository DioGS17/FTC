import re


def tel_validation(telefone):
    match = re.match(r'[\w+]55[\w(]\d{2}[\w)]\d{4}[\w-]\d{4}', telefone)
    if match:
        return True
    else:
        return False


def email_validation(email):
    if email[0].isdigit():
        return False
    else:
        return True


def cpf_validation(cpf):
    cpf_digits = []
    for i in cpf:
        if i.isdigit():
            i = int(i)
            cpf_digits.append(i)

    n1 = 0
    n2 = 0
    for i in range(0, 9):
        n1 = n1 + cpf_digits[i] * (9 - (i % 10))
        n2 = n2 + cpf_digits[i] * (9 - ((i + 1) % 10))

    n1 = (n1 % 11) % 10
    n2 = n2 + n1 * 9
    n2 = (n2 % 11) % 10

    if n1 == cpf_digits[10] and n2 == cpf_digits[9]:
        return True
    else:
        return False


def cnpj_validation(cnpj):
    cnpj_digits = []
    for i in cnpj:
        if i.isdigit():
            i = int(i)
            cnpj_digits.append(i)

    n1 = 5*cnpj_digits[0] + 4*cnpj_digits[1] + 3*cnpj_digits[2] + 2*cnpj_digits[3]
    n1 += 9*cnpj_digits[4] + 8*cnpj_digits[5] + 7*cnpj_digits[6] + 6*cnpj_digits[7]
    n1 += 5*cnpj_digits[8] + 4*cnpj_digits[9] + 3*cnpj_digits[10] + 2*cnpj_digits[11]
    n1 = 11 - n1 % 11
    if n1 >= 10:
        n1 = 0

    n2 = 6*cnpj_digits[0] + 5*cnpj_digits[1] + 4*cnpj_digits[2] + 3*cnpj_digits[3]
    n2 += 2*cnpj_digits[4] + 9*cnpj_digits[5] + 8*cnpj_digits[6] + 7*cnpj_digits[7]
    n2 += 6*cnpj_digits[8] + 5*cnpj_digits[9] + 4*cnpj_digits[10] + 3*cnpj_digits[11] + 2*cnpj_digits[12]
    n2 = 11 - n2 % 11
    if n2 >= 10:
        n2 = 0

    if n1 == cnpj_digits[12] and n2 == cnpj_digits[13]:
        return True

    else:
        return False


def chave_validation(chave):
    match = re.match(r'[0-9A-Fa-f]{2}[\w.][0-9A-Fa-f]{2}[\w.][0-9A-Fa-f]{2}[\w.][0-9A-Fa-f]{2}', chave)
    if not match:
        return False

    if re.search(r'[A-Fa-f]{2}', chave):
        return False

    numeros = re.findall(r'\d{2}', chave)
    for par in numeros:
        if par[0] == par[1]:
            return False

    return True


def validar_transacao(transacao, chaves):
    if transacao[0] == transacao[1]:
        return False

    chaves = chaves.split(" ")
    k1 = False
    k2 = False
    for key in chaves:
        if key == transacao[0]:
            k1 = True
        if key == transacao[1]:
            k2 = True
        if k1 and k2:
            break
        if key == chaves[-1]:
            return False

    info = ''
    for i in transacao[2:]:
        info += i
        if not(i == transacao[-1]):
            info += " "

    valor = re.match(r'R[\w$] \d+,\d{2}', info)
    data = re.match(r'\d{2}/\d{2}/\d{4}', info)
    hora = re.match(r'[0-2]\d:[0-5]\d', info)
    chave_seguranca = re.match(r'', info)


def validar_cliente(cliente):
    cpf = re.match(r'\d{3}[\w.]\d{3}[\w.]\d{3}[\w-]\d{2}', cliente[0])
    cnpj = re.match(r'\d{2}[\w.]\d{3}[\w.]\d{3}/\d{4}[\w-]\d{2}', cliente[0])

    # Se existe um cpf ou cnpj, então tem que ser validado
    if cpf or cnpj:
        if cpf:
            if not cpf_validation(cpf.group()):
                print("cpf inválido")
                return False

        elif cnpj:
            if not cnpj_validation(cnpj.group()):
                print("cnpj invalido")
                return False

    else:
        print("Não há cpf nem cnpj")
        return False

    # Se há mais uma chave, verifica se elas são distintas
    #if len(cliente[1:]) > 1:
    for i in range(1, len(cliente[1:5]) + 1):
        for j in range(i+1, len(cliente[1:5])+1):
            if cliente[i] == cliente[j]:
                print("chaves iguais")
                return False

    # Armazenar as chaves numa única string
    chaves = ''
    for keys in cliente[1:5]:
        chaves += keys
        if not(keys == cliente[-1]): # Separa as chaves por um espaço
            chaves += " "
    print(f"chaves: {chaves}")

    emails = re.findall(r'\w+@[\w.]+', chaves)
    cpfs = re.findall(r'\d{3}[\w.]\d{3}[\w.]\d{3}[\w-]\d{2}', chaves)
    cnpjs = re.findall(r'\d{2}[\w.]\d{3}[\w.]\d{3}/\d{4}[\w-]\d{2}', chaves)
    telefones = re.findall(r'[\w+]\d{2}[\w(]\d{2}[\w)]\d{4}[\w-]\d{4}', chaves)
    chave_rapida = re.findall(r'[0-9A-Za-z]{2}[\w.][0-9A-Za-z]{2}[\w.][0-9A-Za-z]{2}[\w.][0-9A-Za-z]{2}', chaves)

    if emails or cpfs or cnpjs or chave_rapida or telefones:
        if emails:
            for EMAIL in emails:
                if email_validation(EMAIL):
                    continue
                else:
                    print("email inválido")
                    return False

        if cpfs:
            for CPF in cpfs:
                if cpf_validation(CPF):
                    continue
                else:
                    print("cpf chave inválido")
                    return False

        if cnpjs:
            for CNPJS in cnpjs:
                if cnpj_validation(CNPJS):
                    continue
                else:
                    print("cnpj chave inválido")
                    return False

        if chave_rapida:
            for key in chave_rapida:
                if chave_validation(key):
                    continue
                else:
                    print("chave inválida")
                    return False

        if telefones:
            for tel in telefones:
                if tel_validation(tel):
                    continue
                else:
                    print("telefone inválido")
                    return False

    else:
        return False

    # Verificando o separador
    separador = re.match(r'={10}', cliente[5])
    if not separador:
        print("separador invalido")
        return False

    # Verificando as trasações


    return True


# Entrada 1: 136.775.118-79 pmlxew@veracg.com +55(92)3584-0188 90.400.888/0001-42 D5.D9.A9.b6 ==========
# Entrada 2: 04.128.563/0001-10 zxhbpg@jmurip.com +55(92)3656-8985 62.144.175/0001-20 L2.B3.D5.a7
# Entrada 3: 04.280.196/0001-76 uea@uea.edu.br +55(92)3348-7601 09.628.825/0001-20 03.A4.2B.F8 ==========

cliente = input().split(" ")
print(f"Entrada: {cliente}")

pix = validar_cliente(cliente)
print(f"Saída: {pix}")