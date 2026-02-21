# 📝 Bloco de Notas

Um editor de texto completo feito em Python com interface gráfica, suporte a múltiplas abas, notas adesivas, inserção de imagens e links, e muito mais.

## 📋 Funcionalidades

* Criar, abrir e salvar arquivos de texto (`.txt`)
* Sistema de **múltiplas abas** estilo navegador — abra quantos documentos quiser ao mesmo tempo
* **Renomear abas** com duplo clique ou pressionando `F2`
* Fechar abas individualmente com o botão `✖` ou `Ctrl+W`
* Escolher **fonte e tamanho** do texto com todas as fontes instaladas no sistema
* Alinhar o texto à esquerda, centro ou direita
* Inserir **links clicáveis** no texto
* Inserir **imagens** diretamente no documento
* Criar **notas adesivas** flutuantes dentro de cada aba, arrastáveis e redimensionáveis
* Barra de status com contagem de linhas e caracteres em tempo real

## 💻 Exemplo de uso

```
Barra de ferramentas:
📄 Novo | 📂 Abrir | 💾 Salvar | [Fonte] | [Tamanho] | ⬅ ≡ ➡ | 🔗 Link | 🖼️ Imagem | 📌 Nota
```

```
Abas abertas:
  Sem título  ✖     receita.txt  ✖     ideias.txt  ✖
```

```
Nota adesiva flutuante:
┌─────────────────────┐
│ 📌 Nota          ✖ │
│                     │
│  Lembrar de revisar │
│  o parágrafo 3...   │
│                     │
└──────────────────⇲──┘
```

## ⌨️ Atalhos de teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+N` | Nova aba |
| `Ctrl+O` | Abrir arquivo |
| `Ctrl+S` | Salvar arquivo |
| `Ctrl+W` | Fechar aba ativa |
| `Ctrl+A` | Selecionar tudo |
| `F2` | Renomear aba ativa |
| Duplo clique na aba | Renomear aba |

## 🧰 O que foi usado

* `tkinter` e `ttk` — para toda a interface gráfica, janelas, abas e widgets
* `PIL` / `Pillow` — para abrir, redimensionar e exibir imagens no editor
* `font.families()` — para carregar todas as fontes instaladas no sistema
* `filedialog` — para abrir e salvar arquivos com o explorador do sistema
* `webbrowser` — para abrir links clicáveis no navegador padrão
* `subprocess` — para compatibilidade com diálogos de arquivo no Linux
* `ttk.Notebook` — para o sistema de abas estilo navegador

## 🧠 Conceitos abordados

* Criação de interfaces gráficas com `tkinter`
* Gerenciamento dinâmico de widgets com `.place()` e `.pack()`
* Sistema de abas com `ttk.Notebook` e frames independentes
* Eventos de mouse e teclado com `.bind()`
* Widgets flutuantes e arrastáveis dentro da janela
* Manipulação de fontes e estilos de texto em tempo real
* Inserção de imagens em widgets `Text`
* Abertura de links com `webbrowser`

## 👩‍💻 Autora

Feito com 💟 por Aline — Projeto pessoal em Python!
