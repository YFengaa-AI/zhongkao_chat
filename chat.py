# Chat.py
from typing import List, Dict
from datetime import datetime
import os
import json

class Chat:
    """
    聊天功能核心模块
    处理基本的消息发送和接收功能
    支持模块化系统和独立运行两种模式
    """
    
    def __init__(self, main_manager=None, data_dir="data"):
        """
        初始化聊天模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取其他管理器
        - data_dir: 数据存储目录
        """
        self.main_manager = main_manager
        
        # 根据运行模式设置数据目录
        if main_manager is not None and hasattr(main_manager, 'data_dir'):
            self.data_dir = main_manager.data_dir
        else:
            self.data_dir = data_dir
        
        self.messages = []
        self.friend_manager = None
        
        # 确保数据目录存在
        if self.data_dir and not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # 如果在模块化系统中运行，从main_manager获取friend模块
        if main_manager is not None:
            self.friend_manager = main_manager.get_manager('friend')
        
        # 加载消息数据
        self._load_messages()
    
    def send_message(self, sender, content, recipient_id=None):
        """
        发送消息
        返回: (成功与否, 提示信息)
        """
        if not self._can_send_to_chat(sender, recipient_id):
            return False, "❌ 没有权限向此会话发送消息"
        
        # 创建新消息
        new_message = {
            "sender": sender,
            "recipient_id": recipient_id,
            "content": content,
            "timestamp": self._get_current_time()
        }
        
        # 添加到消息列表
        self.messages.append(new_message)
        
        # 保存到文件
        if self._save_messages():
            return True, "✅ 消息发送成功"
        else:
            # 如果保存失败，移除最新消息
            self.messages.pop()
            return False, "❌ 消息发送失败，请重试"
    
    def _can_send_to_chat(self, sender: str, recipient_id: str) -> bool:
        """
        检查用户是否有权限向指定会话发送消息
        """
        if not self.friend_manager:
            return True  # 如果没有好友管理器，默认允许
        
        # 广播室所有人都可以发送
        if recipient_id == self.friend_manager.get_broadcast_room_id():
            return True
        
        # 个人聊天：检查是否是聊天的参与者
        if self.friend_manager.is_personal_chat_id(recipient_id):
            users = self.friend_manager.get_users_from_personal_chat(recipient_id)
            return sender in users
        
        # 群组聊天：检查是否是群组成员
        group_info = self.friend_manager.get_group_info(recipient_id)
        if group_info:
            return sender in group_info.get("members", [])
        
        return False
    
    def get_messages(self, user_id, conversation_id=None):
        """
        获取指定用户在指定会话中的消息
        兼容模块化系统的方法名
        """
        if conversation_id:
            return self.get_chat_history(conversation_id)
        return self.get_user_messages(user_id)
    
    def get_chat_history(self, recipient_id: str, limit: int = None) -> List[Dict]:
        """
        获取指定会话的聊天记录
        """
        # 过滤出指定会话的消息
        chat_messages = [msg for msg in self.messages if msg.get('recipient_id') == recipient_id]
        
        # 按时间排序（确保最新的在后面）
        chat_messages.sort(key=lambda x: x.get('timestamp', ''))
        
        if limit and len(chat_messages) > limit:
            return chat_messages[-limit:]
        
        return chat_messages
    
    def get_recent_chats_for_user(self, username: str) -> List[Dict]:
        """
        获取用户最近参与的会话列表
        """
        if not self.friend_manager:
            return []
        
        recent_chats = []
        
        # 1. 广播室（始终显示）
        broadcast_id = self.friend_manager.get_broadcast_room_id()
        broadcast_messages = self.get_chat_history(broadcast_id, 1)
        last_message = broadcast_messages[-1] if broadcast_messages else None
        
        recent_chats.append({
            "id": broadcast_id,
            "name": "中考加油广播室",
            "type": "broadcast",
            "last_message": last_message,
            "unread_count": 0  # 简化处理，实际应该跟踪未读消息
        })
        
        # 2. 个人聊天
        friends = self.friend_manager.get_friend_list(username)
        for friend in friends:
            chat_id = self.friend_manager.get_personal_chat_id(username, friend)
            chat_messages = self.get_chat_history(chat_id, 1)
            last_message = chat_messages[-1] if chat_messages else None
            
            recent_chats.append({
                "id": chat_id,
                "name": friend,
                "type": "personal",
                "last_message": last_message,
                "unread_count": 0
            })
        
        # 3. 群组聊天
        groups = self.friend_manager.get_group_list(username)
        for group in groups:
            if group["id"] != broadcast_id:  # 排除广播室
                chat_messages = self.get_chat_history(group["id"], 1)
                last_message = chat_messages[-1] if chat_messages else None
                
                recent_chats.append({
                    "id": group["id"],
                    "name": group["name"],
                    "type": "group",
                    "last_message": last_message,
                    "unread_count": 0
                })
        
        # 按最后消息时间排序
        recent_chats.sort(key=lambda x: x["last_message"]["timestamp"] if x["last_message"] else "", reverse=True)
        
        return recent_chats
    
    def get_personal_chat_history(self, user1: str, user2: str) -> List[Dict]:
        """
        获取两人之间的个人聊天记录
        """
        if not self.friend_manager:
            return []
        
        chat_id = self.friend_manager.get_personal_chat_id(user1, user2)
        return self.get_chat_history(chat_id)
    
    def search_messages(self, keyword: str, recipient_id: str = None) -> List[Dict]:
        """
        搜索消息，可以指定会话或全局搜索
        """
        results = []
        for msg in self.messages:
            # 如果指定了会话，只搜索该会话的消息
            if recipient_id and msg.get('recipient_id') != recipient_id:
                continue
            
            if keyword.lower() in msg['content'].lower():
                results.append(msg)
        
        return results
    
    def get_user_messages(self, username: str, recipient_id: str = None) -> List[Dict]:
        """
        获取用户发送的消息，可以指定会话
        """
        user_messages = []
        for msg in self.messages:
            # 检查发送者
            if msg['sender'] != username:
                continue
            
            # 如果指定了会话，只返回该会话的消息
            if recipient_id and msg.get('recipient_id') != recipient_id:
                continue
            
            user_messages.append(msg)
        
        return user_messages
    
    def clear_chat_history(self, recipient_id: str = None) -> (bool, str):
        """
        清空聊天记录，可以指定会话或清空全部
        """
        try:
            if recipient_id:
                # 清空指定会话
                self.messages = [msg for msg in self.messages if msg.get('recipient_id') != recipient_id]
                message = f"已清空会话记录"
            else:
                # 清空所有记录
                self.messages = []
                message = "已清空所有聊天记录"
            
            if self._save_messages():
                return True, message
            else:
                return False, "清空失败"
        except Exception as e:
            return False, f"清空聊天记录时出错: {e}"
    
    def clear_messages(self, conversation_id):
        """
        清空指定会话的消息
        兼容模块化系统的方法名
        """
        return self.clear_chat_history(conversation_id)
    
    def get_message_count(self, recipient_id: str = None) -> int:
        """
        获取消息数量，可以指定会话
        """
        if recipient_id:
            return len([msg for msg in self.messages if msg.get('recipient_id') == recipient_id])
        else:
            return len(self.messages)
    
    def _get_current_time(self) -> str:
        """
        获取当前时间字符串
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _load_messages(self):
        """
        从文件加载消息数据
        """
        try:
            file_path = os.path.join(self.data_dir, "messages.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
        except Exception as e:
            print(f"加载消息数据时出错: {e}")
            self.messages = []
    
    def _save_messages(self) -> bool:
        """
        保存消息数据到文件
        """
        try:
            file_path = os.path.join(self.data_dir, "messages.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存消息数据时出错: {e}")
            return False

# 测试代码
def test_enhanced_chat_system():
    """
    测试增强版聊天系统
    """
    print("🧪 测试增强版聊天系统...")
    
    # 创建聊天管理器（独立模式）
    chat_manager = Chat(data_dir="test_data")
    
    print("\n✅ 增强版聊天系统测试完成")

if __name__ == '__main__':
    test_enhanced_chat_system()