"""Regenerate every page. Python 3 standard library only.
Run from anywhere:  python tools/generator/build_all.py"""
import os, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
for name in ["page_index", "page_telcos", "page_empresas", "page_soluciones",
             "page_reserva", "page_contacto"]:
    runpy.run_path(os.path.join(HERE, name + ".py"), run_name="__main__")
