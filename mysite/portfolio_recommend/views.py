from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

# Create your views here.
def index(request):
    return render(request,'portfolio_recommend/portfolio_optimization.html')

# 風險分類函式
def determine_risk_category(age, experience, tolerance, return_expectation):
    score = 0
    # 年齡區間評分
    if age == "20-30 歲":
        score += 4
    elif age == "31-40 歲":
        score += 3
    elif age == "41-50 歲":
        score += 2
    elif age == "51 歲以上":
        score += 1
    # 投資經驗評分
    if experience == "5+":
        score += 5
    elif experience == "3-5":
        score += 4
    elif experience == "1-3":
        score += 3
    elif experience == "1":
        score += 2
    elif experience == "none":
        score += 1
    # 最大虧損比例評分
    if tolerance == "25+":
        score += 5
    elif tolerance == "20":
        score += 4
    elif tolerance == "15":
        score += 3
    elif tolerance == "10":
        score += 2
    elif tolerance == "5":
        score += 1
    # 期望年化投資報酬率評分
    try:
        if not return_expectation:  # 檢查空值
            return_expectation = 0
        return_expectation = float(return_expectation)
        if return_expectation >= 20:
            score += 5
        elif return_expectation >= 15:
            score += 4
        elif return_expectation >= 10:
            score += 3
        elif return_expectation >= 5:
            score += 2
        else:
            score += 1
    except ValueError:
        return "Invalid input for return expectation"
    # 分數對應風險屬性
    if score >= 16:
        return "高風險"
    elif score >= 12:
        return "中高風險"
    elif score >= 8:
        return "中等風險"
    elif score >= 4:
        return "中低風險"
    else:
        return "低風險"


# 處理提交的問卷資料
def submit_questionnaire(request):
    if request.method == "POST":
        # 打印 POST 數據以調試
        print(request.POST)

        age = request.POST.get("age")
        experience = request.POST.get("investmentExperience")
        tolerance = request.POST.get("riskTolerance")
        return_expectation = request.POST.get("expectedReturn")

        risk_category = determine_risk_category(age, experience, tolerance, return_expectation)
        return render(request, 'portfolio_recommend/result.html', {'risk_category': risk_category})
    return HttpResponse("僅接受 POST 請求")
