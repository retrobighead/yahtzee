from dices import FiveDices
from roles import RoleList, RoleType

class Player:
    def __init__(self, name):
        self.name = name
        self.role_list = RoleList()
        self.dices = FiveDices()
        self.selected_roles = {role: 0 for role in self.role_list.roles}
        self.score = 0
        self.upper_role_score = 0
        self.upper_role_bonus_threshold = 63
        self.can_get_score_bonus = False
        self.bonus_score = 35

    def select_stay(self, stay_list):
        self.dices.select_stay([bool(n) for n in stay_list])

    def roll_dices(self):
        self.dices.roll()

    def reset_dices(self):
        self.dices.reset()

    def select_role(self, role_name):
        role = self.role_list.roles[role_name]
        score = role.calculate(self.dices)
        self.selected_roles[role_name] = score
        self.update_score()

    def update_score(self):
        self.score = sum(list(self.selected_roles.values()))
        self.update_upper_role_score()
        if self.can_get_score_bonus:
            self.score += self.bonus_score

    def update_upper_role_score(self):
        self.upper_role_score = 0
        for role in self.role_list.roles.values():
            if role.role_type == RoleType.UPPER:
                self.upper_role_score += self.selected_roles[role.name]

        self.can_get_score_bonus = (self.upper_role_score >= self.upper_role_bonus_threshold)