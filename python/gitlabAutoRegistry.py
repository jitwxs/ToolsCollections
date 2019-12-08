#encoding:utf-8

from selenium import webdriver

def parserDate(loginUrl,superName,superPassWord,data):
    driver = webdriver.Firefox()  
    driver.get(loginUrl)  
    userNameXpath = ".//*[@id='user_login']"  
    driver.find_element_by_xpath(userNameXpath).clear()  
    driver.find_element_by_xpath(userNameXpath).send_keys(superName)  
    pasWrdXpath = ".//*[@id='user_password']"  
    driver.find_element_by_xpath(pasWrdXpath).clear()  
    driver.find_element_by_xpath(pasWrdXpath).send_keys(superPassWord)  
    loginXpath = ".//*[@id='new_user']/div[2]/input"  
    driver.find_element_by_xpath(loginXpath).click()

    for handle in driver.window_handles:
        driver.switch_to_window(handle)

    for name,email in data.items():
        print("开始处理：",name,email)
    
        nameXPath = ".//*[@id='user_name']"
        driver.find_element_by_xpath(nameXPath).clear()  
        driver.find_element_by_xpath(nameXPath).send_keys(name)  
        userNameXpath = ".//*[@id='user_username']"
        driver.find_element_by_xpath(userNameXpath).clear()  
        driver.find_element_by_xpath(userNameXpath).send_keys(name)  
        emailXpath = ".//*[@id='user_email']"  
        driver.find_element_by_xpath(emailXpath).clear()  
        driver.find_element_by_xpath(emailXpath).send_keys(email)  
        loginXpath = ".//*[@id='new_user']/div/input"
        driver.find_element_by_xpath(loginXpath).click()

        driver.back()

    driver.close()
      
if __name__ == '__main__':
    data = {}
    superName = input("超级用户名：")
    superPassWord = input("密码：")
    try:
        with open(sys.argv[1],'r') as f:
            tmps = f.readlines()
            for i in tmps:
                tmpData = i.strip().split('\t')
                data[tmpData[0]] = tmpData[1]
        parserDate('http://172.19.73.49/admin/users/new',superName,superPassWord,data)
    except:
        print("无法找到数据文件data.txt或数据文件格式错误(name\temail)")
    input("程序结束")
