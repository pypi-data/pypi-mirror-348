from enum import Enum

class PatronId(Enum):
    ANSEI = 0
    DUKE_OF_CROWS = 1
    RAJHIN = 2
    PSIJIC = 3
    ORGNUM = 4
    HLAALU = 5
    PELIN = 6
    RED_EAGLE = 7
    TREASURY = 8
    SAINT_ALESSIA = 9

    @classmethod
    def from_string(cls, patron_str: str) -> 'PatronId':
        try:
            return cls[patron_str]  # Look up the enum member by name
        except KeyError:
            raise ValueError(f"Invalid patron string: {patron_str}")

class MoveEnum(Enum):
    PLAY_CARD = 0
    ACTIVATE_AGENT = 1
    ATTACK = 2
    BUY_CARD = 3
    CALL_PATRON = 4
    MAKE_CHOICE = 5
    END_TURN = 6

class BoardState(Enum):
    NORMAL = 0
    CHOICE_PENDING = 1
    START_OF_TURN_CHOICE_PENDING = 2
    PATRON_CHOICE_PENDING = 3

class PlayerEnum(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    NO_PLAYER_SELECTED = 2

    @classmethod
    def from_string(cls, player_str: str) -> 'PlayerEnum':
        try:
            return cls[player_str]  # Look up the enum member by name
        except KeyError:
            raise ValueError(f"Invalid patron string: {player_str}")

class CardType(Enum):
    ACTION = 0
    AGENT = 1
    CONTRACT_ACTION = 2
    CONTRACT_AGENT = 3
    STARTER = 4
    CURSE = 5

class ChoiceDataType(Enum):
    CARD = 0
    EFFECT = 1
