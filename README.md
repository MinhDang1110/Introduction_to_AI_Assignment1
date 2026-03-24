# 🧠 Introduction to AI - Assignment 1

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📌 Giới thiệu

Đây là bài tập lớn môn **Nhập môn Trí tuệ nhân tạo**, thực hiện so sánh hiệu quả giữa hai phương pháp tìm kiếm:

- **Tìm kiếm mù (Blind Search)** – sử dụng thuật toán **DFS (Depth-First Search)**
- **Tìm kiếm Heuristic (Heuristic Search)** – sử dụng thuật toán **A*** kết hợp các kỹ thuật tối ưu

Hai bài toán được áp dụng:

1. **Sudoku** – giải Sudoku với kỹ thuật **CSP (Constraint Satisfaction Problem)**: MRV, LCV, Forward Checking.
2. **Chess Ranger** – tìm đường ăn quân tối ưu trên bàn cờ vua 8x8.

---

## 🎯 Mục tiêu

- So sánh số node mở rộng, thời gian và bộ nhớ giữa DFS và Heuristic.
- Chứng minh hiệu quả của Heuristic Search trên không gian trạng thái lớn.
- Ứng dụng các kỹ thuật tối ưu trong giải bài toán CSP và tìm kiếm.

---

## 📁 Cấu trúc thư mục

```
Introduction_to_AI_Assignment1/
│
├── Chess_Ranger/
│   ├── main.py                   # Chương trình chính cho Chess Ranger
│   ├── board_generator.py        # Sinh bàn cờ ngẫu nhiên có nước ăn hợp lệ
│   ├── input_parser.py           # Đọc bàn cờ từ file
│   ├── chessRanger_DFS.py        # Giải Chess Ranger bằng DFS
│   ├── chessRanger_Heuristic.py  # Giải Chess Ranger bằng A* + Heuristic
│
├── Sudoku/
│   ├── input.txt                 # File chứa các board Sudoku mẫu
│   ├── Sudoku_main.py            # Chương trình chính cho Sudoku
│   ├── solver_dfs.py             # Giải Sudoku bằng DFS
│   ├── solver_heuristic.py       # Giải Sudoku bằng MRV + LCV + Forward Checking
│
├── Slide.pdf
├── Report.pdf
└── README.md                     # Tài liệu hướng dẫn
```


---

## ⚙️ Cài đặt


1. **Clone repository**

```bash
git clone https://github.com/MinhDang1110/Introduction_to_AI_Assignment1.git
cd Introduction_to_AI_Assignment1
Yêu cầu môi trường

Python 3.8 trở lên

Các thư viện chuẩn: copy, random, heapq, time, tracemalloc, os

Không cần cài đặt thêm thư viện ngoài.
```
---

## 🚀 Hướng dẫn chạy

### 1. Sudoku

Chạy file `main.py`:

```bash
python Sudoku/main.py
```

* **Chọn input:** Tạo Sudoku mới theo độ khó hoặc đọc từ file.
* **Chọn giải thuật:** DFS hoặc Heuristic.
* **In từng bước giải:** Tùy chọn xem quá trình giải chi tiết.

Các board mẫu được lưu trong `input.txt`.

---

### 2. Chess Ranger

Chạy file `main.py`:

```bash
python Chess_Ranger/main.py
```

* **Chọn input:** Nhập tay, đọc từ file, hoặc sinh ngẫu nhiên theo level (4 → 11).
* **Chọn giải thuật:** DFS hoặc A* Heuristic.
* **Chương trình sẽ hiển thị:** Bàn cờ ban đầu, từng bước ăn quân, thời gian, số node mở rộng và bộ nhớ sử dụng.

---

## 📊 Kết quả thực nghiệm

### Sudoku

| Độ khó       | DFS (nodes) | Heuristic (nodes) | DFS (time) | Heuristic (time) |
| ------------ | ----------- | ----------------- | ---------- | ---------------- |
| Easy         | ~5000       | ~100              | 0.12s      | 0.003s           |
| Intermediate | ~12000      | ~200              | 0.28s      | 0.005s           |
| Advanced     | ~25000      | ~400              | 0.65s      | 0.008s           |
| Evil         | ~50000      | ~800              | 1.20s      | 0.015s           |

### Chess Ranger

| Level | DFS (nodes) | A* (nodes) | DFS (time) | A* (time) |
| ----- | ----------- | ---------- | ---------- | --------- |
| 4     | 150         | 45         | 0.02s      | 0.01s     |
| 7     | 1200        | 120        | 0.15s      | 0.05s     |
| 10    | 9500        | 380        | 1.10s      | 0.12s     |

> Heuristic giúp giảm số node mở rộng từ 10 đến 100 lần so với DFS.


## 🧠 Kỹ thuật sử dụng

### Sudoku (Heuristic)

* **MRV (Minimum Remaining Values):** Chọn ô có ít khả năng nhất.
* **LCV (Least Constraining Value):** Sắp xếp giá trị thử sao cho ít ảnh hưởng đến các ô khác.
* **Forward Checking:** Loại bỏ giá trị không hợp lệ khỏi miền của các ô liên quan.

### Chess Ranger (A*)

* **Heuristic =** số thành phần liên thông × 5 + khoảng cách trung bình × 3.
* **Priority queue** để luôn mở rộng trạng thái có f = g + h nhỏ nhất.
* **Cache heuristic** để tránh tính lại.

---

## 🔧 Cải tiến trong tương lai

* Thiết kế heuristic admissible mạnh hơn cho Chess Ranger.
* Áp dụng IDA* để giảm bộ nhớ.
* Thử nghiệm với Beam Search và Learning-based heuristic.


👤 Tác giả
* Đặng Đình Minh Hoàng - 2411068
* Phan Ngọc Xuân Lợi - 2411969
* Phạm Phùng Đăng Khoa - 2433156
* Nguyễn Ngọc Trường Khang - 2411455
