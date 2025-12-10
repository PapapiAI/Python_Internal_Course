# Python Core – Buổi 3: File I/O, Exception, Module, DateTime/Time & OOP thiết yếu

# 1) Module & Tổ Chức Code trong Python

## 1.1 Khái niệm Module

> **Module = 1 file `.py` chứa code** (hàm, biến, class…) và có thể được import vào file khác

Ví dụ:

```
math.py => module chuẩn của Python
utils.py => module do chúng ta tự tạo
main.py => file chính chạy chương trình
```

**Lợi ích của module:**

* Tách code thành nhiều phần nhỏ => dễ quản lý
* Tái sử dụng code giữa nhiều file
* Giảm trùng lặp
* Dễ bảo trì, mở rộng dự án

---

## 1.2 Import module

### Cú pháp 1: `import module_name`

```python
import math

print(math.sqrt(16))
```

### Cú pháp 2: `from module_name import function`

```python
from math import sqrt
print(sqrt(16))
```

### Cú pháp 3: `import module_name as alias`

```python
import math as m
print(m.pi)
```

### Cú pháp 4: Import nhiều hàm

```python
from math import sqrt, sin, cos
```

> **Lưu ý:** chỉ import những gì cần dùng để code rõ ràng hơn

---

## 1.3 Tự tạo module

* Chúng ta có thể tạo file **utils.py** như sau:

```python
def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0
```

Trong **main.py**:

```python
import utils

print(utils.add(3, 4))
print(utils.is_even(10))
```

Hoặc:

```python
from utils import add, is_even
print(add(5, 7))
```

> **Quy tắc:** mỗi module chỉ nên giải quyết một nhóm chức năng nhất định

---

## 1.4 Tổ chức code theo thư mục (package)

**Package = thư mục chứa nhiều module** + file `__init__.py`

* Ví dụ cấu trúc dự án:

```
project/
│
├── main.py
├── utils/
│   ├── __init__.py
│   ├── math_utils.py
│   └── string_utils.py
```

* Trong `math_utils.py`:

```python
def add(a, b):
    return a + b
```

Dùng trong `main.py`:

```python
from utils.math_utils import add
print(add(3, 5))
```

> `__init__.py` giúp Python hiểu thư mục là 1 package có thể import

---

## 1.5 Biến `__name__ == '__main__'` để chạy trực tiếp

Trong `main.py`:

```python
def run():
    print("Chương trình chính đang chạy...")

if __name__ == '__main__':
    run()
```

Mục đích:

* Code **không chạy** khi file được import ở nơi khác
* Chỉ chạy khi file được chạy trực tiếp bằng command:

```
python main.py
```

---

## 1.6 Tổ chức code tốt khi dự án lớn dần

Ví dụ cấu trúc **tốt** hơn cho dự án nhỏ:

```
project/
│── main.py
│── services/
│     ├── __init__.py
│     ├── student_service.py
│     └── file_service.py
│── utils/
      ├── __init__.py
      └── helpers.py
```

**Nguyên tắc quan trọng:**

* Mỗi module chỉ làm 1 nhiệm vụ => *Single Responsibility*
* Tránh file quá dài (lên đến cả ngàn dòng)
* Đặt tên module rõ ràng: `student_service`, `file_service`, `helpers`, ...

---

## 1.7 Lỗi thường gặp khi import

### 1) ImportError: module không tồn tại

```
ImportError: No module named 'utils'
```

**Nguyên nhân:** sai tên file hoặc sai đường dẫn.

### 2) Circular import (import vòng tròn)

```
A import B, B import A => lỗi
```

Cách tránh:

* Đưa hàm chung vào file riêng
* Chỉ import những gì cần

---

# 2) File I/O – Đọc & Ghi File trong Python

## 2.1 Khái niệm File I/O

**File I/O (Input/Output)** là cách Python làm việc với file:

* Đọc dữ liệu từ file => Input
* Ghi dữ liệu vào file => Output

> Đây là kỹ năng cốt lõi giúp chương trình lưu trữ dữ liệu thay vì chỉ chạy trong RAM

Python cung cấp hàm `open()` để làm việc với file

