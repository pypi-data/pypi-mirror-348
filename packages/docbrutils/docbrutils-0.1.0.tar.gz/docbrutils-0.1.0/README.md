
# docbrutils

Pacote Python para validação e geração de CPF e CNPJ válidos.

## Instalação

```bash
pip install docbrutils
```

## Uso

```python
from docbrutils import cpf, cnpj

cpf.validate_cpf('123.456.789-09')
cpf.generate_cpf()

cnpj.validate_cnpj('12.345.678/0001-95')
cnpj.generate_cnpj()
```

## Testes

```bash
python -m unittest discover
```
