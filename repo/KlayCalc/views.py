from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from selenium import webdriver  # For crawling


DONATE_ADDR = '0x2eC41C940731c6CEA7275888835F8c2A6B58Ad79'
TIME_OUT = 3

__SEC = 1
__MIN = __SEC * 60
__HOUR = __MIN * 60
__DAY = __HOUR * 24
__WEEK = __DAY * 7
__MONTH = __DAY * 30

# Create your views here.
def root(request):
    return redirect('index')


def index(request):
    # Someday, 세션에 가장 마지막에 조회했던 주소를 자동으로 추천해주는 기능 넣기 (Session or Cookie 통해서)
    return render(request, 'KlayCalc/index.html')


def account(request, account_id = None):
    # 입력된 주소가 없다면, 메인 화면으로 Redirect.
    if account_id is None:
        return redirect('index')

    __LOG("[LOG] Account ID : {}".format(account_id))
    

    # account_id에 대한 유효성 검증 -> View 에서 처리.
    # Account/Contract : 42 글자 || Block/Transaction : 66 글자
    # 아직, Account랑 Contract 구분 방법을 모르겠음.. 
    # 이 부분은 일단 Parsing 데이터에서 확인하는 방식으로 구현 후 추후 수정.
    # ==> Klaystation도 아직 안되어 있음.

    # TEMP
    #return render(request, 'KlayCalc/account.html')

    resYn = False  # True | False - 조회 결과 있음 | 없음
    parsed_data = dict()
    ##### PARSING START
    try:
        __LOG('[LOG] Start Parsing (with Selenium)')
         # Selenium Setting
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome('C:/dev/tools/chromedriver.exe', options=options)

        driver.implicitly_wait(TIME_OUT)  # 3초 이상 되어야 ERROR가 발생하지 않음

        # URL Setting & Get Data
        url = 'https://klaystation.io/explorer/account/' + account_id
        driver.get(url)

        # Parsing Data
        total_staking      = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[1]/div/p[1]').text
        accumulated_reward = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[2]/div/p[1]').text
        refund             = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[3]/div/p[1]').text
        in_wallet          = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[4]/div/p[1]').text
        parsed_data['total_staking']      = total_staking
        parsed_data['accumulated_reward'] = accumulated_reward
        parsed_data['refund']             = refund
        parsed_data['in_wallet']          = in_wallet


        # URL Setting & Get Data
        url = 'https://klaystation.io/dashboard'
        driver.get(url)

        # Parsing Data
        rate_annu = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[2]/ul/li[3]/div[2]/p/span[1]').text
        rate_annu = float(rate_annu) / 100
        rate = ( rate_annu / 8760 )  # 시이율(시간당 이율)
        
        # 일단 단리로 계산
        temp = float(total_staking)
        # temp = 123456.789  # TEST
        reward_hour  = temp * rate 
        reward_day   = temp * rate * 24
        reward_week  = temp * rate * 24 * 7
        reward_month = temp * rate * 24 * 30
        
        # print('##########################')
        # print(rate)
        # temp = float(total_staking)
        # temp = 86614600.10
        # reward_hour  = temp * ( rate )
        # reward_day   = temp * ( rate ** 24 )
        # reward_week  = temp * ( rate ** (24 * 7) )
        # reward_month = temp * ( rate ** (24 * 30) )

        reward_hour  = "%0.2lf"%reward_hour
        reward_day   = "%0.2lf"%reward_day
        reward_week  = "%0.2lf"%reward_week
        reward_month = "%0.2lf"%reward_month

        parsed_data['reward_hour']  = reward_hour
        parsed_data['reward_day']   = reward_day 
        parsed_data['reward_week']  = reward_week
        parsed_data['reward_month'] = reward_month

        resYn = True
        
    except Exception as err :
        __LOG('[LOG] ERROR >> {}'.format(err))
        err.with_traceback()

    finally:
        driver.quit()

        __LOG('[LOG] End Parsing (with Selenium)')
    ##### PARSING END


    if len(parsed_data) == 0:
        resYn = False

    params = {
        'resYn' : resYn,
        'account_id' : account_id,
        'parsed_data' : parsed_data,
    }

    return render(request, 'KlayCalc/account.html', params)


def donate(request):
    return render(request, 'KlayCalc/donate.html')


# Ajax
def checkDonateAddr(request):
    
    viewAddr = request.POST['donateAddr']
    
    return HttpResponse(True) if DONATE_ADDR == viewAddr else HttpResponse(False)


# Private Func.
def __LOG(msg):
    print(msg)




def test(request):
    account_id = '0x2eC41C940731c6CEA7275888835F8c2A6B58Ad79 ---'


    # Selenium Setting
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome('C:/dev/tools/chromedriver.exe', options=options)

    driver.implicitly_wait(3)  # 3초 이상 되어야 ERROR가 발생하지 않음

    # URL Setting
    url = 'https://klaystation.io/explorer/account/' + account_id

    # Get Data
    driver.get(url)

    a = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[1]/div/p[1]').text
    b = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[1]/ul/li[2]/div/p[1]').text
    
    print("RESULT")
    print(a)
    print(b)

    driver.quit()

    return HttpResponse(a + " : " + b)