Cú pháp: `open(path, mode, encoding)`

---

## 2.2 Các chế độ mở file (mode)

| Mode   | Ý nghĩa                           | Ghi chú                    |
|--------|-----------------------------------|----------------------------|
| `"r"`  | Đọc file                          | Lỗi nếu file không tồn tại |
| `"w"`  | Ghi mới (xóa toàn bộ nội dung cũ) | Tạo file mới nếu chưa có   |
| `"a"`  | Ghi nối thêm vào cuối file        | Không xóa nội dung cũ      |
| `"r+"` | Đọc + Ghi                         | File phải tồn tại          |
| `"b"`  | Binary mode                       | Dùng cho ảnh, pdf, mp3     |


```python
f = open("data.txt", "r", encoding="utf-8")
```

Hàm `open(...)` trả về `TextIOWrapper`, là lớp đại diện cho file text trong Python, cung cấp các hàm:
* `read()` / `readline()` / `readlines()`
* `write()` / `writelines()` ...

---

## 2.3 Đọc file

### 2.3.1 `read()`: đọc toàn bộ file, trả về một chuỗi

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
```

### 2.3.2 `readline()`: đọc từng dòng một

```python
with open("data.txt", "r", encoding="utf-8") as f:
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline().strip()
    line4 = f.readline().strip()

print(line1)
print(line2)
print(line3)
print(line4)
```

> `strip()` giúp loại bỏ ký tự xuống dòng

### 2.3.3 `readlines()`: đọc tất cả dòng, trả về list

```python
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    print(line.strip())
```

Kết quả:
* lines là một list, mỗi phần tử là 1 dòng (bao gồm ký tự xuống dòng `\n`)

```
[
    "Line 1\n",
    "Line 2\n",
    "Line 3\n"
]
```

---

## 2.4 Ghi file

### 2.4.1 Ghi file bằng `write()`

* Chế độ `"w"` => ghi mới hoàn toàn:

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Xin chào Python!\n")
    f.write("Dòng thứ hai\n")
```

* Chế độ `"a"` => ghi nối thêm:

```python
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Dòng mới được thêm vào\n")
```

### 2.4.2 Ghi list vào file

* `write` với vòng lặp

```python
lines = ["Hello", "Python", "File I/O"]
with open("list.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
```

* `writelines`

```python
with open("list.txt", "w", encoding="utf-8") as f:
    lines = ["Xin chào Python!\n", "Dòng thứ hai\n"]
    f.writelines(lines)
```

---

## 2.5 Vì sao nên dùng `with open(...) as f:`

**With Statement Context Manager** giúp:

* Tự đóng file, kể cả khi có lỗi xảy ra
* An toàn hơn `open()` + `close()`

Ví dụ không an toàn:

```python
f = open("data.txt", "r")
data = f.read()
f.close()
```

Ví dụ chuẩn cho file I/O:

```python
with open("data.txt", "r") as f:
    data = f.read()
```

> Quy tắc: **luôn dùng `with open()` khi thao tác file** trong Python

---

## 2.6 Xử lý ngoại lệ khi thao tác file

### File không tồn tại => ném `FileNotFoundError`

```python
try:
    with open("abc.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("Không tìm thấy file!")
```

### Báo lỗi cho người dùng

```python
filename = "data.txt"
try:
    with open(filename, "r", encoding="utf-8") as f:
        print(f.read())
except Exception as e:
    print("Có lỗi xảy ra khi đọc file:", e)
```

---

## 2.7 Làm việc với file nhị phân (binary file)

Dùng mode `"rb"` và `"wb"`:

```python
with open("photo.jpg", "rb") as f:
    data = f.read()

with open("copy.jpg", "wb") as f:
    f.write(data)
```

> Dùng cho ảnh, pdf, video

---

# 3) Exception Handling – Xử lý ngoại lệ trong Python

## 3.1 Khái niệm

**Exception = lỗi xảy ra trong lúc chương trình đang chạy (runtime error)** khiến chương trình dừng lại, trừ khi chúng ta xử lý nó

Ví dụ các lỗi thường gặp:

