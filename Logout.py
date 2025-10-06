# Logout.py

class Logout:
    """
    登出功能模块
    处理用户登出和会话清理
    支持模块化系统
    """
    
    def __init__(self, main_manager=None):
        """
        初始化登出模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取其他管理器
        """
        self.main_manager = main_manager
        self.logged_out_users = []
    
    def logout_user(self, username):
        """
        用户登出处理
        返回: (成功与否, 提示信息)
        """
        if not username:
            return False, "❌ 用户名不能为空"
        
        # 记录登出用户
        if username not in self.logged_out_users:
            self.logged_out_users.append(username)
        
        print(f"👋 用户 {username} 已登出系统")
        return True, f"✅ 用户 {username} 已成功登出"
    
    def is_user_logged_out(self, username):
        """
        检查用户是否已登出
        """
        return username in self.logged_out_users
    
    def clear_logout_history(self):
        """
        清空登出历史记录
        """
        self.logged_out_users.clear()
        return True, "✅ 登出历史记录已清空"
    
    def get_logout_history(self):
        """
        获取登出历史记录
        """
        return self.logged_out_users.copy()