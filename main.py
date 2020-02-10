import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import chromedriver_binary
from cqpapi import API
from constants import chuninet, chimera_id, sega_id, sega_pw

"""
原谅我用中文写注释(X)
工具需要用到cqhttp https://cqhttp.cc/docs/4.13/#/
用selenium模拟登录 用requests发送请求

chuninet设定需要把奇美拉添加到お気に入り
只计算master谱面 因为红谱肯定不进奇美拉best
"""

api = API()


def main():
    def xpath_click(xpath):
        driver.find_element_by_xpath(xpath).click()

    def get_score(elements):
        score_array = []
        for i in elements:
            music_name = i.text.split('\n')[0]
            score = i.text.split('\n')[3]
            score_array.append({
                'music': music_name,
                'score': score
            })
        return score_array

    driver = webdriver.Chrome()
    driver.get(chuninet)
    time.sleep(0.5)

    account_box = driver.find_element_by_name('segaId')
    pw_box = driver.find_element_by_name('password')

    account_box.send_keys(sega_id)
    pw_box.send_keys(sega_pw)
    account_box.submit()
    time.sleep(0.5)

    xpath_click('//*[@id="inner"]/div[1]/div/div[2]/div[1]/form/button')
    time.sleep(0.5)
    xpath_click('//*[@id="main_menu"]/ul/li[4]')
    time.sleep(0.5)
    xpath_click('//*[@id="submenu"]/ul/li[5]')
    time.sleep(0.5)
    xpath_click('//*[@id="inner"]/div[2]/div/div[2]/a')
    time.sleep(0.5)
    xpath_click(
        '//*[@id="inner"]/div[2]/div/div[3]/form/div[1]/select[1]/option[19]')  # LV13
    friend_box = driver.find_element_by_name('friend')
    Select(friend_box).select_by_value(chimera_id)
    driver.find_element_by_class_name("btn_battle").click()
    time.sleep(0.5)
    chimera_card_name = driver.find_element_by_xpath(
        '//*[@id="inner"]/div[2]/div/div[4]/div[1]/div[3]/div[1]').text

    lv13_list = get_score(driver.find_elements_by_class_name("bg_master"))

    xpath_click(
        '//*[@id="inner"]/div[2]/div/div[3]/form/div[1]/select[1]/option[20]')  # LV13+
    driver.find_element_by_class_name("btn_battle").click()
    time.sleep(0.5)
    lv13plus_list = get_score(driver.find_elements_by_class_name("bg_master"))

    xpath_click(
        '//*[@id="inner"]/div[2]/div/div[3]/form/div[1]/select[1]/option[21]')  # LV14
    driver.find_element_by_class_name("btn_battle").click()
    time.sleep(0.5)
    lv14_list = get_score(driver.find_elements_by_class_name("bg_master"))

    score_list = lv13_list + lv13plus_list + lv14_list

    score_msg = ''
    score_msg = score_msg + 'カードネーム：' + chimera_card_name + '\n'
    for i in score_list:
        score_msg = score_msg + '曲名：' + \
            i['music'] + ' スコア：' + i['score'] + '\n'
    print(score_msg)

    api.send_msg(score_msg)


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)
