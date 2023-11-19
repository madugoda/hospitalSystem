import os
import requests

# Função para imprimir o menu
def imprimirMenu():
    print("_" * 25)
    print("         MENU ")
    print("1. Adicionar Paciente")
    print("2. Editar Paciente")
    print("3. Consultar Paciente")
    print("4. Excluir Paciente")
    print("5. Agendar Consulta")
    print("6. Gerenciar Consulta")
    print("7. Sair")
    print("_" * 25)

# Função para consultar o CEP
def consultarCEP(zpc=None):
    if zpc is None:
        zpc = input("Digite o CEP: ")

        while not zpc.isnumeric() or len(zpc) != 8:
            zpc = input("Valor inválido! Digite somente os números: ")

    url = f"https://viacep.com.br/ws/{zpc}/json/"
    request = requests.get(url=url)
    result = request.json()

    if 'erro' in result:
        print("CEP não encontrado!")
        return None
    else:
        return result

# Função para adicionar um novo paciente com consulta de CEP
def adicionarPaciente(lista_pacientes):
    nome = input("Informe o nome do paciente: ")
    idade = int(input("Informe a idade do paciente: "))
    
    # Verificação do sexo (aceita apenas "F" ou "M")
    while True:
        sexo = input("Informe o sexo do paciente (F/M): ").upper()
        if sexo in ["F", "M"]:
            break
        else:
            print("Por favor, digite apenas 'F' para feminino ou 'M' para masculino.")

    # Consultar CEP
    cep_info = consultarCEP()
    
    if cep_info:
        endereco = cep_info.get('logradouro', '')
        bairro = cep_info.get('bairro', '')
        cidade = cep_info.get('localidade', '')
        uf = cep_info.get('uf', '')
    else:
        endereco = input("Informe o endereço do paciente: ")
        bairro = input("Informe o bairro do paciente: ")
        cidade = input("Informe a cidade do paciente: ")
        uf = input("Informe o estado do paciente: ")

    paciente = {'nome': nome, 'idade': idade, 'sexo': sexo, 'endereco': endereco, 'bairro': bairro, 'cidade': cidade, 'uf': uf}
    lista_pacientes.append(paciente)
    print("Paciente adicionado com sucesso!")


# Função para editar informações de um paciente
def editarPaciente(lista_pacientes):
    nome = input("Informe o nome do paciente que deseja editar: ")
    for paciente in lista_pacientes:
        if paciente['nome'] == nome:
            novo_nome = input("Novo nome (deixe em branco para manter o mesmo): ")
            novo_idade = input("Nova idade (deixe em branco para manter a mesma): ")

            # Verificação do novo sexo (aceita apenas "F" ou "M")
            while True:
                novo_sexo = input("Novo sexo (deixe em branco para manter o mesmo) (F/M): ").upper()
                if novo_sexo == '' or novo_sexo in ["F", "M"]:
                    break
                else:
                    print("Por favor, digite apenas 'F' para feminino ou 'M' para masculino.")

            novo_cep = input("Novo CEP (deixe em branco para manter o mesmo): ")

            # Verificar se o CEP é válido (opcional)
            if novo_cep and (not novo_cep.isnumeric() or len(novo_cep) != 8):
                print("CEP inválido. O CEP deve conter exatamente 8 dígitos.")
                continue

            # Consultar CEP se um novo CEP for fornecido
            if novo_cep:
                cep_info = consultarCEP(novo_cep)
                if cep_info:
                    paciente['endereco'] = cep_info.get('logradouro', '')
                    paciente['bairro'] = cep_info.get('bairro', '')
                    paciente['cidade'] = cep_info.get('localidade', '')
                    paciente['uf'] = cep_info.get('uf', '')

            if novo_nome:
                paciente['nome'] = novo_nome
            if novo_idade:
                paciente['idade'] = int(novo_idade)
            if novo_sexo:
                paciente['sexo'] = novo_sexo

            print("Informações do paciente atualizadas com sucesso!")
            return

    print("Paciente não encontrado.")


