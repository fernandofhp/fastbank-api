# 🚀 FASTBANK-API 

Desafio prático de uma API Bancária assíncrona focada em alta performance, segurança e separação de conceitos.

| Tecnologia | Descrição |
| --- | --- |
|🏗️ **Framework** | ⚡FastAPI (Assíncrono) |
|🗄️ **Banco de Dados** | 🎲SQLite3 com driver assíncrono `aiosqlite` |
|🛠️ **Query Builder** | ⚗️SQLAlchemy Core / `databases` |
|🛡️ **Segurança** | 🔐Autenticação via Bearer Token JWT (PyJWT) |
|✔️ **Validação** | 📦Pydantic v2 (Modelos de 📥entrada/📤saída e Payload) |

## Principais Fluxos Implementados
* **Segurança:** Middleware customizado de validação de tokens JWT direto nas requisições.
* **Contas:** Criação e listagem paginada de contas correntes.
* **Transações:** Registro assíncrono de movimentações financeiras com cálculo automático e validação de saldo.