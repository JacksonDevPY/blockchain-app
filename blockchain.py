import hashlib
import time
import json
import os

class Bloco:
    def __init__(self, indice, transacoes, timestamp, hash_anterior, nft_data=None):
        self.indice = indice
        self.transacoes = transacoes
        self.timestamp = timestamp
        self.hash_anterior = hash_anterior
        self.nft_data = nft_data 
        self.nonce = 0
        self.hash = self.gerar_hash()

    def gerar_hash(self):
        conteudo = f"{self.indice}{self.transacoes}{self.timestamp}{self.hash_anterior}{self.nonce}{self.nft_data}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

    def minerar_bloco(self, dificuldade):
        while self.hash[:dificuldade] != "0" * dificuldade:
            self.nonce += 1
            self.hash = self.gerar_hash()
        print(f"Bloco Minerado! Hash: {self.hash}")
            
class Blockchain:
    def __init__(self):
        self.transacoes_pendentes = []
        self.cadeia = []
        self.dificuldade = 4
        self.recompensa = 50
        self.arquivo_db = "blockchain_data.json"
        
        # Se o arquivo existir, carrega; senão, cria o Gênesis
        if os.path.exists(self.arquivo_db):
            self.carregar_blockchain()
        else:
            self.criar_bloco_genesis()

    def criar_bloco_genesis(self):
        bloco_genesis = Bloco(0, [], time.time(), "0")
        self.cadeia.append(bloco_genesis)

    def ultimo_bloco(self):
        return self.cadeia[-1]

    def adicionar_transacao(self, transacao):
        if self.obter_saldo(transacao.remetente) < transacao.quantidade and transacao.remetente != "Sistema":
            raise Exception("Saldo insuficiente!")
        
        self.transacoes_pendentes.append({
            "remetente": transacao.remetente,
            "destinatario": transacao.destinatario,
            "quantidade": transacao.quantidade
        })

    def minerar_pendencias(self, endereco_minerador, nft_data=None):
        novo_bloco = Bloco(len(self.cadeia), self.transacoes_pendentes, time.time(), self.ultimo_bloco().hash, nft_data)
        novo_bloco.minerar_bloco(self.dificuldade)
        self.cadeia.append(novo_bloco)
        
        self.transacoes_pendentes = [
            {'remetente': "Sistema", 'destinatario': endereco_minerador, 'quantidade': self.recompensa}
        ]
        self.salvar_blockchain()

    def obter_saldo(self, endereco):
        saldo = 0
        for bloco in self.cadeia:
            if isinstance(bloco.transacoes, list):
                for t in bloco.transacoes:
                    if t.get('remetente') == endereco: saldo -= t['quantidade']
                    if t.get('destinatario') == endereco: saldo += t['quantidade']
        return saldo

    def salvar_blockchain(self):
        dados = []
        for bloco in self.cadeia:
            dados.append(bloco.__dict__)
        with open(self.arquivo_db, 'w') as f:
            json.dump(dados, f, indent=4)

    def carregar_blockchain(self):
        try:
            with open(self.arquivo_db, 'r') as f:
                dados_carregados = json.load(f)
            self.cadeia = []
            for b in dados_carregados:
                novo_bloco = Bloco(b['indice'], b['transacoes'], b['timestamp'], b['hash_anterior'], b['nft_data'])
                novo_bloco.nonce = b['nonce']
                novo_bloco.hash = b['hash']
                self.cadeia.append(novo_bloco)
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            self.criar_bloco_genesis()
            
    # Dentro da classe Blockchain no arquivo blockchain.py
def validar_corrente(self):
    for i in range(1, len(self.cadeia)):
        bloco_atual = self.cadeia[i]
        bloco_anterior = self.cadeia[i-1]

        # 1. Verifica se o bloco atual aponta corretamente para o anterior
        if bloco_atual.hash_anterior != bloco_anterior.hash:
            print(f"ERRO: Bloco {i} corrompido (Hash Anterior inválido)!")
            return False

        # 2. Verifica se o Hash do bloco atual não foi alterado
        if bloco_atual.hash != bloco_atual.gerar_hash():
            print(f"ERRO: Conteúdo do Bloco {i} foi modificado!")
            return False
            
    print("Sucesso: A Blockchain é 100% íntegra!")
    return True