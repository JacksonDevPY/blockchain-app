import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from blockchain import Blockchain, Bloco # Importa do arquivo ao lado

app = FastAPI()

# ESSENCIAL: Permite que seu navegador acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

minha_blockchain = Blockchain()
MEU_ENDERECO = "endereco-do-meu-servidor"

# No topo do arquivo main.py, junto com os outros modelos
class NFTInput(BaseModel):
    mensagem: str

# Ao final do arquivo main.py
@app.post("/nft/criar")
def criar_nft(dados: NFTInput):
    try:
        # Chamando a função de mineração com o dado do NFT
        minha_blockchain.minerar_pendencias(MEU_ENDERECO, nft_data=dados.mensagem)
        return {
            "mensagem": "NFT registrado com sucesso!",
            "bloco": minha_blockchain.ultimo_bloco().indice,
            "conteudo": dados.mensagem
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Transacao:
    def __init__(self, remetente, destinatario, quantidade):
        self.remetente = remetente
        self.destinatario = destinatario
        self.quantidade = quantidade
        self.assinatura = None

    def assinar_transacao(self, chave_privada):
        # Simulação de assinatura
        self.assinatura = f"sig_{chave_privada}"

    def esta_valida(self):
        if self.remetente == "Sistema": return True
        return self.assinatura is not None

class TransacaoInput(BaseModel):
    remetente: str
    destinatario: str
    quantidade: float
    chave_privada: str

@app.get("/blockchain")
def exibir_blockchain():
    return {
        "tamanho": len(minha_blockchain.cadeia),
        "corrente": minha_blockchain.cadeia,
        "pendentes": minha_blockchain.transacoes_pendentes
    }

@app.post("/transacao/nova")
def nova_transacao(dados: TransacaoInput):
    try:
        t = Transacao(dados.remetente, dados.destinatario, dados.quantidade)
        t.assinar_transacao(dados.chave_privada)
        minha_blockchain.adicionar_transacao(t)
        return {"mensagem": "Transação adicionada!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/minerar")
def minerar():
    minha_blockchain.minerar_pendencias(MEU_ENDERECO)
    return {"mensagem": "Bloco minerado!", "bloco": minha_blockchain.ultimo_bloco()}

@app.get("/saldo/{endereco}")
def consultar_saldo(endereco: str):
    return {"endereco": endereco, "saldo": minha_blockchain.obter_saldo(endereco)}

# No main.py, adicione esta rota:
@app.post("/nft/criar")
def criar_nft(texto: str):
    # Um NFT na nossa rede será um bloco que contém uma mensagem especial imutável
    minha_blockchain.transacoes_pendentes.append({"tipo": "NFT", "conteudo": texto})
    minha_blockchain.minerar_pendencias(MEU_ENDERECO)
    return {"mensagem": "NFT gravado na eternidade da blockchain!", "bloco": minha_blockchain.ultimo_bloco().indice}

class NFTInput(BaseModel):
    mensagem: str

@app.post("/nft/criar")
def criar_nft(dados: NFTInput):
    # Ao criar um NFT, mineramos um bloco imediatamente com essa mensagem
    minha_blockchain.minerar_pendencias(MEU_ENDERECO, nft_data=dados.mensagem)
    return {
        "mensagem": "NFT registrado com sucesso!",
        "bloco": minha_blockchain.ultimo_bloco().indice,
        "conteudo": dados.mensagem
    }