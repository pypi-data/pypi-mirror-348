from setuptools import setup, find_packages

setup(
    name='evilafo-tools',  # N'oublie pas de le mettre en minuscules !
    version='0.1',
    packages=find_packages(),  # Cela va automatiquement trouver tes packages Python
    install_requires=[
        'transformers',  
        'torch', 
        'numpy',  
    ],
    description='A Python library for using BERT and BART',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Emmanuel Evilafo',
    author_email='evil2846@gmail.com',
    url='https://github.com/Evilafo/Evilafo-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
