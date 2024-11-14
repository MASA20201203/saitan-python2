import sys

import pygame

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("エイリアン侵略")

    def run_game(self):
        """ゲームのメインループを開始する"""
        while True:
            # イベントを監視する
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # 最新の画面を表示する
            pygame.display.flip()

if __name__ == '__main__':
    # ゲームのインスタンスを作成し、ゲームを実行する
    ai = AlienInvasion()
    ai.run_game()
