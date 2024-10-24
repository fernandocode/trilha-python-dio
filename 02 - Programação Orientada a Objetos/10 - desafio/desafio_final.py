from abc import ABC, abstractmethod
from datetime import datetime


class Messages:
    class Error:
        VALOR_INVALIDO = "\nOperação falhou! O valor informado é inválido."
        SALDO_INSUFICIENTE = "\nOperação falhou! Você não tem saldo suficiente."
        SALDO_EXCEDE_LIMITE = "\nOperação falhou! O valor do saque excede o limite."
        NUMERO_MAXIMO_SAQUE_EXCEDE_LIMITE = "\nOperação falhou! Número máximo de saques excedido."
        CPF_CLIENTE_EXISTE = "\nJá existe cliente com esse CPF!"
        CLIENTE_NAO_ENCONTRADO_CRIACA_CONTA = "\nCliente não encontrado, fluxo de criação de conta encerrado!"
        NENHUMA_CONTA_VINCULADA_CLIENTE = "\nNenhuma conta vinculada ao cliente!"
        OPERACAO_INVALIDA = "\nOperação inválida, por favor selecione novamente a operação desejada."

    class Success:
        SAQUE = "\nSaque realizado com sucesso!"
        DEPOSITO = "\nDepósito realizado com sucesso!"
        CLIENTE_CRIADO = "\nCliente criado com sucesso!"
        CONTA_CRIADA = "\nConta criada com sucesso!"


class FormatUtils:

    @staticmethod
    def pad_left(value: str, pad_left_size: int):
        return value.ljust(pad_left_size)

    @staticmethod
    def pad_right(value: str, pad_right_size: int):
        return value.rjust(pad_right_size)

    @staticmethod
    def valor(valor: float):
        return FormatUtils.pad_right(f"R$ {valor:.2f}", 15)

    @staticmethod
    def label(label: str, pad_left_size: int = 30):
        return FormatUtils.pad_left(f"{label}:", pad_left_size)

    @staticmethod
    def option_menu(option: str, descricao: str, pad_left_size: int = 5):
        return f"{FormatUtils.pad_left(f"[{option}]", pad_left_size)} {descricao}"


class Menu:
    DEPOSITO = "d"
    SAQUE = "s"
    EXTRATO = "e"
    NOVO_CLIENTE = "ncl"
    LISTAR_CLIENTES = "lcl"
    NOVA_CONTA = "nco"
    LISTAR_CONTA = "lco"
    LISTAR_CONTA_POR_CLIENTE = "lcc"
    SAIR = "q"

    @staticmethod
    def montar_menu():
        print()
        print(" MENU ".center(45, "="))
        print(FormatUtils.option_menu(Menu.DEPOSITO, "Depositar"))
        print(FormatUtils.option_menu(Menu.SAQUE, "Sacar"))
        print(FormatUtils.option_menu(Menu.EXTRATO, "Extrato"))
        print(FormatUtils.option_menu(Menu.NOVO_CLIENTE, "Novo cliente"))
        print(FormatUtils.option_menu(Menu.NOVA_CONTA, "Nova conta"))
        print(FormatUtils.option_menu(Menu.LISTAR_CONTA, "Listar contas"))
        print(FormatUtils.option_menu(Menu.LISTAR_CLIENTES, "Listar clientes"))
        print(FormatUtils.option_menu(
            Menu.LISTAR_CONTA_POR_CLIENTE, "Listar contas por cliente"))
        print(FormatUtils.option_menu(Menu.SAIR, "Sair"))
        return input("Informe a opção desejada:")


class Transacao(ABC):

    def __init__(self):
        self._data = datetime.now()

    @property
    def data(self):
        return self._data

    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def extrato(self):
        for conta in self.contas:
            conta.extrato()


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)


