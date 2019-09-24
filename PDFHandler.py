from pdfminer import high_level

"""
Função que extrai texto de um PDF. Imagens são ignoradas.
Argumento é um arquivo PDF aberto como binário. Retorna um objeto file.
"""
def extrair_texto(pdf):
    outfile = open("return", "x")
    high_level.extract_text_to_fp(pdf, outfile)
    return outfile
