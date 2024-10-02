import streamlit as st
import datetime
import requests, json

password = "#1234560#"

def get_usuarios():
	req_lista_usuarios = requests.get('http://localhost:8000/users')
	if req_lista_usuarios.status_code == 200:
		json_lista_usuarios = json.loads(req_lista_usuarios.content)
		lista_usuarios={}
		for usuario in json_lista_usuarios:
			lista_usuarios[usuario['nome']] = usuario['id']

	return lista_usuarios

lista_usuarios = get_usuarios()

senha = st.text_input("Digite a senha: ", type = "password")

#if st.button("Acessar"):
#data_formatada = datetime.datetime.today().strftime("%d/%m/%Y")
data_formatada = datetime.datetime.today()
data_compra = st.date_input("Data da compra:", data_formatada)
valor_compra = st.text_input("Valor da compra:")
qtd_parcelas = st.number_input("Número de parcelas:", value = 1, format = '%d')
descricao = st.text_input("Descrição:")
usuario_selecionado = st.selectbox('Usuário', list(lista_usuarios.keys()))
id_usuario_selecionado =lista_usuarios[usuario_selecionado]
if st.button("Salvar"):
	if senha == password:
		#print(senha, password)
		data_compra = data_compra.strftime("%Y-%m-%d")
		dados_compra = {'data_compra': data_compra, 'valor_compra': valor_compra, 'qtd_parcelas': qtd_parcelas, 'descricao': descricao, 'id_usuario': id_usuario_selecionado}
		#st.write(dados_compra)
		response = requests.post('http://localhost:8000/compra', json = dados_compra)
		#st.write(response.json())
		if response.status_code == 201:
			st.info("Registro salvo com sucesso!")

	else:
		st.subheader("Senha incorreta!")


