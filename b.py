import subprocess
import time

# Nhập key và kiểm tra
b = int(input("Nhập Key: "))
if b == 123:
    print('XIN CHÀO ADMIN')
else:
    print('XIN CHÀO KHÁCH HÀNG')

# Nhập số từ 1 đến 13 nếu là admin
if b == 123:
    a = int(input("Nhập một số từ 1 đến 13(SỐ TỪ BẢNG TRỨNG THẦY BO :)) ): "))
    with open('trung.txt', 'w') as file:
        file.write(str(a))
    while True:
        quackquack_process = subprocess.Popen(['python', 'quackquack.py'])
        time.sleep(100)
        quackquack_process.terminate()
else:
    while True:
        quackquack_process = subprocess.Popen(['python', 'quackquackv3.py'])
        time.sleep(100)
        quackquack_process.terminate()
