# Pset 2 de linguagem de programação
## Processamento de imagem do MIT 6.009
Esse é o resultado final do exercício requisitado pelo professor Abrantes, com base no processamento de imagem, feito em linguagem python com os objetivos de implementar as funções BLURRED(borrar), INVERTED(inverter), SHARPENED(nitidez) e EDGES(bordas) e também as resoluções de algumas questões requeridas.
## Questão 1
#### Se você passar essa imagem pelo filtro de inversão, qual seria o output esperado?
A saída que se espera (4, 1, [226, 166, 119, 55]). Por que o filtro irá refletir os pixels sobre o valor de cinza. Dessa forma, os parâmetros que foram passados (4, 1, [29, 89, 136, 200]),serão invertidos resultando em [226, 166, 119, 55], utilizando a fórmula 255-c, sendo C os pixels da imagem original.
## Questão 2
#### faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste TestInvertido (incluindo especificamente o que você acabou de criar). Execute seu filtro de inversão na imagem imagens_teste/peixe.png, salve o resultado como uma imagem PNG e salve a imagem em seu repositório GitHub.
![pycharm64_J3zN28gdhk](https://user-images.githubusercontent.com/95299280/188292760-b37f10c1-d450-4ff3-bc5a-9f8d28c31b28.png)

![pycharm64_1IukjhKC9n](https://user-images.githubusercontent.com/95299280/188292745-fed5829a-5495-49ab-ad93-b5372feaf9d2.png)

![peixe](https://user-images.githubusercontent.com/95299280/188292786-d88b436c-52a3-4d6e-b86e-a25283e62355.png)
## Questão 3
####  considere uma etapa de correlacionar uma imagem com o seguinte kernel:

#### 0.00 -0.07 0.00 

#### -0.45 1.20 -0.25

#### 0.00 -0.12 0.00

#### Qual será o valor do pixel na imagem de saída no local indicado pelo destaque vermelho?
Utilizando a fórmula passada no documento para a realização

![opera_RutORpexFa](https://user-images.githubusercontent.com/95299280/188292938-2e1dd1dc-1d87-4f0c-85cc-5c6b99988214.png)

Resultará em :
0.00 x 80 = 0 -0,07 x 53 = -3, 71 0.00 x 99 = 0 -0.45 x 129 = -58.05 1.20 x 127 = 152.4 -0.25 x 148 = -37 0.00 x 175 = 0 -0.12 x 174 = -20.88 0.00 x 193 = 0
0 + (-3, 71) + 0 + (-58.05) + 152.4 + -37 + 0 + -20.88 + 0 = 32.76.

## Questão 4
#### quando você tiver implementado seu código, tente executá-lo em imagens_teste/porco.png com o seguinte kernel 9 × 9:

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 1 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### 0 0 0 0 0 0 0 0 0

#### Ao rodar esse kernel, salve a imagem resultante em seu repositório GitHub.

![pycharm64_ZVM0MbR8aU](https://user-images.githubusercontent.com/95299280/188293271-f8e860f7-32fd-49b6-9f81-5306531a6639.png)

O resultado será

![porco](https://user-images.githubusercontent.com/95299280/188293075-fa287a43-01bc-4937-a3d6-9d8eb4670e19.png)

### Questão 4 parte 2:
#### Implemente o método borrado na classe Imagem, que recebe um número N e retorna uma nova Imagem com altura e largura iguais às dimensões da imagem de entrada que foi desfocada com um kernel de desfoque de caixa de tamanho apropriado. Tome cuidado para produzir valores de brilho inteiros (round(valor), por exemplo) no intervalo [0, 255]. Ou seja, em muitos casos, você precisará recortar valores inteiros explicitamente para esse intervalo. Quando você terminar e seu código passar em todos os testes relacionados ao desfoque, execute seu filtro na imagem imagens_teste/gato.png com um kernel de desfoque de caixa de tamanho 5, salve o resultado como uma imagem PNG e faça o upload para seu repositório GitHub.

![pycharm64_vo4Xw4tF7k](https://user-images.githubusercontent.com/95299280/188293234-3b229628-eb91-41f0-be2e-13461e2f2ffa.png)

![pycharm64_VmNFRcukI1](https://user-images.githubusercontent.com/95299280/188293293-fc7635d1-d68b-4589-9e2d-16c761eaa602.png)

O resultado será

![cat](https://user-images.githubusercontent.com/95299280/188293124-8cf7f3e6-9967-4c53-9af0-96ed12f313ea.png)

## Questão 5
#### Se quisermos usar uma versão desfocada B que foi feita com um kernel de desfoque de caixa de 3 × 3, que kernel k poderíamos usar para calcular toda a imagem nítida com uma única correlação? Justifique sua resposta mostrando os cálculos.Implemente uma máscara de não nitidez como o método focado da classe Imagem, onde n denota o tamanho do kernel de desfoque que deve ser usado para gerar a cópia desfocada da imagem. Este método deve retornar uma nova imagem mais nítida. Você pode implementar isso como uma correlação única ou usando uma subtração explícita, mas se você usar uma subtração explícita, certifique-se de não fazer nenhum arredondamento até o final (a versão desfocada intermediária não deve ser arredondada ou cortada de forma alguma. Quando terminar e seu código passar nos testes relacionados à nitidez, execute seu filtro de nitidez na imagem imagens_teste/python.png usando um kernel de tamanho 11, salve o resultado como uma imagem PNG e faça o upload no seu repositório GitHub.

![pycharm64_VYZo1zJ64L](https://user-images.githubusercontent.com/95299280/188293391-c58d8039-2145-4197-aa83-e5ebaddecebb.png)

![pycharm64_rKfBtEhBa6](https://user-images.githubusercontent.com/95299280/188333116-b5a14063-2e9e-45cb-9ee4-317550f0b476.png)

O resultado será

![python](https://user-images.githubusercontent.com/95299280/188293404-fd6e1500-cc8b-46ad-a5e4-f1df0810061e.png)

## Questão 6
#### Explique o que cada um dos kernels acima, por si só, está fazendo. Tente executar mostrar nos resultados dessas correlações intermediárias para ter uma noção do que está acontecendo aqui.Implemente o detector de bordas como o método bordas dentro da classe Imagem. O método deve retornar uma nova instância de Imagem resultante das operações acima. Quando terminar e seu código passar nos testes de detecção de borda, execute seu detector de borda na imagem imagens_teste/obra.png, salve o resultado como uma imagem PNG e faça o upload para seu repositório GitHub.

![opera_28BKFGxkUA](https://user-images.githubusercontent.com/95299280/188333082-32e17e82-04b0-4ceb-943b-4acb50d0ca10.png)

O que cada um dos kerneis acima fazem é, o KX detecta as bordas verticais e o KY detecta as bordas horizontais.

![pycharm64_qBN4GctPkk](https://user-images.githubusercontent.com/95299280/188293501-0179ad9b-3302-4e81-b0ea-dec08cd7aa38.png)

![pycharm64_oZ1ZchfZaC](https://user-images.githubusercontent.com/95299280/188293503-cd2f4b80-ebe3-4000-9e19-cfcc235bbc6b.png)

O resultado será

![obra](https://user-images.githubusercontent.com/95299280/188293514-28a4938d-5797-46e0-90cd-08e18b7b5f8d.png)


