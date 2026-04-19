# Pyfenstein3D — Demonstração da Versão Go

Esta página mostra capturas de tela e um GIF animado gerados diretamente pelo motor de jogo escrito em Go, sem depender de um terminal real.

As imagens foram produzidas pelo utilitário [`go/cmd/capture`](../go/cmd/capture/main.go), que inicializa o motor, simula uma sequência de ações do jogador e salva cada quadro como arquivo PNG/GIF.

---

## Tela Inicial

Posição de partida do jogador no mapa `map_1_level_1`.

![Tela inicial](captures/00_titulo.png)

---

## Andando para Frente

O jogador avança pelo corredor.

| Início do movimento | Meio do trajeto | Final do movimento |
|---|---|---|
| ![f00](captures/02_andando_frente_f00.png) | ![f07](captures/02_andando_frente_f07.png) | ![f14](captures/02_andando_frente_f14.png) |

---

## Virando para a Direita

O jogador gira 90° para a direita, revelando uma nova seção do mapa.

| Início | Durante | Final |
|---|---|---|
| ![f00](captures/03_virando_direita_f00.png) | ![f04](captures/03_virando_direita_f04.png) | ![f09](captures/03_virando_direita_f09.png) |

---

## Avançando pelo Novo Corredor

Após virar, o jogador continua andando para frente.

| Início | Meio | Final |
|---|---|---|
| ![f00](captures/04_andando_frente2_f00.png) | ![f05](captures/04_andando_frente2_f05.png) | ![f11](captures/04_andando_frente2_f11.png) |

---

## Virando para a Esquerda

O jogador vira levemente para a esquerda.

| Início | Final |
|---|---|
| ![f00](captures/05_virando_esquerda_f00.png) | ![f07](captures/05_virando_esquerda_f07.png) |

---

## Animação de Tiro

Sequência completa da animação da pistola ao atirar.

| Idle | Disparo 1 | Disparo 2 | Disparo 3 | Recuo |
|---|---|---|---|---|
| ![f00](captures/06_atirando_f00.png) | ![f02](captures/06_atirando_f02.png) | ![f04](captures/06_atirando_f04.png) | ![f06](captures/06_atirando_f06.png) | ![f09](captures/06_atirando_f09.png) |

---

## GIF Animado — Percurso Completo

Animação gerada automaticamente com 58 quadros cobrindo todo o percurso acima.

![Walkthrough animado](captures/walkthrough.gif)

---

## Como Reproduzir

Para gerar novamente as capturas localmente:

```bash
cd go
go run ./cmd/capture/
```

As imagens serão salvas em `docs/captures/`.

Para executar o jogo interativamente (Windows ou terminal com suporte a ANSI):

```bash
cd go
go run .
```
