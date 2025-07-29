from setuptools import setup, find_packages
import re
from pathlib import Path

# Ler a versão do __init__.py sem importá-lo diretamente
init_file = Path("automacao_utils/__init__.py").read_text(encoding="utf-8")
version = re.search(r'__version__ = "(.*?)"', init_file).group(1)

setup(
    name="automacao_utils",
    version=version, 
    packages=find_packages(),
    install_requires=[
        "seleniumbase>=4.29.9",
        "psutil>=5.9.0",
        "pandas>=1.3.0",
        "watchdog>=2.1.9",
        "requests>=2.27.1",
    ],
    author="Gedean Zitkoski, Gabriel Pelizzari",
    author_email="gedezitkoski@gmail.com, gpelizzari08@gmail.com",
    description="Funções úteis para automação com Python/Selenium",
    python_requires=">=3.7",
    classifiers=[
    "Development Status :: 3 - Alpha",  
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Operating System :: Microsoft :: Windows",  
    ],
)
