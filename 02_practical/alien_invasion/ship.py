import pygame

class Ship:
    """宇宙船を管理するクラス"""

    def __init__(self, ai_game):
        """宇宙船を初期化し、開始時の位置を設定する"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 宇宙船の画像を読み込み、サイズを取得する
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 新しい宇宙船を画面下部の中央に配置する
        self.rect.midbottom = self.screen_rect.midbottom

        # 左右の移動フラグ: 開始時は宇宙船は移動していない
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """"左右の移動フラグに応じて宇宙船の位置を更新する"""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """宇宙船の現在位置に宇宙船を描画する"""
        self.screen.blit(self.image, self.rect)
