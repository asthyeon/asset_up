from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from accounts.models import User
# from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

from .models import Company, CompanyOption, DepositProduct, DepositOption, SavingProduct, SavingOption, AnnuitySavingProduct, AnnuitySavingOption, MortgageLoanProduct, MortgageLoanOption, RentHouseLoanProduct, RentHouseLoanOption, CreditLoanProduct, CreditLoanOption
from .serializers import CompanySerializer, CompanyOptionSerializer, DepositProductSerializer, DepositOptionSerializer, SavingProductSerializer, SavingOptionSerializer, AnnuitySavingProductSerializer, AnnuitySavingOptionSerializer, MortgageLoanProductSerializer, MortgageLoanOptionSerializer, RentHouseLoanProductSerializer, RentHouseLoanOptionSerializer, CreditLoanProductSerializer, CreditLoanOptionSerializer

api_key = settings.FINANCE_API_KEY
domain = 'http://finlife.fss.or.kr/finlifeapi'
topFinGrpNo_list = ['020000', '030200', '030300', '050000', '060000']

# 금융회사 저장
@api_view(['GET'])
def save_companys(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/companySearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            print(max_page_no, pageNo, topFinGrpNo)
            
            # 은행 목록 순회
            for li in response.get("result").get("baseList"):
                fin_co_no = li['fin_co_no']

                # 이미 존재하는 데이터인지 확인
                if Company.objects.filter(fin_co_no=fin_co_no).exists():
                    continue  # 이미 존재하면 건너뛰기
                
                # 은행 데이터 할당
                save_data = {
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'dcls_chrg_man': li['dcls_chrg_man'],
                    'homp_url': li['homp_url'],
                    'cal_tel': li['cal_tel'],
                }
                # 직렬화
                serializer = CompanySerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    
            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month'],
                fin_co_no = li['fin_co_no']
                area_cd  = li['area_cd']
                area_nm =  li['area_nm']
                
                # 이미 존재하는 데이터인지 확인
                if CompanyOption.objects.filter(dcls_month=dcls_month,
                    fin_co_no=fin_co_no,
                    area_cd=area_cd,
                    area_nm=area_nm
                    ).exists():
                    continue  # 이미 존재하면 건너뛰기
                
                # 데이터 변환
                if li['exis_yn'] == 'Y':
                    exis_yn = True
                else:
                    exis_yn = False
                
                company = Company.objects.get(fin_co_no=fin_co_no)

                option = CompanyOption(company=company, dcls_month=dcls_month,fin_co_no=fin_co_no, area_cd=area_cd, area_nm=area_nm, exis_yn=exis_yn)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 예금 저장
@api_view(['GET'])
def save_deposit_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/depositProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 예금 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.get(fin_co_no=li['fin_co_no'])
                
                # 이미 존재하는 데이터 패스
                if DepositProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 예금 상품 데이터 할당
                save_data = {
                    'company': company.pk,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'mtrt_int': li['mtrt_int'],
                    'spcl_cnd': li['spcl_cnd'],
                    'join_deny': li['join_deny'],
                    'join_member': li['join_member'],
                    'etc_note': li['etc_note'],
                    'max_limit': li['max_limit'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = DepositProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                intr_rate_type = li['intr_rate_type']
                intr_rate_type_nm  = li['intr_rate_type_nm']
                intr_rate =  li['intr_rate']
                intr_rate2 =  li['intr_rate2']
                save_trm =  li['save_trm']
                
                # 이미 존재하는 데이터 패스
                if DepositOption.objects.filter(dcls_month=dcls_month, fin_co_no=fin_co_no, 
                    fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, 
                    intr_rate_type_nm=intr_rate_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm).exists():
                    continue
                
                # 결측치 처리
                if not intr_rate:
                    intr_rate = -1
                if not intr_rate2:
                    intr_rate2 = -1

                product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = DepositOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 적금 저장
@api_view(['GET'])
def save_saving_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/savingProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 적금 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.get(fin_co_no=li['fin_co_no'])
                
                # 중복 데이터 패스
                if SavingProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 적금 상품 데이터 할당
                save_data = {
                    'company': company.pk,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'mtrt_int': li['mtrt_int'],
                    'spcl_cnd': li['spcl_cnd'],
                    'join_deny': li['join_deny'],
                    'join_member': li['join_member'],
                    'etc_note': li['etc_note'],
                    'max_limit': li['max_limit'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = SavingProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                intr_rate_type =li['intr_rate_type']
                intr_rate_type_nm  = li['intr_rate_type_nm']
                rsrv_type = li['rsrv_type']
                rsrv_type_nm = li['rsrv_type_nm']
                intr_rate =  li['intr_rate']
                intr_rate2 =  li['intr_rate2']
                save_trm =  li['save_trm']
                
                # 중복 데이터 패스
                if SavingOption.objects.filter(dcls_month=dcls_month, fin_co_no=fin_co_no, 
                    fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, 
                    intr_rate_type_nm=intr_rate_type_nm,
                    rsrv_type=rsrv_type, 
                    rsrv_type_nm=rsrv_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm).exists():
                    continue
                
                # 결측치 처리
                if not intr_rate:
                    intr_rate = -1
                if not intr_rate2:
                    intr_rate2 = -1

                product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = SavingOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd, intr_rate_type=intr_rate_type, intr_rate_type_nm=intr_rate_type_nm, rsrv_type=rsrv_type, rsrv_type_nm = rsrv_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 연금저축 저장
@api_view(['GET'])
def save_annuity_saving_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/annuitySavingProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 연금저축 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.filter(fin_co_no=li['fin_co_no'])
                if not company:
                    continue
                # 중복 데이터 패스
                if AnnuitySavingProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 연금저축 상품 데이터 할당
                save_data = {
                    'company': company[0].id,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'pnsn_kind': li['pnsn_kind'],
                    'pnsn_kind_nm': li['pnsn_kind_nm'],
                    'sale_strt_day': li['sale_strt_day'],
                    'mntn_cnt': li['mntn_cnt'],
                    'prdt_type': li['prdt_type'],
                    'prdt_type_nm': li['prdt_type_nm'],
                    'avg_prft_rate': li['avg_prft_rate'],
                    'dcls_rate': li['dcls_rate'],
                    'guar_rate': li['guar_rate'],
                    'btrm_prft_rate_1': li['btrm_prft_rate_1'],
                    'btrm_prft_rate_2': li['btrm_prft_rate_2'],
                    'btrm_prft_rate_3': li['btrm_prft_rate_3'],
                    'etc': li['etc'],
                    'sale_co': li['sale_co'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day'],
                }
                # 직렬화
                serializer = AnnuitySavingProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                pnsn_recp_trm = li['pnsn_recp_trm'],
                pnsn_recp_trm_nm = li['pnsn_recp_trm_nm'],
                pnsn_entr_age = li['pnsn_entr_age'],
                pnsn_entr_age_nm = li['pnsn_entr_age_nm'],
                mon_paym_atm = li['mon_paym_atm'],
                mon_paym_atm_nm = li['mon_paym_atm_nm'],
                paym_prd = li['paym_prd'],
                paym_prd_nm = li['paym_prd_nm'],
                pnsn_strt_age = li['pnsn_strt_age'],
                pnsn_strt_age_nm = li['pnsn_strt_age_nm'],
                pnsn_recp_amt = li['pnsn_recp_amt']
                
                # 중복 데이터 패스
                if AnnuitySavingOption.objects.filter(
                    dcls_month=dcls_month,
                    fin_co_no=fin_co_no,
                    fin_prdt_cd=fin_prdt_cd,
                    pnsn_recp_trm=pnsn_recp_trm,
                    pnsn_recp_trm_nm = pnsn_recp_trm_nm,
                    pnsn_entr_age = pnsn_entr_age,
                    pnsn_entr_age_nm = pnsn_entr_age_nm,
                    mon_paym_atm = mon_paym_atm,
                    mon_paym_atm_nm =mon_paym_atm_nm,
                    paym_prd = paym_prd,
                    paym_prd_nm = paym_prd_nm,
                    pnsn_strt_age =pnsn_strt_age,
                    pnsn_strt_age_nm = pnsn_strt_age_nm,
                    pnsn_recp_amt = pnsn_recp_amt).exists():
                    continue
                if not AnnuitySavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                    continue

                product = AnnuitySavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = AnnuitySavingOption(product=product, dcls_month=dcls_month, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd,pnsn_recp_trm=pnsn_recp_trm, pnsn_recp_trm_nm = pnsn_recp_trm_nm, pnsn_entr_age = pnsn_entr_age,pnsn_entr_age_nm = pnsn_entr_age_nm, mon_paym_atm = mon_paym_atm, mon_paym_atm_nm=mon_paym_atm_nm, paym_prd = paym_prd, paym_prd_nm = paym_prd_nm, pnsn_strt_age =pnsn_strt_age, pnsn_strt_age_nm = pnsn_strt_age_nm, pnsn_recp_amt = pnsn_recp_amt)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 주택담보 대출 저장
@api_view(['GET'])
def save_mortgage_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/mortgageLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            print(max_page_no, pageNo, topFinGrpNo)

            
            # 주택담보 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.get(fin_co_no=li['fin_co_no'])
                
                # 중복 데이터 패스
                if MortgageLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 연금저축 상품 데이터 할당
                save_data = {
                    'company': company.pk,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'loan_inci_expn': li['loan_inci_expn'],
                    'erly_rpay_fee': li['erly_rpay_fee'],
                    'dly_rate': li['dly_rate'],
                    'loan_lmt': li['loan_lmt'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day']
                }
                # 직렬화
                serializer = MortgageLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                mrtg_type = li['mrtg_type']
                mrtg_type_nm = li['mrtg_type_nm']
                rpay_type = li['rpay_type']
                rpay_type_nm = li['rpay_type_nm']
                lend_rate_type = li['lend_rate_type']
                lend_rate_type_nm = li['lend_rate_type_nm']
                lend_rate_min = li['lend_rate_min']
                lend_rate_max = li['lend_rate_max']
                lend_rate_avg = li['lend_rate_avg']
                
                # 중복 데이터 패스
                if MortgageLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    mrtg_type = mrtg_type,
                    mrtg_type_nm = mrtg_type_nm,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg).exists():
                    continue

                product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = MortgageLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    mrtg_type = mrtg_type,
                    mrtg_type_nm = mrtg_type_nm,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 전세자금 대출 저장
@api_view(['GET'])
def save_rent_house_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/rentHouseLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 전세자금 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.get(fin_co_no=li['fin_co_no'])
                
                # 중복 데이터 패스
                if RentHouseLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 전세자금 상품 데이터 할당
                save_data = {
                    'company': company.pk,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'loan_inci_expn': li['loan_inci_expn'],
                    'erly_rpay_fee': li['erly_rpay_fee'],
                    'dly_rate': li['dly_rate'],
                    'loan_lmt': li['loan_lmt'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day']
                }
                # 직렬화
                serializer = RentHouseLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                rpay_type = li['rpay_type']
                rpay_type_nm = li['rpay_type_nm']
                lend_rate_type = li['lend_rate_type']
                lend_rate_type_nm = li['lend_rate_type_nm']
                lend_rate_min = li['lend_rate_min']
                lend_rate_max = li['lend_rate_max']
                lend_rate_avg = li['lend_rate_avg']
                
                # 중복 데이터 패스
                if RentHouseLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg):
                    continue

                product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = RentHouseLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    rpay_type = rpay_type,
                    rpay_type_nm = rpay_type_nm,
                    lend_rate_type = lend_rate_type,
                    lend_rate_type_nm = lend_rate_type_nm,
                    lend_rate_min = lend_rate_min,
                    lend_rate_max = lend_rate_max,
                    lend_rate_avg = lend_rate_avg)
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 개인신용 대출 저장
@api_view(['GET'])
def save_credit_loan_products(request):
    for topFinGrpNo in topFinGrpNo_list:
        pageNo = 1
        max_page_no = 1
        while pageNo <= max_page_no:
            url = f'{domain}/creditLoanProductsSearch.json?auth={api_key}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
            response = requests.get(url).json()
            max_page_no = response.get("result").get("max_page_no")
            pageNo += 1
            
            # 개인신용 대출 상품 목록 순회
            for li in response.get("result").get("baseList"):
                company = Company.objects.filter(fin_co_no=li['fin_co_no'])
                if not company.exists():
                    continue
                
                # 중복 데이터 패스
                if CreditLoanProduct.objects.filter(fin_prdt_cd=li['fin_prdt_cd']).exists():
                    continue
                
                # 개인신용대출 상품 데이터 할당
                save_data = {
                    'company': company[0].id,
                    'dcls_month': li['dcls_month'],
                    'fin_co_no': li['fin_co_no'],
                    'kor_co_nm': li['kor_co_nm'],
                    'fin_prdt_cd': li['fin_prdt_cd'],
                    'fin_prdt_nm': li['fin_prdt_nm'],
                    'join_way': li['join_way'],
                    'cb_name': li['cb_name'],
                    'crdt_prdt_type': li['crdt_prdt_type'],
                    'crdt_prdt_type_nm': li['crdt_prdt_type_nm'],
                    'dcls_strt_day': li['dcls_strt_day'],
                    'dcls_end_day': li['dcls_end_day'],
                    'fin_co_subm_day': li['fin_co_subm_day']
                }
                # 직렬화
                serializer = CreditLoanProductSerializer(data=save_data)
                # 유효성 검사 후 저장
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            # 옵션 목록 순회
            for li in response.get("result").get("optionList"):
                dcls_month = li['dcls_month']
                fin_co_no = li['fin_co_no']
                fin_prdt_cd = li['fin_prdt_cd']
                crdt_prdt_type = li['crdt_prdt_type']
                crdt_lend_rate_type = li['crdt_lend_rate_type']
                crdt_lend_rate_type_nm = li['crdt_lend_rate_type_nm']
                crdt_grad_1 = li['crdt_grad_1']
                crdt_grad_4 = li['crdt_grad_4']
                crdt_grad_5 = li['crdt_grad_5']
                crdt_grad_6 = li['crdt_grad_6']
                crdt_grad_10 = li['crdt_grad_10']
                crdt_grad_11 = li['crdt_grad_11']
                crdt_grad_12 = li['crdt_grad_12']
                crdt_grad_13 = li['crdt_grad_13']
                crdt_grad_avg = li['crdt_grad_avg']
                
                # 중복 데이터 패스
                if CreditLoanOption.objects.filter(
                    dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    crdt_prdt_type = crdt_prdt_type,
                    crdt_lend_rate_type = crdt_lend_rate_type,
                    crdt_lend_rate_type_nm = crdt_lend_rate_type_nm,
                    crdt_grad_1 = crdt_grad_1,
                    crdt_grad_4 = crdt_grad_4,
                    crdt_grad_5 = crdt_grad_5,
                    crdt_grad_6 = crdt_grad_6,
                    crdt_grad_10 = crdt_grad_10,
                    crdt_grad_11 = crdt_grad_11, crdt_grad_12=crdt_grad_12, crdt_grad_13=crdt_grad_13, crdt_grad_avg=crdt_grad_avg
                    ).exists():
                    continue

                product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
                option = CreditLoanOption(product=product, dcls_month = dcls_month,
                    fin_co_no = fin_co_no,
                    fin_prdt_cd = fin_prdt_cd,
                    crdt_prdt_type = crdt_prdt_type,
                    crdt_lend_rate_type = crdt_lend_rate_type,
                    crdt_lend_rate_type_nm = crdt_lend_rate_type_nm,
                    crdt_grad_1 = crdt_grad_1,
                    crdt_grad_4 = crdt_grad_4,
                    crdt_grad_5 = crdt_grad_5,
                    crdt_grad_6 = crdt_grad_6,
                    crdt_grad_10 = crdt_grad_10,
                    crdt_grad_11 = crdt_grad_11, crdt_grad_12=crdt_grad_12, crdt_grad_13=crdt_grad_13, crdt_grad_avg=crdt_grad_avg
                    )
                option.save()

    return JsonResponse({ 'message': 'okay'})


# 금융 회사 조회
@api_view(['GET'])
def get_companys(request):
    # 예금 목록 불러오기
    companys = Company.objects.all()
    seralizer = CompanySerializer(companys, many=True)
    return Response(seralizer.data)

# 특정 금융 회사 옵션 조회
@api_view(['GET'])
def get_company_options(request, fin_co_no):
    # 예금 목록 불러오기
    optionlist = CompanyOption.objects.filter(fin_co_no=fin_co_no)
    seralizer = CompanyOptionSerializer(optionlist, many=True)
    return Response(seralizer.data)


# 전체 예금 상품 조회
@api_view(['GET'])
def get_deposit_products(request):
    # 예금 목록 불러오기
    products = DepositProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = DepositOptionSerializer(option_list, many=True)
        serializer2 = DepositProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)
    
    
# 전체 예금 옵션 조회
@api_view(['GET'])
def get_deposit_options(request):
    # 예금 목록 불러오기
    options = DepositOption.objects.all()
    seralizer = DepositOptionSerializer(options, many=True)
    return Response(seralizer.data)


# 단일 예금 상품 조회
@api_view(['GET'])
def get_deposit_product_detail(request, fin_prdt_cd):
    product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = DepositProductSerializer(product)
    return Response(seralizer.data)


# 단일 예금 상품의 옵션 조회
@api_view(['GET'])
def get_deposit_product_options(request, fin_prdt_cd):
    optionlist = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(optionlist, many=True)
    return Response(serializer.data)


# 전체 상품 검색 [예금]
@api_view(['GET'])
def search_deposit_products(request, fin_co_no, save_trm):
    
    # 예금 목록 불러오기
    if fin_co_no != '전체':
        products = DepositProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = DepositProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if save_trm:
            option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, save_trm=save_trm)
        else:
            option_list = DepositOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = DepositOptionSerializer(option_list, many=True)
        serializer2 = DepositProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 모든 적금 상품 조회
@api_view(['GET'])
def get_saving_products(request):
    # 예금 목록 불러오기
    products = SavingProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = SavingOptionSerializer(option_list, many=True)
        serializer2 = SavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 모든 적금 옵션 조회
@api_view(['GET'])
def get_saving_options(request):
    # 예금 목록 불러오기
    options = SavingOption.objects.all()
    seralizer = SavingOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 적금 상품 조회
@api_view(['GET'])
def get_saving_product_detail(request, fin_prdt_cd):
    product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = SavingProductSerializer(product)
    return Response(seralizer.data)

# 단일 적금 상품 옵션 조회
@api_view(['GET'])
def get_saving_product_options(request, fin_prdt_cd):
    optionlist = SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 적금 상품 검색
@api_view(['GET'])
def search_saving_products(request, fin_co_no, save_trm):
    
    # 예금 목록 불러오기
    if fin_co_no != '전체':
        products = SavingProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = SavingProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if save_trm:
            option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, save_trm=save_trm)
        else:
            option_list = SavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = SavingOptionSerializer(option_list, many=True)
        serializer2 = SavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 연금저축
# 전체 상품 조회 [연금저춝]
@api_view(['GET'])
def get_annuity_saving_products(request):
    products = AnnuitySavingProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        serializer2 = AnnuitySavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 모든 옵션 조회
@api_view(['GET'])
def get_annuity_saving_options(request):
    # 예금 목록 불러오기
    options = AnnuitySavingOption.objects.all()
    seralizer = AnnuitySavingOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_annuity_saving_product_detail(request, fin_prdt_cd):
    product = AnnuitySavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = AnnuitySavingProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_annuity_saving_product_options(request, fin_prdt_cd):
    optionlist = AnnuitySavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = AnnuitySavingOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_annuity_saving_products(request, fin_co_no, paym_prd):
    
    if fin_co_no != '전체':
        products = AnnuitySavingProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = AnnuitySavingProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if paym_prd:
            option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, paym_prd=paym_prd)
        else:
            option_list = AnnuitySavingOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = AnnuitySavingOptionSerializer(option_list, many=True)
        serializer2 = AnnuitySavingProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 주택담보 대출
# 전체 상품 조회 [주택담보대출]
@api_view(['GET'])
def get_mortgage_loan_products(request):
    products = MortgageLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_mortgage_loan_options(request):
    options = MortgageLoanOption.objects.all()
    seralizer = MortgageLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_mortgage_loan_product_detail(request, fin_prdt_cd):
    product = MortgageLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = MortgageLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_mortgage_loan_product_options(request, fin_prdt_cd):
    optionlist = MortgageLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = MortgageLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_mortgage_loan_products(request, fin_co_no, mrtg_type, rpay_type, lend_rate_type):
    if fin_co_no != '전체':
        products = MortgageLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = MortgageLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        option_list = MortgageLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, mrtg_type=mrtg_type, rpay_type=rpay_type, lend_rate_type=lend_rate_type)

        serializer1 = MortgageLoanOptionSerializer(option_list, many=True)
        serializer2 = MortgageLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 전세자금 대출