* `ValueError`: sai kiểu dữ liệu đầu vào
* `ZeroDivisionError`: chia cho 0
* `FileNotFoundError`: file không tồn tại
* `TypeError`: truyền sai kiểu tham số
* `IndexError`: truy cập index không tồn tại

Ví dụ:

```python
x = int("abc") # ValueError: invalid literal for int()
```

> Mục tiêu của Exception Handling: **giúp chương trình không bị crash** và **xử lý lỗi một cách an toàn và thân thiện**

---

## 3.2 Cú pháp try / except

```python
try:
    # đoạn code có nguy cơ lỗi
    x = 10 / 0
except ZeroDivisionError:
    print("Không thể chia cho 0!")
```

* Nhiều loại lỗi:

```python
try:
    raw = input("Nhập một số nguyên: ")
    x = int(raw)
    y = 10 / x
    print(f"Kết quả 10 / {x} =", y)
except ValueError:
    print("Lỗi: Bạn phải nhập một số nguyên hợp lệ!")
except ZeroDivisionError:
    print("Lỗi: Không thể chia cho 0!")
except Exception as e:
    print("Lỗi không xác định:", e)
```

> Một `try` có thể có nhiều khối `except` để xử lý từng loại lỗi

---

## 3.3 Bắt nhiều lỗi trong cùng một except

* Gom nhiều loại lỗi vào 1 khối `except` để xử lý chung  

```python
try:
    x = int("abc")
except (ValueError, TypeError):
    print("Lỗi nhập liệu!")
```

---

## 3.4 Bắt mọi lỗi

```python
def risky_code(a):
    print(1/a)

try:
    risky_code(0)
except Exception as e:
    print("Có lỗi xảy ra:", e)
```

> Hữu ích để debug hoặc log lỗi, nhưng không nên lạm dụng vì che giấu lỗi thật => khó debug lỗi

---

## 3.5 Khối else trong try/except

Chạy **khi không có lỗi**:

```python
try:
    x = int(input("Nhập số: "))
except ValueError:
    print("Bạn nhập sai!")
else:
    print("Bạn nhập:", x)
```

Trong thực tế ít dùng khối `else` trong `try/except`

---

## 3.6 Khối finally

* **Luôn chạy** dù có lỗi hay không
* Thường dùng để đóng tài nguyên (file, kết nối DB, ...)

Ví dụ:

```python
# Đóng kết nối DB
try:
    conn = connect_to_db() # mở kết nối DB
    result = conn.query("SELECT * FROM users")
    print(result)
except Exception as e:
    print("Lỗi khi truy vấn:", e)
finally:
    print("Đóng kết nối DB…")
    conn.close()

# Reset trạng thái hệ thống
state = "busy"

try:
    print("Đang chạy tác vụ quan trọng…")
    # risky_task()
except Exception:
    print("Tác vụ lỗi!")
finally:
    state = "idle"
    print("Trạng thái đã reset về:", state)
```

---

## 3.7 Tự tạo exception bằng `raise`

Khi muốn báo lỗi chủ động:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("b không được = 0")
    return a / b

try:
    divide(5, 0)
except ValueError as e:
    print("Lỗi:", e)
```

> Dùng `raise` để kiểm soát logic chương trình rõ ràng hơn

---

## 3.8 Áp dụng Exception vào File I/O

```python
filename = input("Nhập tên file: ")

