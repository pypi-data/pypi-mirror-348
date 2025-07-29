# Always prefer setuptools over distutils
from setuptools import setup


# This call to setup() does all the work
setup(
    name='edat_ingestao_utils',
    version='0.0.9',
    description='Biblioteca de Apoio a Ingestão de Dados no EDAT',
    long_description='# Utilitarios EDAT <br /> Classes utilitarias de ingestão utilizadas pelo EDAT.',
    long_description_content_type='text/markdown',
    author='Escritório de Dados',
    author_email='dados@unicamp.br',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent'
    ],
    packages=['edat_ingestao_utils'],
    include_package_data=True,
    install_requires=['psycopg2==2.8.6', 'SQLAlchemy==1.3.15', 'pandas==0.24.2', 'pgcopy==1.4.1', 'jellyfish==0.8.2', 'boto3==1.33.13'],
    python_requires='>=3.6'
)