# 전체 상품 조회 [전세자금대출]
@api_view(['GET'])
def get_rent_house_loan_products(request):
    products = RentHouseLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_rent_house_loan_options(request):
    options = RentHouseLoanOption.objects.all()
    seralizer = RentHouseLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_rent_house_loan_product_detail(request, fin_prdt_cd):
    product = RentHouseLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = RentHouseLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_rent_house_loan_product_options(request, fin_prdt_cd):
    optionlist = RentHouseLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = RentHouseLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_rent_house_loan_products(request, fin_co_no, rpay_type, lend_rate_type):
    if fin_co_no != '전체':
        products = RentHouseLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = RentHouseLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        option_list = RentHouseLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, rpay_type=rpay_type, lend_rate_type=lend_rate_type)
        
        serializer1 = RentHouseLoanOptionSerializer(option_list, many=True)
        serializer2 = RentHouseLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)


# 신용대출
# 전체 상품 조회 [신용대출]
@api_view(['GET'])
def get_credit_loan_products(request):
    products = CreditLoanProduct.objects.all()
    products_contain_options = []    
    for product in products:
        option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        products_contain_options.append(serializer)

    return Response(products_contain_options)

# 전체 옵션 조회
@api_view(['GET'])
def get_credit_loan_options(request):
    options = CreditLoanOption.objects.all()
    seralizer = CreditLoanOptionSerializer(options, many=True)
    return Response(seralizer.data)

