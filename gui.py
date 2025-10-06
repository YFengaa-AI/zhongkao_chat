# gui.py - 模块化版本（完整版）
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import sys
import threading
import time
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 启动中考加油聊天室...")

# 全局模块化系统标志
MODULE_SYSTEM_AVAILABLE = False
main_manager = None

# 尝试初始化主管理器
try:
    from MainManager import MainManager
    main_manager = MainManager()
    MODULE_SYSTEM_AVAILABLE = True
    print("✅ 模块化系统加载成功")
except Exception as e:
    print(f"⚠️ 模块化系统不可用: {e}")
    MODULE_SYSTEM_AVAILABLE = False

# 导入功能模块（带错误处理和降级方案）
if MODULE_SYSTEM_AVAILABLE:
    # 使用模块化系统
    countdown_manager = main_manager.get_manager('countdown')
    encouragement_manager = main_manager.get_manager('encouragement')
    chat_manager = main_manager.get_manager('chat')
    friend_manager = main_manager.get_manager('friend')
    group_manager = main_manager.get_manager('group')
    login_manager = main_manager.get_manager('login')
    logout_manager = main_manager.get_manager('logout')
    print("✅ 已加载所有模块化组件")
else:
    # 降级方案：使用直接导入
    try:
        import countdown
        COUNTDOWN_AVAILABLE = True
        print("✅ 降级模式：倒计时模块加载成功")
    except ImportError as e:
        print(f"⚠️ 倒计时模块不可用: {e}")
        COUNTDOWN_AVAILABLE = False
    
    try:
        import encouragement
        ENCOURAGEMENT_AVAILABLE = True
        print("✅ 降级模式：鼓励语录模块加载成功")
    except ImportError as e:
        print(f"⚠️ 鼓励语录模块不可用: {e}")
        ENCOURAGEMENT_AVAILABLE = False
    
    try:
        from chat import ChatManager
        CHAT_AVAILABLE = True
        print("✅ 降级模式：聊天模块加载成功")
    except ImportError as e:
        print(f"❌ 聊天模块加载失败: {e}")
        CHAT_AVAILABLE = False

