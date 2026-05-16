import random


def guess_number_game():
    """玩一個簡單的猜數字遊戲。"""
    secret = random.randint(1, 100)
    attempts = 0

    print("歡迎來到猜數字遊戲！")
    print("我已經想好一個 1 到 100 之間的整數。請試著猜看看。")
    print("輸入 q 或 quit 來結束遊戲。")

    while True:
        guess = input("請輸入你的猜測：").strip()
        if guess.lower() in {"q", "quit"}:
            print("遊戲結束。下次再玩吧！")
            break

        if not guess.isdigit():
            print("請輸入 1 到 100 之間的正整數，或輸入 q 退出。")
            continue

        guess_value = int(guess)
        attempts += 1

        if guess_value < 1 or guess_value > 100:
            print("請猜 1 到 100 之間的數字。")
            continue

        if guess_value < secret:
            print("太小了，請再試一次。")
        elif guess_value > secret:
            print("太大了，請再試一次。")
        else:
            print(f"恭喜你！你猜對了。答案是 {secret}。")
            print(f"你總共花了 {attempts} 次猜中。")
            break


if __name__ == "__main__":
    guess_number_game()
