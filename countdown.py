# Countdown.py
import datetime

class Countdown:
    """
    中考倒计时功能模块
    计算距离中考的剩余天数
    支持模块化系统
    """
    
    def __init__(self, main_manager=None):
        """
        初始化倒计时模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取其他管理器
        """
        self.main_manager = main_manager
        # 默认中考日期设置为2025年6月15日
        self.exam_year = 2025
        self.exam_month = 6
        self.exam_day = 15
    
    def set_exam_date(self, year, month, day):
        """
        设置中考日期
        """
        try:
            # 验证日期有效性
            datetime.datetime(year, month, day)
            self.exam_year = year
            self.exam_month = month
            self.exam_day = day
            return True, f"中考日期已设置为：{year}年{month}月{day}日"
        except ValueError as e:
            return False, f"无效的日期：{e}"
    
    def get_exam_date(self):
        """
        获取中考日期
        """
        return {
            'year': self.exam_year,
            'month': self.exam_month,
            'day': self.exam_day
        }
    
    def get_days_left(self):
        """
        计算距离中考的剩余天数
        返回: 剩余天数
        """
        try:
            # 获取当前日期
            today = datetime.datetime.now()
            
            # 构建中考日期
            exam_date = datetime.datetime(self.exam_year, self.exam_month, self.exam_day)
            
            # 计算剩余天数
            days_left = (exam_date - today).days
            
            # 如果已经过了中考日期，则返回0
            if days_left < 0:
                days_left = 0
                
            return days_left
        except Exception as e:
            print(f"计算剩余天数时发生错误：{e}")
            return 0
    
    def get_countdown_message(self):
        """
        获取倒计时消息
        """
        days_left = self.get_days_left()
        
        if days_left == 0:
            return "🎓 中考已经开始！祝你考试顺利！"
        elif days_left == 1:
            return "⏰ 距离中考还有1天！最后冲刺！"
        elif days_left <= 7:
            return f"🔥 距离中考还有{days_left}天！加油！"
        elif days_left <= 30:
            return f"💪 距离中考还有{days_left}天！坚持就是胜利！"
        else:
            return f"📅 距离中考还有{days_left}天！合理规划时间！"

# 为保持向后兼容性，保留原有的函数接口
exam_date = Countdown()

def get_days_left():
    """
    计算并返回距离中考还剩多少天。
    保持向后兼容性的函数接口
    """
    return exam_date.get_days_left()

# 测试代码
if __name__ == '__main__':
    countdown = Countdown()
    days = countdown.get_days_left()
    print(f"距离中考还有: {days} 天")
    print(countdown.get_countdown_message())