class Application(tk.Frame):
    """
    中考加油聊天室 - 完整稳定版（含注销功能）
    """
    
    def __init__(self, master=None, username="同学"):
        super().__init__(master)
        self.master = master
        self.username = username
        
        # 配置主窗口
        self.master.title(f"🎯 中考加油聊天室 - {self.username}")
        self.master.geometry("900x700")
        self.master.minsize(700, 500)
        
        # 设置窗口图标和位置
        self.center_window()
        
        # 初始化聊天管理器 - 兼容模块化和直接导入
        self.chat_manager = None
        if MODULE_SYSTEM_AVAILABLE:
            # 使用模块化系统
            self.chat_manager = chat_manager
            print("✅ 使用模块化聊天管理器")
        else:
            # 降级方案：使用直接导入
            if CHAT_AVAILABLE:
                try:
                    self.chat_manager = ChatManager()
                    print("✅ 降级模式：聊天管理器初始化成功")
                except Exception as e:
                    print(f"❌ 聊天管理器初始化失败: {e}")
        
        # 自动刷新控制
        self.auto_refresh = True
        self.is_closing = False
        
        # 创建界面
        self.create_widgets()
        
        # 初始显示
        self.update_info_display()
        self.display_chat_history()
        
        # 启动自动刷新
        self.start_auto_refresh()
        
        # 设置关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("✅ 应用初始化完成")
    
    def center_window(self):
        """窗口居中显示"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        """创建界面组件"""
        # 配置主框架
        self.configure(bg="#f0f0f0")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. 顶部信息栏
        self.create_top_bar()
        
        # 2. 控制按钮栏
        self.create_control_bar()
        
        # 3. 聊天记录区域
        self.create_chat_area()
        
        # 4. 消息输入区域
        self.create_input_area()
    
    def create_top_bar(self):
        """创建顶部信息栏"""
        top_frame = tk.Frame(self, bg="#2C3E50", relief="raised", bd=1, height=80)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)
        top_frame.pack_propagate(False)  # 保持固定高度
        
        # 左侧：用户信息
        user_frame = tk.Frame(top_frame, bg="#2C3E50")
        user_frame.pack(side="left", fill="y", padx=15)
        
        user_icon = tk.Label(user_frame, text="👤", font=('Arial', 16), bg="#2C3E50", fg="white")
        user_icon.pack(side="left")
        
        user_label = tk.Label(user_frame, text=self.username, 
                             font=('Microsoft YaHei', 12, 'bold'), 
                             bg="#2C3E50", fg="white")
        user_label.pack(side="left", padx=5)
        
        # 中间：倒计时信息
        center_frame = tk.Frame(top_frame, bg="#2C3E50")
        center_frame.pack(side="left", fill="both", expand=True)
        
        self.days_label = tk.Label(center_frame, 
                                  text="正在加载倒计时...",
                                  font=('Microsoft YaHei', 12, 'bold'), 
                                  bg="#2C3E50", fg="#F39C12")
        self.days_label.pack(anchor="center")
        
        # 右侧：鼓励语录
        right_frame = tk.Frame(top_frame, bg="#2C3E50")
        right_frame.pack(side="right", fill="y", padx=15)
        
        self.encouragement_label = tk.Label(right_frame, 
                                           text="正在加载鼓励语...",
                                           font=('Microsoft YaHei', 10, 'italic'), 
                                           bg="#2C3E50", fg="#AED6F1",
                                           wraplength=300)
        self.encouragement_label.pack(anchor="e")
    
    def create_control_bar(self):
        """创建控制按钮栏（已添加注销功能）"""
        control_frame = tk.Frame(self, bg="#ECF0F1", relief="flat", height=40)
        control_frame.pack(side="top", fill="x", padx=5, pady=2)
        control_frame.pack_propagate(False)
        
        # 左侧按钮组
        left_frame = tk.Frame(control_frame, bg="#ECF0F1")
        left_frame.pack(side="left", padx=10)
        
        # 刷新按钮
        refresh_btn = tk.Button(left_frame, text="🔄 刷新", 
                               command=self.manual_refresh,
                               font=('Microsoft YaHei', 9),
                               bg="#3498DB", fg="white",
                               relief="raised", bd=1)
        refresh_btn.pack(side="left", padx=2)
        
        # 自动刷新开关
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_btn = tk.Checkbutton(left_frame, text="自动刷新", 
                                         variable=self.auto_refresh_var,
                                         command=self.toggle_auto_refresh,
                                         font=('Microsoft YaHei', 9),
                                         bg="#ECF0F1")
        auto_refresh_btn.pack(side="left", padx=10)
        
        # 右侧按钮组
        right_frame = tk.Frame(control_frame, bg="#ECF0F1")
        right_frame.pack(side="right", padx=10)
        
        # 用户信息显示（新增）
        user_label = tk.Label(right_frame,
                             text=f"👤 {self.username}",
                             font=('Microsoft YaHei', 9),
                             bg="#ECF0F1",
                             fg="#2C3E50")
        user_label.pack(side="left", padx=5)
        
        # 注销按钮（新增）
        logout_btn = tk.Button(right_frame,
                              text="🚪 注销",
                              command=self.logout,
                              font=('Microsoft YaHei', 9),
                              bg="#E74C3C", fg="white")
        logout_btn.pack(side="left", padx=5)
        
        # 搜索框
        search_frame = tk.Frame(right_frame, bg="#ECF0F1")
        search_frame.pack(side="left", padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=15, font=('Microsoft YaHei', 9))
        self.search_entry.pack(side="left", padx=2)
        self.search_entry.bind('<Return>', self.search_messages)
        
        search_btn = tk.Button(search_frame, text="🔍 搜索", 
                              command=self.search_messages,
                              font=('Microsoft YaHei', 9),
                              bg="#27AE60", fg="white")
        search_btn.pack(side="left", padx=2)
        
        # 清空聊天按钮
        clear_btn = tk.Button(right_frame, text="🗑️ 清空", 
                             command=self.clear_chat_confirm,
                             font=('Microsoft YaHei', 9),
                             bg="#E74C3C", fg="white")
        clear_btn.pack(side="left", padx=5)
    
    def create_chat_area(self):
        """创建聊天记录区域"""
        chat_container = tk.Frame(self, bg="white", relief="sunken", bd=1)
        chat_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        # 聊天标题
        title_frame = tk.Frame(chat_container, bg="#34495E", height=30)
        title_frame.pack(side="top", fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="💬 中考加油群聊", 
                              font=('Microsoft YaHei', 12, 'bold'), 
                              bg="#34495E", fg="white")
        title_label.pack(side="left", padx=15, pady=5)
        
        # 消息计数
        self.message_count_label = tk.Label(title_frame, 
                                          text="消息数: 0",
                                          font=('Microsoft YaHei', 9), 
                                          bg="#34495E", fg="#BDC3C7")
        self.message_count_label.pack(side="right", padx=15, pady=5)
        
        # 聊天记录显示区域
        self.chat_text = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            state='disabled',
            font=('Microsoft YaHei', 10),
            padx=15,
            pady=10,
            bg="#F8F9F9",
            relief="flat"
        )
        self.chat_text.pack(fill="both", expand=True)
        
        # 配置标签样式
        self.chat_text.tag_config("system", foreground="#7F8C8D", font=('Microsoft YaHei', 9, 'italic'))
        self.chat_text.tag_config("self", foreground="#2C3E50", font=('Microsoft YaHei', 10))
        self.chat_text.tag_config("other", foreground="#2C3E50", font=('Microsoft YaHei', 10))
        self.chat_text.tag_config("welcome", foreground="#7F8C8D", font=('Microsoft YaHei', 10, 'italic'), justify='center')
    
    def create_input_area(self):
        """创建消息输入区域"""
        input_frame = tk.Frame(self, bg="#ECF0F1", height=80)
        input_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        input_frame.pack_propagate(False)
        
        # 输入框容器
        input_container = tk.Frame(input_frame, bg="#BDC3C7", relief="sunken", bd=1)
        input_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 多行输入框
        self.input_text = tk.Text(
            input_container,
            height=3,
            wrap=tk.WORD,
            font=('Microsoft YaHei', 11),
            relief="flat",
            bd=0,
            padx=10,
            pady=8
        )
        self.input_text.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 输入框提示
        self.placeholder_text = "输入消息内容...（Ctrl+Enter 发送）"
        self.input_text.insert("1.0", self.placeholder_text)
        self.input_text.config(fg="grey")
        
        # 绑定事件
        self.input_text.bind('<FocusIn>', self.on_input_focus_in)
        self.input_text.bind('<FocusOut>', self.on_input_focus_out)
        self.input_text.bind('<KeyPress>', self.on_input_key)
        self.input_text.bind('<KeyRelease>', self.on_input_key)
        
        # 按钮框架
        button_frame = tk.Frame(input_frame, bg="#ECF0F1")
        button_frame.pack(side="right")
        
        # 发送按钮
        self.send_btn = tk.Button(
            button_frame,
            text="📤 发送",
            command=self.send_message,
            font=('Microsoft YaHei', 11, 'bold'),
            bg="#27AE60",
            fg="white",
            width=8,
            height=2
        )
        self.send_btn.pack(pady=5)
        
        # 消息长度显示
        self.length_label = tk.Label(
            button_frame,
            text="0/500",
            font=('Microsoft YaHei', 8),
            bg="#ECF0F1",
            fg="#7F8C8D"
        )
        self.length_label.pack()
        
        # 绑定快捷键
        self.master.bind('<Control-Return>', lambda e: self.send_message())
    
    def on_input_focus_in(self, event):
        """输入框获得焦点"""
        if self.input_text.get("1.0", "end-1c") == self.placeholder_text:
            self.input_text.delete("1.0", "end")
            self.input_text.config(fg="black")
    
    def on_input_focus_out(self, event):
        """输入框失去焦点"""
        if not self.input_text.get("1.0", "end-1c").strip():
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.config(fg="grey")
    
    def on_input_key(self, event):
        """输入框按键事件"""
        # 更新长度显示
        self.update_length_display()
        
        # Ctrl+Enter 发送
        if event.state == 4 and event.keysym == "Return":
            self.send_message()
            return "break"
    
    def update_length_display(self):
        """更新消息长度显示"""
        try:
            content = self.input_text.get("1.0", "end-1c")
            if content == self.placeholder_text:
                length = 0
            else:
                length = len(content)
            
            self.length_label.config(text=f"{length}/500")
            
            # 颜色警告
            if length > 500:
                self.length_label.config(fg="#E74C3C")
            elif length > 400:
                self.length_label.config(fg="#F39C12")
            else:
                self.length_label.config(fg="#7F8C8D")
                
        except Exception as e:
            print(f"更新长度显示时出错: {e}")
    
    def update_info_display(self):
        """更新顶部信息显示"""
        try:
            # 更新倒计时
            if MODULE_SYSTEM_AVAILABLE and countdown_manager:
                try:
                    # 尝试使用模块化系统的方法
                    if hasattr(countdown_manager, 'get_days_left'):
                        days = countdown_manager.get_days_left()
                    elif hasattr(countdown_manager, 'get_countdown_message'):
                        days = countdown_manager.get_countdown_message()
                    else:
                        days = "功能异常"
                    self.days_label.config(text=f"📅 距离中考还有 {days} 天")
                except Exception as e:
                    print(f"模块化倒计时功能异常: {e}")
                    self.days_label.config(text="📅 倒计时功能异常")
            elif not MODULE_SYSTEM_AVAILABLE and COUNTDOWN_AVAILABLE:
                # 降级方案：使用直接导入
                days = countdown.get_days_left()
                self.days_label.config(text=f"📅 距离中考还有 {days} 天")
            else:
                self.days_label.config(text="📅 倒计时功能暂不可用")
            
            # 更新鼓励语录
            if MODULE_SYSTEM_AVAILABLE and encouragement_manager:
                try:
                    # 尝试使用模块化系统的方法
                    if hasattr(encouragement_manager, 'get_encouragement'):
                        word = encouragement_manager.get_encouragement()
                    elif hasattr(encouragement_manager, 'get_random_quote'):
                        word = encouragement_manager.get_random_quote()
                    else:
                        word = "加油！"
                    self.encouragement_label.config(text=f"💪 {word}")
                except Exception as e:
                    print(f"模块化鼓励语录功能异常: {e}")
                    self.encouragement_label.config(text="💪 功能异常")
            elif not MODULE_SYSTEM_AVAILABLE and ENCOURAGEMENT_AVAILABLE:
                # 降级方案：使用直接导入
                word = encouragement.get_encouragement()
                self.encouragement_label.config(text=f"💪 {word}")
            else:
                self.encouragement_label.config(text="💪 加油！你可以的！")
                
        except Exception as e:
            print(f"更新信息显示时出错: {e}")
    
    def display_chat_history(self, messages=None):
        """显示聊天记录"""
        try:
            # 获取消息
            if messages is None and self.chat_manager:
                # 兼容不同的获取聊天记录方法名
                if hasattr(self.chat_manager, 'get_chat_history'):
                    messages = self.chat_manager.get_chat_history()
                elif hasattr(self.chat_manager, 'get_messages'):
                    messages = self.chat_manager.get_messages()
                elif hasattr(self.chat_manager, 'messages'):
                    # 如果有messages属性，直接使用
                    messages = self.chat_manager.messages
                else:
                    messages = []
            elif messages is None:
                messages = []
            
            # 更新消息计数
            self.message_count_label.config(text=f"消息数: {len(messages)}")
            
            # 允许编辑
            self.chat_text.config(state='normal')
            self.chat_text.delete('1.0', tk.END)
            
            if not messages:
                # 显示欢迎信息
                welcome_msg = """💬 欢迎来到中考加油聊天室！

