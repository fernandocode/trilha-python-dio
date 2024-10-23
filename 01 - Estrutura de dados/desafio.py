
OPERACAO_DEPOSITO = "d"
OPERACAO_SAQUE = "s"
OPERACAO_EXTRATO = "e"
OPERACAO_NOVO_USUARIO = "nu"
OPERACAO_LISTAR_USUARIOS = "lu"
OPERACAO_NOVO_CONTA = "nc"
OPERACAO_LISTAR_CONTA = "lc"
OPERACAO_LISTAR_CONTA_POR_USUARIO = "lcu"
OPERACAO_SAIR = "q" 

VALOR_LIMITE_POR_SAQUE = 500
LIMITE_SAQUES = 3
AGENCIA = "0001"

MSG_VALOR_INVALIDO = "Operação falhou! O valor informado é inválido."
    
    
def format_valor(valor: float):
    return format_pad_right(f"R$ {valor:.2f}", 15)


def format_label(label: str, pad_left_size: int = 30):
    return format_pad_left(f"{label}:", pad_left_size)


def format_pad_left(value: str, pad_left_size: int):
    return value.ljust(pad_left_size)


def format_pad_right(value: str, pad_right_size: int):
    return value.rjust(pad_right_size)

def format_option_menu(option: str, descricao: str, pad_left_size: int = 5):
    return f"{format_pad_left(f"[{option}]", pad_left_size)} {descricao}"
       

def decricao_operacao(operacao):
    if operacao == OPERACAO_DEPOSITO:
        return "Depósito"
    elif operacao == OPERACAO_SAQUE:
        return "Saque"
     
        
def gerar_extrato(saldo, /, *, transacoes: list):
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        print(" EXTRATO ".center(45, "="))
        print()
        for tipo, valor in transacoes:
            print(f"{format_label(decricao_operacao(tipo))}{format_valor(valor)}")
        print(f"\n{format_label("Saldo atual")}{format_valor(saldo)}\n")
        print("".center(45, "="))
    
    
def registar_deposito(valor: float, saldo: float, transacoes: list, /):
    if valor > 0:
        saldo += valor
        transacoes.append((OPERACAO_DEPOSITO, valor))
        print("\nDepósito realizado com sucesso!")
    else:
        print(MSG_VALOR_INVALIDO)
    return saldo
    
def registar_saque(*, valor: float, saldo: float, transacoes: list, numero_saques: int):    
    excedeu_saldo = valor > saldo
    excedeu_limite_por_saque = valor > VALOR_LIMITE_POR_SAQUE
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite_por_saque:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        transacoes.append((OPERACAO_SAQUE, valor))
        numero_saques += 1
    else:
        print(MSG_VALOR_INVALIDO)
    return saldo, numero_saques

    
def try_parse_numerico(valor_str: str):
    try:
        return float(valor_str)
    except:
        return 0
    
    
def menu():
    print()
    print(" MENU ".center(45, "="))
    print(format_option_menu(OPERACAO_DEPOSITO, "Depositar"))
    print(format_option_menu(OPERACAO_SAQUE, "Sacar"))
    print(format_option_menu(OPERACAO_EXTRATO, "Extrato"))
    print(format_option_menu(OPERACAO_NOVO_USUARIO, "Novo usuário"))
    print(format_option_menu(OPERACAO_NOVO_CONTA, "Nova conta"))
    print(format_option_menu(OPERACAO_LISTAR_CONTA, "Listar contas"))
    print(format_option_menu(OPERACAO_LISTAR_USUARIOS, "Listar usuários"))
    print(format_option_menu(OPERACAO_LISTAR_CONTA_POR_USUARIO, "Listar contas por usuário"))
    print(format_option_menu(OPERACAO_SAIR, "Sair"))
    return input("Informe a opção desejada:")


def filtrar_usuario(cpf: str, usuarios: list):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def filtrar_contas(cpf: str, contas: list):
    contas_filtrados = [conta for conta in contas if conta["usuario"] and conta["usuario"]["cpf"] == cpf]
    return contas_filtrados


def criar_usuario(usuarios: list):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\nUsuário criado com sucesso!")
    
    
def criar_conta(numero_conta: int, usuarios: list, contas: list):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario})
        print("\nConta criada com sucesso!")
    else:
        print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
        

def listar_contas(contas: list):
    for conta in contas:
        print("".center(45, "="))
        print_conta(conta)
        print_titulo_conta(conta)
        
        
def print_conta(conta: dict):
    print(f"Agência: {conta['agencia']}")
    print(f"C/C: {conta['numero_conta']}")
    
    
def print_titulo_conta(conta: dict):
    print(f"Titular: {conta['usuario']['nome']}")
        

def listar_usuarios(usuarios: list, contas: list):
    for usuario in usuarios:
        print("".center(45, "="))
        print(f"Titular: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        listar_contas_por_usuario(contas, usuario["cpf"])
        

def listar_contas_por_usuario(contas: list, cpf: str = None):    
    cpf = cpf if cpf else input("Informe o CPF do usuário: ")
    contas_do_usuario = filtrar_contas(cpf, contas)
    if contas_do_usuario:
        print("\nContas:\n")        
        for conta in contas_do_usuario:
            print_conta(conta)
            print()
    else:
        print("\nNenhuma conta vinculada ao usuário!")
    
def main():
    saldo = 0
    numero_saques = 0
    transacoes = []
    usuarios = []
    contas = []
    id_conta_incremento: int = 0
    
    while True:
        opcao = menu()
        
        if opcao == OPERACAO_DEPOSITO:
            valor = try_parse_numerico(input("Informe o valor do depósito: "))
            saldo = registar_deposito(valor, saldo, transacoes)
        elif opcao == OPERACAO_SAQUE:
            valor = try_parse_numerico(input("Informe o valor do saque: "))
            saldo, numero_saques = registar_saque(valor=valor, saldo=saldo, transacoes=transacoes, numero_saques=numero_saques)
        elif opcao == OPERACAO_EXTRATO:
            gerar_extrato(saldo, transacoes=transacoes)
        elif opcao == OPERACAO_NOVO_USUARIO:
            criar_usuario(usuarios)
        elif opcao == OPERACAO_NOVO_CONTA:
            id_conta_incremento += 1
            criar_conta(id_conta_incremento, usuarios, contas)
        elif opcao == OPERACAO_LISTAR_CONTA:
            listar_contas(contas)
        elif opcao == OPERACAO_LISTAR_USUARIOS:
            listar_usuarios(usuarios, contas)
        elif opcao == OPERACAO_LISTAR_CONTA_POR_USUARIO:
            listar_contas_por_usuario(contas)
        elif opcao == OPERACAO_SAIR:
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
            
main()