# BP: Simulador Banco Imobiliário (simplificado)

Este projeto implementa uma HTTP API em FastAPI para simular uma partida do jogo descrito no desafio.
Outras *features* foram implementadas para incrementar o desafio :)

## Sobre o jogo

O jogo simulado é uma versão simplificada de Banco Imobiliário.  
A partida acontece com quatro jogadores, cada um com saldo inicial de 300, e a ordem de turno é definida aleatoriamente no início.

O tabuleiro possui 20 propriedades em sequência. Cada propriedade tem um valor de venda, um valor de aluguel e pode ou não ter um proprietário.

Em sua vez, o jogador lança um dado de 6 faces e avança pelo tabuleiro. Ao completar uma volta, recebe 100 de saldo.    

Se cair em uma propriedade sem dono, pode comprá-la caso tenha saldo suficiente e sua estratégia permita.     
Se cair em uma propriedade com dono, paga o aluguel ao proprietário.

Cada jogador segue uma estratégia de compra:

- `impulsivo`: compra qualquer propriedade disponível em que parar.
- `exigente`: compra apenas propriedades com aluguel maior que 50.
- `cauteloso`: compra apenas se ainda ficar com pelo menos 80 de saldo após a compra.
- `aleatorio`: compra com probabilidade de 50%.

Um jogador é eliminado quando fica com saldo negativo. Ao ser eliminado, deixa de jogar e todas as suas propriedades ficam novamente disponíveis para compra.

A partida termina quando resta apenas um jogador ativo. Caso isso não aconteça até a milésima rodada, vence o jogador com maior saldo.   

Em caso de empate, o desempate segue a ordem de turno definida no início da partida.

## Decisões

- Como o enunciado não fornece a tabela de custos e alugueis das 20 propriedades, foi definida uma lista de tuplas (compra/aluguel) fixa no codigo em `app/game.py`.
- O limite de 1000 rodadas foi interpretado como 1000 turnos individuais de jogadores.
- A ordem de turno dos jogadores é sorteada no inicio da partida.
- Em caso de empate por saldo, vence quem aparece antes na ordem de turno sorteada.
- Ao ficar com saldo negativo, o jogador é eliminado e todas as suas propriedades ficam sem dono.
- O *endpoint* aceita um parâmetro opcional `seed` para reproduzir uma simulação específica e movimentar o fator de aleatoriedade.

## Como executar

Instale as dependencias com Poetry:

```bash
poetry install
```

Inicie a API com Poetry:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Caso nao tenha Poetry instalado, use o `requirements.txt`:

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
