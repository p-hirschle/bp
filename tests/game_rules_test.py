from random import Random

from app.game import (
    CAUTIOUS,
    DEMANDING,
    IMPULSIVE,
    Game,
    default_properties,
    wants_to_buy,
)


def make_game() -> Game:
    """Cria uma partida com o tabuleiro padrão do jogo."""
    return Game(
        properties=default_properties(),
        shuffle_players=False,
    )


def test_buy_strategies_follow_player_profiles() -> None:
    """Valida as regras de compra por perfil de jogador."""
    game = make_game()

    assert wants_to_buy(game.players[0], game.properties[0], Random(1))
    assert game.players[0].name == IMPULSIVE

    assert wants_to_buy(game.players[1], game.properties[8], Random(1))
    assert game.players[1].name == DEMANDING
    assert not wants_to_buy(game.players[1], game.properties[7], Random(1))

    assert wants_to_buy(game.players[2], game.properties[12], Random(1))
    assert game.players[2].name == CAUTIOUS
    assert not wants_to_buy(game.players[2], game.properties[14], Random(1))


def test_player_pays_rent_to_property_owner() -> None:
    """Valida o pagamento de aluguel ao proprietário."""
    game = make_game()
    owner = game.players[0]
    payer = game.players[1]
    game.properties[2].owner = owner.name

    game.play_turn(payer, die_roll=2)

    assert payer.balance == 280
    assert owner.balance == 320


def test_eliminated_player_releases_owned_properties() -> None:
    """Valida eliminação e liberação de propriedades."""
    game = make_game()
    owner = game.players[0]
    payer = game.players[1]
    payer.balance = 10
    game.properties[2].owner = owner.name
    game.properties[3].owner = payer.name

    game.play_turn(payer, die_roll=2)

    assert payer.balance == -10
    assert not payer.active
    assert game.properties[3].owner is None


def test_turn_order_breaks_balance_ties() -> None:
    """Valida o desempate pela ordem de turno."""
    game = make_game()
    game.players[0].balance = 300
    game.players[1].balance = 300
    game.players[2].balance = 100
    game.players[3].balance = 100

    ranked_players = game.ranked_players()

    assert ranked_players[0].name == IMPULSIVE
    assert ranked_players[1].name == DEMANDING
