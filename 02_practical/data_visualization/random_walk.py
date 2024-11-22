from random import choice

class RandomWalk:
    """ランダムウォークを生成するクラス"""

    def __init__(self, num_points=5000):
        """ランダムウォークの属性を初期化する"""
        self.num_points = num_points

        # すべてのランダムウォークは(0, 0)から開始する
        self.x_values = [0]
        self.y_values = [0]
