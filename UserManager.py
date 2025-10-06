# UserManager.py
import json
import os
from pathlib import Path

class UserManager:
    """
    用户管理类：负责用户的注册、登录和数据存储
    """
    
    def __init__(self, data_dir="data"):
        """
        初始化用户管理器
        data_dir: 数据存储目录
        """
        # 创建数据目录
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)  # 如果目录不存在就创建
        
        # 用户数据文件路径
        self.users_file = self.data_dir / "users.json"
        
        # 加载现有用户数据
        self.users = self._load_users()
    
    def _load_users(self):
        """
        从JSON文件加载用户数据
        如果文件不存在或格式错误，返回空字典
        """
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    print(f"✅ 成功加载用户数据，共有 {len(users_data)} 个用户")
                    return users_data
            else:
                print("📝 用户数据文件不存在，将创建新文件")
                return {}
        except (json.JSONDecodeError, Exception) as e:
            print(f"❌ 加载用户数据时出错: {e}")
            return {}
    
    def _save_users(self):
        """
        将用户数据保存到JSON文件
        """
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            print("✅ 用户数据保存成功")
            return True
        except Exception as e:
            print(f"❌ 保存用户数据时出错: {e}")
            return False
    
    def register(self, username, password):
        """
        用户注册功能
        返回: (成功与否, 提示信息)
        """
        # 输入验证
        if not username or not password:
            return False, "❌ 用户名和密码不能为空"
        
        if len(username) < 3:
            return False, "❌ 用户名至少需要3个字符"
        
        if len(password) < 4:
            return False, "❌ 密码至少需要4个字符"
        
        # 检查用户名是否已存在
        if username in self.users:
            return False, "❌ 用户名已存在，请选择其他用户名"
        
        # 注册新用户
        self.users[username] = password
        
        # 保存数据
        if self._save_users():
            return True, f"✅ 注册成功！欢迎 {username} 加入中考加油大家庭！"
        else:
            # 如果保存失败，回滚用户数据
            if username in self.users:
                del self.users[username]
            return False, "❌ 注册失败，请稍后重试"
    
    def login(self, username, password):
        """
        用户登录功能
        返回: (成功与否, 提示信息)
        """
        # 输入验证
        if not username or not password:
            return False, "❌ 请输入用户名和密码"
        
        # 检查用户名是否存在
        if username not in self.users:
            return False, "❌ 用户名不存在，请先注册"
        
        # 验证密码
        if self.users[username] != password:
            return False, "❌ 密码错误，请重试"
        
        return True, f"✅ 登录成功！欢迎回来，{username}！"
    
    def logout(self, username):
        """
        用户登出功能
        """
        print(f"👋 用户 {username} 已登出")
        return True, f"✅ 用户 {username} 已成功登出"
    
    def get_all_users(self):
        """
        获取所有注册用户
        """
        return list(self.users.keys())
    
    def get_user_count(self):
        """
        获取当前用户数量
        这个方法是为了兼容Login模块而添加的
        """
        return len(self.users)
    
    def user_exists(self, username):
        """
        检查用户是否存在
        这个方法是为了兼容Login模块而添加的
        """
        return username in self.users