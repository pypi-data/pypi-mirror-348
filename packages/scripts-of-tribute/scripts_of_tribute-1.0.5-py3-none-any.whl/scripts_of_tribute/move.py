from typing import List, Union

from scripts_of_tribute.protos import basics_pb2
from scripts_of_tribute.protos.basics_pb2 import BasicMove as ProtoBasicMove, Move
from scripts_of_tribute.enums import MoveEnum, PatronId

class BasicMove:
    def __init__(self, move_id: int, command: MoveEnum):
        self.move_id = move_id
        self.command = command

    def to_proto(self) -> Move:
        move_proto = Move()
        move_proto.id = self.move_id
        move_proto.command = self.command.value
        move_proto.Basic.CopyFrom(ProtoBasicMove()) 
        return move_proto

class SimpleCardMove(BasicMove):
    def __init__(self, move_id: int, command: MoveEnum, cardUniqueId: int):
        super().__init__(move_id, command)
        self.cardUniqueId = cardUniqueId

    def to_proto(self) -> Move:
        move_proto = super().to_proto()
        move_proto.CardMove.cardUniqueId = self.cardUniqueId
        return move_proto

class SimplePatronMove(BasicMove):
    def __init__(self, move_id: int, command: MoveEnum, patronId: PatronId):
        super().__init__(move_id, command)
        self.patronId = patronId
    
    def to_proto(self) -> Move:
        move_proto = super().to_proto()
        move_proto.PatronMove.patronId = self.patronId.value
        return move_proto

class MakeChoiceMoveUniqueCard(BasicMove):
    def __init__(self, move_id: int, command: MoveEnum, cardsUniqueIds: List[int]):
        super().__init__(move_id, command)
        self.cardsUniqueIds = cardsUniqueIds

    def to_proto(self) -> Move:
        move_proto = super().to_proto()
        move_proto.CardChoiceMove.cardsUniqueIds.extend(self.cardsUniqueIds)
        return move_proto

class MakeChoiceMoveUniqueEffect(BasicMove):
    def __init__(self, move_id: int, command: MoveEnum, effects: List[str]):
        super().__init__(move_id, command)
        self.effects = effects

    def to_proto(self) -> Move:
        move_proto = super().to_proto()
        move_proto.EffectChoiceMove.effects.extend(self.effects)
        return move_proto
    

def from_proto_move(move_proto: basics_pb2.Move) -> Union[BasicMove, SimpleCardMove, SimplePatronMove, MakeChoiceMoveUniqueCard, MakeChoiceMoveUniqueEffect]:
    move_id = move_proto.id
    command = MoveEnum(move_proto.command)

    if move_proto.HasField("Basic"):
        return BasicMove(move_id=move_id, command=command)
    elif move_proto.HasField("CardMove"):
        return SimpleCardMove(
            move_id=move_id,
            command=command,
            cardUniqueId=move_proto.CardMove.cardUniqueId
        )
    elif move_proto.HasField("PatronMove"):
        return SimplePatronMove(
            move_id=move_id,
            command=command,
            patronId=PatronId(move_proto.PatronMove.patronId)
        )
    elif move_proto.HasField("CardChoiceMove"):
        return MakeChoiceMoveUniqueCard(
            move_id=move_id,
            command=command,
            cardsUniqueIds=list(move_proto.CardChoiceMove.cardsUniqueIds)
        )
    elif move_proto.HasField("EffectChoiceMove"):
        return MakeChoiceMoveUniqueEffect(
            move_id=move_id,
            command=command,
            effects=list(move_proto.EffectChoiceMove.effects)
        )
    else:
        raise ValueError("Invalid Move proto: No move type set in the oneof field")
