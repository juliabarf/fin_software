from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'RELATÓRIO DE GASTOS PESSOAIS', 0, 1, 'C')
        self.ln(5)

def gerar_pdf(dados, saida):
    pdf = PDFReport()
    pdf.add_page()
    total_geral = 0
    for cat, itens in dados.items():
        if itens:
            pdf.set_font("Arial", 'B', 12)
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(0, 10, cat.upper().encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L', 1)
            pdf.set_font("Arial", '', 9)
            total_cat = 0
            for d, v in itens:
                pdf.cell(145, 6, str(d)[:75].encode('latin-1', 'replace').decode('latin-1'), 0)
                pdf.cell(35, 6, f"R$ {v:.2f}".replace('.', ','), 0, 1, 'R')
                total_cat += v
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(180, 7, f"SUBTOTAL: R$ {total_cat:.2f}".replace('.', ','), 0, 1, 'R')
            pdf.ln(2)
            total_geral += total_cat
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"TOTAL GERAL: R$ {total_geral:.2f}".replace('.', ','), 0, 1, 'R')
    pdf.output(saida)