import os
import math
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

#追加機能１
def gameover(screen: pg.Surface) -> None:
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.set_alpha(160)
    pg.draw.rect(black_sfc, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

    font = pg.font.Font(None, 80)
    txt_sfc = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_sfc.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    kk_img = pg.image.load("fig/8.png")
    kk_rct_l = kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    kk_rct_r = kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))

    screen.blit(black_sfc, (0, 0))
    screen.blit(txt_sfc, txt_rct)
    screen.blit(kk_img, kk_rct_l)
    screen.blit(kk_img, kk_rct_r)
    pg.display.update()

    time.sleep(5)

#追加機能２
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))  # 黒い背景部分を透過
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_base = pg.image.load("fig/3.png")
    kk_flip = pg.transform.flip(kk_base, True, False)  # 左右反転画像

    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_base, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(kk_base, 0, 0.9),  # 左
        (-5, -5): pg.transform.rotozoom(kk_base, -45, 0.9),  # 左上
        (0, -5): pg.transform.rotozoom(kk_flip, 90, 0.9),  # 上
        (+5, -5): pg.transform.rotozoom(kk_flip, 45, 0.9),  # 右上
        (+5, 0): pg.transform.rotozoom(kk_flip, 0, 0.9),  # 右
        (+5, +5): pg.transform.rotozoom(kk_flip, -45, 0.9),  # 右下
        (0, +5): pg.transform.rotozoom(kk_flip, -90, 0.9),  # 下
        (-5, +5): pg.transform.rotozoom(kk_base, 45, 0.9),  # 左下
    }
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2：赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    vx, vy = +5, +5  # 練習2：爆弾の初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこからしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセルする

        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = center

        acc = bb_accs[idx]
        avx = vx * (acc / 1.0)
        avy = vy * (acc / 1.0)

        bb_rct.move_ip(avx, avy)

        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()