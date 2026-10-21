import numpy as np
import streamlit as st


def ampliar(imagem, k=30):
    return imagem.repeat(k, axis=0).repeat(k, axis=1)


st.title("Imagem como matriz")

# Experimentos da aula: imagem 8x8 em tons de cinza
imagem = np.zeros((8, 8), dtype=np.uint8)
imagem[2, 5] = 255        # um pixel branco (linha 2, coluna 5)
imagem[4:, :] = 128       # metade de baixo em cinza
st.image(ampliar(imagem))
st.write(imagem)

# Atividade: bandeira do Cazaquistão (cores descobertas com o conta-gotas do Paint)
st.header("Bandeira do Cazaquistão")

AZUL = (0, 171, 194)      # #00ABC2
OURO = (255, 236, 45)     # #FFEC2D

H, W = 40, 80
bandeira = np.zeros((H, W, 3), dtype=np.uint8)
bandeira[:] = AZUL        # fundo azul-celeste

# sol: disco + 16 raios com largura constante
cy, cx = 11.5, 44.5
yy, xx = np.mgrid[0:H, 0:W]
dx, dy = xx - cx, yy - cy
dist = np.hypot(dx, dy)
ang = np.arctan2(dy, dx)
passo = 2 * np.pi / 16
delta = (ang + passo / 2) % passo - passo / 2          # desvio até o raio mais próximo
dist_raio = np.abs(dist * np.sin(delta))                # distância perpendicular ao raio
disco = dist <= 5.0
raios = (dist >= 6.6) & (dist <= 10.2) & (dist_raio <= 0.8)
bandeira[disco | raios] = OURO

# águia: metade esquerda (14 colunas), espelhada para formar a águia inteira
meia = [
    ".............#",
    ".............#",
    "#...........##",
    "##........####",
    ".#############",
    "..############",
    "..#.#.#.#...##",
    "............##",
    "............##",
    "............##",
    "...........###",
    "..........####",
    ".........#.#.#",
]
aguia = np.array([[c == "#" for c in (r + r[::-1])] for r in meia])
ay, ax = 23, int(round(cx)) - aguia.shape[1] // 2
bandeira[ay:ay + aguia.shape[0], ax:ax + aguia.shape[1]][aguia] = OURO

# ornamento vertical na esquerda: 4 elos ligados, perto da borda sem tocar
elo = [
    "..##..",
    ".####.",
    "##..##",
    "#....#",
    "#....#",
    "##..##",
    ".####.",
    "..##..",
]
ligacao = ["..##..", "..##.."]
corrente = []
for i in range(4):
    corrente += elo
    if i < 3:
        corrente += ligacao
for linha_n, linha in enumerate(corrente):
    for coluna_n, c in enumerate(linha):
        if c == "#":
            bandeira[1 + linha_n, 3 + coluna_n] = OURO   # sobra 1 linha de azul em cima e embaixo

st.image(ampliar(bandeira))