这里是专为中考学子打造的交流平台。

✨ 你可以在这里：
• 与同学交流学习心得
• 分享备考经验
• 互相鼓励支持
• 获取每日鼓励语录

发出第一条消息，开始你的中考加油之旅吧！"""
                self.chat_text.insert(tk.END, welcome_msg, "welcome")
            else:
                # 显示所有消息
                for msg in messages:
                    sender = msg.get('sender', '未知用户')
                    content = msg.get('content', '')
                    timestamp = msg.get('timestamp', '')
                    
                    # 格式化时间
                    try:
                        time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                        display_time = time_obj.strftime("%m/%d %H:%M")
                    except:
                        display_time = timestamp
                    
                    # 确定消息样式
                    if sender == "系统":
                        tag = "system"
                        prefix = "⚙️ 系统: "
                    elif sender == self.username:
                        tag = "self"
                        prefix = "👤 我: "
                    else:
                        tag = "other"
                        prefix = f"👤 {sender}: "
                    
                    # 插入消息
                    display_line = f"[{display_time}] {prefix}{content}\n\n"
                    self.chat_text.insert(tk.END, display_line, tag)
            
            # 禁用编辑并滚动到底部
            self.chat_text.config(state='disabled')
            self.chat_text.see(tk.END)
            
        except Exception as e:
            print(f"显示聊天记录时出错: {e}")
            self.chat_text.config(state='normal')
            self.chat_text.delete('1.0', tk.END)
            self.chat_text.insert(tk.END, f"❌ 加载聊天记录时出错: {e}\n")
            self.chat_text.config(state='disabled')
    
    def send_message(self):
        """发送消息"""
        try:
            # 获取消息内容
            content = self.input_text.get("1.0", "end-1c").strip()
            
            # 检查占位符
            if content == self.placeholder_text:
                content = ""
            
            # 验证输入
            if not content:
                messagebox.showwarning("输入提示", "请输入消息内容！")
                return
            
            if len(content) > 500:
                messagebox.showwarning("输入提示", "消息内容不能超过500字！")
                return
            
            # 禁用发送按钮
            self.send_btn.config(state='disabled', text="发送中...", bg="#95A5A6")
            
            # 在后台线程中发送
            thread = threading.Thread(target=self._send_message_thread, args=(content,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"发送消息时出错: {e}")
            self.reset_send_button()
    
    def _send_message_thread(self, content):
        """在后台线程中发送消息"""
        try:
            if self.chat_manager:
                # 兼容不同的发送消息方法名
                if hasattr(self.chat_manager, 'send_message'):
                    success, result = self.chat_manager.send_message(self.username, content)
                elif hasattr(self.chat_manager, 'add_message'):
                    # 最简单的发送消息方法
                    success = self.chat_manager.add_message(self.username, content)
                    result = "消息发送成功" if success else "消息发送失败"
                else:
                    success, result = False, "聊天功能方法不支持"
                self.master.after(0, lambda: self._on_send_complete(success, result, content))
            else:
                self.master.after(0, lambda: self._on_send_complete(False, "聊天功能不可用", content))
        except Exception as e:
            self.master.after(0, lambda: self._on_send_complete(False, str(e), content))
    
    def _on_send_complete(self, success, result, content):
        """发送完成处理"""
        if success:
            # 清空输入框
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.config(fg="grey")
            self.length_label.config(text="0/500", fg="#7F8C8D")
            
            # 刷新显示
            self.display_chat_history()
            self.update_info_display()
            
            # 显示成功反馈
            self.send_btn.config(text="✅ 成功", bg="#2ECC71")
            self.master.after(1000, self.reset_send_button)
        else:
            messagebox.showerror("发送失败", result)
            self.reset_send_button()
    
    def reset_send_button(self):
        """重置发送按钮状态"""
        self.send_btn.config(state='normal', text="📤 发送", bg="#27AE60")
    
    def manual_refresh(self):
        """手动刷新"""
        self.display_chat_history()
        self.update_info_display()
    
    def toggle_auto_refresh(self):
        """切换自动刷新"""
        self.auto_refresh = self.auto_refresh_var.get()
    
    def start_auto_refresh(self):
        """开始自动刷新"""
        if self.auto_refresh and not self.is_closing:
            self.manual_refresh()
            self.master.after(30000, self.start_auto_refresh)  # 30秒后再次刷新
    
    def search_messages(self, event=None):
        """搜索消息"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("搜索", "请输入搜索关键词！")
            return
        
        try:
            if self.chat_manager:
                # 兼容不同的搜索方法名
                if hasattr(self.chat_manager, 'search_messages'):
                    results = self.chat_manager.search_messages(keyword)
                elif hasattr(self.chat_manager, 'filter_messages'):
                    results = self.chat_manager.filter_messages(keyword)
                else:
                    # 降级搜索实现
                    messages = self.chat_manager.get_chat_history() if hasattr(self.chat_manager, 'get_chat_history') else \
                              self.chat_manager.get_messages() if hasattr(self.chat_manager, 'get_messages') else \
                              self.chat_manager.messages if hasattr(self.chat_manager, 'messages') else []
                    results = [msg for msg in messages if keyword.lower() in str(msg).lower()]
                
                if results:
                    self.display_chat_history(results)
                    messagebox.showinfo("搜索结果", f"找到 {len(results)} 条包含 '{keyword}' 的消息")
                else:
                    messagebox.showinfo("搜索结果", f"没有找到包含 '{keyword}' 的消息")
                    self.display_chat_history()  # 恢复显示所有消息
            else:
                messagebox.showerror("错误", "搜索功能暂不可用")
        except Exception as e:
            messagebox.showerror("搜索错误", f"搜索时出错: {e}")
    
    def clear_chat_confirm(self):
        """确认清空聊天记录"""
        if messagebox.askyesno("确认清空", "确定要清空所有聊天记录吗？此操作不可恢复！"):
            self.clear_chat()
    
    def clear_chat(self):
        """清空聊天记录"""
        try:
            if self.chat_manager:
                # 兼容不同的清空方法名
                if hasattr(self.chat_manager, 'clear_chat_history'):
                    success, result = self.chat_manager.clear_chat_history()
                elif hasattr(self.chat_manager, 'clear_messages'):
                    success = self.chat_manager.clear_messages()
                    result = "聊天记录已清空" if success else "清空失败"
                else:
                    success, result = False, "清空方法不支持"
                
                if success:
                    self.display_chat_history()
                    messagebox.showinfo("清空成功", result)
                else:
                    messagebox.showerror("清空失败", result)
            else:
                messagebox.showerror("错误", "清空功能暂不可用")
        except Exception as e:
            messagebox.showerror("错误", f"清空聊天记录时出错: {e}")
    
    def logout(self):
        """注销用户"""
        if messagebox.askyesno("确认注销", "确定要注销当前账号并返回登录界面吗？"):
            print(f"👋 用户 {self.username} 注销")
            
            # 调用Logout模块进行注销处理
            if MODULE_SYSTEM_AVAILABLE and logout_manager:
                try:
                    logout_manager.logout_user(self.username)
                    print("✅ 模块化注销成功")
                except Exception as e:
                    print(f"⚠️ 模块化注销失败: {e}")
            
            self.is_closing = True
            self.master.destroy()
            
            # 重新启动登录界面
            try:
                # 导入并启动登录GUI
                from login_gui import start_login_gui
                start_login_gui()
            except ImportError as e:
                print(f"❌ 无法启动登录界面: {e}")
                messagebox.showerror("错误", "无法返回登录界面，请重新启动程序")
            except Exception as e:
                print(f"❌ 启动登录界面时出错: {e}")
                messagebox.showerror("错误", f"返回登录界面时出错: {e}")
    
    def on_closing(self):
        """关闭窗口事件"""
        self.is_closing = True
        if messagebox.askokcancel("退出", "确定要退出中考加油聊天室吗？"):
            print("👋 退出中考加油聊天室")
            self.master.destroy()

def start_main_app(username):
    """
    启动主应用程序
    """
    print(f"🎉 欢迎 {username}！")
    print("💡 提示：使用 Ctrl+Enter 快速发送消息")
    
    try:
        root = tk.Tk()
        
        # 设置窗口大小和位置
        root.geometry("900x700")
        root.minsize(700, 500)
        
        # 创建应用
        app = Application(master=root, username=username)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("启动错误", f"启动应用程序时出错: {e}")
        print(f"❌ 启动错误: {e}")

# 测试函数
def test_gui():
    """测试GUI"""
    start_main_app("测试用户")

if __name__ == '__main__':
    test_gui()