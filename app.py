import streamlit as st
from datetime import datetime
# Importação do Firebase/Firestore
# Se não estiver usando, comente ou remova as linhas relacionadas ao firestore
# from google.cloud import firestore


# Configuração da conexão com o Firestore (Manter se for usar)
# Assumindo que você tem o arquivo 'firebase.json' e a biblioteca instalada.
try:
   db = firestore.Client.from_service_account_json("firebase.json")
except Exception as e:
   st.error(f"Erro ao conectar ao Firestore: {e}. Certifique-se de que 'firebase.json' está correto.")
   db = None # Define como None se a conexão falhar


# --- Configuração da Página ---
st.set_page_config(page_title="Seu Título do Blog", layout="wide")


# --- Dados Mock (Posts de Exemplo) ---
# Use links de imagem placeholder
PLACEHOLDER_IMAGE_URL_1 = "https://via.placeholder.com/770x300?text=Imagem+do+Post+Recente+1"
PLACEHOLDER_IMAGE_URL_2 = "https://via.placeholder.com/770x300?text=Imagem+do+Post+Recente+2"
PLACEHOLDER_AVATAR_URL = "https://via.placeholder.com/150?text=Avatar"


POSTS = [
   {
       "id": 1,
       "title": "Tornados, Ciclones e Furacões",
       "author": "Lorena Monteiro Moreira",
       "date": "2025-11-01",
       "summary": "saiba a diferença entre cada um e como são formados.",
       "image": PLACEHOLDER_IMAGE_URL_1
   },
   {
       "id": 2,
       "title": "Outro Post Interessante Aqui",
       "author": "Nome do Autor 2",
       "date": "2025-10-15",
       "summary": "Este resumo destaca os pontos-chave e o que o leitor aprenderá ou encontrará neste artigo.",
       "image": PLACEHOLDER_IMAGE_URL_2,
   },
   # Adicione mais posts conforme necessário
]


# --- Funções Auxiliares ---
def render_post_card(post):
   """Renderiza um card de post com imagem, título, autor e resumo."""
   st.image(post["image"], use_container_width=True)
   st.markdown(f"### {post['title']}")
   st.markdown(f"por *{post['author']}* — {post['date']}")
   st.write(post["summary"])
if st.button("Leia mais", key=f"btn_{post['title']}"):
        st.query_parameters["post"] = post['title']
        st.rerun()


# --- Layout e Interatividade ---


# O toggle de tema nativo do Streamlit é geralmente preferido.
# Se você quiser um toggle customizado, você precisará de CSS mais robusto.
# O código de aplicação de CSS para tema foi removido, pois o tema nativo
# do Streamlit pode ser controlado nas configurações.
# O toggle abaixo apenas demonstra um widget:


# Exemplo de um toggle (você pode usá-lo para controlar outras cores customizadas)
st.toggle("Tema Customizado", value=False)


# --- Barra Superior / Hero Section ---
col1, col2 = st.columns([3, 1])
with col1:
   st.title("Nome do Seu Blog Aqui")
   st.markdown("## Uma breve e impactante linha de slogan ou descrição do blog.")
with col2:
   st.image(PLACEHOLDER_AVATAR_URL) # Avatar/Logo placeholder


st.markdown("---")


# --- Seção Principal + Barra Lateral ---
main, sidebar = st.columns([3, 1])


with sidebar:
   st.header("Navegação 🧭")
   # Define a página inicial
   page = st.radio("Ir para", ["Início", "Sobre", "Contato"])
  
   st.header("Pesquisar 🔍")
   query = st.text_input("Buscar por título ou autor")
  
   st.markdown("---")
   st.write("Siga nas redes:")
   st.write("• X / Twitter: @seuperfil")
   st.write("• LinkedIn: /seuperfil")


with main:
   if page == "Início":
      
       st.header("Posts Recentes ✨")
      if "post" in st.query_parameters:
        titulo_selecionado = st.query_parameters["post"]
        
        # Chama o seu outro arquivo para mostrar o texto completo
        from pagina_post import mostrar_post_completo
        mostrar_post_completo(titulo_selecionado) 
        
    else:
        # Se NÃO clicou em nada, roda o código original que mostra a lista de cards
        st.title("Posts Recentes ✨")
        
        # Aqui deve estar o seu loop atual que mostra os posts, por exemplo:
        for post in lista_de_posts:
            render_post_card(post)


       # Filtro de pesquisa simples
       filtered = POSTS
       if query:
           q = query.lower()
           filtered = [p for p in POSTS if q in p['title'].lower() or q in p['author'].lower()]


       if filtered:
           for post in filtered:
               with st.container():
                   render_post_card(post)
                   st.markdown("---")
       else:
            st.info("Nenhum post encontrado com o critério de pesquisa.")


   elif page == "Sobre":
       st.header("Sobre Este Blog 💡")
       st.markdown(
           "Este blog serve como um *template* e um espaço para o autor compartilhar "
           "seu conhecimento, paixões e perspectivas sobre [Tópico Principal do Blog]."
       )
       st.subheader("Missão")
       st.write("Compartilhar conteúdo de forma clara, acessível e inspiradora.")


   elif page == "Contato":
       with st.form("fale_conosco"):
           st.header("Fale Conosco 📧")
           st.write("Preencha o formulário abaixo para entrar em contato.")
           name = st.text_input("Seu nome")
           email = st.text_input("Seu e-mail")
           message = st.text_area("Mensagem")
          
           if st.form_submit_button("Enviar"):  
              if not name or not email or not message:
                  st.warning("Preencha todos os campos antes de enviar.")
              elif db is None:
                   # Mensagem para o caso do Firestore não ter sido conectado
                   st.error("O formulário foi preenchido, mas a conexão com o banco de dados (Firestore) falhou. Verifique 'firebase.json'.")
                  
              else:
                   # Lógica de salvamento no Firestore (Manter se for usar)
                   try:
                       novo_documento = db.collection("contato_mensagem").document() # Usa ID gerado automaticamente
                       novo_documento.set(
                           {
                               "name" : name,
                               "email" : email,
                               "message" : message,
                               "timestamp": datetime.now() # Adiciona um carimbo de data/hora
                           }
                       )
                       st.success("Obrigado! Sua mensagem foi enviada.")
                   except Exception as e:
                       st.error(f"Erro ao salvar mensagem no Firestore: {e}")


# --- Rodapé (Footer) ---
st.markdown("---")
colf1, colf2 = st.columns([1, 3])
with colf1:
   st.write(f"© {datetime.now().year} Nome do Seu Blog")
with colf2:
   st.write("Template de exemplo para Streamlit — personalize cores, fontes e layout conforme a necessidade.")
