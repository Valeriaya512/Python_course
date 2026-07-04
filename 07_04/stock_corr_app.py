#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yfinance as yf
import pandas as pd
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QStatusBar, QFrame, QLineEdit, QListWidget, QListWidgetItem,
    QScrollArea, QGridLayout, QSizePolicy, QAbstractItemView,
    QCompleter,
)
from PySide6.QtCore import Qt, QThread, Signal, QSize, QRectF, QStringListModel
from PySide6.QtGui import (
    QColor, QFont, QBrush, QPainter, QLinearGradient,
    QPalette,
)

STYLE = """
QMainWindow { background-color: #09090b; }
QLabel {
    color: #e4e4e7;
    font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;
    font-size: 13px;
}
QLabel#titleLabel {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
}
QLabel#subTitleLabel {
    color: #71717a;
    font-size: 12px;
    margin-bottom: 4px;
}
QFrame#searchFrame {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 10px;
    padding: 16px;
}
QFrame#infoCard {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 10px;
    padding: 14px;
}
QLineEdit {
    background-color: #09090b;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 10px 14px;
    color: #e4e4e7;
    font-size: 14px;
    font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;
}
QLineEdit:focus {
    border: 1px solid #7c3aed;
}
QLineEdit::placeholder { color: #52525b; }
QPushButton {
    background-color: #7c3aed;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 700;
    font-size: 13px;
    font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;
}
QPushButton:hover { background-color: #8b5cf6; }
QPushButton:pressed { background-color: #6d28d9; }
QPushButton:disabled { background-color: #27272a; color: #52525b; }
QPushButton#removeBtn {
    background-color: transparent;
    border: 1px solid #3f3f46;
    border-radius: 14px;
    padding: 4px 10px;
    color: #f87171;
    font-size: 11px;
    font-weight: 600;
}
QPushButton#removeBtn:hover { background-color: #7f1d1d; border-color: #ef4444; }
QTableWidget {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 8px;
    gridline-color: #27272a;
    font-family: "Microsoft JhengHei", "Noto Sans TC", "Consolas", sans-serif;
    font-size: 12px;
    color: #e4e4e7;
}
QTableWidget::item { padding: 6px 10px; }
QTableWidget::item:selected { background-color: #7c3aed; }
QHeaderView::section {
    background-color: #09090b;
    color: #a1a1aa;
    border: none;
    border-bottom: 1px solid #27272a;
    padding: 8px 10px;
    font-weight: 700;
    font-size: 12px;
    font-family: "Microsoft JhengHei", "Noto Sans TC", sans-serif;
}
QStatusBar { background-color: #09090b; color: #71717a; border-top: 1px solid #27272a; font-size: 12px; }
QScrollBar:horizontal { background: #09090b; height: 8px; }
QScrollBar::handle:horizontal { background: #27272a; border-radius: 4px; min-width: 20px; }
QScrollBar::handle:horizontal:hover { background: #3f3f46; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""

TAIWAN_STOCKS = {
    "台積電": "2330.TW", "鴻海精密": "2317.TW", "聯發科": "2454.TW",
    "台達電": "2308.TW", "中華電": "2412.TW", "國泰金": "2882.TW",
    "富邦金": "2881.TW", "中信金": "2891.TW", "兆豐金": "2886.TW",
    "日月光投控": "3711.TW", "聯電": "2303.TW", "廣達": "2382.TW",
    "華碩": "2357.TW", "緯創": "3231.TW", "聯詠": "3034.TW",
    "瑞昱": "2379.TW", "大立光": "3008.TW", "台塑": "1301.TW",
    "南亞": "1303.TW", "台化": "1326.TW", "中鋼": "2002.TW",
    "統一": "1216.TW", "長榮": "2603.TW", "陽明": "2609.TW",
    "萬海": "2615.TW", "和泰車": "2207.TW", "裕隆": "2201.TW",
    "台泥": "1101.TW", "亞泥": "1102.TW", "遠東新": "1402.TW",
    "中鼎": "9933.TW", "力積電": "6770.TW", "世界先進": "5347.TW",
    "穩懋": "3105.TW", "環球晶": "6488.TW", "中美晶": "5483.TW",
    "台光電": "2383.TW", "欣興": "3037.TW", "南電": "8046.TW",
    "景碩": "3189.TW", "華通": "2313.TW", "金像電": "2368.TW",
    "健鼎": "3044.TW", "台達化": "1309.TW", "中石化": "1314.TW",
    "長興": "1717.TW", "永光": "1711.TW", "中纖": "1718.TW",
    "東和鋼鐵": "2006.TW", "豐興": "2015.TW", "大成鋼": "2027.TW",
    "台橡": "2103.TW", "正新": "2105.TW", "建大": "2106.TW",
    "國巨": "2327.TW", "華新科": "2492.TW", "奇力新": "2456.TW",
    "鴻準": "2354.TW", "可成": "2474.TW", "臻鼎-KY": "4958.TW",
    "台達電": "2308.TW", "仁寶": "2324.TW", "英業達": "2356.TW",
    "和碩": "4938.TW", "微星": "2377.TW", "技嘉": "2376.TW",
    "光寶科": "2301.TW", "佳世達": "2352.TW", "友達": "2409.TW",
    "群創": "3481.TW", "晶睿": "3454.TW", "中興電": "1513.TW",
    "東元": "1504.TW", "大同": "2371.TW", "亞德客-KY": "1590.TW",
    "上銀": "2049.TW", "台玻": "1802.TW", "寶成": "9904.TW",
    "豐泰": "9910.TW", "儒鴻": "1476.TW", "聚陽": "1477.TW",
    "富邦媒": "8454.TW", "網家": "8044.TW", "全家": "5903.TW",
    "瓦城": "2729.TW", "晶華": "2707.TW", "漢來美食": "1268.TW",
    "王品": "2727.TW", "台灣高鐵": "2633.TW", "華航": "2610.TW",
    "長榮航": "2618.TW", "星宇航空": "2646.TW", "玉山金": "2884.TW",
    "元大金": "2885.TW", "永豐金": "2890.TW", "開發金": "2883.TW",
    "新光金": "2888.TW", "台新金": "2887.TW", "第一金": "2892.TW",
    "合庫金": "5880.TW", "彰銀": "2801.TW", "華南金": "2880.TW",
    "中租-KY": "5871.TW", "上海商銀": "5876.TW", "京城銀": "2809.TW",
}

MAX_STOCKS = 4


class FetchWorker(QThread):
    finished = Signal(object, object, object)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, tickers, start_date):
        super().__init__()
        self.tickers = tickers
        self.start_date = start_date

    def run(self):
        try:
            codes = list(self.tickers.values())
            self.progress.emit(f"正在下載 {len(codes)} 檔股票資料...")
            data = yf.download(
                codes, start=self.start_date, interval="1d",
                auto_adjust=True, progress=False,
            )
            if data.empty:
                self.error.emit("無法取得資料，請確認網路或股票代碼是否正確")
                return
            close = data["Close"]
            close.columns = [str(c) for c in close.columns]
            self.progress.emit("計算報酬率與相關係數...")
            returns = close.pct_change().dropna()
            corr = returns.corr()
            self.finished.emit(close, returns, corr)
        except Exception as e:
            self.error.emit(f"錯誤：{str(e)}")


class HeatmapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.corr_matrix = None
        self.labels = []
        self.setMinimumSize(320, 320)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, corr_matrix, labels):
        self.corr_matrix = corr_matrix
        self.labels = labels
        self.update()

    def _interpolate_color(self, t):
        t = max(-1.0, min(1.0, t))
        if t < 0:
            ratio = (t + 1.0)
            r = int(33 + (179 - 33) * ratio)
            g = int(33 + (218 - 33) * ratio)
            b = int(120 + (255 - 120) * ratio)
        else:
            ratio = t
            r = int(239 + (220 - 239) * ratio)
            g = int(68 + (38 - 68) * ratio)
            b = int(68 + (38 - 68) * ratio)
        return QColor(r, g, b)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        if self.corr_matrix is None or len(self.labels) == 0:
            painter.setPen(QColor("#52525b"))
            painter.setFont(QFont("Microsoft JhengHei", 12))
            painter.drawText(self.rect(), Qt.AlignCenter, "請選擇股票並下載資料")
            return

        n = len(self.labels)
        margin_left = 70
        margin_top = 60
        margin_right = 20
        margin_bottom = 20
        cell_w = (w - margin_left - margin_right) / n
        cell_h = (h - margin_top - margin_bottom) / n
        cell_size = min(cell_w, cell_h)
        total_size = cell_size * n
        offset_x = margin_left + (w - margin_left - margin_right - total_size) / 2
        offset_y = margin_top

        font = QFont("Consolas", 10, QFont.Bold)
        painter.setFont(font)

        for i in range(n):
            for j in range(n):
                val = self.corr_matrix.iloc[i, j]
                x = offset_x + j * cell_size
                y = offset_y + i * cell_size
                rect = QRectF(x, y, cell_size, cell_size)

                color = self._interpolate_color(val)
                painter.setBrush(color)
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
                painter.drawRoundedRect(rect, 3, 3)

                text_color = QColor("#ffffff") if abs(val) > 0.4 else QColor("#e4e4e7")
                painter.setPen(text_color)
                f = QFont("Consolas", int(max(8, cell_size * 0.24)), QFont.Bold)
                painter.setFont(f)
                painter.drawText(rect, Qt.AlignCenter, f"{val:.3f}")

        painter.setPen(QColor("#a1a1aa"))
        name_font = QFont("Microsoft JhengHei", int(max(8, cell_size * 0.2)))
        painter.setFont(name_font)

        for i in range(n):
            label = self.labels[i]
            tr = len(label)
            if tr > 4 and cell_size < 60:
                label = label[:3] + ".."
            x = offset_x - 6
            y = offset_y + i * cell_size + cell_size / 2 + 4
            painter.drawText(QRectF(0, offset_y + i * cell_size, offset_x - 8, cell_size),
                             Qt.AlignRight | Qt.AlignVCenter, label)

            x = offset_x + i * cell_size + cell_size / 2
            y = offset_y - 8
            painter.save()
            painter.translate(x, y)
            painter.rotate(30)
            painter.drawText(QRectF(-cell_size, 0, cell_size * 2, 20),
                             Qt.AlignLeft | Qt.AlignVCenter, label)
            painter.restore()

        painter.end()


class StockChip(QFrame):
    removed = Signal(str)

    def __init__(self, name, code):
        super().__init__()
        self.code = code
        self.name = name
        self.setObjectName("infoCard")
        self.setStyleSheet("""
            QFrame#infoCard {
                background-color: #18181b;
                border: 1px solid #7c3aed;
                border-radius: 16px;
                padding: 4px 8px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 4, 4)
        layout.setSpacing(6)
        label = QLabel(f"{name}  ({code.replace('.TW', '')})")
        label.setStyleSheet("color: #e4e4e7; font-size: 12px; font-weight: 600; border: none; background: transparent;")
        layout.addWidget(label)
        btn = QPushButton("✕")
        btn.setObjectName("removeBtn")
        btn.setFixedSize(22, 22)
        btn.clicked.connect(lambda: self.removed.emit(self.code))
        layout.addWidget(btn)

    def sizeHint(self):
        return QSize(120, 32)


class StockCorrelationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台股相關係數分析平台")
        self.resize(1100, 850)
        self.setStyleSheet(STYLE)

        self.selected_stocks = {}
        self.close_data = None
        self.returns_data = None
        self.corr_data = None

        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 20, 24, 16)
        main_layout.setSpacing(14)
        main_layout.setAlignment(Qt.AlignTop)

        # ── Header ──
        title = QLabel("台股相關係數分析平台")
        title.setObjectName("titleLabel")
        subtitle = QLabel("搜尋並選擇最多 4 檔台股，即時計算日報酬率相關係數")
        subtitle.setObjectName("subTitleLabel")
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ── Search + Controls ──
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QVBoxLayout(search_frame)
        search_layout.setContentsMargins(16, 14, 16, 14)
        search_layout.setSpacing(10)

        row1 = QHBoxLayout()
        row1.setSpacing(10)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("輸入股票名稱或代碼搜尋，如：台積電、2330")
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._add_selected_stock)

        completer = QCompleter(list(TAIWAN_STOCKS.keys()) + [v.replace(".TW", "") for v in TAIWAN_STOCKS.values()])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.search_input.setCompleter(completer)

        self.fetch_btn = QPushButton("📊 下載資料 & 分析")
        self.fetch_btn.clicked.connect(self.fetch_data)
        self.fetch_btn.setEnabled(False)

        self.clear_btn = QPushButton("🗑 清除全部")
        self.clear_btn.setStyleSheet(self.clear_btn.styleSheet().replace("#7c3aed", "#27272a"))
        self.clear_btn.clicked.connect(self._clear_all)

        row1.addWidget(self.search_input, stretch=3)
        row1.addWidget(self.clear_btn)
        row1.addWidget(self.fetch_btn)
        search_layout.addLayout(row1)

        # ── Suggest + chips ──
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        hint = QLabel("熱門：")
        hint.setStyleSheet("color: #71717a; font-size: 11px; border: none; background: transparent;")
        row2.addWidget(hint)

        self.suggest_layout = QHBoxLayout()
        self.suggest_layout.setSpacing(6)
        for name, code in list(TAIWAN_STOCKS.items())[:6]:
            btn = QPushButton(f"{name}")
            btn.setStyleSheet("""
                QPushButton { background-color: #27272a; color: #a1a1aa; border-radius: 12px;
                              padding: 3px 10px; font-size: 11px; font-weight: 500; }
                QPushButton:hover { background-color: #3f3f46; color: #e4e4e7; }
            """)
            btn.clicked.connect(lambda checked, n=name, c=code: self._add_stock(n, c))
            self.suggest_layout.addWidget(btn)
        row2.addLayout(self.suggest_layout)
        row2.addStretch()
        search_layout.addLayout(row2)

        # ── Chips area ──
        self.chips_widget = QWidget()
        self.chips_layout = QHBoxLayout(self.chips_widget)
        self.chips_layout.setContentsMargins(0, 4, 0, 0)
        self.chips_layout.setSpacing(8)
        self.chips_layout.setAlignment(Qt.AlignLeft)
        self.chips_placeholder = QLabel("尚未選擇任何股票，請從上方搜尋或點選熱門標的")
        self.chips_placeholder.setStyleSheet("color: #52525b; font-size: 12px; border: none; background: transparent;")
        self.chips_layout.addWidget(self.chips_placeholder)
        search_layout.addWidget(self.chips_widget)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #71717a; font-size: 11px; border: none; background: transparent;")
        search_layout.addWidget(self.status_label)

        main_layout.addWidget(search_frame)

        # ── Content area ──
        content = QHBoxLayout()
        content.setSpacing(14)

        # left: price table
        price_frame = QFrame()
        price_frame.setObjectName("infoCard")
        price_layout = QVBoxLayout(price_frame)
        price_layout.setContentsMargins(0, 0, 0, 0)
        price_layout.setSpacing(4)
        price_title = QLabel("📈 收盤價走勢（近 30 筆）")
        price_title.setStyleSheet("color: #a1a1aa; font-size: 12px; font-weight: 600; "
                                  "padding: 10px 14px 4px 14px; border: none; background: transparent;")
        price_layout.addWidget(price_title)
        self.price_table = QTableWidget()
        self.price_table.verticalHeader().setDefaultSectionSize(26)
        price_layout.addWidget(self.price_table)
        content.addWidget(price_frame, stretch=2)

        # right: heatmap
        heat_frame = QFrame()
        heat_frame.setObjectName("infoCard")
        heat_layout = QVBoxLayout(heat_frame)
        heat_layout.setContentsMargins(0, 0, 0, 0)
        heat_layout.setSpacing(4)
        heat_title = QLabel("🔥 相關係數熱力圖")
        heat_title.setStyleSheet("color: #a1a1aa; font-size: 12px; font-weight: 600; "
                                 "padding: 10px 14px 4px 14px; border: none; background: transparent;")
        heat_layout.addWidget(heat_title)
        self.heatmap = HeatmapWidget()
        heat_layout.addWidget(self.heatmap)
        content.addWidget(heat_frame, stretch=3)

        main_layout.addLayout(content, stretch=1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就緒 — 請選擇股票")

    def _on_search_text_changed(self, text):
        pass

    def _add_stock(self, name, code):
        if len(self.selected_stocks) >= MAX_STOCKS:
            self.status_label.setText(f"⚠ 最多只能選擇 {MAX_STOCKS} 檔股票")
            return
        if code in self.selected_stocks:
            self.status_label.setText(f"⚠ {name} 已經選過了")
            return

        self.selected_stocks[code] = name
        self._update_chips()
        self.search_input.clear()
        self.search_input.setFocus()
        self.status_label.setText(f"✅ 已加入 {name}（{len(self.selected_stocks)}/{MAX_STOCKS}）")
        self.fetch_btn.setEnabled(len(self.selected_stocks) >= 2)

    def _remove_stock(self, code):
        name = self.selected_stocks.pop(code, "")
        self._update_chips()
        self.status_label.setText(f"已移除 {name}")
        self.fetch_btn.setEnabled(len(self.selected_stocks) >= 2)

    def _clear_all(self):
        self.selected_stocks.clear()
        self._update_chips()
        self.status_label.setText("已清除所有選擇")
        self.fetch_btn.setEnabled(False)
        self.price_table.setRowCount(0)
        self.price_table.setColumnCount(0)
        self.heatmap.set_data(None, [])
        self.close_data = None
        self.corr_data = None

    def _update_chips(self):
        for i in reversed(range(self.chips_layout.count())):
            w = self.chips_layout.itemAt(i).widget()
            if w and w != self.chips_placeholder:
                w.deleteLater()
        self.chips_placeholder.setVisible(len(self.selected_stocks) == 0)

        for code, name in self.selected_stocks.items():
            chip = StockChip(name, code)
            chip.removed.connect(self._remove_stock)
            self.chips_layout.addWidget(chip)

    def _add_selected_stock(self):
        text = self.search_input.text().strip()
        if not text:
            return
        if text in TAIWAN_STOCKS:
            self._add_stock(text, TAIWAN_STOCKS[text])
            return
        code = text if text.endswith(".TW") else f"{text}.TW"
        for name, c in TAIWAN_STOCKS.items():
            if c == code:
                self._add_stock(name, code)
                return
        self._add_stock(text, code)

    def fetch_data(self):
        if len(self.selected_stocks) < 2:
            self.status_label.setText("⚠ 請至少選擇 2 檔股票")
            return
        self.fetch_btn.setEnabled(False)
        self.status_bar.showMessage("正在下載資料...")
        self.status_label.setText("⏳ 下載中，請稍候...")
        start = "2026-01-01"
        self.worker = FetchWorker(self.selected_stocks, start)
        self.worker.finished.connect(self._on_data_loaded)
        self.worker.error.connect(self._on_error)
        self.worker.progress.connect(lambda m: self.status_bar.showMessage(m))
        self.worker.start()

    def _on_data_loaded(self, close, returns, corr):
        self.close_data = close
        self.returns_data = returns
        self.corr_data = corr
        self._update_price_table()
        self._update_heatmap()
        self.fetch_btn.setEnabled(True)
        period = f"{close.index[0].date()} ~ {close.index[-1].date()}"
        self.status_bar.showMessage(
            f"✅ 資料更新完成 — {len(close)} 筆交易日 | {period}"
        )
        self.status_label.setText(
            f"✅ 分析完成！共 {len(close)} 筆交易日的日報酬率相關係數"
        )

    def _on_error(self, msg):
        self.fetch_btn.setEnabled(len(self.selected_stocks) >= 2)
        self.status_bar.showMessage(f"❌ {msg}")
        self.status_label.setText(f"❌ {msg}")

    def _update_price_table(self):
        df = self.close_data.tail(30)
        ticker_map = {v: k for k, v in self.selected_stocks.items()}
        cols = []
        for c in df.columns:
            clean = c.replace(".TW", "").strip()
            cols.append(f"{ticker_map.get(c, clean)}\n({clean})")
        self.price_table.setColumnCount(len(cols) + 1)
        self.price_table.setHorizontalHeaderLabels(["日期"] + cols)
        self.price_table.setRowCount(len(df))
        self.price_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.price_table.verticalHeader().setVisible(False)

        for r in range(len(df)):
            date_item = QTableWidgetItem(str(df.index[r].date()))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.price_table.setItem(r, 0, date_item)
            for c in range(len(cols)):
                val = float(df.iloc[r, c]) if hasattr(df.iloc[r, c], 'iloc') else float(df.iloc[r, c])
                item = QTableWidgetItem(f"{val:.2f}")
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if r > 0:
                    prev = float(df.iloc[r-1, c])
                    change = val - prev
                    if change > 0:
                        item.setForeground(QColor("#34d399"))
                    elif change < 0:
                        item.setForeground(QColor("#f87171"))
                    else:
                        item.setForeground(QColor("#e4e4e7"))
                self.price_table.setItem(r, c + 1, item)

    def _update_heatmap(self):
        if self.corr_data is None:
            return
        ticker_map = {v: k for k, v in self.selected_stocks.items()}
        labels = [ticker_map.get(c, c.replace(".TW", "")) for c in self.corr_data.columns]
        self.heatmap.set_data(self.corr_data, labels)


def main():
    app = QApplication(sys.argv)
    font = QFont("Microsoft JhengHei", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    window = StockCorrelationApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
