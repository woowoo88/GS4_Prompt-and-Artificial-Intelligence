"""Executa o notebook Colab em um kernel Python temporário.

Uso: python executar_notebook.py
Valida preparação, agente, interface, testes e evidências sem repetir o benchmark completo.
"""
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parent


def main():
    arquivo=ROOT/'Citizen_Assist_Colab.ipynb'
    nb=nbformat.read(arquivo,as_version=4)
    with TemporaryDirectory(prefix='citizen_notebook_') as pasta:
        kernels=Path(pasta)/'kernels'
        spec=kernels/'citizen-python'
        spec.mkdir(parents=True)
        config={'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
                'display_name':'Python 3 - Citizen Assist','language':'python',
                'env':{'IPYTHONDIR':str(Path(pasta)/'ipython'),
                       'PYDEVD_DISABLE_FILE_VALIDATION':'1'}}
        (spec/'kernel.json').write_text(json.dumps(config),encoding='utf-8')
        km=KernelManager(kernel_name='citizen-python',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernels)]))
        try:
            cliente=NotebookClient(nb,km=km,timeout=300,resources={'metadata':{'path':str(ROOT)}},allow_errors=False)
            cliente.execute()
        finally:
            if km.has_kernel:
                km.shutdown_kernel(now=True)
    nbformat.validate(nb)
    assert all(c.execution_count is not None and not any(o.output_type=='error' for o in c.outputs)
               for c in nb.cells if c.cell_type=='code')
    nbformat.write(nb,arquivo)
    print('Notebook executado e validado, sem erros de células.')


if __name__=='__main__':
    main()
