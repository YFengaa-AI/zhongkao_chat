# MainManager.py
import os
import sys
from UserManager import UserManager
from ChatManager import ChatManager
from FriendManager import FriendManager
from GUIManager import GUIManager
from login import Login
from Logout import Logout
from Register import Register
from chat import Chat
from friend import Friend
from Group import Group
from countdown import Countdown
from encouragement import Encouragement

class MainManager:
    """
    主管理器
    作为整个应用的中央协调器，管理所有功能模块
    """
    
    def __init__(self, data_dir="data"):
        """
        初始化主管理器
        """
        self.data_dir = data_dir
        
        # 确保数据目录存在
        self._ensure_data_dir()
        
        # 初始化各个管理器
        self.init_managers()
        
        print("🚀 中考加油聊天室 - 模块系统初始化完成")
    
    def _ensure_data_dir(self):
        """
        确保数据目录存在
        """
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
                print(f"✅ 创建数据目录: {self.data_dir}")
            except Exception as e:
                print(f"❌ 创建数据目录失败: {e}")
                sys.exit(1)
    
    def init_managers(self):
        """
        初始化所有功能管理器
        """
        # 核心管理器
        self.user_manager = UserManager(self.data_dir)
        self.chat_manager = ChatManager(self.data_dir)
        self.friend_manager = FriendManager(self.data_dir)
        self.gui_manager = GUIManager()
        
        # 初始化所有功能模块，确保顺序正确
        self.register = Register(self)
        self.chat = Chat(self)
        self.friend = Friend(self)
        self.group = Group(self)
        
        # 添加倒计时和鼓励模块
        self.countdown = Countdown(self)
        self.encouragement = Encouragement(self)
        
        # 最后初始化login和logout，避免循环依赖
        try:
            self.login = Login(self)
            print("✅ login模块初始化成功")
        except Exception as e:
            print(f"❌ login模块初始化失败: {e}")
            self.login = None
        
        try:
            self.logout = Logout(self)
            print("✅ logout模块初始化成功")
        except Exception as e:
            print(f"❌ logout模块初始化失败: {e}")
            self.logout = None
        
        # 添加倒计时和鼓励模块
        self.countdown = Countdown(self)
        self.encouragement = Encouragement(self)
    
    def start_application(self):
        """
        启动应用程序
        """
        try:
            # 尝试启动增强版登录界面
            from login_gui_enhanced import start_enhanced_login
            print("🚀 启动增强版系统...")
            start_enhanced_login(self)
        except ImportError as e:
            print(f"⚠️ 增强版启动失败: {e}")
            
            # 尝试启动基础版登录界面
            try:
                from login_gui import start_login_gui
                print("🔄 启动基础版系统...")
                start_login_gui()
            except ImportError as e2:
                print(f"❌ 基础版也启动失败: {e2}")
                input("按回车键退出...")
                sys.exit(1)
    
    def get_manager(self, manager_name):
        """
        获取指定的管理器实例
        manager_name: 管理器名称，如 'user', 'chat', 'friend' 等
        """
        # 使用字典推导式和hasattr来安全地获取管理器，避免属性未初始化时的错误
        managers = {
            'user': self.user_manager if hasattr(self, 'user_manager') else None,
            'chat': self.chat_manager if hasattr(self, 'chat_manager') else None,
            'friend': self.friend_manager if hasattr(self, 'friend_manager') else None,
            'gui': self.gui_manager if hasattr(self, 'gui_manager') else None,
            'login': self.login if hasattr(self, 'login') else None,
            'logout': self.logout if hasattr(self, 'logout') else None,
            'register': self.register if hasattr(self, 'register') else None,
            'chat_module': self.chat if hasattr(self, 'chat') else None,
            'friend_module': self.friend if hasattr(self, 'friend') else None,
            'group_module': self.group if hasattr(self, 'group') else None,
            'countdown': self.countdown if hasattr(self, 'countdown') else None,
            'encouragement': self.encouragement if hasattr(self, 'encouragement') else None
        }
        
        result = managers.get(manager_name.lower())
        if result is None:
            print(f"⚠️ 警告：未找到管理器 '{manager_name}'")
        return result
    
    def shutdown(self):
        """
        关闭应用程序
        """
        print("👋 感谢使用中考加油聊天室，再见！")
        sys.exit(0)

# 启动应用的快捷方式
if __name__ == "__main__":
    main_manager = MainManager()
    main_manager.start_application()