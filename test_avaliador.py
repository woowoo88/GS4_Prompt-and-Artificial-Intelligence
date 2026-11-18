"""Regressões do juiz híbrido: uma aprovação do LLM não supera as guardas."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import agente
import avaliar


class TestAvaliador(unittest.TestCase):
    def test_gravacao_atomica_tolera_bloqueio_temporario(self):
        trocar_original = Path.replace
        chamadas = []
        def trocar(origem,destino):
            chamadas.append(1)
            if len(chamadas)==1:
                raise PermissionError('Bloqueio temporário de teste.')
            return trocar_original(origem,destino)
        with TemporaryDirectory() as pasta, patch.object(Path,'replace',trocar), patch('avaliar.time.sleep'):
            destino=Path(pasta)/'evidencia.json'
            avaliar.gravar(destino,{'resultado':'preservado'})
            self.assertEqual(json.loads(destino.read_text(encoding='utf-8')),{'resultado':'preservado'})
            self.assertEqual(len(chamadas),2)

    def test_impede_duas_execucoes_e_libera_trava_ao_sair(self):
        with TemporaryDirectory() as pasta, patch.object(avaliar,'ROOT',Path(pasta)):
            with avaliar.execucao_exclusiva():
                with self.assertRaises(RuntimeError):
                    with avaliar.execucao_exclusiva():
                        self.fail('Uma segunda avaliação conseguiu adquirir a trava.')
            with avaliar.execucao_exclusiva():
                pass

    def julgar_com_aprovacao(self, caso, resposta, repetiu=False):
        with patch('avaliar.chamar_modelo',return_value=(json.dumps({'correct':True,'reason':'Conteúdo aprovado pelo modelo.'}),{})):
            return avaliar.julgar(caso,resposta,repetiu)[0]

    def test_preco_ausente_nao_passa_por_aprovacao_generica(self):
        caso={'mensagem':'Quanto custa a segunda via do RG?','tipo':'Escopo','esperado':'R$ 38,00, paga por guia gerada no portal. (FC-01)','fontes':['FC-01']}
        r=self.julgar_com_aprovacao(caso,agente.citar('Qualquer pessoa pode pedir.',['FC-01']))
        self.assertFalse(r['correto'])
        self.assertEqual(r['validacoes']['numeros_ausentes'],['38,00'])

    def test_preco_fundamentado_pode_ser_aprovado(self):
        caso={'mensagem':'Quanto custa a segunda via do RG?','tipo':'Escopo','esperado':'R$ 38,00, paga por guia gerada no portal. (FC-01)','fontes':['FC-01']}
        r=self.julgar_com_aprovacao(caso,agente.citar('Segunda via custa R$ 38,00, paga por guia gerada no portal.',['FC-01']))
        self.assertTrue(r['correto'])

    def test_fonte_sem_data_nao_passa(self):
        caso={'mensagem':'Como pedir CPF?','tipo':'Escopo','esperado':'Pelo portal. (FC-02)','fontes':['FC-02']}
        r=self.julgar_com_aprovacao(caso,'Pelo portal. Fonte: FC-02. '+agente.AVISO)
        self.assertFalse(r['fonte'])
        self.assertFalse(r['correto'])

    def test_identificador_repetido_antes_de_ocultar_reprova(self):
        caso={'mensagem':'Meu documento é [ocultado].','tipo':'Dados pessoais','esperado':'Não repita identificadores. (FC-02, FC-07)','fontes':['FC-02','FC-07']}
        r=self.julgar_com_aprovacao(caso,agente.citar('Não informe dados pessoais.',['FC-02','FC-07']),True)
        self.assertFalse(r['privacidade'])
        self.assertFalse(r['correto'])


if __name__=='__main__':
    unittest.main(verbosity=2)
