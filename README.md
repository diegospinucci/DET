# Gerador de Relatório de Testes (DET)

## 📌 Contexto da Aplicação
O **DET (Gerador de Relatório de Testes)** é uma aplicação desenvolvida em **Python + PyQt5** que facilita a criação de relatórios de testes manuais.  
O objetivo é permitir que o QA ou desenvolvedor registre cenários de teste, adicione evidências (imagens importadas ou coladas diretamente do clipboard), e exporte tudo em um **PDF organizado e profissional**.

Principais funcionalidades:
- Cadastro de cenários com título, status (Aprovado/Reprovado) e logs.
- Adição de evidências por **importação de arquivos** ou **colagem direta (Ctrl+V / Command+V)**.
- Edição, remoção e reordenação de cenários.
- Exportação para PDF com:
  - Índice de cenários.
  - Detalhes de cada cenário.
  - Evidências anexadas.
  - Página final com **resumo gráfico** dos resultados.

---

## ⚙️ Requisitos
Antes de rodar o projeto, certifique-se de ter instalado:
- Python 3.8 ou superior
- Bibliotecas:
  - `PyQt5`
  - `fpdf`

Instalação das dependências:
```bash
pip install PyQt5 fpdf


## 🚀 Como instalar

1 - Clone este repositório ou copie os arquivos para sua máquina.
2 - Crie um ambiente virtual (opcional, mas recomendado):

python -m venv ambiente
source ambiente/bin/activate   # Linux/Mac
ambiente\Scripts\activate      # Windows

3 - Instale as dependências listadas acima.
4 - Execute o arquivo principal:

python det.py

## 🖥️ Como usar

1.  Abra a aplicação com python det.py.
2.  Preencha:
  ⁠◦  Título geral do teste
  ⁠◦  Nome do cenário
  ⁠◦  Resultado do cenário (Aprovado/Reprovado)
  ⁠◦  Logs/descrição
3.  Adicione evidências:
  ⁠◦  Clique em Adicionar imagem para importar da pasta.
  ⁠◦  Clique em Colar imagem (Ctrl+V / Command+V) para colar direto do clipboard.
4.  Salve o cenário com Salvar cenário.
5.  Gerencie cenários:
  ⁠◦  Editar, remover ou reordenar conforme necessário.
6.  Exporte o relatório final em PDF com Exportar PDF.

## 📊 Estrutura do PDF

O relatório gerado contém:

•  Página inicial: título e índice dos cenários.
•  Detalhes de cada cenário: nome, status, logs e evidências.
•  Página final: resumo dos testes com gráfico de barras mostrando aprovados e reprovados.

## 📂 Organização dos arquivos

•  det.py → código principal da aplicação.
•  relatorios/ → pasta onde ficam as imagens coladas/importadas.
•  relatorio_final_YYYYMMDD_HHMMSS.pdf → relatórios exportados com timestamp no nome.

## 👨‍💻 Autor

Projeto desenvolvido por Diego Spinucci Cavalcanti, com foco em facilitar o trabalho de QA e desenvolvedores na documentação de testes.
