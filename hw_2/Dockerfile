FROM archlinux:latest

RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm python python-pip gcc graphviz texlive-most
RUN pip install pygraphviz==1.7
RUN pip install --upgrade -i https://test.pypi.org/simple/ astplot==0.0.1

WORKDIR /src
COPY . .
RUN python latex.py
RUN pdflatex -output-directory artifacts artifacts/example.tex