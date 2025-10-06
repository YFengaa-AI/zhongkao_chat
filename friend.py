# Friend.py
import json
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

class Friend:
    """
    好友功能模块
    处理好友添加、删除和好友关系管理
    支持模块化系统和独立运行模式
    """
    
    def __init__(self, main_manager=None, data_dir="data"):
        """
        初始化好友模块
        
        Args:
            main_manager: 主管理器实例，用于模块化系统
            data_dir: 数据存储目录
        """
        self.main_manager = main_manager
        
        # 根据运行模式设置数据目录
        if main_manager is not None and hasattr(main_manager, 'data_dir'):
            self.data_dir = Path(main_manager.data_dir)
        else:
            self.data_dir = Path(data_dir)
        
        # 确保数据目录存在
        self.data_dir.mkdir(exist_ok=True)
        
        # 好友数据文件
        self.friends_file = self.data_dir / "friends.json"
        
        # 加载数据
        self.friends_data = self._load_friends_data()
        
        print("✅ 好友管理系统初始化完成")
    
    def _load_friends_data(self) -> Dict:
        """
        加载好友关系数据
        """
        try:
            if self.friends_file.exists():
                with open(self.friends_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ 加载好友数据，共 {len(data)} 个用户的好友关系")
                    return data
            else:
                print("📝 好友数据文件不存在，创建新文件")
                return {}
        except Exception as e:
            print(f"❌ 加载好友数据失败: {e}")
            return {}
    
    def _save_friends_data(self):
        """
        保存好友数据
        """
        try:
            with open(self.friends_file, 'w', encoding='utf-8') as f:
                json.dump(self.friends_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存好友数据失败: {e}")
            return False
    
    def add_friend(self, user1: str, user2: str) -> (bool, str):
        """
        添加好友关系（双向）
        """
        if user1 == user2:
            return False, "❌ 不能添加自己为好友"
        
        # 初始化用户的好友列表
        if user1 not in self.friends_data:
            self.friends_data[user1] = []
        if user2 not in self.friends_data:
            self.friends_data[user2] = []
        
        # 检查是否已经是好友
        if user2 in self.friends_data[user1]:
            return False, f"❌ 你们已经是好友了"
        
        # 建立好友关系
        self.friends_data[user1].append(user2)
        self.friends_data[user2].append(user1)
        
        # 保存数据
        if self._save_friends_data():
            return True, f"✅ 成功添加好友 {user2}"
        else:
            # 回滚操作
            if user2 in self.friends_data[user1]:
                self.friends_data[user1].remove(user2)
            if user1 in self.friends_data[user2]:
                self.friends_data[user2].remove(user1)
            return False, "❌ 添加好友失败，请稍后重试"
    
    def remove_friend(self, user1: str, user2: str) -> (bool, str):
        """
        移除好友关系
        """
        # 检查用户数据结构
        if user1 not in self.friends_data or user2 not in self.friends_data:
            return False, "❌ 好友关系不存在"
        
        # 检查是否是好友
        if user2 not in self.friends_data[user1]:
            return False, "❌ 你们不是好友"
        
        # 解除好友关系
        self.friends_data[user1].remove(user2)
        self.friends_data[user2].remove(user1)
        
        # 清理空列表
        if not self.friends_data[user1]:
            del self.friends_data[user1]
        if not self.friends_data[user2]:
            del self.friends_data[user2]
        
        # 保存数据
        if self._save_friends_data():
            return True, f"✅ 已解除与 {user2} 的好友关系"
        else:
            # 回滚操作
            if user1 not in self.friends_data:
                self.friends_data[user1] = []
            if user2 not in self.friends_data:
                self.friends_data[user2] = []
            self.friends_data[user1].append(user2)
            self.friends_data[user2].append(user1)
            return False, "❌ 移除好友失败，请稍后重试"
    
    def get_user_friends(self, user_id: str) -> List[str]:
        """
        获取用户的所有好友
        """
        if user_id not in self.friends_data:
            return []
        return self.friends_data[user_id]
    
    # 兼容旧接口
    get_friend_list = get_user_friends
    
    def is_friends_with(self, user_id: str, other_user_id: str) -> bool:
        """
        检查两个用户是否是好友
        """
        friends = self.get_user_friends(user_id)
        return other_user_id in friends
    
    def get_personal_chat_id(self, user1: str, user2: str) -> str:
        """
        生成个人聊天的会话ID
        规则：按字母顺序排序用户名，用_PM_连接
        """
        sorted_users = sorted([user1, user2])
        return f"PM_{sorted_users[0]}_{sorted_users[1]}"
    
    def is_personal_chat_id(self, chat_id: str) -> bool:
        """
        检查是否为个人聊天ID
        """
        return chat_id.startswith("PM_")
    
    def get_users_from_personal_chat(self, chat_id: str) -> List[str]:
        """
        从个人聊天ID解析出两个用户名
        """
        if not self.is_personal_chat_id(chat_id):
            return []
        
        try:
            parts = chat_id.split("_")
            if len(parts) == 3:
                return [parts[1], parts[2]]
        except:
            pass
        return []
    
    def _get_current_time(self) -> str:
        """
        获取当前时间字符串
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def search_users(self, current_user: str, keyword: str) -> List[str]:
        """
        搜索用户
        """
        # 这里我们模拟一个用户列表
        all_users = set()
        
        # 添加当前所有好友
        for user, friends in self.friends_data.items():
            all_users.add(user)
            all_users.update(friends)
        
        # 如果在模块化系统中，还可以通过用户管理器获取更多用户
        if self.main_manager:
            user_manager = self.main_manager.get_manager('user')
            if user_manager:
                # 尝试获取所有用户（如果UserManager支持）
                if hasattr(user_manager, 'get_all_users'):
                    all_users.update(user_manager.get_all_users())
        
        # 移除当前用户自己
        all_users.discard(current_user)
        
        # 根据关键词过滤
        if keyword.strip():
            filtered_users = [user for user in all_users if keyword.lower() in user.lower()]
        else:
            filtered_users = list(all_users)
        
        return sorted(filtered_users)
    
    # 群组相关功能委托给Group模块
    def get_broadcast_room_id(self) -> str:
        """
        获取广播室ID
        通过模块化系统调用Group模块
        """
        if self.main_manager:
            group_manager = self.main_manager.get_manager('group_module')
            if group_manager and hasattr(group_manager, 'get_broadcast_room_id'):
                return group_manager.get_broadcast_room_id()
        # 默认值
        return "BROADCAST_ROOM"

# 测试代码
def test_friend_system():
    """
    测试好友系统功能
    """
    print("🧪 测试好友系统...")
    
    # 创建好友管理器
    friend_manager = Friend()
    
    # 测试添加好友
    print("\n1. 测试添加好友:")
    success, message = friend_manager.add_friend("小明", "小红")
    print(f"   小明添加小红: {success} - {message}")
    
    success, message = friend_manager.add_friend("小红", "小刚")
    print(f"   小红添加小刚: {success} - {message}")
    
    # 测试获取好友列表
    print("\n2. 测试好友列表:")
    xiaoming_friends = friend_manager.get_friend_list("小明")
    print(f"   小明的好友: {xiaoming_friends}")
    
    xiaohong_friends = friend_manager.get_friend_list("小红")
    print(f"   小红的好友: {xiaohong_friends}")
    
    # 测试个人聊天ID生成
    print("\n3. 测试个人聊天ID:")
    chat_id = friend_manager.get_personal_chat_id("小明", "小红")
    print(f"   小明和小红的聊天ID: {chat_id}")
    
    users = friend_manager.get_users_from_personal_chat(chat_id)
    print(f"   从聊天ID解析用户: {users}")
    
    # 测试搜索用户
    print("\n4. 测试搜索用户:")
    search_results = friend_manager.search_users("小明", "小")
    print(f"   搜索'小': {search_results}")
    
    # 测试移除好友
    print("\n5. 测试移除好友:")
    success, message = friend_manager.remove_friend("小明", "小红")
    print(f"   小明移除小红: {success} - {message}")
    
    print("\n✅ 好友系统测试完成")

if __name__ == '__main__':
    test_friend_system()