import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("エイリアン侵略")

        # ゲームの統計情報とスコアボードのインスタンスを生成する
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # エイリアン侵略ゲームをアクティブな状態で開始する
        self.game_active = False

        # Play ボタンを作成する
        self.play_button = Button(self, "Play")

    def run_game(self):
        """ゲームのメインループを開始する"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(60)

            self._update_screen()

    def _check_events(self):
        """キーボードとマウスのイベントを監視する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """キーを押すイベントに応答する"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """キーを離すイベントに応答する"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """プレイヤーが Play ボタンをクリックしたら新規ゲームを開始する"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # ゲームの設定をリセットする
            self.settings.initialize_dynamic_settings()

            # ゲームの統計情報をリセットする
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 残った弾とエイリアンを廃棄する
            self.bullets.empty()
            self.aliens.empty()

            # 新しい艦隊を生成し、宇宙船を画面の中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            # マウスカーソルを非表示にする
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """新しい弾を生成し bullets グループに追加する"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        self.bullets.update()

        # 見えなくなった弾を廃棄する
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """弾とエイリアンの衝突に対応する"""
        # 衝突した弾とエイリアンを削除する
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 存在する弾を破壊し、新しい艦隊を作成し、速度を上げる
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # レベルを増やす
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """艦隊が画面の端にいるか確認してから、位置を更新する"""
        self._check_fleet_edges()
        self.aliens.update()

        # エイリアンと宇宙船の衝突をチェックする
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 画面の一番下に到達したエイリアンを探す
        self._check_aliens_bottom()

    def _ship_hit(self):
        """エイリアンと宇宙船の衝突に対応する"""
        if self.stats.ships_left > 0:
            # 残りの宇宙船の数を減らす
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 残ったエイリアンと弾を廃棄する
            self.bullets.empty()
            self.aliens.empty()

            # 新しい艦隊を生成し、宇宙船を画面の中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            # 一時停止する
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """エイリアンが画面の底に達したかを確認する"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 宇宙船を破壊した時と同じように処理する
                self._ship_hit()
                break

    def _create_fleet(self):
        """エイリアン艦隊を作成する"""
        # 1匹のエイリアンを生成し、スペースがなくなるまでエイリアンを追加し続ける
        # 各エイリアンの間には縦横ともにエイリアン1匹分のスペースを空ける
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width -2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 列の最後でX座標をリセットし、Y座標を増加する
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_positoin, y_position):
        """エイリアンを1匹作成し列の中に配置する"""
        new_alien = Alien(self)
        new_alien.x = x_positoin
        new_alien.rect.x = x_positoin
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """エイリアンが画面の端に達した場合に適切な処理を行う"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """艦隊を下に移動し、移動方向を変更する"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """画面上の画像を更新し、新しい画面に切り替える"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 得点の情報を描画する
        self.sb.show_score()

        # ゲームが非アクティブの場合は Play ボタンを描画する
        if not self.game_active:
            self.play_button.draw_button()

        # 最新の画面を表示する
        pygame.display.flip()

if __name__ == '__main__':
    # ゲームのインスタンスを作成し、ゲームを実行する
    ai = AlienInvasion()
    ai.run_game()
