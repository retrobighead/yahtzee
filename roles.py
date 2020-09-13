from enum import Enum
from collections import Counter

class RoleType(Enum):
    LOWER = 0,
    UPPER = 1

class Role:
    def __init__(self, name, description, role_type, checkFunc, scoreFunc):
        self.name = name
        self.description = description
        self.role_type = role_type
        self.checkFunc = checkFunc
        self.scoreFunc = scoreFunc

    def calculate(self, dices):
        if not self.checkFunc(dices):
            return 0
        return self.scoreFunc(dices)


class RoleList:
    def __init__(self):
        self.dice_num = 5
        self.NoneCheck = lambda dices: all([(val is not None) for val in dices.values])
        self.CountList = lambda dices: [item[1] for item in Counter(dices.values).most_common()]

        # aces
        self.acesCheckFunc = lambda dices: self.NoneCheck(dices)
        self.acesScoreFunc = lambda dices: dices.values.count(1)
        self.aces = Role("Aces", "The sum of dice with the number 1", RoleType.UPPER, self.acesCheckFunc,
                         self.acesScoreFunc)

        # twos
        self.twosCheckFunc = lambda dices: self.NoneCheck(dices)
        self.twosScoreFunc = lambda dices: dices.values.count(2) * 2
        self.twos = Role("Twos", "The sum of dice with the number 2", RoleType.UPPER, self.twosCheckFunc,
                         self.twosScoreFunc)

        # threes
        self.threesCheckFunc = lambda dices: self.NoneCheck(dices)
        self.threesScoreFunc = lambda dices: dices.values.count(3) * 3
        self.threes = Role("Threes", "The sum of dice with the number 3", RoleType.UPPER, self.threesCheckFunc,
                           self.threesScoreFunc)

        # fours
        self.foursCheckFunc = lambda dices: self.NoneCheck(dices)
        self.foursScoreFunc = lambda dices: dices.values.count(4) * 4
        self.fours = Role("Fours", "The sum of dice with the number 4", RoleType.UPPER, self.foursCheckFunc,
                          self.foursScoreFunc)

        # fives
        self.fivesCheckFunc = lambda dices: self.NoneCheck(dices)
        self.fivesScoreFunc = lambda dices: dices.values.count(5) * 5
        self.fives = Role("Fives", "The sum of dice with the number 5", RoleType.UPPER, self.fivesCheckFunc,
                          self.fivesScoreFunc)

        # sixes
        self.sixesCheckFunc = lambda dices: self.NoneCheck(dices)
        self.sixesScoreFunc = lambda dices: dices.values.count(6) * 6
        self.sixes = Role("Sixes", "The sum of dice with the number 6", RoleType.UPPER, self.sixesCheckFunc,
                          self.sixesScoreFunc)

        # three of a kind
        self.threeOfAKindCheckFunc = lambda dices: self.NoneCheck(dices) and Counter(dices.values).most_common(1)[0][
            1] >= 3
        self.threeOfAKindScoreFunc = lambda dices: sum(dices.values)
        self.three_of_a_kind = Role("ThreeOfAKind", "At least three dice the same", RoleType.LOWER,
                                    self.threeOfAKindCheckFunc, self.threeOfAKindScoreFunc)

        # four of a kind
        self.fourOfAKindCheckFunc = lambda dices: self.NoneCheck(dices) and Counter(dices.values).most_common(1)[0][
            1] >= 4
        self.fourOfAKindScoreFunc = lambda dices: sum(dices.values)
        self.four_of_a_kind = Role("FourOfAKind", "At least four dice the same", RoleType.LOWER,
                                   self.fourOfAKindCheckFunc, self.fourOfAKindScoreFunc)

        # full house
        self.fullHouseScoreFunc = lambda dices: 25
        self.full_house = Role("FullHouse", "Three of one number and two of another", RoleType.LOWER,
                               self.fullHouseCheckFunc, self.fullHouseScoreFunc)

        # small straight
        self.smallStraightScoreFunc = lambda dices: 30
        self.small_straight = Role("SmallStraight", "Four sequential dice (1-2-3-4, 2-3-4-5, or 3-4-5-6)",
                                   RoleType.LOWER, self.smallStraightCheckFunc, self.smallStraightScoreFunc)

        # large straight
        self.largeStraightScoreFunc = lambda dices: 40
        self.large_straight = Role("LargeStraight", "Five sequential dice (1-2-3-4-5 or 2-3-4-5-6)", RoleType.LOWER,
                                   self.largeStraightCheckFunc, self.largeStraightScoreFunc)

        # yahtzee
        self.yahtzeeCheckFunc = lambda dices: self.NoneCheck(dices) and len(self.CountList(dices)) == 1
        self.yahtzeeScoreFunc = lambda dices: 50
        self.yahtzee = Role("Yahtzee", "All five dice the same", RoleType.LOWER, self.yahtzeeCheckFunc,
                            self.yahtzeeScoreFunc)

        # chance
        self.chanceCheckFunc = lambda dices: self.NoneCheck(dices)
        self.chanceScoreFunc = lambda dices: sum(dices.values)
        self.chance = Role("Chance", "Any combination", RoleType.LOWER, self.chanceCheckFunc, self.chanceScoreFunc)

        self.roles = {"Aces": self.aces, "Twos": self.twos, "Threes": self.threes, "Fours": self.fours,
                      "Fives": self.fives, "Sixes": self.sixes,
                      "ThreeOfAKind": self.three_of_a_kind, "FourOfAKind": self.four_of_a_kind,
                      "FullHouse": self.full_house,
                      "SmallStraight": self.small_straight, "LargeStraight": self.large_straight,
                      "Yahtzee": self.yahtzee, "Chance": self.chance}

    def fullHouseCheckFunc(self, dices):
        if not self.NoneCheck(dices): return False
        freqs = self.CountList(dices)
        if (len(freqs) == 1):
            return True
        else:
            return freqs[0] + freqs[1] == 5

    def smallStraightCheckFunc(self, dices):
        if not self.NoneCheck(dices): return False
        list_set = set(dices.values)
        return {1, 2, 3, 4}.issubset(list_set) or {2, 3, 4, 5}.issubset(list_set) or {3, 4, 5, 6}.issubset(list_set)

    def largeStraightCheckFunc(self, dices):
        if not self.NoneCheck(dices): return False
        list_set = set(dices.values)
        return list_set == {1, 2, 3, 4, 5} or list_set == {2, 3, 4, 5, 6}