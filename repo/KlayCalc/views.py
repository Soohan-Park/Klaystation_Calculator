from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from .models import RateData

from selenium import webdriver  # For crawling


# Global Var.
SELENIUM_DRIVER_PATH = './KlayCalc/static/klaycalcAssets/files/chromedriver.exe'  # 상대경로
DONATE_ADDR = '0x2eC41C940731c6CEA7275888835F8c2A6B58Ad79'
TIME_OUT = 3


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

    resYn = False  # True | False - 조회 결과 있음 | 없음
    parsed_data = dict()
    ##### PARSING START
    try:
        __LOG('[LOG] Start Parsing (with Selenium)')
        # Selenium Setting
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(SELENIUM_DRIVER_PATH, options=options)

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

        # Get Annu-rate Data
        rate = RateData.objects.last().rate

        # 일단 단리로 계산
        amount = float(total_staking)
        reward_hour  = amount * rate 
        reward_day   = reward_hour * 24
        reward_week  = reward_day  * 7
        reward_month = reward_day  * 30

        parsed_data['reward_hour']  = "%0.3lf"%reward_hour
        parsed_data['reward_day']   = "%0.3lf"%reward_day
        parsed_data['reward_week']  = "%0.3lf"%reward_week
        parsed_data['reward_month'] = "%0.3lf"%reward_month

        resYn = True
        
    except Exception as err :
        __LOG('[LOG] ERROR >> {}'.format(err))
        err.with_traceback()

        return account(request, account_id)

    finally:
        driver.close()

        __LOG('[LOG] End Parsing (with Selenium)')
    ##### PARSING END


    # 실패 시 재시도 방안 고려하기
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


def getRate(request):
    flag = True
    rate_annu = None

    try:
        # Selenium Setting
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(SELENIUM_DRIVER_PATH, options=options)
        driver.implicitly_wait(TIME_OUT)  # 3초 이상 되어야 ERROR가 발생하지 않음

        # URL Setting & Get Data
        url = 'https://klaystation.io/dashboard'
        driver.get(url)

        # Parsing Data
        rate_annu = driver.find_element_by_xpath('//*[@id="router-wrapper"]/div/section/div[2]/div/div[2]/ul/li[3]/div[2]/p/span[1]').text
        rate_annu = float(rate_annu) / 100

        print("GET RATE ANNU")
        print(rate_annu)
    except Exception as err:
        __LOG('[LOG] ERROR HAS OCCURED (GETRATE) >> {}'.format(err))
        flag = False
    finally:
        driver.quit()
    
    try:
        db = RateData(rate=rate_annu)
        db.save()
    except Exception as err:
        __LOG('[LOG] ERROR HAS OCCURED (GETRATE) >> {}'.format(err))
        flag = False
    
    if flag is False or rate_annu is None:
        return HttpResponse('Fail.')
    
    return HttpResponse('Success!')


# Private Func.
def __LOG(msg):
    print(msg)
