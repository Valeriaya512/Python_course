#Homework使用AI寫猜數字遊戲

import tkinter as tk
import random

# =========================
# 視窗設定
# =========================

root = tk.Tk()
root.title("🎮 猜數字 GAME")
root.geometry("520x720")
root.configure(bg="#FFF6E9")
root.resizable(False, False)

# =========================
# 遊戲資料
# =========================

answer = random.randint(1, 100)
min_num = 1
max_num = 100
count = 0

# =========================
# 主卡片
# =========================

card = tk.Frame(
    root,
    bg="white",
    width=430,
    height=600,
    bd=0
)

card.place(relx=0.5, rely=0.5, anchor="center")

# 陰影感
shadow = tk.Frame(
    root,
    bg="#E5D7C5",
    width=440,
    height=610
)

shadow.place(relx=0.5, rely=0.5, anchor="center")
shadow.lower(card)

# =========================
# 標題
# =========================

title = tk.Label(
    card,
    text="🧸 猜數字大冒險",
    font=("Arial", 28, "bold"),
    bg="white",
    fg="#FF8A65"
)

title.pack(pady=(35, 10))

subtitle = tk.Label(
    card,
    text="猜猜看神秘數字是多少？",
    font=("Arial", 14),
    bg="white",
    fg="#999999"
)

subtitle.pack()

# =========================
# 範圍顯示
# =========================

range_frame = tk.Frame(
    card,
    bg="#FFF3E0",
    bd=0
)

range_frame.pack(pady=30, ipadx=30, ipady=15)

range_label = tk.Label(
    range_frame,
    text=f"🎯 範圍：{min_num} ~ {max_num}",
    font=("Arial", 22, "bold"),
    bg="#FFF3E0",
    fg="#FF7043"
)

range_label.pack()

# =========================
# 訊息框
# =========================

message_label = tk.Label(
    card,
    text="開始猜數字吧！",
    font=("Arial", 22, "bold"),
    bg="#F8FAFF",
    fg="#5C6BC0",
    width=20,
    height=3,
    relief="flat"
)

message_label.pack(pady=20)

# =========================
# 輸入框
# =========================

entry = tk.Entry(
    card,
    font=("Arial", 30, "bold"),
    justify="center",
    relief="flat",
    bg="#F4F7FF",
    fg="#333333",
    width=10
)

entry.pack(ipady=15)

# =========================
# 動畫效果
# =========================

def flash(color1, color2, times=6):

    def blink(i):

        if i > 0:

            current = message_label.cget("bg")

            if current == color1:
                message_label.config(bg=color2)
            else:
                message_label.config(bg=color1)

            root.after(120, blink, i - 1)

    blink(times)

# =========================
# 重設
# =========================

def reset_game():

    global answer
    global min_num
    global max_num
    global count

    answer = random.randint(1, 100)

    min_num = 1
    max_num = 100
    count = 0

    range_label.config(
        text=f"🎯 範圍：{min_num} ~ {max_num}"
    )

    message_label.config(
        text="重新開始！",
        fg="#5C6BC0",
        bg="#F8FAFF"
    )

    entry.delete(0, tk.END)

# =========================
# 猜數字
# =========================

def check_guess():

    global answer
    global min_num
    global max_num
    global count

    text = entry.get().strip()

    if not text.isdigit():

        message_label.config(
            text="⚠️ 請輸入數字",
            fg="#E53935"
        )

        flash("#FFDADA", "#F8FAFF")
        return

    guess = int(text)

    if guess < min_num or guess > max_num:

        message_label.config(
            text=f"⚠️ 請輸入 {min_num} ~ {max_num}",
            fg="#E53935"
        )

        flash("#FFDADA", "#F8FAFF")
        return

    count += 1

    # 猜對
    if guess == answer:

        message_label.config(
            text=f"🎉 猜對了！\n用了 {count} 次",
            fg="#43A047",
            bg="#FFF9C4"
        )

        flash("#FFF59D", "#FFF9C4", 10)

    # 太小
    elif guess < answer:

        min_num = guess + 1

        message_label.config(
            text="📈 太小了！",
            fg="#1E88E5",
            bg="#E3F2FD"
        )

    # 太大
    else:

        max_num = guess - 1

        message_label.config(
            text="📉 太大了！",
            fg="#FB8C00",
            bg="#FFF3E0"
        )

    range_label.config(
        text=f"🎯 範圍：{min_num} ~ {max_num}"
    )

    entry.delete(0, tk.END)

# =========================
# 按鈕區
# =========================

button_frame = tk.Frame(
    card,
    bg="white"
)

button_frame.pack(pady=35)

guess_btn = tk.Button(
    button_frame,
    text="🎯 猜看看",
    font=("Arial", 18, "bold"),
    bg="#5C6BC0",
    fg="white",
    relief="flat",
    activebackground="#3F51B5",
    activeforeground="white",
    width=12,
    height=2,
    cursor="hand2",
    command=check_guess
)

guess_btn.grid(row=0, column=0, padx=10)

reset_btn = tk.Button(
    button_frame,
    text="🔄 重玩",
    font=("Arial", 18, "bold"),
    bg="#FFB74D",
    fg="white",
    relief="flat",
    activebackground="#FB8C00",
    activeforeground="white",
    width=12,
    height=2,
    cursor="hand2",
    command=reset_game
)

reset_btn.grid(row=0, column=1, padx=10)

# =========================
# 次數顯示
# =========================

count_label = tk.Label(
    card,
    text="✨ 猜猜看神秘數字吧 ✨",
    font=("Arial", 14),
    bg="white",
    fg="#999999"
)

count_label.pack(pady=10)

# =========================
# Enter 鍵支援
# =========================

root.bind("<Return>", lambda event: check_guess())

# =========================
# 啟動
# =========================

root.mainloop()