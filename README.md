# pyfenstein3d
![Codecov](https://img.shields.io/codecov/c/github/grrriiim/pyfenstein3d?color=green&label=coverage&logo=python&token=dc139c33-e7e9-4e28-89bf-68c9e9913c02)


Projeto realizado em python com intuido educacional de tentar reproduzir o jogo [Wolfenstein 3d](https://pt.wikipedia.org/wiki/Wolfenstein_3D) no prompt de comando.

Utilizando a fonte __Consolas__, é possivel considerar que cada __2 caracteres__ representem __1 pixel__. E assim "_renderizar_" qualquer imagem no prompt utilizando [ANSI escap code](https://en.wikipedia.org/wiki/ANSI_escape_code) para dar cor.

Para manter o número de quadros por segundo estável, o projeto foi desenvolvido considerando uma renderização de 100x62

![](docs/readme_gif1.gif)

## Instalação

Para executar o projeto é necessario instalar [python 3](https://www.python.org/downloads/windows/)

Instale [pip](https://pypi.org/project/pip/) utilizando o commando:
```shell
python get-pip.py
```
Execute o comando para realizar a instalação do pyfenstein3d:
```shell
python -m pip install git+https://github.com/GrrriiiM/pyfenstein3d.git@master#egg=pyfenstein3d
```

## Configuração
Devido a performance do prompt cmd, o pyfenstein3d roda em uma resolução de 100x62
Para ter uma visualização ideal do jogo realize as seguintes instruções

1. Clique na barra superior do prompt com o botão direito e selecione __Propriedades__
![](docs/readme_image1.jpg)

2. Clique na aba __Fonte__
![](docs/readme_image2.jpg)

3. Altere a __Tamanho__ para __10__
![](docs/readme_image3.jpg)

4. Altere a __Fonte__ para __Consolas__
![](docs/readme_image4.jpg)

5. Clique na aba __Layout__
![](docs/readme_image5.jpg)

4. Altere o __Tamanho da Janela__ para __largura 200__ e __altura 62__
![](docs/readme_image6.jpg)


## Execução
Após instalação e configuração do prompt, execute o modulo com o comando abaixo
```shel
python -m pyfenstein3d
```

## Comandos
|Comando            | Tecla            |
|-------------------|------------------|
|Andar para frente  | __W__            |
|Andar para trás    | __S__            |
|Andar para esquerda| __A__            |
|Andar para direita | __D__            |
|Virar para esquerda| __Seta esquerda__|
|Virar para direita | __Seta direta__  |
|Abrir porta        | __Espaço__       |

## Desenvolvimento
- [X] "Renderizar Pixel"
- [x] Raycasting 2d
- [X] Raycasting "3d"
- [X] Textura parede
- [X] Sprites
- [X] Animação
- [X] Portas
- [X] Arma
- [ ] Tiro
- [ ] Interação itens
- [ ] Inimigo
- [ ] Inteligencia artificial