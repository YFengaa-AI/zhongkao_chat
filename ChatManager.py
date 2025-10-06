# ChatManager.py
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class ChatManager:
    """
    聊天管理器重构版 - 支持广播室、个人消息、群聊
    """
    
    def __init__(self, data_dir="data"):
        """
        初始化聊天管理器
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.messages_file = self.data_dir / "messages.json"
        
        # 导入好友管理器
        try:
            from FriendManager import FriendManager
            self.friend_manager = FriendManager(data_dir)
            print("✅ 好友管理器加载成功")
        except ImportError as e:
            print(f"❌ 好友管理器加载失败: {e}")
            self.friend_manager = None
        
        # 加载现有消息数据
        self.messages = self._load_messages()
        print(f"💬 聊天系统初始化完成，已加载 {len(self.messages)} 条历史消息")
    
    def _load_messages(self) -> List[Dict]:
        """
        从JSON文件加载历史聊天记录
        """
        try:
            if self.messages_file.exists():
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    print(f"✅ 成功加载聊天记录，共 {len(messages)} 条消息")
                    return messages
            else:
                print("📝 聊天记录文件不存在，将创建新文件")
                # 创建欢迎消息
                welcome_messages = [
                    {
                        "sender": "系统",
                        "recipient_id": self.friend_manager.get_broadcast_room_id() if self.friend_manager else "BROADCAST_ROOM",
                        "content": "🎉 欢迎来到中考加油聊天室！",
                        "timestamp": self._get_current_time()
                    },
                    {
                        "sender": "系统", 
                        "recipient_id": self.friend_manager.get_broadcast_room_id() if self.friend_manager else "BROADCAST_ROOM",
                        "content": "💪 在这里你可以和战友们交流学习心得，互相鼓励！",
                        "timestamp": self._get_current_time()
                    }
                ]
                # 保存初始消息
                self._save_messages(welcome_messages)
                return welcome_messages
        except Exception as e:
            print(f"❌ 加载聊天记录时出错: {e}")
            return []
    
    def _save_messages(self, messages=None) -> bool:
        """
        将聊天记录保存到JSON文件
        """
        try:
            if messages is None:
                messages = self.messages
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 保存聊天记录时出错: {e}")
            return False
    
    def send_message(self, sender: str, content: str, recipient_id: str = None) -> (bool, str):
        """
        发送消息到指定会话
        如果未指定recipient_id，则发送到广播室
        """
        if not sender or not content:
            return False, "❌ 发送者或内容不能为空"
        
        if len(content.strip()) == 0:
            return False, "❌ 消息内容不能为空"
        
        # 默认发送到广播室
        if recipient_id is None:
            if self.friend_manager:
                recipient_id = self.friend_manager.get_broadcast_room_id()
            else:
                recipient_id = "BROADCAST_ROOM"
        
        # 验证会话权限
        if self.friend_manager:
            if not self.friend_manager.can_access_conversation(sender, recipient_id):
                return False, "❌ 您没有权限访问这个会话"
        
        # 创建消息
        message = {
            "sender": sender,
            "recipient_id": recipient_id,
            "content": content,
            "timestamp": self._get_current_time()
        }
        
        # 添加到消息列表
        self.messages.append(message)
        
        # 保存消息
        if self._save_messages():
            return True, "✅ 消息发送成功"
        else:
            # 如果保存失败，从列表中移除
            self.messages.remove(message)
            return False, "❌ 消息发送失败，请稍后重试"
    
    def get_messages(self, user_id: str, conversation_id: str = None) -> List[Dict]:
        """
        获取指定用户在指定会话中的消息
        如果未指定conversation_id，则返回广播室消息
        """
        # 默认获取广播室消息
        if conversation_id is None:
            if self.friend_manager:
                conversation_id = self.friend_manager.get_broadcast_room_id()
            else:
                conversation_id = "BROADCAST_ROOM"
        
        # 验证会话权限
        if self.friend_manager:
            if not self.friend_manager.can_access_conversation(user_id, conversation_id):
                return []
        
        # 过滤消息
        filtered_messages = []
        for message in self.messages:
            if message["recipient_id"] == conversation_id:
                filtered_messages.append(message)
        
        return filtered_messages
    
    def _get_current_time(self) -> str:
        """
        获取当前时间的字符串表示
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def clear_messages(self, conversation_id: str) -> bool:
        """
        清空指定会话的消息
        """
        try:
            self.messages = [msg for msg in self.messages if msg["recipient_id"] != conversation_id]
            return self._save_messages()
        except Exception as e:
            print(f"❌ 清空消息失败: {e}")
            return False
    
    def get_recent_chats_for_user(self, username: str) -> List[Dict]:
        """
        获取用户参与的最近会话列表
        
        参数:
        - username: 用户名
        
        返回:
        - 会话列表，每个会话包含id和name等基本信息
        """
        try:
            recent_chats = []
            
            # 始终包含广播室
            broadcast_room_id = "BROADCAST_ROOM"
            broadcast_name = "中考加油广播室"
            if self.friend_manager:
                broadcast_room_id = self.friend_manager.get_broadcast_room_id()
                groups = self.friend_manager.get_all_groups()
                if broadcast_room_id in groups:
                    broadcast_name = groups[broadcast_room_id].get("name", broadcast_name)
            
            recent_chats.append({
                "id": broadcast_room_id,
                "name": broadcast_name,
                "type": "broadcast",
                "unread_count": 0
            })
            
            # 如果有好友管理器，可以获取更多会话
            if self.friend_manager:
                # 获取用户的好友列表
                friends = self.friend_manager.get_user_friends(username)
                for friend_id in friends:
                    friend_name = friend_id  # 默认使用ID作为名称
                    # 这里可以根据实际需求获取好友的显示名称
                    recent_chats.append({
                        "id": friend_id,
                        "name": friend_name,
                        "type": "personal",
                        "unread_count": 0
                    })
                
                # 获取用户加入的群组
                user_groups = self.friend_manager.get_user_groups(username)
                all_groups = self.friend_manager.get_all_groups()
                for group_id in user_groups:
                    if group_id in all_groups and group_id != broadcast_room_id:
                        recent_chats.append({
                            "id": group_id,
                            "name": all_groups[group_id].get("name", f"群组{group_id}"),
                            "type": "group",
                            "unread_count": 0
                        })
            
            return recent_chats
        except Exception as e:
            print(f"❌ 获取最近会话失败: {e}")
            # 至少返回广播室作为默认会话
            return [{
                "id": "BROADCAST_ROOM",
                "name": "中考加油广播室",
                "type": "broadcast",
                "unread_count": 0
            }]
    
    def get_chat_history(self, user_id: str, conversation_id: str = None) -> List[Dict]:
        """
        获取指定用户在指定会话中的聊天历史记录
        
        参数:
        - user_id: 用户ID
        - conversation_id: 会话ID，默认为广播室
        
        返回:
        - 聊天历史消息列表
        """
        try:
            # 直接调用现有的get_messages方法获取历史记录
            messages = self.get_messages(user_id, conversation_id)
            print(f"✅ 获取聊天历史成功，共 {len(messages)} 条消息")
            return messages
        except Exception as e:
            print(f"❌ 获取聊天历史失败: {e}")
            return []