class Conta:
    def __init__(self, numero, cliente: Cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(Messages.Error.SALDO_INSUFICIENTE)

        elif valor > 0:
            self._saldo -= valor
            print(Messages.Success.SAQUE)
            return True
        else:
            print(Messages.Error.VALOR_INVALIDO)

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(Messages.Success.DEPOSITO)
        else:
            print(Messages.Error.VALOR_INVALIDO)
            return False

        return True

    def extrato(self):
        if not self.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            print(" EXTRATO ".center(45, "="))
            print(f" Conta {self.numero} ".center(45, "="))
            print()
            for transacao in self.historico.transacoes:
                print(f"{FormatUtils.label(transacao.__class__.__name__)}{
                    FormatUtils.valor(transacao.valor)}")
            print(f"\n{FormatUtils.label("Saldo atual")}{
                  FormatUtils.valor(self.saldo)}\n")
            print("".center(45, "="))


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao.__class__.__name__
                == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(Messages.Error.SALDO_EXCEDE_LIMITE)

        elif excedeu_saques:
            print(Messages.Error.NUMERO_MAXIMO_SAQUE_EXCEDE_LIMITE)

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"{self.dados_conta_str()}\n{self.dados_titular_conta_str()}"

    def dados_conta_str(self):
        return f"\nAgência: {self.agencia}\nC/C: {self.numero}"

    def dados_titular_conta_str(self):
        return f"Titular: {self.cliente.nome}"


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def input_conta(contas: list):
    numero_conta = try_parse_numerico(input("Informe o numero da conta: "))
    conta = filtrar_contas(contas, numero_conta=numero_conta)
    if conta:
        return conta[0]
    print(f"\nNenhuma conta encontrada com numero {numero_conta}!")    


def solicitar_extrato(contas: list):
    for conta in contas:
        conta.extrato()


def solicitar_deposito(contas: list):
    conta = input_conta(contas)

    if conta:
        valor = try_parse_numerico(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        # TODO: Faria mais sentido a operacao "realizar_transacao" ser da classe "Conta" ao invés da classe "Cliente", vou manter assim para atender os requisitos do UML do desafio
        conta.cliente.realizar_transacao(conta, transacao)


def solicitar_saque(contas: list):
    conta = input_conta(contas)

    if conta:
        valor = try_parse_numerico(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        # TODO: Faria mais sentido a operacao "realizar_transacao" ser da classe "Conta" ao invés da classe "Cliente", vou manter assim para atender os requisitos do UML do desafio
        conta.cliente.realizar_transacao(conta, transacao)


def try_parse_numerico(valor_str: str):
    try:
        return float(valor_str)
    except:
        return 0


def filtrar_cliente(cpf: str, clientes: list):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def filtrar_contas(contas: list, *, cpf: str = None, numero_conta: int = None):
    contas_filtrados = [
        conta for conta in contas if (not cpf or conta.cliente.cpf == cpf) and (not numero_conta or conta.numero == numero_conta)]
    return contas_filtrados


def criar_cliente(clientes: list):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_cliente(cpf, clientes)

    if usuario:
        print(Messages.Error.CPF_CLIENTE_EXISTE)
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print(Messages.Success.CLIENTE_CRIADO)


def criar_conta(numero_conta: int, clientes: list, contas: list):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print(Messages.Success.CONTA_CRIADA)
    else:
        print(Messages.Error.CLIENTE_NAO_ENCONTRADO_CRIACA_CONTA)


def listar_contas(contas: list):
    for conta in contas:
        print("".center(45, "="))
        print(conta)


def listar_clientes(clientes: list, contas: list):
    for cliente in clientes:
        print("".center(45, "="))
        print(f"Titular: {cliente.nome}")
        print(f"CPF: {cliente.cpf}")
        print(f"Data Nascimento: {cliente.data_nascimento}")
        print(f"Endereço: {cliente.endereco}")
        listar_contas_por_cliente(contas, cliente.cpf)


def listar_contas_por_cliente(contas: list, cpf: str = None):
    cpf = cpf if cpf else input("Informe o CPF do cliente: ")
    contas_do_usuario = filtrar_contas(contas, cpf=cpf)
    if contas_do_usuario:
        print("\nContas:")
        for conta in contas_do_usuario:
            print(f"{conta.dados_conta_str()}\n")
    else:
        print(Messages.Error.NENHUMA_CONTA_VINCULADA_CLIENTE)


def main():
    clientes = []
    contas = []
    id_conta_incremento: int = 0

    while True:
        opcao = Menu.montar_menu()

        if opcao == Menu.DEPOSITO:
            solicitar_deposito(contas)
        elif opcao == Menu.SAQUE:
            solicitar_saque(contas)
        elif opcao == Menu.EXTRATO:
            solicitar_extrato(contas)
        elif opcao == Menu.NOVO_CLIENTE:
            criar_cliente(clientes)
        elif opcao == Menu.NOVA_CONTA:
            id_conta_incremento += 1
            criar_conta(id_conta_incremento, clientes, contas)
        elif opcao == Menu.LISTAR_CONTA:
            listar_contas(contas)
        elif opcao == Menu.LISTAR_CLIENTES:
            listar_clientes(clientes, contas)
        elif opcao == Menu.LISTAR_CONTA_POR_CLIENTE:
            listar_contas_por_cliente(contas)
        elif opcao == Menu.SAIR:
            break
        else:
            print(Messages.Error.OPERACAO_INVALIDA)


main()
