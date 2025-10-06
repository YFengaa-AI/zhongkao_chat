# GUIManager.py
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import os
import sys
import threading
import time
from datetime import datetime

class GUIManager:
    """
    图形用户界面管理器
    统一管理所有UI组件和界面切换
    """
    
    def __init__(self):
        """
        初始化GUI管理器
        """
        self.root = None
        self.current_user = None
        self.current_frame = None
        
        # 模块可用性标记
        self.modules_available = {
            'countdown': False,
            'encouragement': False,
            'chat_manager': False,
            'friend_manager': False
        }
        
        # 导入功能模块
        self._load_modules()
        
    def _load_modules(self):
        """
        加载所需的功能模块
        """
        try:
            import countdown
            self.countdown = countdown
            self.modules_available['countdown'] = True
            print("✅ 倒计时模块加载成功")
        except ImportError as e:
            print(f"⚠️ 倒计时模块不可用: {e}")
        
        try:
            import encouragement
            self.encouragement = encouragement
            self.modules_available['encouragement'] = True
            print("✅ 鼓励语录模块加载成功")
        except ImportError as e:
            print(f"⚠️ 鼓励语录模块不可用: {e}")
        
        try:
            from ChatManager import ChatManager
            self.chat_manager_class = ChatManager
            self.modules_available['chat_manager'] = True
            print("✅ 聊天模块加载成功")
        except ImportError as e:
            print(f"❌ 聊天模块加载失败: {e}")
        
        try:
            from FriendManager import FriendManager
            self.friend_manager_class = FriendManager
            self.modules_available['friend_manager'] = True
            print("✅ 好友模块加载成功")
        except ImportError as e:
            print(f"❌ 好友模块加载失败: {e}")
        
    def center_window(self, window):
        """
        将窗口居中显示
        """
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def clear_window(self, window):
        """
        清空窗口内容
        """
        for widget in window.winfo_children():
            widget.destroy()
    
    def show_message(self, title, message, msg_type="info"):
        """
        显示消息对话框
        msg_type: info, warning, error, question
        """
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "question":
            return messagebox.askyesno(title, message)
        return None
    
    def create_scrolled_text(self, parent, width=50, height=10, wrap=tk.WORD, bg="white", fg="black"):
        """
        创建带滚动条的文本框
        """
        text_frame = tk.Frame(parent)
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = scrolledtext.ScrolledText(text_frame, width=width, height=height, wrap=wrap, bg=bg, fg=fg)
        text_widget.pack(side="left", fill="both", expand=True)
        
        # 连接滚动条
        scrollbar.config(command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        return text_widget
    
    def create_button(self, parent, text, command, width=20, height=1, bg="#3498DB", fg="white", font=('Microsoft YaHei', 10)):
        """
        创建按钮
        """
        button = tk.Button(parent, text=text, command=command, width=width, height=height, bg=bg, fg=fg, font=font)
        return button
    
    def create_label(self, parent, text, font=('Microsoft YaHei', 10), fg="#2C3E50", bg="#f5f5f5"):
        """
        创建标签
        """
        label = tk.Label(parent, text=text, font=font, fg=fg, bg=bg)
        return label
    
    def create_entry(self, parent, width=30, show="", font=('Microsoft YaHei', 10)):
        """
        创建输入框
        """
        entry = tk.Entry(parent, width=width, show=show, font=font)
        return entry
    
    def start_thread(self, target, args=()):
        """
        启动一个新线程
        """
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True  # 设置为守护线程，主程序结束时自动终止
        thread.start()
        return thread
    
    def get_current_time(self, format_str="%Y-%m-%d %H:%M:%S"):
        """
        获取当前时间的格式化字符串
        """
        return datetime.now().strftime(format_str)
    
    def get_days_left(self):
        """
        获取距离中考剩余天数
        """
        if self.modules_available['countdown']:
            return self.countdown.get_days_left()
        return 0
    
    def get_encouragement(self):
        """
        获取随机鼓励语录
        """
        if self.modules_available['encouragement']:
            return self.encouragement.get_encouragement()
        return "加油！你一定可以的！"
    
    def setup_window_icon(self, window):
        """
        设置窗口图标
        """
        # 这里可以添加窗口图标设置代码
        pass