# 단일 상품 조회
@api_view(['GET'])
def get_credit_loan_product_detail(request, fin_prdt_cd):
    product = CreditLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
    seralizer = CreditLoanProductSerializer(product)
    return Response(seralizer.data)

# 단일 상품의 옵션 조회
@api_view(['GET'])
def get_credit_loan_product_options(request, fin_prdt_cd):
    optionlist = CreditLoanOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = CreditLoanOptionSerializer(optionlist, many=True)
    return Response(serializer.data)

# 전체 상품 검색
@api_view(['GET'])
def search_credit_loan_products(request, fin_co_no, crdt_lend_rate_type):
    if fin_co_no != '전체':
        products = CreditLoanProduct.objects.filter(fin_co_no=fin_co_no)
    else:
        products = CreditLoanProduct.objects.all()
        
    filtered_products = []
    
    for product in products:
        # 옵션 목록 불러오기
        if crdt_lend_rate_type:
            option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd, crdt_lend_rate_type=crdt_lend_rate_type)
        else:
            option_list = CreditLoanOption.objects.filter(fin_prdt_cd=product.fin_prdt_cd)
        serializer1 = CreditLoanOptionSerializer(option_list, many=True)
        serializer2 = CreditLoanProductSerializer(product)
        serializer = {
            'product':serializer2.data,
            'options':serializer1.data
        }
        filtered_products.append(serializer)

    return Response(filtered_products)




