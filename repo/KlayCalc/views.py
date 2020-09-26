from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

# Create your views here.
def root(request):
    return redirect('index')


def index(request):
    # Someday, 세션에 가장 마지막에 조회했던 주소를 자동으로 추천해주는 기능 넣기 (Session or Cookie 통해서)
    return render(request, 'KlayCalc/index.html')


def account(request, account_id = None):
    # Temp Redirect - 나중에 가운데 주소 입력하는 거 보여주는 방식으로!
    if account_id is None:
        return redirect('index')
    
    # account_id에 대한 유효성 검증과정 필요
    # account_id를 통해 Parsing 해온 데이터 정제 후 전달하는 처리과정 필요

    account_id_valid = ''  # ID | NULL | OTHER - 정상 주소 | 없음 | 잘못된 주소
    parsed_data = None

    params = {
        'account_id_valid' : account_id_valid,
        'account_id' : account_id,
        'parsed_data' : parsed_data,
    }

    return render(request, 'KlayCalc/account.html', params)


def donate(request):
    return render(request, 'KlayCalc/donate.html')