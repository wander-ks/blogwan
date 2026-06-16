from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from datetime import timedelta
from points.services import update_points
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from points.models import SignInRecord, UserPoints

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def daily_sign(request):
    user = request.user
    today = timezone.now().date()
    if SignInRecord.objects.filter(user=user, sign_date=today).exists():
        return Response({'error': '今日已签到'}, status=status.HTTP_400_BAD_REQUEST)
    update_points(user, 1, 'sign_in', description=f'{today} 签到')
    current_month = today.strftime('%Y-%m')
    SignInRecord.objects.create(user=user, sign_date=today, month=current_month, points_gained=1)

    month_sign_count = SignInRecord.objects.filter(user=user, month=current_month).count()
    import calendar
    last_day = calendar.monthrange(today.year, today.month)[1]
    if month_sign_count == last_day:
        update_points(user, 10, 'sign_bonus', description=f'{current_month} 全勤奖励')
        return Response({'message': '签到成功，获得1积分，本月全勤额外获得10积分！'})
    return Response({'message': '签到成功，获得1积分'})



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_points(request):
    user = request.user
    points, _ = UserPoints.objects.get_or_create(user=user)
    today = timezone.now().date()
    signed_today = SignInRecord.objects.filter(user=user, sign_date=today).exists()
    return Response({
        'balance': points.balance,
        'total_earned': points.total_earned,
        'signed_today': signed_today
    })