# 전체 상품 검색 [예금]
@api_view(['POST'])
def filter_user(request):  
    print(request.POST)  
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    SAVING_TYPE_CHOICES = [
        ('thrifty', '알뜰형'),
        ('challenging', '도전형'),
        ('diligent', '성실형'),
    ]

    # 필터 인자
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    address = request.POST.get('address')
    salary = request.POST.get('salary')
    money = request.POST.get('money')
    target_asset = request.POST.get('target_asset')
    saving_type = request.POST.get('saving_type')
    favorite_company = request.POST.get('favorite_company')
    mbti = request.POST.get('mbti')
    print(gender, age, address, salary, money, target_asset, saving_type, favorite_company, mbti)

    # 필터링
    filtered_users = User.objects.all()
    if gender:
        filtered_users = filtered_users.filter(gender=gender)
    if age:
        filtered_users = filtered_users.filter(age=int(age))
    if address:
        filtered_users = filtered_users.filter(address=address)
    if salary:
        filtered_users = filtered_users.filter(salary=int(salary))
    if money:
        filtered_users = filtered_users.filter(money=int(money))
    if target_asset:
        filtered_users = filtered_users.filter(target_asset=int(target_asset))
    if saving_type:
        filtered_users = filtered_users.filter(saving_type=saving_type)
    if favorite_company:
        filtered_users = filtered_users.filter(favorite_company=favorite_company)
    if mbti:
        filtered_users = filtered_users.filter(mbti=mbti)

    # 필터링된 유저들이 가입한 상품
    products = {}
    
    for user in filtered_users:
        financial_products = user.financial_products.split(',')
        for product in financial_products:
            if product:
                products.setdefault(product, 0)
                products[product] += 1

    print('상품', products)
    sorted_products = dict(sorted(products.items(), key=lambda item: item[1], reverse=True))
    print(sorted_products)
    return Response(sorted_products)
