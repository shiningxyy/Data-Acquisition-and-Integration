import requests
from bs4 import BeautifulSoup
import csv
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import matplotlib.pyplot as plt

def getHTMLtext_selenium(url):
    driver = webdriver.Chrome()  # 需要安装 ChromeDriver
    driver.get(url)
    html = driver.page_source  # 获取动态加载后的 HTML
    driver.quit()
    return html

def gethtml_byclick(url):
    driver = webdriver.Chrome()  # 确保已安装ChromeDriver
    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 模拟点击向前翻页，直到显示9月份的数据
    try:
        for _ in range(1):  # 假设需要点击5次翻页按钮才能回到9月
            prev_button = driver.find_element(By.CLASS_NAME, "Y_left")  # 根据按钮的CSS类名查找
            prev_button.click()
            time.sleep(2)  # 等待每次翻页加载完成

        # 获取页面内容
        html_content = driver.page_source
        # 此处可以用 BeautifulSoup 或其他方法提取HTML数据
        return html_content
        
    except Exception as e:
        print("翻页或爬取出错:", e)

    finally:
        driver.quit()


def get_content(html):
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    data = body.find('div', {'class': 'city_40'})  
    w_left=data.find_all('div', {'class': 'W_left'})[1]
    tbody=w_left.find('tbody')
    trs=tbody.find_all('tr')
    count=0
    history=[]
    for tr in trs:
        if(count>0 and count<6):
            tds=tr.find_all('td')
            
            for td in tds:
                temp=[]
                h2=td.find('h2')
                day=h2.find_all('span')[1].text
                
                temp.append(day) #日期

                w_xian=td.find('div',{'class':'w_xian'})
                max_t=w_xian.find('span',{'class':'max'}).text
                min_t=w_xian.find('span',{'class':'min'}).text
                min_t=re.search(r"\d+", min_t).group()
                temp.append(int(max_t))
                temp.append(int(min_t))
                
                rain=w_xian.find('span',{'class':'tubiao'}).text
                temp.append(rain)
                history.append(temp)
        count+=1

    return history

today=[]
def get_content2(html):
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    data = body.find('div', {'class': 'conMidtab'})  
    provinces=data.find_all('div',{'class':'conMidtab2'})
    
    for province in provinces:
        temp=[]
        tbody=province.find('tbody')
        tr=tbody.find_all('tr')[2]
        #print(tr)
        city=tr.find_all('td')[1]
        acity=city.find('a').text
        temp.append(acity)
        phenomena=tr.find_all('td')[2].text
        temp.append(phenomena)
        wind=tr.find_all('td')[3]
        direction=wind.find_all('span')[0].text
        force=wind.find_all('span')[1].text
        temp.append(direction)
        temp.append(force)
        max_temp=tr.find_all('td')[4].text
        temp.append(int(max_temp))
        today.append(temp)

def get_content3(html):
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    data = body.find('div', {'class': 'conMidtab'})  
    provinces=data.find('div',{'class':'conMidtab2'})
    tables=provinces.find_all('table')
    for table in tables:
        temp=[]
        tr=table.find_all('tr')[2]
        city=tr.find_all('td')[1]
        acity=city.find('a').text
        temp.append(acity)
        phenomena=tr.find_all('td')[2].text
        temp.append(phenomena)
        wind=tr.find_all('td')[3]
        direction=wind.find_all('span')[0].text
        force=wind.find_all('span')[1].text
        temp.append(direction)
        temp.append(force)
        max_temp=tr.find_all('td')[4].text
        temp.append(int(max_temp))
        today.append(temp)


def write_to_csv(data):
    # 移除最后五个元素
    filtered_data = data[:-5]

    # 写入 CSV 文件
    with open("weather_shanghai.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["日期", "最高温", "最低温","降水概率"])
        # 写入数据
        writer.writerows(filtered_data)

    print("数据已成功写入 weather_shanghai.csv 文件")

def write_to_csv2(data):
    with open("weather_capital.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["城市", "天气现象", "风向","风力","最高温"])
        # 写入数据
        writer.writerows(data)

    print("数据已成功写入 weather_capital.csv 文件")

def draw_temp_curve(data):
        # 移除最后五天的数据
    filtered_data = data[:-5]
    
    # 分离日期、最高温和最低温
    dates = [day[0] for day in filtered_data]
    highs = [day[1] for day in filtered_data]
    lows = [day[2] for day in filtered_data]
    
    # 绘制最高温曲线
    plt.figure(figsize=(12, 6))
    plt.plot(dates, highs, color='red', marker='o', label='max')
    plt.plot(dates, lows, color='blue', marker='o', label='min')
    
    # 添加标题和标签
    plt.title('Temperature curve of Shanghai in September')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 显示图形
    plt.show()

# 全国各区域URL列表
urls = [
    'http://www.weather.com.cn/textFC/hb.shtml',  # 华北地区
    'http://www.weather.com.cn/textFC/db.shtml',  # 东北地区
    'http://www.weather.com.cn/textFC/hd.shtml',  # 华东地区
    'http://www.weather.com.cn/textFC/hz.shtml',  # 华中地区
    'http://www.weather.com.cn/textFC/hn.shtml',  # 华南地区
    'http://www.weather.com.cn/textFC/xb.shtml',  # 西北地区
    'http://www.weather.com.cn/textFC/xn.shtml',  # 西南地区
    
]

if __name__ == '__main__':
    #爬取9月份上海天气
    url='https://www.weather.com.cn/weather40d/101020100.shtml'
    html=gethtml_byclick(url)
    data=get_content(html)
    write_to_csv(data)
    draw_temp_curve(data)
    
    #爬取当天全国省会城市天气
    for ur in urls:
        htmls=getHTMLtext_selenium(ur)
        get_content2(htmls) 
    url2='http://www.weather.com.cn/textFC/gat.shtml'  # 港澳台
    html2=getHTMLtext_selenium(url2)
    get_content3(html2)
    write_to_csv2(today)
    

