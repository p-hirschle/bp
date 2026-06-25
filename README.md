# BP: Simulador Banco Imobiliário (simplificado)

Este projeto implementa uma HTTP API em FastAPI para simular uma partida do jogo descrito no desafio.
Outras *features* foram implementadas para incrementar o desafio :)

## Decisões

- Como o enunciado não fornece a tabela de custos e aluguéis das 20 propriedades, foi definida uma lista fixa no código em `app/game.py`.
- O limite de 1000 rodadas foi interpretado como 1000 turnos individuais de jogadores.
- A ordem de turno dos jogadores é sorteada no início da partida.
- Em caso de empate por saldo, vence quem aparece antes na ordem de turno sorteada.
- Ao ficar com saldo negativo, o jogador é eliminado e todas as suas propriedades ficam sem dono.
- O *endpoint* aceita um parâmetro opcional `seed` para reproduzir uma simulação específica e movimentar o fator de aleatoriedade.

## Como executar/rodar

Instale as dependências com Poetry (recomendado):

```bash
poetry install
```

Inicie a API com Poetry:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Caso não possua o Poetry instalado, use o `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Acesse:

```http
GET http://localhost:8080/jogo/simular
```

Exemplo com seed:

```http
GET http://localhost:8080/jogo/simular?seed=42
```

Resposta esperada:

```json
{
  "vencedor": "cauteloso",
  "jogadores": ["cauteloso", "aleatorio", "exigente", "impulsivo"]
}
```

Você também pode simplesmente acessar a documentação e testar de forma mais interativa:  

```http
GET http://localhost:8080/docs
```

---
Pedro Hirschle — software engineer, 2026.