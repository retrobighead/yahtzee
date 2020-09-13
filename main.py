from yahtzee import YahtzeeEnv
import re

# main
game = YahtzeeEnv(player_num=1, turn_num=2)
game.reset()

for i in range(3*2*12):
    game.render()

    ope = [0, 0, 0, 0, 0, None]
    if game.current_round == game.max_round_num-1:
        valid_roles = list(game.players[0].role_list.roles.keys())
        print("select role:", valid_roles)
        selected_role = None
        while (not selected_role):
            inp = input("*** select role *** : ")
            if inp in valid_roles:
                selected_role = inp
        ope[5] = selected_role
    else:
        valid_input = [1, 2, 3, 4, 5]
        print("select dice:", valid_input)
        num_list = []
        is_valid = False
        while (not is_valid):
            inp = input("*** select stay dices *** : ")
            inp = inp.replace(" ", "")
            m = re.match(r'[0-9\,]*', inp)
            if m:
                if inp == "": break
                nums = [int(num) for num in inp.split(",")]
                if set(nums).issubset(set(valid_input)):
                    num_list = nums
                    is_valid = True
        
        for num in num_list:
            ope[num-1] = 1
        
    print("operation:", ope)
        
    observation, reward, done, info = game.step(ope)