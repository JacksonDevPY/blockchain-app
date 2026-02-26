# 🔗 Blockchain & NFT Academic Wallet

Um sistema de blockchain educacional completo com mineração (Proof of Work), transferências de ativos e cunhagem de NFTs imutáveis.

## 🛠️ Tecnologias
- **Back-end:** Python, FastAPI, Pydantic.
- **Blockchain:** Algoritmo SHA-256 para hashing, sistema de recompensas e Proof of Work.
- **Front-end:** HTML5, Tailwind CSS, Axios.
- **Deploy:** Vercel (API) e GitHub Pages (Interface).

## 🚀 Funcionalidades
* **Mineração:** Implementação de dificuldade variável para validação de blocos.
* **NFT Factory:** Registro de metadados imutáveis diretamente na cadeia de blocos.
* **Persistence:** Armazenamento do estado da rede em estrutura JSON (simulando um ledger).
* **Segurança Simulada:** Sistema de assinaturas e validação de integridade da corrente.

## 📄 Notas de Arquitetura
Este projeto foi desenvolvido para fins acadêmicos. A blockchain utiliza um arquivo JSON para persistência. Em um cenário de produção, a camada de dados seria substituída por uma solução distribuída ou banco de dados NoSQL para escalabilidade.
