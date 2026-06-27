import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（微軟正黑體，適用於 Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 產生 X 軸資料：0 到 4π
x = np.linspace(0, 4 * np.pi, 1000)

# 建立圖表與軸
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)  # 預留空間給滑桿

# 初始參數值
A_init = 1.0
omega_init = 1.0
phi_init = 0.0

# 計算初始波形
y_sin = A_init * np.sin(omega_init * x + phi_init)
y_cos = A_init * np.cos(omega_init * x + phi_init)

# 繪製 sin 與 cos 曲線
line_sin, = ax.plot(x, y_sin, label='sin', color='blue')
line_cos, = ax.plot(x, y_cos, label='cos', color='orange')

# 設定圖表標題、軸標籤、格線與圖例
ax.set_title('正弦（sin）與餘弦（cos）波形', fontsize=14)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper right')

# 設定 X 軸範圍
ax.set_xlim(0, 4 * np.pi)

# 建立三個滑桿的座標 [左, 下, 寬, 高]
ax_amp = plt.axes([0.2, 0.20, 0.6, 0.03])
ax_freq = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_phase = plt.axes([0.2, 0.10, 0.6, 0.03])

# 建立滑桿物件
slider_amp = Slider(ax_amp, '振幅 A', 0.1, 5.0, valinit=A_init)
slider_freq = Slider(ax_freq, '頻率 ω', 0.1, 10.0, valinit=omega_init)
slider_phase = Slider(ax_phase, '相位 φ', 0, 2 * np.pi, valinit=phi_init)

# 定義更新函數
def update(val):
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    # 更新曲線資料
    line_sin.set_ydata(A * np.sin(omega * x + phi))
    line_cos.set_ydata(A * np.cos(omega * x + phi))

    # 重新繪製
    fig.canvas.draw_idle()

# 註冊滑桿事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

# 顯示互動視窗
plt.show()
