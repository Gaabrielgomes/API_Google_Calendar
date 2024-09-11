### Para a utilização dessa API integrada com o Google Calendar, siga os passos abaixo:

1. **Criar uma conta Google:**
   Caso ainda não tenha uma conta Google, você pode criar uma [aqui](https://accounts.google.com/signup).

2. **Cadastrar um novo projeto no Google Cloud:**
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - No canto superior esquerdo, clique em "Selecionar projeto" e, em seguida, clique em "Novo Projeto".
   - Dê um nome ao projeto e clique em "Criar".

3. **Gerar credenciais para o projeto:**
   - Acesse o menu "APIs e Serviços" > "Credenciais".
   - Clique em "Criar credenciais" e selecione "ID do cliente OAuth 2.0".
   - Escolha o tipo de aplicativo (por exemplo, "Aplicativo Web").
   - Adicione os URIs de redirecionamento autorizados, caso necessário, e clique em "Criar".
   - Faça o download do arquivo de credenciais gerado, geralmente chamado de `credentials.json`.

4. **Configurar a API do Google Calendar:**
   - No menu "Biblioteca" do Google Cloud Console, pesquise por "Google Calendar API" e ative-a para o seu projeto.
   - Retorne à seção "APIs e Serviços" > "Credenciais" para verificar se as credenciais estão ativas.

5. **Implementar na pasta:**
   - Com `credentials.json` baixado, mova-o para a pasta principal "myproject".

6. **Gerar token:**
   - Execute "gerar_token.py"

7. **Execução:**

   *Método GET*
   - Para adquirir todos os eventos, acesse: `http://localhost:8000/`.
   - Para buscar um evento específico por id, copie o id do evento em questão e execute esse modelo de url: `http://localhost:8000/event/<id copiada>/`
   - Para buscar os eventos que estão cadastrados num determinado período, use esse modelo de url: `http://localhost:8000/events/<início>|<fim>/`
     e atente-se para usar datas com esse padrão: `2024-09-11T16:30:00-03:00`.
   - Para buscar eventos por sumário(título), pesquise pela url desta forma: `http://localhost:8000/events/<título>`

   *Método POST*
   - Postar um novo evento pode ser feito por `http://localhost:8000/new-event/` com programas como Postman e Insomnia ao selecionar em "Body" o método "raw",
     que tornará possível o usuário escrever em modelo JSON o título, data de início e data de fim do evento, seguindo o modelo abaixo:
     ```json
     {
       "summary": "título do evento",
       "start_time": "2024-09-15T10:00:00-03:00",
       "end_time": "2024-09-15T11:00:00-03:00",
     }
     ```

   *Método PUT*
    - Para alterar um evento, a lógica é quase a mesma do método POST, com as diferenças:
      url: `http://localhost:8000/update-event/`,
        ```json
        {
          "id": "id do evento",
          "summary": "título do evento",
          "start_time": "2024-09-15T10:00:00-03:00",
          "end_time": "2024-09-15T11:00:00-03:00",
        }
        ```
    - Nesse método, fica a critério do usuário o quê será alterado, exceto o id do evento.

   *Método DELETE*
   - Para deletar um evento é simples, basta executar a url: `http://localhost:8000/delete-event/` adicionando o JSON:
     ```json
     {
       "id": "id do evento",
     }
     ```
     E pronto, evento deletado.


---
