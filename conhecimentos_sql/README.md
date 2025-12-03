Para as questões seguintes, considere a seguinte estrutura de tabela:

Produto -> Id, descrição, unidade de medida, valor, tamanho em metros quadrados.
Armazém -> Id, nome, espaço disponível em metros quadrados.
ProdxArmazem -> IdProduto, IdArmazem, Qtd.



Considerando o banco de dados anterior e usando linguagem SQL.
1. Realize as criações das tabelas, definindo seus relacionamentos e chaves.
2. Crie uma consulta que informe todos os armazéns com o total ocupado.
3. Crie uma procedure que dado um produto como parâmetro, informe os 5 armazéns com maior quantidade desse
produto.
4. Crie um relatório que mostre os produtos que estão em mais armazéns (em quantidade de armazéns e não em
acumulado).
5. Crie uma consulta que mostre os produtos sem armazém alocados.
6. Crie um relatório que mostre a lista de armazém com maior valor financeiro para empresa em ordem decrescente.