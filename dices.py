from enum import Enum
import random

class DiceState(Enum):
    ROLL = 0,
    STAY = 1

class Dice:
    def __init__(self):
        self.rolls = [1, 2, 3, 4, 5, 6]
        self.state = DiceState.ROLL
        self.value = None

    def roll(self):
        if (self.state == DiceState.ROLL):
            self.value = random.choice(self.rolls)
        return self.value

    def set_stay_state(self):
        self.state = DiceState.STAY

    def set_roll_state(self):
        self.state = DiceState.ROLL

class FiveDices:
    def __init__(self):
        self.dice_num = 5
        self.dices = [Dice() for _ in range(self.dice_num)]
        self.values = [None for _ in range(self.dice_num)]

    def reset(self):
        self.dices = [Dice() for _ in range(self.dice_num)]
        # self.values = [None for _ in range(self.dice_num)]
        self.values = [dice.roll() for dice in self.dices]

    def roll(self):
        self.values = [dice.roll() for dice in self.dices]
        return self.values

    def select_stay(self, stayList):
        assert len(stayList) == self.dice_num, "input list is invalid"

        for i in range(self.dice_num):
            if stayList[i]:
                self.dices[i].set_stay_state()