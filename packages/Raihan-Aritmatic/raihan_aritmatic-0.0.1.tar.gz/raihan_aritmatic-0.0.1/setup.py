from setuptools import setup, find_packages

setup(
    name='Raihan-Aritmatic',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    author='MD. Mostafa Raihan',
    author_email="m.raihan.computerscience@gmail.com",
    description="This is a simple arithmetic raihan_arithmatic for ADD, SUB, MUL, DIV operations.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
