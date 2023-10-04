from setuptools import setup, find_packages

setup(
    name='Medios_ARG',
    description="Librería de Python para realizar 'scrapping' de Medios Argentinos. Desarrollada por Hernán A. Teszkiewicz Novick, para el equipo dev. de Ch'aska.",
    version='0.1',
    author           = 'Hernán A. Teszkiewicz Novick',
    author_email     = 'herni@cajadeideas.ar',
    license          =  'MIT'    ,
    url= 'https://github.com/Hernanatn/Medios_ARG',
    download_url     =  'https://github.com/Hernanatn/Goog_API/raw/main/dist/Goog_API-0.22.tar.gz',
    packages=['Medios_ARG'],
    install_requires=[
        'bs4',
        'requests',
    ],
)