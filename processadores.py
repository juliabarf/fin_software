import csv
import pandas as pd
import os

KEYWORDS = {
    "Saúde": ["farmacia", "drogaria", "drogar", "hospital", "medico", "exame", "saude", "odontolog"],
    "Alimentação": ["ifood", "restaurante", "lanchonete", "pizzaria", "mcdonalds", "burger", "supermercado", "mercado", "padaria", "cafe", "sorveteria", "churrasquinho", "degus", "kfc"],
    "Transporte": ["uber", "99", "taxi", "onibus", "metro", "combustivel", "posto", "shell", "petrobras", "vlt", "maismobi"],
    "Educação": ["curso", "livraria", "faculdade", "escola", "udemy", "cultura", "editora"],
    "Lazer/Outros": ["kinoplex", "netflix", "spotify", "ingresso", "cinema", "seguro"]
}

def limpar_valor(valor_str):
    if isinstance(valor_str, (int, float)): return float(valor_str)
    try:
        clean = str(valor_str).replace('−', '-').replace('R$', '').replace(' ', '').replace('\xa0', '').strip()
        if '.' in clean and ',' in clean: clean = clean.replace('.', '').replace(',', '.')
        elif ',' in clean: clean = clean.replace(',', '.')
        return float(clean)
    except: return 0.0

def categorizar(relatorio, desc, valor_abs):
    desc_lower = str(desc).lower()
    for cat, palavras in KEYWORDS.items():
        if any(p in desc_lower for p in palavras):
            relatorio[cat].append((desc.strip(), valor_abs))
            return
    relatorio["Outros"].append((desc.strip(), valor_abs))

class Processadores:
    @staticmethod
    def nubank(caminho):
        rel = {cat: [] for cat in KEYWORDS.keys()}
        rel["Outros"] = []
        with open(caminho, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                v = limpar_valor(row.get('Valor', "0"))
                if v < 0: categorizar(rel, row.get('Descrição', ""), abs(v))
        return rel

    @staticmethod
    def inter(caminho):
        rel = {cat: [] for cat in KEYWORDS.keys()}
        rel["Outros"] = []
        with open(caminho, 'r', encoding='utf-8-sig') as f:
            linhas = f.readlines()
            start = next(i for i, l in enumerate(linhas) if "Data Lançamento" in l)
            f.seek(0)
            for _ in range(start): next(f)
            for row in csv.DictReader(f, delimiter=';'):
                v = limpar_valor(row.get('Valor', "0"))
                if v < 0: categorizar(rel, f"{row.get('Histórico','')} - {row.get('Descrição','')}", abs(v))
        return rel

    @staticmethod
    def picpay(caminho):
        rel = {cat: [] for cat in KEYWORDS.keys()}
        rel["Outros"] = []
        try:
            df = pd.read_excel(caminho)
        except:
            df = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8-sig')
        for _, row in df.iterrows():
            r = {str(k).lower(): v for k, v in row.items()}
            v = limpar_valor(r.get('valor', "0"))
            if v < 0: categorizar(rel, f"{r.get('tipo','')} - {r.get('origem / destino','')}", abs(v))
        return rel