try:
    with open(filename, "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("File không tồn tại!")
except PermissionError:
    print("Bạn không có quyền đọc file này!")
except Exception as e:
    print("Lỗi khác:", e)
```

---

## 3.9 Tư duy xử lý lỗi đúng cách

* Khi viết code, hãy tự hỏi:
  * Đoạn nào có nguy cơ lỗi? => cần bọc `try/except`
  * Người dùng cần biết gì? => cần trả thông báo dễ hiểu
  * Có cần đóng file, giải phóng tài nguyên?
  * Có nên dừng chương trình hay tiếp tục?

* Sai lầm thường gặp:
  * Bắt lỗi chung chung (bắt Exception) mà không xử lý gì
  * Che dấu lỗi khiến debug khó hơn
  * Bỏ qua `finally` khiến file hoặc tài nguyên không được đóng

---

## 3.10 Thực hành Exception Handling

### BTTH1 – Bắt lỗi nhập số

Viết chương trình:

* Nhập một số nguyên dương từ người dùng
* Nếu nhập sai => báo lỗi và yêu cầu nhập lại

Ví dụ:

```
Nhập số: abc
Nhập sai, vui lòng nhập lại
Nhập số: 123
Bạn đã nhập: 123
```

### BTTH2 – Tạo menu và xử lý lỗi lựa chọn

Menu:

```
1. Xin chào
2. Tính chỉ số BMI
3. Thoát
```

Yêu cầu:

* Nếu người dùng nhập ký tự không phải số => báo lỗi
* Nếu nhập số ngoài 1–3 => báo lỗi
* Nếu đúng => thực thi chức năng

### BTTH3 – Đọc file an toàn

  Viết chương trình với menu:

Chọn chức năng:

1. Đọc toàn bộ file (read)
2. Đọc từng dòng (readline)
3. Ghi đè file (write)
4. Ghi thêm vào file (append)
5. Thoát

---

# 4) DateTime & Đo thời gian thực thi trong Python

## 4.1 DateTime trong Python

Python cung cấp module `datetime` để làm việc với thời gian và ngày tháng:

* Lấy thời gian hiện tại
* Tạo đối tượng ngày giờ cụ thể
* Cộng/trừ ngày giờ
* Format ngày giờ theo ý muốn
* Parse (chuyển từ chuỗi => datetime)

Import:

```python
from datetime import datetime, timedelta
```

---

## 4.2 Lấy thời gian hiện tại

```python
from datetime import datetime

now = datetime.now()
print(now) 
```

### Các thuộc tính thường dùng:

```python
print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)
```

---

## 4.3 Tạo đối tượng DateTime cụ thể

```python
specific = datetime(2025, 1, 1, 8, 30, 0)
print(specific)
```

> Thứ tự tham số: `year, month, day, hour, minute, second`

---

## 4.4 Định dạng ngày giờ: `strftime`

Dùng để **chuyển** datetime => chuỗi

```python
now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted) 
```

### Các ký hiệu format phổ biến

| Ký hiệu | Ý nghĩa                       |
|---------|-------------------------------|
| `%Y`    | Năm (4 chữ số)                |
| `%m`    | Tháng (01–12)                 |
| `%d`    | Ngày                          |
| `%H`    | Giờ (00–23)                   |
| `%M`    | Phút                          |
| `%S`    | Giây                          |
| `%A`    | Tên thứ (Monday, Tuesday ...) |

```python
print(now.strftime("Hôm nay là %A, ngày %d/%m/%Y"))
```

---

## 4.5 Chuyển chuỗi thành datetime: `strptime`

Dùng khi **đọc** dữ liệu dạng text từ file hoặc API

```python
s = "2025-02-14 20:30:00"
dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
print(dt)
```

---

## 4.6 Cộng / trừ ngày: `timedelta`

`timedelta` cho phép cộng/trừ số ngày, giờ, phút

```python
from datetime import timedelta

now = datetime.now()
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)

print(tomorrow)
print(yesterday)

in_three_hours = now + timedelta(hours=3)
two_weeks_ago = now - timedelta(weeks=2)

print(in_three_hours)
print(two_weeks_ago)
```

---

## 4.7 So sánh thời gian

`Datetime` hỗ trợ các phép so sánh trực tiếp:

```python
x = datetime(2025, 1, 1)
y = datetime(2024, 1, 1)

print(x > y) # True
print(x == y) # False
```

---

## 4.8 Đo thời gian thực thi đoạn code

Có nhiều cách đo thời gian chạy, nhưng cách phổ biến nhất là dùng module `time`

```python
import time

start = time.time()

# --- đoạn code cần đo thời gian ---
result = 0
for i in range(1_000_000):
    result += i
# ----------------------------------

end = time.time()
elapsed = end - start
print("Thời gian thực thi:", elapsed, "giây")
```

### Dùng `perf_counter()` (chính xác hơn)

```python
from time import perf_counter

start = perf_counter()
for i in range(1_000_000):
    pass
