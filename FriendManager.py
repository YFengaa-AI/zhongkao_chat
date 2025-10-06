# FriendManager.py
import json
import os
import uuid
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime

class FriendManager:
    """
    好友和群组管理系统
    管理用户的好友关系、群组创建和成员管理
    """
    
    def __init__(self, data_dir="data"):
        """
        初始化好友管理器
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 好友数据文件
        self.friends_file = self.data_dir / "friends.json"
        
        # 群组数据文件
        self.groups_file = self.data_dir / "groups.json"
        
        # 先定义固定会话ID，确保_load_groups_data能访问到
        self.BROADCAST_ROOM_ID = "BROADCAST_ROOM"
        
        # 加载数据
        self.friends_data = self._load_friends_data()
        self.groups_data = self._load_groups_data()
        
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
    
    def _save_friends_data(self):
        """保存好友数据"""
        try:
            with open(self.friends_file, 'w', encoding='utf-8') as f:
                json.dump(self.friends_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存好友数据失败: {e}")
            return False
    
    def _save_groups_data(self, data=None):
        """保存群组数据"""
        try:
            if data is None:
                data = self.groups_data
            with open(self.groups_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存群组数据失败: {e}")
            return False
    
    def get_broadcast_room_id(self) -> str:
        """
        获取广播室ID
        """
        return self.BROADCAST_ROOM_ID
    
    def add_friend(self, user_id: str, friend_id: str) -> (bool, str):
        """
        添加好友
        """
        # 确保用户数据结构存在
        if user_id not in self.friends_data:
            self.friends_data[user_id] = []
        
        if friend_id not in self.friends_data:
            self.friends_data[friend_id] = []
        
        # 检查是否已经是好友
        if friend_id in self.friends_data[user_id]:
            return False, "❌ 你们已经是好友了"
        
        # 检查是否是添加自己
        if user_id == friend_id:
            return False, "❌ 不能添加自己为好友"
        
        # 建立好友关系
        self.friends_data[user_id].append(friend_id)
        self.friends_data[friend_id].append(user_id)
        
        # 保存数据
        if self._save_friends_data():
            return True, f"✅ 成功添加好友 {friend_id}"
        else:
            # 回滚操作
            self.friends_data[user_id].remove(friend_id)
            self.friends_data[friend_id].remove(user_id)
            return False, "❌ 添加好友失败，请稍后重试"
    
    def remove_friend(self, user_id: str, friend_id: str) -> (bool, str):
        """
        移除好友
        """
        # 检查用户数据结构
        if user_id not in self.friends_data or friend_id not in self.friends_data:
            return False, "❌ 好友关系不存在"
        
        # 检查是否是好友
        if friend_id not in self.friends_data[user_id]:
            return False, "❌ 你们不是好友"
        
        # 解除好友关系
        self.friends_data[user_id].remove(friend_id)
        self.friends_data[friend_id].remove(user_id)
        
        # 保存数据
        if self._save_friends_data():
            return True, f"✅ 已解除与 {friend_id} 的好友关系"
        else:
            # 回滚操作
            self.friends_data[user_id].append(friend_id)
            self.friends_data[friend_id].append(user_id)
            return False, "❌ 移除好友失败，请稍后重试"
    
    def create_group(self, creator_id: str, group_name: str) -> (bool, str, str):
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
    
    def add_group_member(self, group_id: str, user_id: str, admin_id: str) -> (bool, str):
        """
        添加群组成员
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
    
    def remove_group_member(self, group_id: str, user_id: str, admin_id: str) -> (bool, str):
        """
        移除群组成员
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
    
    def can_access_conversation(self, user_id: str, conversation_id: str) -> bool:
        """
        检查用户是否有权限访问指定会话
        """
        # 广播室对所有用户开放
        if conversation_id == self.BROADCAST_ROOM_ID:
            return True
        
        # 检查是否是好友对话
        for user, friends in self.friends_data.items():
            if user == user_id and conversation_id in friends:
                return True
            if user == conversation_id and user_id in friends:
                return True
        
        # 检查是否是群组成员
        if conversation_id in self.groups_data:
            return user_id in self.groups_data[conversation_id]["members"]
        
        return False
    
    def get_user_friends(self, user_id: str) -> List[str]:
        """
        获取用户的所有好友
        """
        if user_id not in self.friends_data:
            return []
        return self.friends_data[user_id]
    
    def get_user_groups(self, user_id: str) -> Dict[str, Dict]:
        """
        获取用户加入的所有群组
        """
        user_groups = {}
        for group_id, group_info in self.groups_data.items():
            if group_id != self.BROADCAST_ROOM_ID and user_id in group_info["members"]:
                user_groups[group_id] = group_info
        return user_groups
    
    def get_conversation_name(self, conversation_id: str) -> str:
        """
        获取会话名称
        """
        # 检查是否是广播室
        if conversation_id == self.BROADCAST_ROOM_ID:
            return "中考加油广播室"
        
        # 检查是否是群组
        if conversation_id in self.groups_data:
            return self.groups_data[conversation_id]["name"]
        
        # 默认为用户ID
        return conversation_id
    
    def get_all_groups(self) -> Dict[str, Dict]:
        """
        获取所有群组信息（包括广播室）
        返回: 所有群组的完整数据
        """
        try:
            print(f"✅ 获取所有群组，共 {len(self.groups_data)} 个群组")
            return self.groups_data
        except Exception as e:
            print(f"❌ 获取群组列表失败: {e}")
            return {}