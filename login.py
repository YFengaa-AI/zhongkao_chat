# Login.py
class Login:
    """
    登录功能模块
    处理用户登录验证和会话管理
    支持模块化系统和独立运行两种模式
    """
    
    def __init__(self, main_manager=None):
        """
        初始化登录模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取其他管理器
        """
        self.main_manager = main_manager
        self.current_user = None
        self.user_manager = None
        
        # 如果在模块化系统中运行，从main_manager获取user_manager
        if main_manager is not None:
            self.user_manager = main_manager.get_manager('user')
    
    def login_user(self, username, password):
        """
        用户登录验证
        返回: (成功与否, 提示信息)
        """
        if not self.user_manager:
            return False, "❌ 用户管理器未初始化"
        
        # 调用用户管理器进行登录验证
        success, message = self.user_manager.login(username, password)
        
        # 如果登录成功，记录当前用户
        if success:
            self.current_user = username
            print(f"👤 用户 {username} 登录成功")
        
        return success, message
    
    def get_current_user(self):
        """
        获取当前登录用户
        """
        return self.current_user
    
    def is_logged_in(self):
        """
        检查是否有用户登录
        """
        return self.current_user is not None
    
    def logout(self, username=None):
        """
        用户登出功能
        
        参数:
        - username: 可选，指定要登出的用户名
        
        返回: (成功与否, 提示信息)
        """
        # 如果指定了用户名，则检查是否是当前登录用户
        if username:
            if username == self.current_user:
                print(f"👋 用户 {username} 已登出")
                self.current_user = None
                return True, f"✅ 用户 {username} 注销成功"
            else:
                return False, "❌ 无效的用户名或未登录"
        
        # 如果没有指定用户名，则登出当前用户
        if self.current_user:
            print(f"👋 用户 {self.current_user} 已登出")
            self.current_user = None
            return True, "✅ 成功登出"
        
        return False, "❌ 没有用户登录"
    
    def get_user_count(self):
        """
        获取当前用户数量
        """
        if not self.user_manager:
            return 0
        
        return self.user_manager.get_user_count()
    
    def user_exists(self, username):
        """
        检查用户是否存在
        """
        if not self.user_manager:
            return False
        
        return self.user_manager.user_exists(username)

# 需要在模块外导入UserManager以支持独立测试
from UserManager import UserManager

def test_login_system():
    """
    登录系统的测试函数
    """
    print("🧪 开始测试登录系统...")
    print("=" * 40)
    
    # 创建用户管理器实例（用于测试）
    user_manager = UserManager()
    
    # 测试注册
    test_cases = [
        ("小明", "123456"),
        ("小红", "abc123"),
        ("", "password"),  # 空用户名
        ("小李", ""),      # 空密码
        ("小明", "another")  # 重复用户名
    ]
    
    for username, password in test_cases:
        success, message = user_manager.register(username, password)
        print(f"注册测试 - 用户名:'{username}': {message}")
    
    print("-" * 40)
    
    # 创建登录模块实例（独立模式，没有main_manager）
    login_module = Login()
    # 手动设置user_manager用于测试
    login_module.user_manager = user_manager
    
    # 测试登录
    login_cases = [
        ("小明", "123456"),      # 正确登录
        ("小明", "wrong"),       # 错误密码
        ("不存在用户", "123"),    # 不存在的用户
        ("小红", "abc123")       # 正确登录
    ]
    
    for username, password in login_cases:
        success, message = login_module.login_user(username, password)
        print(f"登录测试 - 用户名:'{username}': {message}")
    
    # 测试登出功能
    print("-" * 40)
    if login_module.is_logged_in():
        success, message = login_module.logout()
        print(f"登出测试: {message}")
    
    print("=" * 40)
    print(f"📊 当前用户总数: {login_module.get_user_count()}")

# 简单的命令行交互界面
def command_line_interface():
    """
    命令行交互界面，方便测试
    """
    # 创建用户管理器实例
    user_manager = UserManager()
    
    # 创建登录模块实例
    login_module = Login()
    login_module.user_manager = user_manager
    
    while True:
        print("\n🎯 中考加油 - 用户系统")
        print("1. 注册")
        print("2. 登录") 
        print("3. 查看用户数")
        print("4. 退出")
        
        choice = input("请选择操作 (1-4): ").strip()
        
        if choice == "1":
            username = input("请输入用户名: ").strip()
            password = input("请输入密码: ").strip()
            success, message = user_manager.register(username, password)
            print(message)
            
        elif choice == "2":
            username = input("请输入用户名: ").strip()
            password = input("请输入密码: ").strip()
            success, message = login_module.login_user(username, password)
            print(message)
            
        elif choice == "3":
            count = login_module.get_user_count()
            print(f"📊 当前共有 {count} 个注册用户")
            
        elif choice == "4":
            print("👋 再见！中考加油！")
            break
            
        else:
            print("❌ 请输入有效的选项 (1-4)")

if __name__ == '__main__':
    print("🚀 启动登录系统测试...")
    
    # 运行自动化测试
    test_login_system()
    
    print("\n" + "="*50)
    print("🎮 现在进入交互模式，你可以手动测试注册和登录功能")
    print("="*50)
    
    # 启动命令行交互界面
    command_line_interface()