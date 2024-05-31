# BD: Trabalho Prático APF-T

**Grupo**: P11G1
- Rui Machado, MEC: 113765
- Martim Santos, MEC: 2000


## Introdução
 
Este projeto tem o objetivo de explorar o universo do jogo “League Of Legends” e ajudar novos jogadores a perceber o funcionamento geral do jogo, que é bastante complexo. Funciona como uma simulação do jogo e dá a conhecer a vasta gama de Champions (personagens), Skins (personalização de champions) e itens do jogo. 

Nesta entrega, incluímos a análise de requisitos, o Diagrama Entidade-Relacionamento, o Esquema Relacional, os ficheiros para a criação e inicialização da base de dados, além dos ficheiros contendo as funções necessárias para realizar consultas, inserções, atualizações e remoções de dados na base. Também fornecemos o código que implementa uma interface para executar todas essas operações.


## ​Análise de Requisitos 

O Utilizador pode…
- Criar uma conta;
- Dar login/logout;
- Visualizar o seu inventário;
- Comprar Champions/Skins/Items;
- Abrir Chests (item), e resgatar um item surpresa;
- Simular a compra da moeda do jogo com dinheiro “real”;
- Aplicar filtros de pesquisa em todas as suas procuras;
- Dar undo (reverter) uma compra feita
- Simular um jogo num mapa escolhido;;
- Visualizar o histórico de compras/jogos;
- Visualizar o seu inventário;
- Aumentar o seu Rank através da simulação de jogos;


## DER - Diagrama Entidade Relacionamento

### Versão final

![DER Diagram!](DER.png "AnImage")

## ER - Esquema Relacional

### Versão final

![ER Diagram!](MR.png "AnImage")


## ​SQL DDL - Data Definition Language

[SQL DDL File](sql/01_ddl.sql "SQLFileQuestion")

## SQL DML - Data Manipulation Language

Uma secção por formulário.
A section for each form.

### Formulario exemplo/Example Form

![Exemplo Screenshot!](screenshots/screenshot_1.jpg "AnImage")

```sql
-- Show data on the form
SELECT * FROM MY_TABLE ....;

-- Insert new element
INSERT INTO MY_TABLE ....;
```

...

## Normalização


Ao revermos o nosso sistema, verificámos que este já se encontrava conforme a terceira forma normal. Tal deve-se ao cuidado que tivemos ao analisar o Diagrama de Entidade e Relacionamento (DER) antes de elaborarmos o Esquema Relacional. Desde o início, assegurámo-nos de que as tabelas continham atributos atómicos, evitámos incorporar relações dentro de outras e eliminámos quaisquer dependências parciais.

## Stored Procedures

## Triggers

## UDF

## Indexs

Para melhorar a velocidade das pesquisas de champions e skins, optámos por utilizar índices. Apesar da nossa base de dados ser de tamanho relativamente pequeno, decidimos implementar esta estrutura nessas tabelas devido à sua utillizaçao frequente.

```sql
-- Create an index to speed
CREATE INDEX index_name ON table_name (column1, column2, ...);
```

## Views







 