from setuptools import setup, find_packages

setup(
    name="menu_select",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        # Liste suas dependências aqui
    ],
    author="VG-Correa",
    author_email="v.victorgabriel2014@gmail.com",
    description="Uma biblioteca para criação de menus seletivos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VG-Correa/menu_select",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)