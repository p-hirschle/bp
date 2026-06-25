from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.game import simulate_game


app = FastAPI(
    title="Simulador Banco Imobiliario",
    version="0.1.0",
)


class SimulationResponse(BaseModel):
    vencedor: str
    jogadores: list[str]


@app.get("/jogo/simular", response_model=SimulationResponse)
def simulate(seed: int | None = Query(default=None)) -> SimulationResponse:
    result = simulate_game(seed=seed)
    return SimulationResponse(
        vencedor=result.winner,
        jogadores=result.players_by_balance,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
