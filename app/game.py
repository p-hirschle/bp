from __future__ import annotations

from dataclasses import dataclass
from random import Random


INITIAL_BALANCE = 300
BOARD_SIZE = 20
LAP_BONUS = 100
MAX_TURNS = 1000

IMPULSIVE = "impulsivo"
DEMANDING = "exigente"
CAUTIOUS = "cauteloso"
RANDOM = "aleatorio"

PLAYER_NAMES = [IMPULSIVE, DEMANDING, CAUTIOUS, RANDOM]


@dataclass
class Property:
    position: int
    sale_price: int
    rent: int
    owner: str | None = None


@dataclass
class Player:
    name: str
    turn_order: int
    balance: int = INITIAL_BALANCE
    position: int = 0
    active: bool = True


@dataclass(frozen=True)
class GameResult:
    winner: str
    players_by_balance: list[str]
    turns_played: int


@dataclass(frozen=True)
class StatisticsResult:
    biggest_winner: str
    win_percentage_by_player: dict[str, str]


def default_properties() -> list[Property]:
    """
    Valores de compra e aluguel definidos 
    particularmente pra cada propriedade.
    """
    values = [
        (60, 10),
        (60, 20),
        (80, 20),
        (100, 30),
        (100, 35),
        (120, 40),
        (140, 45),
        (140, 50),
        (160, 55),
        (180, 60),
        (180, 65),
        (200, 70),
        (220, 75),
        (220, 80),
        (240, 85),
        (260, 90),
        (280, 95),
        (300, 100),
        (320, 110),
        (350, 120),
    ]
    return [
        Property(position=index, sale_price=sale_price, rent=rent)
        for index, (sale_price, rent) in enumerate(values)
    ]


def wants_to_buy(player: Player, property_: Property, rng: Random) -> bool:
    """
    Critério de compra baseado na personalidade de cada tipo de jogador.
    """
    if player.balance < property_.sale_price:
        return False
    if player.name == IMPULSIVE:
        return True
    if player.name == DEMANDING:
        return property_.rent > 50
    if player.name == CAUTIOUS:
        return player.balance - property_.sale_price >= 80
    if player.name == RANDOM:
        return rng.random() < 0.5
    return False


class Game:
    """
    Classe responsável pelo jogo e sua lógica.
    """
    def __init__(
        self,
        properties: list[Property] | None = None,
        seed: int | None = None,
        max_turns: int = MAX_TURNS,
        shuffle_players: bool = True,
    ) -> None:
        self.rng = Random(seed)
        self.properties = properties or default_properties()
        self.max_turns = max_turns
        self.turns_played = 0

        player_names = PLAYER_NAMES.copy()
        if shuffle_players:
            self.rng.shuffle(player_names)

        self.players = [
            Player(name=name, turn_order=index) for index, name in enumerate(player_names)
        ]

        self.current_player_index = 0

    def play(self) -> GameResult:
        """
        Regra de continuidade e finalização do jogo.
        """
        while self.turns_played < self.max_turns and self.active_players_count > 1:
            player = self.players[self.current_player_index]

            if player.active:
                self.play_turn(player)
                self.turns_played += 1

            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )

        ranked_players = self.ranked_players()
        return GameResult(
            winner=ranked_players[0].name,
            players_by_balance=[player.name for player in ranked_players],
            turns_played=self.turns_played,
        )

    @property
    def active_players_count(self) -> int:
        return sum(1 for player in self.players if player.active)

    def play_turn(self, player: Player, die_roll: int | None = None) -> None:
        """
        Função de jogada do jogador.
        """
        die = die_roll or self.rng.randint(1, 6)
        next_position = player.position + die

        if next_position >= BOARD_SIZE:
            player.balance += LAP_BONUS

        player.position = next_position % BOARD_SIZE
        current_property = self.properties[player.position]

        if current_property.owner is None:
            if wants_to_buy(player, current_property, self.rng):
                player.balance -= current_property.sale_price
                current_property.owner = player.name
            return

        if current_property.owner == player.name:
            return

        owner = self.find_player(current_property.owner)
        player.balance -= current_property.rent
        owner.balance += current_property.rent

        if player.balance < 0:
            self.eliminate(player)

    def find_player(self, name: str) -> Player:
        """
        Auxiliar para retornar/apontar um jogador em questão.
        """
        return next(player for player in self.players if player.name == name)

    def eliminate(self, player: Player) -> None:
        """
        Elimina um jogador e 'solta' suas propriedades.
        """
        player.active = False
        for property_ in self.properties:
            if property_.owner == player.name:
                property_.owner = None

    def ranked_players(self) -> list[Player]:
        """
        Ranqueamento dos jogadores baseado na balança final de cada um.
        Critério de desempate: ordem de turno.
        """
        return sorted(self.players, key=lambda player: (-player.balance, player.turn_order))


def simulate_game(seed: int | None = None) -> GameResult:
    """
    Roda o jogo :)
    """
    return Game(seed=seed).play()


def simulate_statistics(total_games: int, seed: int | None = None) -> StatisticsResult:
    """
    Roda vários jogos completos e calcula a porcentagem de vitória por estilo de jogador.
    """
    if total_games <= 0:
        raise ValueError("O número de jogos completos deve ser maior que zero")

    rng = Random(seed)
    victories = {player_name: 0 for player_name in PLAYER_NAMES}

    for _ in range(total_games):
        game_seed = rng.randint(1, 1_000_000_000)
        result = simulate_game(seed=game_seed)
        victories[result.winner] += 1

    ranked_players = sorted(
        PLAYER_NAMES,
        key=lambda player_name: (-victories[player_name], PLAYER_NAMES.index(player_name)),
    )
    biggest_winner = ranked_players[0]
    win_percentage_by_player = {
        player_name: f"{round((victories[player_name] / total_games) * 100)}%"
        for player_name in ranked_players
    }

    return StatisticsResult(
        biggest_winner=biggest_winner,
        win_percentage_by_player=win_percentage_by_player,
    )
