# Group.py
import json
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

class Group:
    """
    群组功能模块
    处理群组创建、成员管理和群组聊天功能
    支持模块化系统和独立运行模式
    """
    
    def __init__(self, main_manager=None, data_dir="data"):
        """
        初始化群组模块
        
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
        
        # 群组数据文件
        self.groups_file = self.data_dir / "groups.json"
        
        # 加载数据
        self.groups_data = self._load_groups_data()
        
        # 固定会话ID
        self.BROADCAST_ROOM_ID = "BROADCAST_ROOM"
        
        print("✅ 群组管理系统初始化完成")
    
    def _load_groups_data(self) -> Dict:
        """
        加载群组数据
        """
        try:
            if self.groups_file.exists():
                with open(self.groups_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ 加载群组数据，共 {len(data)} 个群组")
                    return data
            else:
                print("📝 群组数据文件不存在，创建新文件")
                # 创建默认的广播室
                default_groups = {
                    self.BROADCAST_ROOM_ID: {
                        "name": "中考加油广播室",
                        "creator": "系统",
                        "members": [],
                        "created_at": "2024-01-01 00:00:00",
                        "type": "broadcast"
                    }
                }
                self._save_groups_data(default_groups)
                return default_groups
        except Exception as e:
            print(f"❌ 加载群组数据失败: {e}")
            return {}
    
    def _save_groups_data(self, data=None):
        """
        保存群组数据
        """
        try:
            if data is None:
                data = self.groups_data
            with open(self.groups_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存群组数据失败: {e}")
            return False
    
    def create_group(self, creator_id, group_name):
        """
        创建群组
        返回: (成功与否, 提示信息, 群组ID)
        """
        if not group_name or len(group_name.strip()) == 0:
            return False, "❌ 群组名称不能为空", ""
        
        # 生成群组ID
        group_id = str(uuid.uuid4())
        
        # 创建群组
        self.groups_data[group_id] = {
            "name": group_name.strip(),
            "creator": creator_id,
            "members": [creator_id],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "group"
        }
        
        # 保存数据
        if self._save_groups_data():
            return True, f"✅ 群组 '{group_name}' 创建成功", group_id
        else:
            # 回滚操作
            del self.groups_data[group_id]
            return False, "❌ 创建群组失败，请稍后重试", ""
    
    def add_group_member(self, group_id, user_id, admin_id):
        """
        添加群组成员
        返回: (成功与否, 提示信息)
        """
        # 检查群组是否存在
        if group_id not in self.groups_data:
            return False, "❌ 群组不存在"
        
        # 检查管理员权限
        if self.groups_data[group_id]["creator"] != admin_id:
            return False, "❌ 只有群主才能添加成员"
        
        # 检查用户是否已经在群里
        if user_id in self.groups_data[group_id]["members"]:
            return False, "❌ 用户已经在群组中"
        
        # 添加成员
        self.groups_data[group_id]["members"].append(user_id)
        
        # 保存数据
        if self._save_groups_data():
            return True, f"✅ 用户 {user_id} 已成功加入群组"
        else:
            # 回滚操作
            self.groups_data[group_id]["members"].remove(user_id)
            return False, "❌ 添加成员失败，请稍后重试"
    
    def remove_group_member(self, group_id, user_id, admin_id):
        """
        移除群组成员
        返回: (成功与否, 提示信息)
        """
        # 检查群组是否存在
        if group_id not in self.groups_data:
            return False, "❌ 群组不存在"
        
        # 检查管理员权限
        if self.groups_data[group_id]["creator"] != admin_id:
            return False, "❌ 只有群主才能移除成员"
        
        # 检查用户是否在群里
        if user_id not in self.groups_data[group_id]["members"]:
            return False, "❌ 用户不在群组中"
        
        # 群主不能移除自己
        if user_id == admin_id:
            return False, "❌ 群主不能移除自己，如需解散群组请使用解散功能"
        
        # 移除成员
        self.groups_data[group_id]["members"].remove(user_id)
        
        # 保存数据
        if self._save_groups_data():
            return True, f"✅ 用户 {user_id} 已被移除出群组"
        else:
            # 回滚操作
            self.groups_data[group_id]["members"].append(user_id)
            return False, "❌ 移除成员失败，请稍后重试"
    
    def get_user_groups(self, user_id):
        """
        获取用户加入的所有群组
        """
        user_groups = {}
        for group_id, group_info in self.groups_data.items():
            if group_id != self.BROADCAST_ROOM_ID and user_id in group_info["members"]:
                user_groups[group_id] = group_info
        return user_groups
    
    def get_group_info(self, group_id):
        """
        获取群组信息
        """
        if group_id in self.groups_data:
            return self.groups_data[group_id]
        return None
    
    def get_broadcast_room_id(self):
        """
        获取广播室ID
        """
        return self.BROADCAST_ROOM_ID
    
    def can_access_conversation(self, user_id, conversation_id):
        """
        检查用户是否有权限访问指定会话
        """
        # 广播室对所有用户开放
        if conversation_id == self.BROADCAST_ROOM_ID:
            return True
        
        # 检查是否是群组成员
        if conversation_id in self.groups_data:
            return user_id in self.groups_data[conversation_id]["members"]
        
        # 如果在模块化系统中，还需要检查好友关系
        if self.main_manager:
            friend_manager = self.main_manager.get_manager('friend')
            if friend_manager:
                # 检查好友关系
                friends_data = getattr(friend_manager, 'friends_data', {})
                if user_id in friends_data and conversation_id in friends_data[user_id]:
                    return True
                if conversation_id in friends_data and user_id in friends_data[conversation_id]:
                    return True
        
        return False
    
    def get_conversation_name(self, conversation_id):
        """
        获取会话名称
        """
        # 检查是否是广播室
        if conversation_id == self.BROADCAST_ROOM_ID:
            return "中考加油广播室"
        
        # 检查是否是群组
        if conversation_id in self.groups_data:
            return self.groups_data[conversation_id]["name"]
        
        # 如果在模块化系统中，尝试通过好友管理器获取用户名称
        if self.main_manager:
            user_manager = self.main_manager.get_manager('user')
            if user_manager:
                user_info = user_manager.get_user_by_id(conversation_id)
                if user_info and 'username' in user_info:
                    return user_info['username']
        
        # 默认为用户ID
        return conversation_id