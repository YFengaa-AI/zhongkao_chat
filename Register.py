# Register.py
class Register:
    """
    注册功能模块
    处理新用户注册和账号创建
    支持模块化系统
    """
    
    def __init__(self, main_manager=None):
        """
        初始化注册模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取用户管理器
        """
        self.main_manager = main_manager
        self.user_manager = main_manager.user_manager if main_manager else None
        self.registered_users = []
    
    def register_user(self, username, password):
        """
        用户注册处理
        返回: (成功与否, 提示信息)
        """
        # 检查用户管理器是否存在
        if not self.user_manager:
            return False, "❌ 用户管理器未初始化"
        
        # 调用用户管理器进行注册
        success, message = self.user_manager.register(username, password)
        
        # 如果注册成功，记录已注册用户
        if success:
            if username not in self.registered_users:
                self.registered_users.append(username)
            print(f"✨ 新用户 {username} 注册成功")
        
        return success, message
    
    def validate_username(self, username):
        """
        验证用户名格式
        返回: (是否有效, 提示信息)
        """
        # 检查用户管理器是否存在
        if not self.user_manager:
            return False, "❌ 用户管理器未初始化"
            
        if not username:
            return False, "❌ 用户名不能为空"
        
        if len(username) < 3:
            return False, "❌ 用户名至少需要3个字符"
        
        # 检查用户名是否已存在
        if username in self.user_manager.get_all_users():
            return False, "❌ 用户名已存在，请选择其他用户名"
        
        return True, "✅ 用户名可用"
    
    def validate_password(self, password):
        """
        验证密码格式
        返回: (是否有效, 提示信息)
        """
        if not password:
            return False, "❌ 密码不能为空"
        
        if len(password) < 4:
            return False, "❌ 密码至少需要4个字符"
        
        return True, "✅ 密码符合要求"