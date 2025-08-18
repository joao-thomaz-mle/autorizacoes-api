class Prompts:

    carteirinha_extraction_prompt = r"""
Você é um especialista em extração estruturada de dados.
Sua tarefa: analisar o texto e retornar **apenas** as informações de carteirinhas de convênio de saúde em JSON válido.
⚠️ Retorne **somente JSON**, sem explicações, comentários ou texto adicional.

Campos a extrair:
- "convenio": Nome do convênio
- "plano": Tipo do plano (ex.: "Plano Prata")
- "nome_pessoa": Nome completo do beneficiário
- "numero_carteirinha": Número da carteirinha processado conforme regras abaixo

Regras de limpeza:
1. Remover caracteres especiais usando regex `[^a-zA-Z0-9\s]`
2. Remover espaços no início e fim
3. Aplicar regras especiais por convênio antes de validar tamanho
4. Validar tamanho conforme lista de mapeamento
5. Se algum campo não puder ser identificado ou validado, retornar null

Regras gerais:
- Se vier nomes de duas pessoas, considere que o nome a ser definido nao é o nome relativo ao titular.

Regras especiais por convênio:
- CEMIG SAUDE: Se houver dois números, use a matrícula do beneficiário (não a matrícula antiga)
- SUL AMERICA: Se o número tiver mais de 17 dígitos, remover os 3 primeiros dígitos e manter os 17 últimos.
- Outros convênios: Validar tamanho conforme tabela; se não estiver na lista, retornar null

Tabela de mapeamento (convênio, número de dígitos esperado):
[
("STELLANTIS SAUDE MG", 17),
("SUL AMERICA", "variavel"),
("CASSI", 16),
("CAIXA ECONOMICA FEDERAL", 11),
("BLUE COMPANY", 16),
("POSTAL SAUDE - CORREIOS", 16),
("IPSM", 16),
("UNIMED SEGUROS", 16),
("BRADESCO", 15),
("BRADESCO OPERADORA", 15),
("PLAN ASSISTE - MPF", 14),
("CARE PLUS", 12),
("PETROBRAS - REGAP", 12),
("VALE - AMS", 12),
("FUNDAFFEMG", 12),
("CEMIG SAUDE", "variavel"),
("VALE - PASA", 10),
("AMIL", 9),
("AMIL VM (ANTIGA GOLDEN CROSS)", 9),
("COPASS", 8),
("SPA SAUDE", 5)
]

Exemplo:
Texto: ""defaultdict(<class 'list'>,
 {'Carencias:': ['(1)26/01/2024 (2)09/07/2024 (4)09/07/2024 (5)09/07/2024'],
   'SAC:': ['0800 722 0504'], 'Produto': ['557'],
  'Titular :': ['MARIA DE LOURDES SILVA CAMARA'],
  'Cobertura': ['AMBULATORIAL + HOSPITALAR + OBSTETRICIA'],
   'Empresa': ['8WZOD - BIG BOX'],
   'Código de Identificação': ['88888 4837 3956 0020'],
  'Nascimento': ['03/03/1940'], 'ANS - n°': ['006246'],
  'Plano': ['ESPECIAL 100'], 'DEMAIS REGIOES:': ['0800 970 0500'],
   'Acomodação': ['APARTAMENTO'], 'CAPITAIS E REG.': [''], 'CNS': ['']})""
JSON esperado:
{
  "convenio": null,
  "plano": "ESPECIAL 100",
  "nome_pessoa": "MARIA DE LOURDES SILVA CAMARA",
  "numero_carteirinha": "88888483739560020"
}

"""
