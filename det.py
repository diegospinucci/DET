import sys
import os
from datetime import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QMessageBox, QLineEdit, QLabel, QListWidget, QComboBox
)
from fpdf import FPDF

class PDFComRodape(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

class RelatorioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Relatório de Testes")
        self.layout = QVBoxLayout()

        # Cria área de rolagem
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Container para o layout
        container = QWidget()
        container.setLayout(self.layout)
        scroll.setWidget(container)

        # Layout principal da janela
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.resize(600, 800)      

        # Título geral
        self.layout.addWidget(QLabel("Caso de Teste:"))
        self.entry_titulo = QLineEdit()
        self.layout.addWidget(self.entry_titulo)

        # Nome do cenário
        self.layout.addWidget(QLabel("Nome do cenário:"))
        self.entry_nome = QLineEdit()
        self.layout.addWidget(self.entry_nome)

        # Status do cenário (aprovado/reprovado)
        self.layout.addWidget(QLabel("Resultado do cenário:"))
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Aprovado", "Reprovado"])
        self.layout.addWidget(self.combo_status)

        # Logs/descrição
        self.layout.addWidget(QLabel("Logs/descrição:"))
        self.text_log = QTextEdit()
        self.layout.addWidget(self.text_log)

        # Botão adicionar imagem
        self.btn_imagem = QPushButton("Adicionar imagem")
        self.btn_imagem.clicked.connect(self.adicionar_imagem)
        self.layout.addWidget(self.btn_imagem)

        # Botão colar imagem
        self.btn_colar = QPushButton("Colar imagem da área de Transferência")
        self.btn_colar.clicked.connect(self.colar_imagem)
        self.layout.addWidget(self.btn_colar)        

        # Lista de imagens temporárias (com possibilidade de remover)
        self.list_imagens = QListWidget()
        self.layout.addWidget(self.list_imagens)

        self.btn_remover_img = QPushButton("Remover imagem selecionada")
        self.btn_remover_img.clicked.connect(self.remover_imagem)
        self.layout.addWidget(self.btn_remover_img)

        # Botão salvar cenário
        self.btn_salvar = QPushButton("Salvar cenário")
        self.btn_salvar.clicked.connect(self.salvar_cenario)
        self.layout.addWidget(self.btn_salvar)

        # Lista de cenários salvos
        self.list_cenarios = QListWidget()
        self.layout.addWidget(self.list_cenarios)

        # Botões editar, remover e reordenar
        self.btn_editar = QPushButton("Editar cenário selecionado")
        self.btn_editar.clicked.connect(self.editar_cenario)
        self.layout.addWidget(self.btn_editar)

        self.btn_remover = QPushButton("Remover cenário selecionado")
        self.btn_remover.clicked.connect(self.remover_cenario)
        self.layout.addWidget(self.btn_remover)

        self.btn_up = QPushButton("Mover cenário para cima")
        self.btn_up.clicked.connect(self.mover_cenario_cima)
        self.layout.addWidget(self.btn_up)

        self.btn_down = QPushButton("Mover cenário para baixo")
        self.btn_down.clicked.connect(self.mover_cenario_baixo)
        self.layout.addWidget(self.btn_down)

        # Botão exportar PDF
        self.btn_exportar = QPushButton("Exportar PDF")
        self.btn_exportar.clicked.connect(self.exportar_pdf)
        self.layout.addWidget(self.btn_exportar)

        self.setLayout(self.layout)

        # Estruturas de dados
        self.cenarios = []
        self.imagens_temp = []

    def colar_imagem(self):
        clipboard = QApplication.clipboard()
        mime = clipboard.mimeData()
        if mime.hasImage():
            img = clipboard.image()
            if not img.isNull():
                os.makedirs("relatorios", exist_ok=True)
                nome_arquivo = f"evidencia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                caminho = os.path.join("relatorios", nome_arquivo)
                img.save(caminho, "PNG")
                self.imagens_temp.append(caminho)
                self.list_imagens.addItem(os.path.basename(caminho))
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem encontrada no clipboard.")

    def adicionar_imagem(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar imagem", "", "Imagens (*.png *.jpg *.jpeg)")
        if caminho:
            self.imagens_temp.append(caminho)
            self.list_imagens.addItem(os.path.basename(caminho))

    def remover_imagem(self):
        idx = self.list_imagens.currentRow()
        if idx >= 0:
            self.imagens_temp.pop(idx)
            self.list_imagens.takeItem(idx)

    def salvar_cenario(self):
        nome = self.entry_nome.text().strip()
        log = self.text_log.toPlainText().strip()
        status = self.combo_status.currentText()
        if not nome:
            QMessageBox.warning(self, "Erro", "Informe o nome do cenário.")
            return
        self.cenarios.append({
            "nome": nome,
            "log": log,
            "status": status,
            "imagens": self.imagens_temp.copy()
        })
        self.list_cenarios.addItem(f"{nome} ({status})")

        # Limpa campos
        self.entry_nome.clear()
        self.text_log.clear()
        self.list_imagens.clear()
        self.imagens_temp.clear()

        QMessageBox.information(self, "Sucesso", f"Cenário '{nome}' salvo como {status}.")





    def editar_cenario(self):
        idx = self.list_cenarios.currentRow()
        if idx < 0:
            QMessageBox.warning(self, "Erro", "Selecione um cenário para editar.")
            return
        c = self.cenarios[idx]
        # Carrega dados do cenário selecionado nos campos
        self.entry_nome.setText(c["nome"])
        self.text_log.setPlainText(c["log"])
        self.list_imagens.clear()
        self.imagens_temp = c["imagens"].copy()
        for img in self.imagens_temp:
            self.list_imagens.addItem(os.path.basename(img))
        # Remove da lista para salvar novamente depois
        self.cenarios.pop(idx)
        self.list_cenarios.takeItem(idx)
        QMessageBox.information(self, "Editar", "Cenário carregado para edição. Após ajustar, clique em 'Salvar cenário'.")

    def remover_cenario(self):
        idx = self.list_cenarios.currentRow()
        if idx < 0:
            QMessageBox.warning(self, "Erro", "Selecione um cenário para remover.")
            return
        nome = self.cenarios[idx]["nome"]
        self.cenarios.pop(idx)
        self.list_cenarios.takeItem(idx)
        QMessageBox.information(self, "Removido", f"Cenário '{nome}' removido.")

    def mover_cenario_cima(self):
        idx = self.list_cenarios.currentRow()
        if idx > 0:
            self.cenarios[idx-1], self.cenarios[idx] = self.cenarios[idx], self.cenarios[idx-1]
            item = self.list_cenarios.takeItem(idx)
            self.list_cenarios.insertItem(idx-1, item)
            self.list_cenarios.setCurrentRow(idx-1)

    def mover_cenario_baixo(self):
        idx = self.list_cenarios.currentRow()
        if idx < len(self.cenarios)-1 and idx >= 0:
            self.cenarios[idx+1], self.cenarios[idx] = self.cenarios[idx], self.cenarios[idx+1]
            item = self.list_cenarios.takeItem(idx)
            self.list_cenarios.insertItem(idx+1, item)
            self.list_cenarios.setCurrentRow(idx+1)

    def exportar_pdf(self):
        if not self.cenarios:
            QMessageBox.warning(self, "Erro", "Nenhum cenário salvo.")
            return

        titulo = self.entry_titulo.text().strip() or "Relatório de Testes"
        pdf = PDFComRodape()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Primeira página: título e índice
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=titulo, ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        pdf.ln(15)

        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Índice de Cenários", ln=True, align="L")
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for i, c in enumerate(self.cenarios, start=1):
            pdf.cell(0, 10, txt=f"{i}. {c['nome']} ({c['status']})", ln=True, align="L")

    # Páginas de cada cenário
        for i, c in enumerate(self.cenarios, start=1):
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt=f"Cenário {i}: {c['nome']} ({c['status']})", ln=True, align="L")
            pdf.ln(5)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Evidências:\n{c['log']}")
            pdf.ln(5)
            for img in c["imagens"]:
                if os.path.exists(img):
                    pdf.image(img, w=100)
                    pdf.ln(5)

        # ✅ Página final: resumo (fora do loop)
        total = len(self.cenarios)
        aprovados = sum(1 for c in self.cenarios if c["status"] == "Aprovado")
        reprovados = sum(1 for c in self.cenarios if c["status"] == "Reprovado")

        # cálculo dos percentuais
        percentual_aprovados = (aprovados / total * 100) if total > 0 else 0
        percentual_reprovados = (reprovados / total * 100) if total > 0 else 0

        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Resumo dos Testes", ln=True, align="C")
        pdf.ln(10)

        # imprime lista de reprovados, se houver
        cenarios_reprovados = [c["nome"] for c in self.cenarios if c["status"] == "Reprovado"]
        if cenarios_reprovados:
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt="Cenários Reprovados:", ln=True)
            for nome in cenarios_reprovados:
                pdf.cell(0, 10, txt=f"- {nome}", ln=True)
            pdf.ln(10)

        # gráfico de barras simples com FPDF
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Gráfico de Resultados:", ln=True)

        max_width = 100

        # barra de aprovados (verde)
        pdf.set_fill_color(0, 200, 0)  # verde
        pdf.cell(aprovados / total * max_width, 10, txt=f"Aprovados {aprovados} ({percentual_aprovados:.1f}%)", ln=True, fill=True)

        # barra de reprovados (vermelho)
        pdf.set_fill_color(200, 0, 0)  # vermelho
        pdf.cell(reprovados / total * max_width, 10, txt=f"Reprovados {reprovados} ({percentual_reprovados:.1f}%)", ln=True, fill=True)

        # gera nome com data e hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"DET_{timestamp}.pdf"

        pdf.output(nome_arquivo)
        QMessageBox.information(self, "PDF Gerado", f"✅ Relatório exportado como '{nome_arquivo}'.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RelatorioApp()
    window.show()
    sys.exit(app.exec_())
