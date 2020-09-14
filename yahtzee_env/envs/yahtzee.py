from yahtzee_env.envs.player import Player
from yahtzee_env.envs.dices import DiceState
from yahtzee_env.envs.roles import RoleList
import gym
import gym.spaces
import numpy as np

class YahtzeeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, player_num=2, turn_num=12, round_num=3):
        super().__init__()
        self.action_space = gym.spaces.MultiDiscrete([2,2,2,2,2,12])
        self.observation_space = gym.spaces.MultiDiscrete([6,6,6,6,6])

        self.dice_num = 5
        self.player_num = player_num
        self.max_turn_num = turn_num
        self.max_round_num = round_num
        self.current_player = 0
        self.current_round = 0
        self.current_turn = 0
        self.players = [Player("Player" + str(p+1)) for p in range(self.player_num)]
        self.roll_dices()
        self.role_list = RoleList().role_names

    def get_observation(self):
        return np.array(self.players[self.current_player].dices.values, dtype=np.int32)

    def get_reward(self):
        if (self.current_round != self.max_round_num-1): return 0
        elif self.get_done(): return self.players[self.current_player].score

        updated_score = self.players[self.current_player].updated_score
        if updated_score <= 0: return -10
        return updated_score

    def get_done(self):
        return (self.current_round == self.max_round_num - 1 and self.current_player == self.player_num - 1 and self.current_turn == self.max_turn_num - 1)

    def reset(self):
        self.current_player = 0
        self.current_round = 0
        self.current_turn = 0
        self.players = [Player("Player" + str(p+1)) for p in range(self.player_num)]
        self.roll_dices()

        return self.get_observation()

    def roll_dices(self):
        for player in self.players:
            player.roll_dices()

    def increment(self):
        self.current_round = (self.current_round +1) % self.max_round_num
        if self.current_round == 0:
            self.current_player = (self.current_player +1) % self.player_num
            if self.current_player == 0:
                self.current_turn = (self.current_turn +1) % self.max_turn_num

        if self.current_round == 0 and self.current_player == 0 and self.current_turn == 0:
            self.reset()

    def is_role_selected_round(self):
        return self.current_round == self.max_round_num - 1

    def step(self, operation):
        stay_list = operation[:self.dice_num]
        selected_role = self.role_list[operation[self.dice_num]]
        player = self.players[self.current_player]

        valid_input = True
        if valid_input:
            player.select_stay(stay_list)

            if self.is_role_selected_round():
                player.select_role(selected_role)
                player.reset_dices()
            else:
                self.roll_dices()

            observation = self.get_observation()
            reward = self.get_reward()
            done = self.get_done()
            info = {}

            self.increment()

            return observation, reward, done, info
        else:
            return None, None, None, {}

    def render(self):
        print("================== Score Board ====================")
        roles = list(self.role_list.roles.keys())
        for role in roles:
            output = [role] + [str(player.selected_roles[role]) for player in self.players]
            print(self.make_output_line(output))

        print("---------------------------------------------------")
        output = ["bonus"] + [str(player.bonus_score if player.can_get_score_bonus else 0) for player in self.players]
        print(self.make_output_line(output))
        output = ["score"] + [str(player.score) for player in self.players]
        print(self.make_output_line(output))

        print("===================== Play ========================")
        player = self.players[self.current_player]
        print("turn:", self.current_turn, ", player:", player.name, ", round:", self.current_round)

        print("---------------------------------------------------")
        print("dices:", ["{}{}".format(str(dice.value), "[S]" if dice.state == DiceState.STAY else "") for dice in
                         player.dices.dices])

    def make_output_line(self, str_list, length=14):
        output = [str(ele).center(length) for ele in str_list]
        return "| " + " | ".join(output) + "|"
