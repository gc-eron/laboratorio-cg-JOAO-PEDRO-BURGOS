import numpy as np
import streamlit as st

def ampliar(img, f=12):
    return np.kron(img, np.ones((f, f, 1), dtype=np.uint8))

AZUL = (0, 171, 194)
OURO = (255, 236, 45)

H, W = 40, 80
bandeira = np.zeros((H, W, 3), dtype=np.uint8)
bandeira[:] = AZUL

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

# águia: metade esquerda (14 colunas) espelhada
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

# ornamento vertical (koshkar-muiz simplificado): 4 elos ligados, perto da borda sem tocar
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
for k in range(4):
    corrente += elo
    if k < 3:
        corrente += ligacao
for j, linha in enumerate(corrente):
    for k, c in enumerate(linha):
        if c == "#":
            bandeira[1 + j, 3 + k] = OURO          # começa na linha 1: sobra 1 linha de azul em cima e embaixo

st.image(ampliar(bandeira))