end = perf_counter()

print("Elapsed:", end - start)
```

> `perf_counter()` phù hợp để đo các đoạn code nhỏ, độ chính xác cao

---

## 4.9 Ứng dụng DateTime trong dự án thực tế

* Log thời gian thực thi (performance logging)
* Gắn timestamp khi tạo/sửa bản ghi trong database
* Tạo file backup theo ngày (`backup_2050_01_01.txt`)
* Tính toán hạn sử dụng, ngày hết hạn
* Phân tích log server theo mốc thời gian

---

## 4.10 Thực hành DateTime

### BTTH4: In ngày giờ hiện tại theo nhiều định dạng

In ra:

```
Năm-Tháng-Ngày: DD-MM-YYYY
Giờ:Phút:Giây: HH:MM:SS
Hôm nay là thứ mấy?
```

### BTTH5: Tính tuổi từ ngày sinh

Nhập vào ngày sinh dạng `dd/mm/yyyy`, tính số tuổi hiện tại

Gợi ý:

```python
dob = datetime.strptime(input_str, "%d/%m/%Y")
age = (datetime.now() - dob).days // 365
```

### BTTH6: Đo thời gian thực thi thuật toán

So sánh thời gian chạy giữa:

1. Vòng lặp tính tổng từ 1 đến 1 triệu (dùng `time.time()`)
2. Dùng công thức toán học: `n*(n+1)/2` (dùng `perf_counter()`)

---

# 5) OOP thiết yếu

## 5.1 Vì sao cần OOP?

Trước giờ, chúng ta viết code **theo kiểu thủ tục (procedural)**:

* Dữ liệu: list, dict, ...
* Hàm: nhận dữ liệu => xử lý => trả kết quả

Khi chương trình lớn lên:

* Nhiều biến rời rạc: `student_name`, `student_age`, `student_score`, ...
* Nhiều hàm nhận rất nhiều tham số
* Khó nhóm logic theo từng "thực thể" (học sinh, khóa học, đơn hàng, sản phẩm, ...)

**OOP giúp**:

* Gắn **dữ liệu (attributes)** và **hành vi (methods)** vào chung 1 đối tượng
* Dễ mô hình hóa "thực thể thật" ngoài đời: Student, Course, Invoice, Product
* Code rõ hơn, dễ bảo trì, dễ mở rộng

Ví dụ: thay vì

```python
student_name = "An"
student_age = 20
student_score = 8.5
```

Chúng ta muốn có:

```python
student = Student(name="An", age=20, score=8.5)
```

---

## 5.2 Khái niệm Class & Object

* **Class**: "bản thiết kế" cho đối tượng
  * Ví dụ: class `Student` mô tả *một kiểu* sinh viên (có name, age, score ...)
  
* **Object (instance)**: "đối tượng cụ thể" được tạo từ class
  * Ví dụ: `student1`, `student2` là 2 sinh viên cụ thể

Hãy hình dung:

* Class `Student` giống như bản thiết kế một chiếc ghế
* Mỗi "chiếc ghế" thực tế là một object

---

## 5.3 Định nghĩa class cơ bản, `__init__` và `self`

### 5.3.1 Thêm hàm khởi tạo `__init__`

```python
class Student:
    def __init__(self, name, age, score):
        self.name = name # thuộc tính (attribute) của object
        self.age = age
        self.score = score
```

Giải thích:

* `__init__` là **hàm khởi tạo** (constructor): tự động chạy khi tạo object
* Tham số đầu tiên **luôn là `self`**:
  * Đại diện cho **chính object đang được tạo/truy cập**
  * `self.name` là thuộc tính name của đối tượng hiện tại

Khởi tạo object:

```python
from student import Student

s1 = Student("An", 20, 8.5)
print(s1.name) # An
print(s1.age) # 20
print(s1.score) # 8.5

s2 = Student("Binh", 21, 7.8)
```

> **`self` ~ "this object"** (tương tự `this` trong nhiều ngôn ngữ khác)

---

## 5.4 Thuộc tính & Phương thức (Attributes & Methods)

### 5.4.1 Thuộc tính (Attribute)

Là "biến" gắn với từng object

```python
class Student:
    def __init__(self, name: str, age: int, score: float):
        self.name = name
        self.age = age
        self.score = score
