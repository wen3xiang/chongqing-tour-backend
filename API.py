# api/all_api.py
"""所有场景API - 统一入口"""

from flask import Blueprint, jsonify
from datetime import datetime
from services.crowd_prediction_service import CrowdPredictionService

bp = Blueprint('api', __name__)


# ============================================================
# 场景一：交通拥堵治理
# ============================================================

@bp.route('/api/traffic/analyze', methods=['GET'])
def traffic_analyze():
    """交通实时分析"""
    from services._1traffic_service import TrafficService
    service = TrafficService()
    result = service.get_summary()
    return jsonify({
        'code': 200,
        'data': result,
        'update_time': datetime.now().strftime('%H:%M:%S')
    })


# ============================================================
# 场景二：人流管控（基于真实预测模型）
# ============================================================

@bp.route('/api/visitor/analyze', methods=['GET'])
def visitor_analyze():
    """人流实时分析 - 基于随机森林预测模型"""
    CROWD_DATA_PATH = r'D:\pycharm\backend_traffic\data\chongqing_crowd_2025_sampled.csv'
    MODEL_PATH = r'D:\pycharm\backend_traffic\crowd_model.pkl'
    service = CrowdPredictionService(CROWD_DATA_PATH, MODEL_PATH)
    current_time = datetime.now()

    # 修改：使用 get_all_attractions_summary 方法，预测未来60分钟
    new_result = service.get_all_attractions_summary(current_time, 60)

    # 转换为旧格式（保持前端兼容）
    result = {
        'total_attractions': new_result['total_attractions'],
        'red_alerts': new_result['critical'],
        'yellow_alerts': new_result['warning'],
        'green_alerts': new_result['normal'],
        'base_time': new_result['base_time'],
        'details': new_result['details']
    }

    return jsonify({
        'code': 200,
        'data': result,
        'update_time': current_time.strftime('%H:%M:%S')
    })


# ============================================================
# 场景五：满意度分析
# ============================================================

@bp.route('/api/satisfaction/analyze', methods=['GET'])
def satisfaction_analyze():
    """满意度实时分析"""
    from services._5satisfaction_service import SatisfactionService
    service = SatisfactionService()
    result = service.get_full_analysis(review_count=20)
    return jsonify({
        'code': 200,
        'data': result,
        'update_time': datetime.now().strftime('%H:%M:%S')
    })


# ============================================================
# 大屏综合数据（整合所有场景）
# ============================================================

@bp.route('/api/dashboard/overview', methods=['GET'])
def dashboard_overview():
    """大屏综合数据 - 一次获取所有场景"""

    # 交通
    from services._1traffic_service import TrafficService
    traffic_service = TrafficService()
    traffic_result = traffic_service.get_summary()

    # 人流（使用新预测服务）
    CROWD_DATA_PATH = r'D:\pycharm\backend_traffic\data\chongqing_crowd_2025_sampled.csv'
    MODEL_PATH = r'D:\pycharm\backend_traffic\crowd_model.pkl'
    crowd_service = CrowdPredictionService(CROWD_DATA_PATH, MODEL_PATH)

    # 修改：使用 get_all_attractions_summary 方法
    new_visitor_result = crowd_service.get_all_attractions_summary(datetime.now(), 60)

    # 转换为旧格式
    visitor_result = {
        'total_attractions': new_visitor_result['total_attractions'],
        'red_alerts': new_visitor_result['critical'],
        'yellow_alerts': new_visitor_result['warning'],
        'green_alerts': new_visitor_result['normal'],
        'base_time': new_visitor_result['base_time'],
        'details': new_visitor_result['details']
    }

    # 满意度
    from services._5satisfaction_service import SatisfactionService
    satisfaction_service = SatisfactionService()
    satisfaction_result = satisfaction_service.get_full_analysis(15)

    return jsonify({
        'code': 200,
        'data': {
            'traffic': traffic_result,
            'visitor': visitor_result,
            'satisfaction': satisfaction_result
        },
        'update_time': datetime.now().strftime('%H:%M:%S')
    })