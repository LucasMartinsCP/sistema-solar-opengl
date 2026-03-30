# Simulação do Sistema Solar com PyOpenGL

Este projeto consiste em uma simulação 3D do sistema solar desenvolvida em Python utilizando **PyOpenGL**, como atividade acadêmica da disciplina de **Computação Gráfica** no curso **Bacharelado em Ciência da Computação**, **IFPR - Campus Pinhais**.

A aplicação renderiza o Sol, planetas, lua, anéis de Saturno e um campo de estrelas, com animações de rotação e translação, além de aplicação de texturas realistas.

---

## Objetivo

O objetivo deste projeto é aplicar conceitos fundamentais de computação gráfica, incluindo:

- Renderização 3D
- Transformações geométricas (translação e rotação)
- Mapeamento de texturas
- Iluminação básica
- Animação em tempo real
- Uso de bibliotecas gráficas em Python

---

## Tecnologias Utilizadas

- Python 3
- PyOpenGL
- GLUT
- PIL (Python Imaging Library)

---

## Funcionalidades

- Sol central com textura
- Planetas orbitando com velocidades proporcionais
- Terra com Lua em órbita
- Campo de estrelas gerado aleatoriamente
- Anéis de Saturno com transparência e textura
- Rotação própria dos planetas
- Encerramento automático da simulação após 50 segundos

---

## Estrutura do Projeto

```text
sistema-solar/
│
├── img/
│ ├── sol.jpg
│ ├── mercurio.jpg
│ ├── venus.jpg
│ ├── terra.jpg
│ ├── lua.jpg
│ ├── marte.jpg
│ ├── jupiter.jpg
│ ├── saturno.jpg
│ ├── urano.jpg
│ ├── netuno.jpg
│ └── aneis_saturno.png
│
├── sistema_solar.py
└── README.md
```
---

## Como Executar

### 1. Instale as dependências

```bash
pip install PyOpenGL PyOpenGL_accelerate Pillow
```
### 2. Execute o projeto

```bash
python sistema_solar.py
```