```

Đây là **instance attributes**, mỗi object có giá trị riêng

### 5.4.2 Phương thức (Method)

Là **hàm được định nghĩa bên trong class**, luôn có `self`:

```python
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def is_passed(self):
        return self.score >= 5.0

    def introduce(self):
        print(f"Xin chào, mình là {self.name}, {self.age} tuổi.")
```

Dùng:

```python
s = Student("An", 20, 8.5)

s.introduce() # Xin chào, mình là An, 20 tuổi.
print(s.is_passed()) # True
```

> `self.score` truy cập vào điểm của **chính sinh viên đó**.

---

## 5.5 Danh sách đối tượng: `list[Student]`

Khi đã có class `Student`, có thể tạo **danh sách sinh viên**:

```python
students = [
    Student("An", 20, 8.5),
    Student("Binh", 21, 6.0),
    Student("Chi", 19, 4.5),
]
```

* In danh sách sinh viên:

```python
for s in students:
    s.introduce()
```

* Tính điểm trung bình của lớp

```python
def calc_avg_score(students):
    if not students:
        return 0
    total = 0
    for s in students:
        total += s.score
    return total / len(students)

avg = calc_avg_score(students)
print("Điểm trung bình lớp:", avg)
```

* Tìm sinh viên điểm cao nhất

```python
def find_top_student(students: list[Student]) -> Student | None:
    if not students:
        return None
    top = students[0]
    for s in students[1:]:
        if s.score > top.score:
            top = s
    return top

empty_list = []
best = find_top_student(student_list)

if not best:
    print("Ko có data")
else:
    print("Top student:", best.name, best.score)
```

> Đây là pattern rất quan trọng `Collection + Operations on Collection`: **list các object** + **hàm hoặc method xử lý list đó**

---

## 5.6 Tính đóng gói (Encapsulation)

Trong Python, không có "private" thật sự như Java/C#, nhưng có **quy ước**:

* Thuộc tính/hàm bắt đầu bằng `_` => xem như internal (không nên dùng bên ngoài)

Ví dụ:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # "private" theo quy ước

    def deposit(self, amount):
        if amount <= 0:
            print("Số tiền nạp phải > 0")
            return
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            print("Không đủ số dư")
            return
        self._balance -= amount

    def get_balance(self):
        return self._balance
```

Dùng:

```python
acc = BankAccount("An", 1000)
acc.deposit(500)
acc.withdraw(300)
print(acc.get_balance()) # 1200
```

> Mục đích: code bên ngoài **không nên chỉnh sửa _balance trực tiếp**, mà đi qua method `deposit`/`withdraw` để đảm bảo logic an toàn

## 5.7 Sử dụng `@property`

> Trong Python, chúng ta có thể biến method thành thuộc tính nhờ decorator `@property`, điều này giúp:
> * Giấu đi logic `getter`/`setter`
> * Viết code gọn, tự nhiên hơn
> * Dễ thay đổi logic bên trong mà không ảnh hưởng nơi sử dụng
> * Đảm bảo tính đóng gói theo đúng tinh thần OOP

### 5.7.1 Vấn đề nếu không dùng `@property`

Trong OOP, thuộc tính đôi khi cần:
* kiểm tra dữ liệu đầu vào (age phải ≥ 0)
* giới hạn quyền truy cập
* tự động tính toán giá trị

Nếu không dùng property, DEV phải viết `getter`/`setter` theo kiểu truyền thống:

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("Age must be non-negative")
        self._age = value
```

Nơi dùng:

```python
p.set_age(25)
print(p.get_age())
```

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age must be non-negative")
        self._age = value
```

Sử dụng như thuộc tính bình thường:

```python
p = Person("An", 20)
print(p.age)

p.age = 25          # gọi setter
# p.age = -1       # sẽ raise ValueError
```

---

## 5.7 `__str__` và `__repr__` – in object cho đẹp

Mặc định, in object cho kết quả khó đọc:

```python
s = Student("An", 20, 8.5)
print(s)  # <__main__.Student object at 0x00000123>
```

