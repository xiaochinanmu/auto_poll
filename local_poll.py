import tkinter as tk
from lxml import etree
from selenium import webdriver
import time
# 从输入框的字符串获取设备号列表
def get_device_tab(device_num):
    number_tab = []
    substrings = device_num.split(',')
    for substring in substrings:
        number = int(substring)
        number_tab.append(number)
    return number_tab

def show_webpage_content():
    global stop_flag
    stop_flag = False
    # 获取设备号字符串
    device_string = entry.get()
    # 获取设备号列表
    num = get_device_tab(device_string)

    # 获取li标签对应设备号
    option = webdriver.ChromeOptions()
    # 是为了禁用 Chrome 的自动化标志，以避免被网站检测到使用了自动化工具。
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    # 是为了指定 Chrome 使用的用户数据目录和配置文件目录。这样可以使用存储在目录中的个人偏好设置和登录信息。
    # option.add_argument(r'--user-data-dir=C:\Users\TU\AppData\Local\googleuser\User Data')
    # option.add_argument("--profile-directory=Default")
    # 如果需要在无界面模式下执行操作
    # option.add_argument('--headless')
    tu = webdriver.Chrome(options=option)
    tu.get("file:///D:/Desktop/gongsi/test1.html")
    # tu.get("http://lab.hulisoft.cn:8081/#/device/status")
    # time.sleep(4)  # /html/body/div[2]/div[1]/div[1]/ul/li[8]/span
    # tu.find_element(by=By.XPATH,value='/html/body/div[1]/section/section/main/div/div/form/div[1]/div[2]/div/div/div/input').click()
    page_source = tu.page_source
    tree = etree.HTML(page_source)
    device_li_dict = {}
    # 获取网页设备号对应的li标签号，有382个li标签对应
    for i in range(1, 382):
        device_num = tree.xpath(f"/html/body/div[2]/div[1]/div[1]/ul/li[{i}]/span/text()")
        device_li_dict[f'{device_num}'] = i
    print(device_li_dict)
    # tu.quit()
    # return in_device_li_dict

    in_device_li_dict={}
    for i in num:
        for key, value in device_li_dict.items():
            if str(i) in key:
                # li_num = value
                in_device_li_dict[f'{str(i)}'] = value
    print(device_li_dict)
    print(in_device_li_dict)

    count=0
    while True:
        text.delete("1.0", tk.END)
        text.insert(tk.END, "设备号" + "          " + "时间" + "                      " + "gps" + "      " + "相机" + "     " + "gravit")
        for key, value in in_device_li_dict.items():
            time.sleep(2)
            print(key, value)

            # 获取设备号数据
            # tu.find_element(by=By.XPATH,value=f'/html/body/div[2]/div[1]/div[1]/ul/li[{value}]/span').click()  # 50006-49386=170
            # time.sleep(4)
            # tu.find_element(by=By.XPATH,value='/html/body/div[1]/section/section/main/div/div/form/div[1]/div[3]/div/button[1]').click()
            # time.sleep(4)

            page_source = tu.page_source

            tree = etree.HTML(page_source)
            seri_num = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div/span/text()')
            time1 = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/span/text()')
            time2 = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[3]/div/span/text()')
            gps = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[4]/div/div/span/text()')
            xiangji = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div/div/span/text()')
            gravity = tree.xpath('//*[@id="app"]/section/section/main/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[6]/div/div/span/text()')

            # tu.quit()
            print(seri_num[0])
            print(time1[0])
            print(time2[0])
            print(gps[0])
            print(xiangji[0])
            print(gravity[0])
            # print()

            if (gps == ['status:2'] and xiangji == ['status:1'] and gravity == ['status:1']) or (gps == ['status:1'] and xiangji == ['status:1'] and gravity == ['status:1']):
                print("111")
                text.insert(tk.END,
                            "\n" + str(key) + "  " + time2[0] + "  " + gps[0] + "  " + xiangji[0] + "  " + gravity[0]+"   ")
                text.tag_configure("red_circle", foreground="green")
                text.insert(tk.END, "\u25CF ", "red_circle")  # 插入一个红色圆圈
            else:
                print("222")
                text.insert(tk.END,
                            "\n" + str(key) + "  " + time2[0] + "  " + gps[0] + "  " + xiangji[0] + "  " + gravity[0]+"   ")
                text.tag_configure("red_circle", foreground="red")
                text.insert(tk.END, "\u25CF ", "red_circle")  # 插入一个红色圆圈
            text.update()
        if stop_flag == True:
            print(stop_flag)
            break
        count += 1
        print(count)
        time.sleep(2)




def stop_webpage_content():
    global stop_flag
    stop_flag = True

window = tk.Tk()
window.title("自动查询")
stop_flag = False
label = tk.Label(window, text="               请输入要查询的设备号用','隔开")
label.pack(anchor="w")  # 使用 anchor="w" 将标签靠左对齐

# 创建一个框架，用于容纳按钮
button_frame = tk.Frame(window)
button_frame.pack()

entry = tk.Entry(button_frame, width=50)
entry.pack(side="left")

button = tk.Button(button_frame, text="查询", command=show_webpage_content)
button.pack(side="left", padx=10)

stop_button = tk.Button(button_frame, text="停止",command=stop_webpage_content)
stop_button.pack(side="left")

text = tk.Text(window)
text.pack()

window.mainloop()
