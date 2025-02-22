import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """宇宙船を管理するクラス"""

    def __init__(self, ai_game):
        """宇宙船を初期化し、開始時の位置を設定する"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 宇宙船の画像を読み込み、サイズを取得する
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 新しい宇宙船を画面下部の中央に配置する
        self.rect.midbottom = self.screen_rect.midbottom

        # 宇宙船の水平位置を浮動小数点数で格納する
        self.x = float(self.rect.x)

        # 左右の移動フラグ: 開始時は宇宙船は移動していない
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """"左右の移動フラグに応じて宇宙船の位置を更新する"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # self.xの値を更新した後にself.rectの位置を更新する
        self.rect.x = self.x

    def blitme(self):
        """宇宙船の現在位置に宇宙船を描画する"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """宇宙船を画面の中央に配置する"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
