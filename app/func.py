import re, os
from email_validator import validate_email, EmailNotValidError
import requests

def validar_email(email):
    try:
        # Valida e normaliza o formato
        emailinfo = validate_email(email)
        return emailinfo.normalized
    except EmailNotValidError as e:
        return "Formato Incopatível"



def validar_cpf(cpf):
    # 1. Limpeza: Remove pontos, traços e espaços
    cpf = re.sub(r'\D', '', cpf)

    # 2. Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # 3. Verifica se todos os dígitos são iguais (ex: 111.111.111-11 é inválido)
    if cpf == cpf[0] * 11:
        return False

    # 4. Cálculo do primeiro dígito verificador (10º dígito)
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)

    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0

    # 5. Cálculo do segundo dígito verificador (11º dígito)
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)

    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0

    # 6. Validação final
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True
    else:
        return False
    