
from setuptools import setup, find_packages

setup(
    name='docbrutils',
    version='0.1.0',
    description='Validação e geração de CPF e CNPJ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Maurício Campos',
    author_email='mauriciocamposdev@gmail.com',
    url='https://github.com/mauriciocampos1234/docbrutils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
