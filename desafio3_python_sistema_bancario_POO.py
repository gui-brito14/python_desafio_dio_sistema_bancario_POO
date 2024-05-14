import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class PessoaJuridica(Cliente):
    def __init__(self, nome_empresa, cnpj, endereco):
        super().__init__(endereco)
        self.nome_empresa = nome_empresa
        self.cnpj = cnpj


class Conta:
    def __init__(self, numero, cliente):
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
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._alteracoes_limite = 0

    @property
    def limite(self):
        return self._limite

    def alterar_limite(self, novo_limite):
        if self._alteracoes_limite >= 3:
            print("\n@@@ Operação falhou! Limite de alterações atingido. @@@")
            return False

        if novo_limite > 10000:
            print("\n@@@ Operação falhou! O novo limite excede o máximo permitido de R$ 10.000,00. @@@")
            return False

        self._limite = novo_limite
        self._alteracoes_limite += 1
        print("\n=== Limite de saque alterado com sucesso! ===")
        return True

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome if isinstance(self.cliente, PessoaFisica) else self.cliente.nome_empresa}
            Limite de Saque:\tR$ {self._limite:.2f}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
        )


class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Banco:
    def __init__(self, agencia, endereco):
        self._agencia = agencia
        self._endereco = endereco
        self._clientes = []
        self._contas = []

    def menu(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [al]\tAlterar limite de saque
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))

    def filtrar_cliente(self, cpf_cnpj):
        clientes_filtrados = [cliente for cliente in self._clientes if (getattr(cliente, 'cpf', None) == cpf_cnpj or getattr(cliente, 'cnpj', None) == cpf_cnpj)]
        return clientes_filtrados[0] if clientes_filtrados else None

    def escolher_conta(self, cliente):
        if len(cliente.contas) == 1:
            return cliente.contas[0]

        print("\nSelecione uma conta:")
        for i, conta in enumerate(cliente.contas, start=1):
            print(f"[{i}] Agência: {conta.agencia} - Número: {conta.numero}")

        escolha = int(input("Digite o número da conta: ")) - 1

        if escolha < 0 or escolha >= len(cliente.contas):
            print("\n@@@ Opção inválida! @@@")
            return None

        return cliente.contas[escolha]

    def realizar_operacao(self, operacao):
        cpf_cnpj = input("Informe o CPF/CNPJ do cliente: ")
        cliente = self.filtrar_cliente(cpf_cnpj)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = self.escolher_conta(cliente)
        if not conta:
            return

        operacao(cliente, conta)

    def depositar(self, cliente, conta):
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)

    def sacar(self, cliente, conta):
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)

    def exibir_extrato(self, cliente, conta):
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n\tData: {transacao['data']}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")

    def alterar_limite(self, cliente, conta):
        if not isinstance(conta, ContaCorrente):
            print("\n@@@ Alteração de limite disponível apenas para contas correntes. @@@")
            return

        novo_limite = float(input("Informe o novo limite de saque: "))
        conta.alterar_limite(novo_limite)

    def criar_cliente(self):
        tipo_cliente = input("Informe o tipo de cliente (1 - Pessoa Física, 2 - Pessoa Jurídica): ")
        
        if tipo_cliente == '1':
            cpf = input("Informe o CPF (somente número): ")
            cliente = self.filtrar_cliente(cpf)

            if cliente:
                print("\n@@@ Já existe cliente com esse CPF! @@@")
                return

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        elif tipo_cliente == '2':
            cnpj = input("Informe o CNPJ (somente número): ")
            cliente = self.filtrar_cliente(cnpj)

            if cliente:
                print("\n@@@ Já existe cliente com esse CNPJ! @@@")
                return

            nome_empresa = input("Informe o nome da empresa: ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            cliente = PessoaJuridica(nome_empresa=nome_empresa, cnpj=cnpj, endereco=endereco)

        else:
            print("\n@@@ Tipo de cliente inválido! @@@")
            return

        self._clientes.append(cliente)

        print("\n=== Cliente criado com sucesso! ===")

    def criar_conta(self):
        cpf_cnpj = input("Informe o CPF/CNPJ do cliente: ")
        cliente = self.filtrar_cliente(cpf_cnpj)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        numero_conta = len(self._contas) + 1
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        self._contas.append(conta)
        cliente.adicionar_conta(conta)

        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        if not self._contas:
            print("\n@@@ Nenhuma conta cadastrada! @@@")
            return

        for conta in self._contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == "d":
                self.realizar_operacao(self.depositar)

            elif opcao == "s":
                self.realizar_operacao(self.sacar)

            elif opcao == "e":
                self.realizar_operacao(self.exibir_extrato)

            elif opcao == "nu":
                self.criar_cliente()

            elif opcao == "nc":
                self.criar_conta()

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "al":
                self.realizar_operacao(self.alterar_limite)

            elif opcao == "q":
                break

            else:
                print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    banco = Banco(agencia="0001", endereco="123 Rua Principal, Cidade/UF")
    banco.executar()
