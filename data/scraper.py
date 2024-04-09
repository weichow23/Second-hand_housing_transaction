from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.common.exceptions import TimeoutException


def read_communities():
    '''
    读取CSV文件中的小区名称
    '''
    communities = []
    with open('community_name_map_updated.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['flagQ'] != '1' and row['flagQ'] != '-1':  # 只读取尚未查询的小区
                communities.append(row)
    return communities


def update_community_flag(community, flag='1'):
    '''
    读取CSV文件中的小区名称
    '''
    all_communities = []
    with open('community_name_map_updated.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Community'] == community:
                row['flagQ'] = flag  # 更新匹配小区的flagQ
            all_communities.append(row)  # 保留所有行，包括已更新的

    # 然后，将更新后的列表写回到文件中，保留所有原有行
    with open('community_name_map_updated.csv', 'w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['District', 'Street', 'Community', 'Coordinates', 'flagC', 'flagQ']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_communities)  # 使用writerows写入整个列表


# 启动浏览器
driver = webdriver.Chrome()
driver.get("https://ershoufangdata.com/sellinfo?city=hz")

communities = read_communities()

try:
    for community in communities:
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
        input_box = driver.find_element(By.ID, "community")
        input_box.clear()
        input_box.send_keys(community['Community'])

        # 定位提交按钮并点击查询按钮
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='getsellbycommunity()']")))
        submit_button = driver.find_element(By.XPATH, "//button[@onclick='getsellbycommunity()']")
        submit_button.click()

        # 等待表格加载完成; 如果不存在则等待3s 就退出
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@id='dataTable']/tbody/tr")))
        except TimeoutException:
            update_community_flag(community['Community'], '-1')
            continue
        # # 定位提交按钮并点击查询按钮
        # WebDriverWait(driver, 3).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[@onclick='getsellbycommunity()']")))
        # submit_button = driver.find_element(By.XPATH, "//button[@onclick='getsellbycommunity()']")
        # submit_button.click()
        #
        # # 检查是否存在"不存在该小区"的警告信息
        # alert_present = WebDriverWait(driver, 2).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@id='alert'][contains(@class,'alert-danger')]")),
        #     'Alert not found'  # 这个消息是`until`函数在找不到元素时返回的，默认行为是抛出TimeoutException
        # )
        # if alert_present:
        #     update_community_flag(community['Community'], '-1')  # 更新flagQ为-1
        #     continue  # 继续下一个循环迭代（即查询下一个小区）

        # 点击"Show all rows"按钮
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-controls='dataTable'][contains(@class,'buttons-page-length')]")))
        show_all_button = driver.find_element(By.XPATH,
                                              "//button[@aria-controls='dataTable'][contains(@class,'buttons-page-length')]")
        show_all_button.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='dt-button button-page-length']//span[text()='Show all']")))
        show_all_button_2 = driver.find_element(By.XPATH,
                                                "//button[@class='dt-button button-page-length']//span[text()='Show all']")
        show_all_button_2.click()

        # 验证数据是否全部显示
        # WebDriverWait(driver, 10).until_not(
        #     EC.text_to_be_present_in_element((By.ID, "dataTable_info"), "Showing 1 to"))
        # 定位到表格
        table = driver.find_element(By.ID, "dataTable")
        # 获取所有行，不包括在thead中的行
        rows = table.find_elements(By.XPATH, "./tbody/tr")
        headers = table.find_elements(By.XPATH, "./thead/tr/th")

        # 打开一个csv文件用于写入
        with open('result.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow([th.text for th in headers])
            for row in rows:
                data = [td.text for td in row.find_elements(By.XPATH, ".//td|.//th")]
                if data:
                    writer.writerow(data)

        update_community_flag(community['Community'])
        driver.refresh()  # 刷新网页
        time.sleep(1)  # 避免过快请求

finally:
    # 关闭浏览器
    driver.quit()
