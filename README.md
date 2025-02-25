# Neresbot
*(on hold)*

O projeto consiste em aplicar um algoritmo convolucional (utilizado comumente em visão computacional), que consiste em aprendizado de máquina supervisionado, para a previsão de preços de ativos negociados na B3.

Algoritmos convolucionais costumam ser aplicados na classificação de imagens. A imagem é transformada em um tensor (ou matriz tri-dimensional), com seus eixos X e Y correspondendo aos pixels da imagem, enquanto que o eixo Z corresponde à escala RGB de cada pixel. De acordo com os padrões de cor e proximidade entre os pixels, o algoritmo identifica quais desses padrões corresponde aos rótulos fornecidas junto com o banco de dados de treino.

Neste projeto, os dados de todas as ações das empresas negociadas na B3 (exceto produtos derivados) são baixados via API Yahoo Finance, com cada incidência correspondendo a um dia de negociação), incluindo: preço de abertura, preço de fechamento, máxima, mínima, volume de negociação e dia da semana.
Para cada dia de negociação (chamado de "Dia 0"), é criado um tensor com as seguintes características:
* Primeiro eixo: cada ativo negociado;
* Segundo eixo: o dia selecionado para aquele tensor, e os N dias anteriores (do Dia 0 ao Dia N);
* Terceiro eixo: preço de **abertura**, preço de **fechamento**, **máxima**, **mínima**, **volume** de negociação e dia da **semana**;
* É escolhido um dos **ATIVO DE INTERESSE** como resposta para o modelo;
* Rótulo: decisão de **COMPRAR** (aumento de, ao menos, 10% do preço), **VENDER** (queda de ao menos 10% no preço no dia seguinte) ou **IGNORAR** (oscilação menor que 10%) comparando o Dia 0 com o Dia -1 (um dia no futuro), apenas para o ativo de interesse.

O experimento consiste em descobrir se existe um padrão de proximidade pontual que se alastra entre os ativos, os dias e as variáveis.
