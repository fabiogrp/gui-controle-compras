import streamlit as st
import requests, json
import datetime
import locale


st.set_page_config(layout="wide")
#loc = locale.getlocale()
#locale.setlocale(locale.LC_NUMERIC, "pt_BR")
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
data_ano = datetime.date.today().year
data_mes = datetime.date.today().month

url_base = "http://localhost:8000/compra/"

def get_usuarios():
	req_lista_usuarios = requests.get('http://localhost:8000/users')
	if req_lista_usuarios.status_code == 200:
		json_lista_usuarios = json.loads(req_lista_usuarios.content)
		lista_usuarios={}
		for usuario in json_lista_usuarios:
			lista_usuarios[usuario['nome']] = usuario['id']

	return lista_usuarios

lista_usuarios = get_usuarios()

col_esquerda, col_direita,  = st.columns([1,3])

with col_esquerda:
	#st.title("Aqui tem outra coluna")
	data_consulta = st.date_input("Data:", datetime.date(data_ano, data_mes , 1))
	#st.write(data_consulta)
	usuario_selecionado = st.selectbox("Usuário", list(lista_usuarios.keys()))
	id_usuario_selecionado = lista_usuarios[usuario_selecionado]
	url = url_base + str(id_usuario_selecionado) + "/" + str(data_consulta).split("-")[0] + "-" + str(data_consulta).split("-")[1]

with col_direita:
	#st.title("Aqui tem uma coluna")
	#st.write(url)
	#response = requests.get(url_base + str(id_usuario) + "/2023-06")
	response = requests.get(url)
	if len(response.json()) > 0:
		dados_compras = json.loads(response.content)
		lista_compras = []
		valor_total_compras = 0
		quantidade_compras = 0
		dados_compras_formatados = []
		for compra in dados_compras:
			data_compra_formatada = datetime.datetime.strptime(compra['data_compra'],"%Y-%m-%d")
			data_compra_formatada = data_compra_formatada.strftime("%d/%m/%Y")
			valor_parcela_formatado = locale.currency(compra['valor_parcela'])
			#valor_parcela_formatado = "%.2f" % compra['valor_parcela']
			descricao_compra = compra['descricao']
			qtd_parcelas_formatado = compra['parcela'] + "/"  + str(compra['qtd_parcelas'])
			dados_compras_formatados.append({'Data': data_compra_formatada, 'Valor': valor_parcela_formatado, 'Descrição': descricao_compra, 'Parcela(s)': qtd_parcelas_formatado})
			quantidade_compras += 1
			valor_total_compras += compra['valor_parcela']


		st.table(dados_compras_formatados)
		#st.write("Compras: " + str(quantidade_compras))
		#st.write("Total: " +  "%.2f" % valor_total_compras)
		st.markdown("###### Compras:  "  + str(quantidade_compras))
		st.markdown("###### Total: " + locale.currency(valor_total_compras, grouping = True))
		#st.markdown("###### Total:  %.2f" % valor_total_compras)
	else:
		st.subheader("Nenhuma compra localizada")



