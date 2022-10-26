import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/projects/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


@pytest.fixture()
def go_to_my_pets():
    pytest.driver.find_element_by_id('email').send_keys('polinapolina@mail.ru')
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element_by_id('pass').send_keys('12345')
    pytest.driver.implicitly_wait(20)
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    WebDriverWait(pytest.driver, 10).until(EC.title_contains("PetFriends"))
    pytest.driver.find_element_by_link_text('Мои питомцы').click()


def test_count_mypets(go_to_my_pets):
    pets_number = int(pytest.driver.find_element_by_css_selector('html>body>div>div>div').text.split("\n")[1].split(":")
                      [1].strip())
    pets_on_page = pytest.driver.find_elements_by_css_selector('tbody>tr')
    assert pets_number == len(pets_on_page)


def test_different_name_age_breed(go_to_my_pets):

    pet_data = pytest.driver.find_elements_by_tag_name('td')
    for i in pet_data:
        assert i.text != ''

def test_photo_more_than_half_pets(go_to_my_pets):
    pets_number = int(pytest.driver.find_element_by_css_selector('html>body>div>div>div').text.split("\n")[1].split(":")
                      [1].strip())
    images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')
    number_of_photo = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_photo += 1

    assert number_of_photo >= (pets_number // 2)



def test_all_pets_different(go_to_my_pets):

    pets_cards = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    pets_name = []
    for i in range(len(pets_cards)):
        pets_data = pets_cards[i].text.replace('\n', '').replace('×', '')
        split_pets_data = pets_data.split(' ')
        pets_name.append(split_pets_data[0])
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
        assert r == 0


def test_no_duplicate_pets(go_to_my_pets):

    pets_cards = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    list_data = []
    for i in range(len(pets_cards)):
        pets_data = pets_cards[i].text.replace('\n', '').replace('×', '')
        split_pets_data = pets_data.split(' ')
        list_data.append(split_pets_data)
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '
    list_line = line.split(' ')
    set_list_line = set(list_line)
    a = len(list_line)
    b = len(set_list_line)
    result = a - b
    assert result == 0