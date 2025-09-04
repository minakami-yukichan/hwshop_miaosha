# coding = utf-8

from selenium import webdriver
import time
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

ACCOUNTS = {
    '13873171733': 'tt030519'
}


chrome_driver = "C:\\Users\\26817\\anaconda3\\chromedriver.exe"   # Win32_76.0.3809.126

# Mate 20 X(5G)
BUY_URL = 'https://www.vmall.com/product/comdetail/index.html?prdId=10086989076790&sbomCode=2601010515134'
# 测试P30 Pro
#BUY_URL = 'https://www.vmall.com/product/comdetail/index.html?prdId=10086157311748&sbomCode=2601010486628'
# 登录url
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/index.html'
# 开始自动刷新等待抢购按钮出现的时间点,提前3分钟
BEGIN_GO = '2024-12-23 10:08:00'


# 进到购买页面后提交订单
def submitOrder(driver, user):
    time.sleep(1)
    while BUY_URL == driver.current_url:
        print(user + ':当前页面还在商品详情！！！')
        time.sleep(3)

    while True:
        try:
            submitOrder = driver.find_elements(By.LINK_TEXT,'提交订单')
            actions = ActionChains(driver)
            actions.move_to_element(submitOrder).click().perform()
            print(user + ':成功提交订单')
            break
        except:
            print(user + ':提交不了订单！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
            time.sleep(1)  # 到了订单提交页面提交不了订单一直等待
            pass
    while True:
        time.sleep(3000)
        print(user + ':进入睡眠3000s')
        pass


# 排队中
def onQueue(driver, user):
    time.sleep(1)
    nowUrl = driver.current_url
    while True:
        try:
            errorbutton = driver.find_elements(By.LINK_TEXT,'返回活动页面')  # 出现这个一般是失败了。。
            if errorbutton.is_enabled():
                print(user + "：出现返回活动页面，可能抢购失败。。。")
                actions = ActionChains(driver)
                actions.move_to_element(errorbutton).click().perform()
            pass
        except:
            print(user + ':排队中')
            time.sleep(0.3)  # 排队中
            pass
        if nowUrl != driver.current_url and nowUrl != BUY_URL:
            print(user + ':排队页面跳转了!!!!!!!!!!!!!!')
            break
        '''else:
            goToBuy(driver, user)'''
    submitOrder(driver, user)


# 登录成功去到购买页面
def goToBuy(driver, user):
    driver.get(BUY_URL)
    print(user + '打开购买页面')
    # 转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # 结束标志位
    over = False
    while True:
        if time.time() > timestamp:  # 到了抢购时间
            button = driver.find_elements(By.XPATH,'//*[@id="prd-botnav-rightbtn-txt"]')[0]
            text = driver.find_elements(By.XPATH,'//*[@id="prd-botnav-rightbtn-txt"]/div')[0].text
            if text == '暂时缺货':
                over = True
                break
            if text == '立即购买' and button.get_attribute('class') != 'product-button02 disabled':
            # buyButton = driver.find_element_by_link_text('立即申购')
                print(user + '立即申购按钮出现了！！！')
                #button.click()
                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()
                print(user + '立即购买')
                break
            time.sleep(0.2)
        else:
            time.sleep(0.05)
            print(user + '睡眠0.05s，未到脚本开启时间：' + BEGIN_GO)
    if over:
        print("很遗憾，抢购结束。。。")
        exit(0)
    else:
        onQueue(driver, user)


# 登录商城,登陆成功后至商城首页然后跳转至抢购页面
def loginMall(user, pwd):
    driver = webdriver.Chrome()
    driver.get(BUY_URL)
    '''try:
        time.sleep(5)  # 等待页面加载完成
        account = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[3]/div[3]/span[3]/div[1]/form/div[2]/div/div/div/input')
        #account = driver.find_element_by_xpath('//*[@id="login_userName"]')
        account.send_keys(user)
        time.sleep(1)
        password = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[3]/div[3]/span[3]/div[1]/form/div[3]/div/div/div/input')
        #password = driver.find_element_by_xpath('//*[@id="login_password"]')
        password.send_keys(pwd)
        print(user + '输入了账号密码，等待手动登录')
    except:
        print(user + '账号密码不能输入')'''

    button = driver.find_elements(By.XPATH,'//*[@id="prd-botnav-rightbtn-txt"]')[0]
    text = driver.find_elements(By.XPATH,'//*[@id="prd-botnav-rightbtn-txt"]/div')[0].text
    print(text)
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()
    print("请扫码登陆")

    while True:
        time.sleep(3)
        if BUY_URL == driver.current_url:
            print(user + '登录成功！')
            break
    goToBuy(driver, user)


if __name__ == "__main__":
    # 账号密码
    data = ACCOUNTS
    # 构建线程
    threads = []
    for account, pwd in data.items():
        t = Thread(target=loginMall, args=(account, pwd,))
        threads.append(t)
        # 启动所有线程
    for thr in threads:
        time.sleep(2)
        thr.start()
    time.sleep(60)