import pandas as pd
import copy


class Miragine:

    def __init__(self, path='./data/army_infos.csv'):
        df = pd.read_csv(path, index_col='position')
        self.positions = df.index.tolist()
        self.data = df.T.to_dict()

    def decide_harm(self, left, right):
        """
        Decide the harm one soldier can cause to the enemy.
        """
        if right['armor_type'] == 'light':
            left_harm = left['harm_vs_light']
        elif right['armor_type'] == 'armored':
            left_harm = left['harm_vs_armored']

        if left['armor_type'] == 'light':
            right_harm = right['harm_vs_light']
        elif left['armor_type'] == 'armored':
            right_harm = right['harm_vs_armored']

        # 魔法攻击远程加成为原来的3倍，结论更符合大兵团作战。但作为出兵方（right），我们尽量不在无监督的情况下贸然派法师，因此加成系数小一点，为0.8
        left_harm = left_harm * (1 + 2 * left['ismagic'])
        right_harm = right_harm * (1 + 0.8 * right['ismagic'])

        return left_harm, right_harm

    def decide_time(self, left, right):
        """
        Decide how long a soldier can live under one enemy's attack.
        """
        left_harm, right_harm = self.decide_harm(left, right)

        left_time = (int(left['hp'] / right_harm) + 1) * right['weapon_speed']
        right_time = (int(right['hp'] / left_harm) + 1) * left['weapon_speed']

        return left_time, right_time

    def compare(self, army1, army2, mode):
        """
        Compare the time army1 and army2 exist on the battlefield.
        """
        left = self.data[army1]
        right = self.data[army2]

        left_time, right_time = self.decide_time(left, right)

        left_coef = 1 / left[mode]
        right_coef = 1 / right[mode]

        score = (right_time * right_coef - left_time *
                 left_coef) / (right_time * right_coef)

        return score

    def select_best(self, army1=1, mode='money'):
        """
        Choose best army2 to defeat army1 by comparing the time they exist.
        """
        pos = copy.deepcopy(self.positions)
        scores = []

        for army2 in pos:
            score = self.compare(army1, army2, mode)
            scores.append(score)

        res = pd.DataFrame({'pos': pos, 'score': scores}).sort_values(
            'score', ascending=False).reset_index(drop=True)

        return res
