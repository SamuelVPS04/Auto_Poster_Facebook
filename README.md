# 🧠 Automatizador de Postagens no Facebook

Este web app permite **criar e enviar postagens automaticamente para múltiplas páginas do Facebook**, utilizando tokens de acesso obtidos pelo **Meta for Developers**.  
Ele foi desenvolvido em **Python (Flask)**, com integração à **API Graph do Meta** e banco de dados **MySQL**.

---

## ⚙️ Pré-requisitos

Antes de tudo, certifique-se de ter instalado:

- Python 3.10+  
- MySQL Server e MySQL Workbench  
- Conta no **Meta for Developers** com permissões de administrador em uma ou mais **Páginas do Facebook**

---

## 🧩 1. Criando o App no Meta for Developers

1. Acesse: [https://developers.facebook.com/apps](https://developers.facebook.com/apps)  
2. Clique em **“Criar aplicativo”**  
3. Escolha o tipo **"Negócios" (Business)**  
4. Dê um nome ao aplicativo e confirme.  

Após criado:
- Vá em **Configurações → Básico**
- Copie o **App ID** e o **App Secret**
- Adicione o produto **Facebook Login** → **Configurar**

---

## 🔑 2. Obter o Token de Acesso do Usuário

1. Vá até o menu lateral esquerdo e clique em **“Graph API Explorer”**  
   👉 [https://developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer)

2. Selecione o **App** que você criou.  
3. Em **“Gerar token de acesso do usuário”**, marque as permissões:
   ```
   pages_show_list
   pages_manage_posts
   pages_read_engagement
   business_management
   ```
4. Clique em **“Gerar token de acesso”**  
   → Um token temporário será criado (válido por 1 hora).  

5. Copie esse token e cole no **Graph API Explorer**.

---

## 🧾 3. Obter o ID da Página e o Token da Página

Com o token de usuário gerado, execute esta chamada no **Graph API Explorer**:

```
GET /me/accounts
```

Isso retornará uma lista de páginas que você administra, algo como:

```json
{
  "data": [
    {
      "name": "Nome da Página",
      "id": "123456789012345",
      "access_token": "EAAGm0PX4ZCpsBA..."
    }
  ]
}
```

📌 **Anote:**
- `id` → é o **ID da Página** 
- `access_token` → é o **Token da Página**

---

## 🧱 4. Inserindo os Dados no Web App

1. Abra o sistema localmente (`python app.py`)
2. Acesse no navegador:
   👉 `http://localhost:5000/cadastro`
3. Preencha os campos:
   - **Nome da Página:** Nome de exibição (ex: “Zap de Cérebro”)
   - **ID da Página:** (copiado do passo anterior)
   - **Access Token da Página:** (copiado do passo anterior)
   - **Data de Expiração:** Informe a validade do token (caso seja temporário)

💾 Clique em **Salvar** — a página será armazenada no banco MySQL e aparecerá na lista de páginas disponíveis para postagens.

---

## 🧠 5. Testando Postagens

1. Vá para a página inicial do app.
2. Preencha:
   - Texto principal
   - Hashtags
   - Link
   - Imagem (opcional)
   - Selecione uma ou mais páginas

3. Clique em **Publicar**.
Se tudo estiver correto, o post aparecerá nas páginas selecionadas.

---

## ⚠️ 6. Renovação de Token (quando expirar)

Tokens de página normalmente expiram após **60 dias**.
Para renovar:
1. Gere novamente o token de usuário (passo 2)
2. Execute `/me/accounts` (passo 3)
3. Substitua o **access_token** antigo pelo novo no painel de páginas.

---

## 🧩 Estrutura do Projeto

```
📁 facebook_automatizador/
 ┣ 📂 static/
 ┃ ┗ style.css
 ┣ 📂 templates/
 ┃ ┣ index.html
 ┃ ┗ cadastro.html
 ┣ app.py
 ┣ requirements.txt
 ┗ README.md
```

---

## 🖥️ 7. Configuração do Banco MySQL

1. Crie um banco manualmente no MySQL Workbench:
   ```sql
   CREATE DATABASE automatizador_facebook;
   USE automatizador_facebook;
   ```

2. Crie a tabela:
   ```sql
   CREATE TABLE paginas (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome VARCHAR(255),
       page_id VARCHAR(100) UNIQUE,
       access_token TEXT,
       data_expiracao DATE
   );
   ```

3. Configure as credenciais no `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'SENHA_AQUI'
   app.config['MYSQL_DB'] = 'automatizador_facebook'
   ```
# Auto_Poster_Facebook
