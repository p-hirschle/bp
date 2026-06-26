from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.game import simulate_game, simulate_statistics


app = FastAPI(
    title="Simulador Banco Imobiliario",
    version="0.1.0",
)


class SimulationResponse(BaseModel):
    vencedor: str
    jogadores: list[str]


class StatisticsResponse(BaseModel):
    maior_vencedor: str
    porcentagem_vitoria_por_jogador: dict[str, str]


@app.get("/jogo/simular", response_model=SimulationResponse)
def simulate(seed: int | None = Query(default=None)) -> SimulationResponse:
    result = simulate_game(seed=seed)
    return SimulationResponse(
        vencedor=result.winner,
        jogadores=result.players_by_balance,
    )


@app.get("/jogo/simular_e_estatistica", response_model=StatisticsResponse)
def simulate_and_calculate_statistics(
    n: int = Query(gt=0),
    seed: int | None = Query(default=None),
) -> StatisticsResponse:
    result = simulate_statistics(total_games=n, seed=seed)
    return StatisticsResponse(
        maior_vencedor=result.biggest_winner,
        porcentagem_vitoria_por_jogador=result.win_percentage_by_player,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
