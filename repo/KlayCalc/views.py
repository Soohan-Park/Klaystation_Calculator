from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

DONATE_ADDR = '0x2eC41C940731c6CEA7275888835F8c2A6B58Ad79'

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

    __LOG("Account ID : {}".format(account_id))
    
    # account_id에 대한 유효성 검증 -> View 에서 처리.
    # Account/Contract : 42 글자 || Block/Transaction : 66 글자
    # 아직, Account랑 Contract 구분 방법을 모르겠음.. 
    # 이 부분은 일단 Parsing 데이터에서 확인하는 방식으로 구현 후 추후 수정.
    # account_id를 통해 Parsing 해온 데이터 정제 후 전달하는 처리과정 필요

    resYn = None  # True | False - 조회 결과 있음 | 없음
    parsed_data = None

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