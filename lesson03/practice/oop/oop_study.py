# ===== Khởi tạo object =====
from lesson03.practice.oop.bank_account import BankAccount
from student import Student

# s1 = Student("An", 20, 8.5)
# print(s1.name) # An
# print(s1.age) # 20
# print(s1.score) # 8.5
#
# s2 = Student("Binh", 21, 7.8)


# ===== Method =====
# s3 = Student("An", 20, 7.5)
#
# s3.introduce() # Hi, mình là An, 20 tuổi
# print(s3.is_passed()) # True


# ===== list[Student] =====
# student_list = [
#     Student("An", 20, 8.5),
#     Student("Binh", 21, 6.0),
#     Student("Chi", 19, 4.5),
# ]

# In danh sách sinh viên
# for s in students:
#     s.introduce()

# Tính điểm trung bình của lớp
# def calc_avg_score(students: list[Student]) -> float:
#     if not students:
#         return 0
#     total = 0
#     for s in students:
#         total += s.score
#     return total / len(students)
#
# avg = calc_avg_score(student_list)
# print("Điểm trung bình lớp:", avg)

# Tìm sinh viên điểm cao nhất
# def find_top_student(students: list[Student]) -> Student | None:
#     if not students:
#         return None
#     top = students[0]
#     for s in students[1:]:
#         if s.score > top.score:
#             top = s
#     return top
#
# empty_list = []
# best = find_top_student(student_list)
#
# if not best:
#     print("Ko có data")
# else:
#     print("Top student:", best.name, best.score)


# ===== Encapsulation =====
acc = BankAccount("An", 1000)
acc.deposit(500)
acc.withdraw(300)
print(acc.get_balance()) # 1200