# Função para consultar informações de um paciente
def consultarPaciente(lista_pacientes):
    nome = input("Informe o nome do paciente que deseja consultar: ")
    for paciente in lista_pacientes:
        if paciente['nome'] == nome:
            print("\nInformações do Paciente:")
            print(f"Nome: {paciente['nome']}")
            print(f"Idade: {paciente['idade']}")
            print(f"Sexo: {paciente['sexo']}")
            
            # Verificar se os campos de endereço existem antes de imprimir
            if 'endereco' in paciente:
                print(f"Endereço: {paciente['endereco']}")
            if 'bairro' in paciente:
                print(f"Bairro: {paciente['bairro']}")
            if 'cidade' in paciente:
                print(f"Cidade: {paciente['cidade']}")
            if 'uf' in paciente:
                print(f"UF: {paciente['uf']}")

            if 'consulta_agendada' in paciente:
                print(f"Consulta Agendada para: {paciente['consulta_agendada']}")
            
            return

    print("Paciente não encontrado.")

# Função para excluir um paciente
def excluirPaciente(lista_pacientes):
    nome = input("Informe o nome do paciente que deseja excluir: ")
    for paciente in lista_pacientes:
        if paciente['nome'] == nome:
            lista_pacientes.remove(paciente)
            print("Paciente excluído com sucesso!")
            return

    print("Paciente não encontrado.")

# Função para adicionar uma consulta
def agendarConsulta(lista_pacientes):
    nome = input("Informe o nome do paciente para agendar a consulta: ")
    for paciente in lista_pacientes:
        if paciente['nome'] == nome:
            if 'consulta_agendada' in paciente:
                opcao = input("Este paciente já tem uma consulta agendada. Deseja reagendar (R), excluir (E) ou cancelar (C)? ").lower()
                if opcao == 'r':
                    data_consulta = input("Informe a nova data da consulta (formato: DD/MM/YYYY): ")
                    paciente['consulta_agendada'] = data_consulta
                    print("Consulta reagendada com sucesso!")
                elif opcao == 'e':
                    del paciente['consulta_agendada']
                    print("Consulta excluída com sucesso!")
                else:
                    print("Operação cancelada.")
            else:
                data_consulta = input("Informe a data da consulta (formato: DD/MM/YYYY): ")
                paciente['consulta_agendada'] = data_consulta
                print("Consulta agendada com sucesso!")
            return

    print("Paciente não encontrado.")

# Função para excluir ou reagendar uma consulta
def gerenciarConsulta(lista_pacientes):
    nome = input("Informe o nome do paciente para gerenciar a consulta: ")
    for paciente in lista_pacientes:
        if paciente['nome'] == nome:
            if 'consulta_agendada' in paciente:
                print(f"Consulta agendada para o paciente {paciente['nome']} em {paciente['consulta_agendada']}")
                opcao = input("Deseja reagendar (R), excluir (E) ou cancelar (C)? ").lower()
                if opcao == 'r':
                    data_consulta = input("Informe a nova data da consulta (formato: DD/MM/YYYY): ")
                    paciente['consulta_agendada'] = data_consulta
                    print("Consulta reagendada com sucesso!")
                elif opcao == 'e':
                    del paciente['consulta_agendada']
                    print("Consulta excluída com sucesso!")
                else:
                    print("Operação cancelada.")
            else:
                print("Este paciente não tem uma consulta agendada.")
            return

    print("Paciente não encontrado.")

# Função principal
def main():
    pacientes = []

    while True:
        imprimirMenu()

        opcao = input("Escolha uma opção (1-7): ")

        if opcao == '1':
            adicionarPaciente(pacientes)
        elif opcao == '2':
            editarPaciente(pacientes)
        elif opcao == '3':
            consultarPaciente(pacientes)
        elif opcao == '4':
            excluirPaciente(pacientes)
        elif opcao == '5':
            agendarConsulta(pacientes)
        elif opcao == '6':
            gerenciarConsulta(pacientes)
        elif opcao == '7':
            print("Saindo da aplicação. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução da rotina principal
if __name__ == "__main__":
    main()
