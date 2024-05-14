# Sistema Bancário OOP

Este sistema foi desenvolvido como parte do Bootcamp de Python da plataforma DIO. O objetivo deste desafio era aperfeiçoar o sistema desenvolvido no desafio 2, disponível [aqui](https://github.com/gui-brito14/python_desafio_dio_sistema_bancario_otimizado), atualizando a implementação para armazenar os dados de clientes e contas bancárias em objetos ao invés de dicionários, transcrevendo o código para o paradigma de orientação a objetos, respeitando a hierarquia e o encapsulamento. 

Além disso, como desafio extra, foi orientado atualizar os métodos que tratam as opções do menu para funcionarem com as classes modeladas.

# Estrutura do Algoritmo Bancário

## Classes Principais

1. **Conta**
   - **Atributos**:
     - `saldo`: float
     - `limite`: float
     - `numero`: int
     - `cliente`: Cliente
     - `historico`: Historico
   - **Métodos**:
     - `__init__(self, cliente: Cliente, numero: int)`: Inicializa a conta com o cliente, número e saldo inicial.
     - `sacar(self, valor: float)`: Realiza um saque na conta.
     - `depositar(self, valor: float)`: Realiza um depósito na conta.

2. **Historico**
   - **Atributos**:
     - `transacoes`: List[Transacao]
   - **Métodos**:
     - `adicionar_transacao(self, transacao: Transacao)`: Adiciona uma transação ao histórico.

3. **Cliente**
   - **Atributos**:
     - `endereco`: str
     - `historico`: Historico
   - **Métodos**:
     - `realizar_transacao(self, conta: Conta, transacao: Transacao)`: Realiza uma transação em uma conta.
     - `adicionar_conta(self, conta: Conta)`: Adiciona uma conta ao cliente.

4. **PessoaFisica (Herda de Cliente)**
   - **Atributos**:
     - `cpf`: str
     - `data_nascimento`: date

5. **ContaCorrente (Herda de Conta)**
   - **Atributos**:
     - `limite_saque`: int

## Interfaces

1. **Transacao**
   - **Métodos**:
     - `registrar(self, conta: Conta)`: Registra a transação em uma conta.

## Implementações de Transacao

1. **Deposito (Implementa Transacao)**
   - **Atributos**:
     - `valor`: float
   - **Métodos**:
     - `registrar(self, conta: Conta)`: Registra um depósito na conta.

2. **Saque (Implementa Transacao)**
   - **Atributos**:
     - `valor`: float
   - **Métodos**:
     - `registrar(self, conta: Conta)`: Registra um saque na conta.

---

## Descrição Geral

O sistema bancário implementado permite a criação de contas bancárias para clientes, que podem realizar operações de depósito e saque. Cada operação é registrada no histórico da conta e do cliente. A estrutura segue o modelo de classes UML, onde as classes principais são `Conta`, `Historico`, `Cliente`, `PessoaFisica`, e `ContaCorrente`. As operações de transação são tratadas através da interface `Transacao`, com implementações específicas para `Deposito` e `Saque`.

## Funcionalidades

- **Criação de Clientes e Contas**: Permite a criação de clientes e suas respectivas contas bancárias.
- **Depósito e Saque**: Os clientes podem realizar depósitos e saques em suas contas.
- **Registro de Transações**: Todas as transações são registradas no histórico da conta e do cliente, garantindo a rastreabilidade das operações.
- **Herança e Polimorfismo**: Utilização de herança para especializar clientes (PessoaFisica) e contas (ContaCorrente). O polimorfismo é utilizado para tratar diferentes tipos de transações através de uma interface comum.

---

Essa descrição fornece uma visão geral da estrutura do algoritmo e suas principais funcionalidades, seguindo o modelo de classes UML apresentado.


## Funcionalidades Adicionais

Para além dos requisitos do desafio, o código foi aperfeiçoado para incluir as seguintes funcionalidades:

- **Classe Banco:** Substituição do método main por uma classe `Banco`, que armazena as contas e os clientes, e possui atributos privados como agência e endereço.
- **Escolha de Conta:** Caso o cliente tenha mais de uma conta, ele pode escolher a conta desejada.
- **Transações Simplificadas:** Adaptação dos métodos de saque e depósito para aceitarem apenas uma instância de transação.
- **Pessoa Jurídica:** Inclusão da opção de criar uma pessoa jurídica, além da física.
- **Limite de Saque:** Opção de alterar o limite de saque, com limitações de valor e número de operações.

## Estrutura do Projeto

O projeto está organizado da seguinte maneira:

- `banco.py`: Contém a classe `Banco` responsável por gerenciar clientes e contas.
- `cliente.py`: Contém as classes `PessoaFisica` e `PessoaJuridica`.
- `conta.py`: Contém a classe `ContaCorrente`.
- `transacao.py`: Contém a classe `Transacao` para gerenciar depósitos e saques.

## Contribuição

Sinta-se à vontade para contribuir com melhorias para o projeto. Faça um fork do repositório, crie uma nova branch para suas modificações e abra um pull request.

---

Desenvolvido como parte do Bootcamp de Python da plataforma DIO.
```