Ta có thể định nghĩa `__str__` để in đẹp hơn:

```python
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __str__(self):
        return f"Student(name={self.name}, age={self.age}, score={self.score})"
```

Giờ in:

```python
s = Student("An", 20, 8.5)
print(s)
# Student(name=An, age=20, score=8.5)
```

> `__str__` rất hữu ích khi debug & log dữ liệu.

---

## 5.8 `*args` và `**kwargs` – linh hoạt tham số (giới thiệu thiết yếu)

Trong OOP, đôi khi ta muốn constructor hoặc method **nhận số lượng tham số linh hoạt**.

* `*args` → nhận **tuple** các tham số không đặt tên
* `**kwargs` → nhận **dict** các tham số có tên

Ví dụ đơn giản:

```python
class Logger:
    def log(self, *args):
        # ghép tất cả args thành một chuỗi
        message = " ".join(str(x) for x in args)
        print("[LOG]", message)

logger = Logger()
logger.log("Xin chao", "Python", 3)
```

Trong `__init__`:

```python
class Config:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 8000)

cfg = Config(host="127.0.0.1", port=9000)
```

> Phần này giúp học viên hiểu dần các constructor/method "linh hoạt" trong code thực tế.

---

## 5.9 Thực hành OOP thiết yếu

### BTTH16 – Class Student cơ bản

Yêu cầu:

1. Tạo class `Student` với các thuộc tính: `name`, `age`, `score`.
2. Thêm method:

   * `is_passed()` → trả về True nếu score ≥ 5
   * `introduce()` → in giới thiệu đơn giản.
3. Tạo 3 object Student và gọi thử các method.

---

### BTTH17 – Danh sách sinh viên & xử lý

Dựa trên class `Student` ở BTTH16:

1. Tạo list `students` chứa 5 sinh viên.
2. Viết hàm:

   * `print_all(students)` → in thông tin tất cả sinh viên
   * `get_avg_score(students)` → trả về điểm trung bình
   * `get_top_student(students)` → trả về sinh viên có score cao nhất
3. Gọi các hàm trên để test.

---

### BTTH18 – Class BankAccount với đóng gói

Thiết kế class `BankAccount`:

* Thuộc tính: `owner`, `_balance` (mặc định = 0)
* Method:

  * `deposit(amount)` → nạp tiền, amount phải > 0
  * `withdraw(amount)` → rút tiền, không cho phép rút quá số dư
  * `get_balance()` → trả về số dư hiện tại

Viết chương trình demo:

* Tạo 1 tài khoản
* Nạp tiền, rút tiền, in số dư sau mỗi lần.

---

### BTTH19 – Dùng `__str__` để debug

Thêm `__str__` cho `Student` hoặc `BankAccount` để khi `print(object)` sẽ in ra thông tin rõ ràng.

Ví dụ mong muốn:

```text
Student(name=An, age=20, score=8.5)
BankAccount(owner=An, balance=1200)
```

---

### BTTH20 – Bài tập mở rộng (tuỳ thời gian)

Thiết kế class `Course`:

* Thuộc tính: `name`, `students` (list[Student])
* Method:

  * `add_student(student)`
  * `get_avg_score()` → điểm trung bình của khoá học
  * `get_top_student()` → sinh viên điểm cao nhất

Viết chương trình demo:

* Tạo vài Student
* Thêm vào Course
* In điểm trung bình và sinh viên có điểm cao nhất.

---

## 5.10 Kết luận phần OOP thiết yếu

Sau phần này, học viên cần:

* Hiểu rõ khái niệm **class** và **object**
* Biết định nghĩa `__init__`, dùng `self`, tạo attributes & methods
* Biết dùng list các object và viết hàm xử lý danh sách đó
* Nắm khái niệm đóng gói cơ bản, hiểu quy ước `_attribute`
* Biết dùng `__str__` để hỗ trợ debug/log
* Bắt đầu làm quen với `*args`, `**kwargs` trong method/constructor

> Đây là nền tảng để sang các buổi sau dùng OOP cho FastAPI (models, schemas, services, …) một cách tự nhiên.
