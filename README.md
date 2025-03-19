# Case de dados
Repositorio destinado a resolução do case de dados, aqui se encontram todas as intrucoes para rodar o codigo bem como a estrutura e definicao dos dados.


# Iniciando o docker
Para iniciar o docker, basta rodar o comando abaixo no iretorio raiz do projeto.
```bash
docker compose up
```
Nesse momento, o docker ira subir os bancos de dados fonte\alvo e a API, apos isso, o endponit http://localhost:5000/data ficara acessivel para resgatar os dados do banco fonte.

# Estrutura dos dados no banco fonte
O banco de dados fonte é um banco de dados relacional, com a seguinte estrutura:

- Tabela: `data`
  - Colunas:
    - `timestamp` (datetime): Data e hora da medição com frequencia 1-minutal a contar do momento em que o banco foi criado
    - `wind_speed` (float): Velocidade do vento em km/h
    - `power` (float): Potência gerada em MW
    - `ambient_temperature` (float): Temperatura ambiente em graus Celsius

Os dados desse banco são gerados automaticamente assim que o banco é criado, a data e hora da primeira medição é a data e hora de criação desse. Os dados são gerados por minuto ate um periodo de 10 anos a partir da data de criacao do banco.
 
# Estrutura dos dados no banco alvo
O banco de dados alvo é um banco de dados relacional, com a seguinte estrutura:

  signal_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    mean = Column(Float)
    min = Column(Float)
    max = Column(Float)
    std = Column(Float)
    timestamp = Column(DateTime)

- Tabela: `signal`
    - Colunas:
        - `signal_id` (int): Identificador único da medição
        - `name` (str): Nome da variável medida
        - `mean` (float): Média dos valores da medição
        - `min` (float): Valor mínimo da medição
        - `max` (float): Valor máximo da medição
        - `std` (float): Desvio padrão dos valores da medição
        - `timestamp` (datetime): Data e hora da medição com frequencia 10-minutal a contar da data escolhida para o inicio da medição


# Estrutura da API
A API possui um único endpoint, que é acessível através do método GET no endereço http://localhost:5000/data que aceita duas variaveis de query:
- `day` (str): Data e hora de início da medição no formato `DD/MM/YYYY`
- `variables` (str): Variáveis a serem retornadas separadas por vírgula. As variáveis disponíveis são `wind_speed`, `power` e `ambient_temperature`. Caso não seja passada nenhuma variável, todas as variáveis serão retornadas.

Exemplo de requisição: http://localhost:5000/data/?day=19/03/2025&variables=power,wind_speed


# Codigo python
O codigo python se encontra no arquivo `./etl/main.ipynb` e é responsável por realizar a extração dos dados do banco fonte, o processamento desses dados e a inserção dos dados processados no banco alvo.

Importante ressaltar que o codigo python foi desenvolvido em um notebook, e para rodar o codigo, basta executar todas as celulas do notebook.

As bibliotecas se encontram no arquivo `./etl/requirements.txt` e podem ser instaladas com o comando abaixo:
```bash
pip install -r requirements.txt
```