# gui_enhanced.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
import threading
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 启动中考加油聊天室 - 增强版")

# 导入功能模块
try:
    import countdown
    COUNTDOWN_AVAILABLE = True
    print("✅ 倒计时模块加载成功")
except ImportError as e:
    print(f"⚠️ 倒计时模块不可用: {e}")
    COUNTDOWN_AVAILABLE = False

try:
    import encouragement
    ENCOURAGEMENT_AVAILABLE = True
    print("✅ 鼓励语录模块加载成功")
except ImportError as e:
    print(f"⚠️ 鼓励语录模块不可用: {e}")
    ENCOURAGEMENT_AVAILABLE = False

try:
    from ChatManager import ChatManager
    CHAT_AVAILABLE = True
    print("✅ 聊天模块加载成功")
except ImportError as e:
    # 如果管理器版本不可用，尝试使用简单模块版本
    try:
        from chat import Chat
        ChatManager = Chat  # 别名，保持代码兼容性
        CHAT_AVAILABLE = True
        print("✅ 简单聊天模块加载成功")
    except ImportError:
        print(f"❌ 聊天模块加载失败: {e}")
        CHAT_AVAILABLE = False

try:
    from FriendManager import FriendManager
    FRIEND_AVAILABLE = True
    print("✅ 好友模块加载成功")
except ImportError as e:
    # 如果管理器版本不可用，尝试使用简单模块版本
    try:
        from friend import Friend
        FriendManager = Friend  # 别名，保持代码兼容性
        FRIEND_AVAILABLE = True
        print("✅ 简单好友模块加载成功")
    except ImportError:
        print(f"❌ 好友模块加载失败: {e}")
        FRIEND_AVAILABLE = False

class EnhancedApplication(tk.Frame):
    """
    中考加油聊天室 - 增强版
    支持多会话：广播室、个人聊天、群组聊天
    """
    
    def __init__(self, master=None, username="同学"):
        super().__init__(master)
        self.master = master
        self.username = username
        
        # 配置主窗口
        self.master.title(f"🎯 中考加油聊天室 - {self.username}")
        self.master.geometry("1000x700")
        self.master.minsize(800, 500)
        
        # 设置窗口位置
        self.center_window()
        
        # 初始化管理器
        self.chat_manager = ChatManager() if CHAT_AVAILABLE else None
        self.friend_manager = FriendManager() if FRIEND_AVAILABLE else None
        
        # 当前会话状态
        self.current_chat_id = None
        self.current_chat_name = "中考加油广播室"
        self.current_chat_type = "broadcast"
        
        # 自动刷新控制
        self.auto_refresh = True
        self.is_closing = False
        
        # 创建界面
        self.create_widgets()
        
        # 初始显示
        self.update_info_display()
        self.load_conversations()
        self.switch_to_broadcast()
        
        # 启动自动刷新
        self.start_auto_refresh()
        
        # 设置关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("✅ 增强版应用初始化完成")
    
    def center_window(self):
        """窗口居中显示"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """创建增强版界面组件"""
        # 配置主框架
        self.configure(bg="#f0f0f0")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. 顶部信息栏
        self.create_top_bar()
        
        # 2. 主内容区域（左侧会话列表 + 右侧聊天区域）
        self.create_main_content()
    
    def create_top_bar(self):
        """创建顶部信息栏"""
        top_frame = tk.Frame(self, bg="#2C3E50", relief="raised", bd=1, height=60)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)
        top_frame.pack_propagate(False)
        
        # 左侧：应用标题和用户信息
        left_frame = tk.Frame(top_frame, bg="#2C3E50")
        left_frame.pack(side="left", fill="y", padx=15)
        
        title_label = tk.Label(left_frame, 
                              text="🎯 中考加油聊天室",
                              font=('Microsoft YaHei', 14, 'bold'), 
                              bg="#2C3E50", fg="white")
        title_label.pack(side="left")
        
        user_label = tk.Label(left_frame, 
                             text=f"👤 {self.username}",
                             font=('Microsoft YaHei', 11), 
                             bg="#2C3E50", fg="#BDC3C7")
        user_label.pack(side="left", padx=20)
        
        # 中间：当前会话信息
        center_frame = tk.Frame(top_frame, bg="#2C3E50")
        center_frame.pack(side="left", fill="both", expand=True)
        
        self.current_chat_label = tk.Label(center_frame, 
                                          text="正在加载...",
                                          font=('Microsoft YaHei', 12, 'bold'), 
                                          bg="#2C3E50", fg="#F39C12")
        self.current_chat_label.pack(anchor="center")
        
        # 右侧：系统信息和按钮
        right_frame = tk.Frame(top_frame, bg="#2C3E50")
        right_frame.pack(side="right", fill="y", padx=15)
        
        # 倒计时信息
        self.days_label = tk.Label(right_frame, 
                                  text="加载中...",
                                  font=('Microsoft YaHei', 10), 
                                  bg="#2C3E50", fg="#AED6F1")
        self.days_label.pack(side="left", padx=10)
        
        # 注销按钮
        logout_btn = tk.Button(right_frame,
                              text="🚪 注销",
                              command=self.logout,
                              font=('Microsoft YaHei', 9),
                              bg="#E74C3C", fg="white")
        logout_btn.pack(side="left", padx=5)
    
    def create_main_content(self):
        """创建主内容区域"""
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(side="top", fill="both", expand=True, pady=5)
        
        # 左侧：会话列表面板
        self.create_conversation_panel(main_frame)
        
        # 右侧：聊天主面板
        self.create_chat_panel(main_frame)
    
    def create_conversation_panel(self, parent):
        """创建左侧会话列表面板"""
        # 会话列表容器
        conv_frame = tk.Frame(parent, bg="#ECF0F1", width=250)
        conv_frame.pack(side="left", fill="y", padx=(0, 5))
        conv_frame.pack_propagate(False)
        
        # 会话列表标题
        title_frame = tk.Frame(conv_frame, bg="#34495E", height=40)
        title_frame.pack(side="top", fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="💬 会话列表",
                              font=('Microsoft YaHei', 12, 'bold'), 
                              bg="#34495E", fg="white")
        title_label.pack(side="left", padx=15, pady=10)
        
        # 刷新按钮
        refresh_btn = tk.Button(title_frame,
                               text="🔄",
                               command=self.load_conversations,
                               font=('Microsoft YaHei', 10),
                               bg="#3498DB", fg="white",
                               width=3)
        refresh_btn.pack(side="right", padx=10, pady=10)
        
        # 操作按钮区域
        button_frame = tk.Frame(conv_frame, bg="#ECF0F1", height=40)
        button_frame.pack(side="top", fill="x", pady=5)
        button_frame.pack_propagate(False)
        
        # 添加好友按钮
        add_friend_btn = tk.Button(button_frame,
                                  text="👥 添加好友",
                                  command=self.show_add_friend_dialog,
                                  font=('Microsoft YaHei', 9),
                                  bg="#27AE60", fg="white")
        add_friend_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # 创建群组按钮
        create_group_btn = tk.Button(button_frame,
                                    text="👨‍👩‍👧‍👦 创建群组",
                                    command=self.show_create_group_dialog,
                                    font=('Microsoft YaHei', 9),
                                    bg="#3498DB", fg="white")
        create_group_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # 会话列表
        list_frame = tk.Frame(conv_frame, bg="white")
        list_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        # 创建树形视图显示会话列表
        columns = ("name", "type")
        self.conversation_tree = ttk.Treeview(list_frame, columns=columns, show="tree", height=15)
        
        # 设置列
        self.conversation_tree.column("#0", width=0, stretch=tk.NO)  # 隐藏第一列
        self.conversation_tree.column("name", width=180)
        self.conversation_tree.column("type", width=0, stretch=tk.NO)  # 隐藏类型列
        
        # 创建滚动条
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.conversation_tree.yview)
        self.conversation_tree.configure(yscrollcommand=tree_scroll.set)
        
        # 布局
        self.conversation_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        # 绑定选择事件
        self.conversation_tree.bind("<<TreeviewSelect>>", self.on_conversation_select)
    
    def create_chat_panel(self, parent):
        """创建右侧聊天主面板"""
        # 聊天主容器
        chat_frame = tk.Frame(parent, bg="white", relief="sunken", bd=1)
        chat_frame.pack(side="left", fill="both", expand=True)
        
        # 聊天标题栏
        title_frame = tk.Frame(chat_frame, bg="#34495E", height=40)
        title_frame.pack(side="top", fill="x")
        title_frame.pack_propagate(False)
        
        self.chat_title_label = tk.Label(title_frame, 
                                        text="中考加油广播室",
                                        font=('Microsoft YaHei', 12, 'bold'), 
                                        bg="#34495E", fg="white")
        self.chat_title_label.pack(side="left", padx=15, pady=10)
        
        # 消息统计
        self.message_count_label = tk.Label(title_frame, 
                                           text="消息数: 0",
                                           font=('Microsoft YaHei', 9), 
                                           bg="#34495E", fg="#BDC3C7")
        self.message_count_label.pack(side="right", padx=15, pady=10)
        
        # 控制按钮区域
        control_frame = tk.Frame(chat_frame, bg="#ECF0F1", height=30)
        control_frame.pack(side="top", fill="x")
        control_frame.pack_propagate(False)
        
        # 刷新按钮
        refresh_btn = tk.Button(control_frame, 
                               text="🔄 刷新",
                               command=self.refresh_current_chat,
                               font=('Microsoft YaHei', 8),
                               bg="#3498DB", fg="white")
        refresh_btn.pack(side="left", padx=5, pady=2)
        
        # 自动刷新开关
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_btn = tk.Checkbutton(control_frame, 
                                         text="自动刷新",
                                         variable=self.auto_refresh_var,
                                         command=self.toggle_auto_refresh,
                                         font=('Microsoft YaHei', 8),
                                         bg="#ECF0F1")
        auto_refresh_btn.pack(side="left", padx=10, pady=2)
        
        # 搜索框
        search_frame = tk.Frame(control_frame, bg="#ECF0F1")
        search_frame.pack(side="right", padx=5, pady=2)
        
        self.search_entry = tk.Entry(search_frame, width=15, font=('Microsoft YaHei', 8))
        self.search_entry.pack(side="left", padx=2)
        self.search_entry.bind('<Return>', self.search_messages)
        
        search_btn = tk.Button(search_frame, 
                              text="🔍",
                              command=self.search_messages,
                              font=('Microsoft YaHei', 8),
                              bg="#27AE60", fg="white")
        search_btn.pack(side="left", padx=2)
        
        # 聊天记录显示区域
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state='disabled',
            font=('Microsoft YaHei', 10),
            padx=15,
            pady=10,
            bg="#F8F9F9",
            relief="flat"
        )
        self.chat_text.pack(fill="both", expand=True)
        
        # 消息输入区域
        input_frame = tk.Frame(chat_frame, bg="#ECF0F1", height=80)
        input_frame.pack(side="bottom", fill="x")
        input_frame.pack_propagate(False)
        
        # 输入框容器
        input_container = tk.Frame(input_frame, bg="#BDC3C7", relief="sunken", bd=1)
        input_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
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
        button_frame.pack(side="right", padx=5, pady=5)
        
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
        self.send_btn.pack(pady=2)
        
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
    
    def load_conversations(self):
        """加载会话列表"""
        if not self.chat_manager or not self.friend_manager:
            messagebox.showerror("错误", "聊天系统不可用")
            return
        
        # 清空现有会话列表
        for item in self.conversation_tree.get_children():
            self.conversation_tree.delete(item)
        
        # 获取用户最近会话
        recent_chats = self.chat_manager.get_recent_chats_for_user(self.username)
        
        # 添加广播室（始终显示在顶部）
        broadcast_item = None
        for chat in recent_chats:
            if chat.get("type") == "broadcast":
                broadcast_item = self.conversation_tree.insert("", "end", 
                                                             values=(chat["name"], "broadcast"),
                                                             tags=("broadcast",))
                break
        
        # 如果没有找到广播室，手动添加
        if not broadcast_item:
            broadcast_item = self.conversation_tree.insert("", "end", 
                                                         values=("中考加油广播室", "broadcast"),
                                                         tags=("broadcast",))
        
        # 添加个人聊天
        personal_chats = [chat for chat in recent_chats if chat.get("type") == "personal"]
        if personal_chats:
            personal_folder = self.conversation_tree.insert("", "end", 
                                                          values=("👥 好友聊天", "folder"),
                                                          tags=("folder",))
            for chat in personal_chats:
                self.conversation_tree.insert(personal_folder, "end", 
                                            values=(chat["name"], "personal"),
                                            tags=("personal",))
        
        # 添加群组聊天
        group_chats = [chat for chat in recent_chats if chat.get("type") == "group"]
        if group_chats:
            group_folder = self.conversation_tree.insert("", "end", 
                                                        values=("👨‍👩‍👧‍👦 我的群组", "folder"),
                                                        tags=("folder",))
            for chat in group_chats:
                self.conversation_tree.insert(group_folder, "end", 
                                            values=(chat["name"], "group"),
                                            tags=("group",))
        
        # 设置标签样式
        self.conversation_tree.tag_configure("broadcast", foreground="#2C3E50")
        self.conversation_tree.tag_configure("folder", foreground="#7F8C8D", font=('Microsoft YaHei', 9, 'bold'))
        self.conversation_tree.tag_configure("personal", foreground="#27AE60")
        self.conversation_tree.tag_configure("group", foreground="#3498DB")
        
        # 展开所有文件夹
        for folder in self.conversation_tree.get_children():
            self.conversation_tree.item(folder, open=True)
    
    def on_conversation_select(self, event):
        """会话选择事件"""
        selection = self.conversation_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.conversation_tree.item(item, "values")
        
        if not values:
            return
        
        chat_name = values[0]
        chat_type = values[1]
        
        # 如果是文件夹，不处理
        if chat_type == "folder":
            return
        
        # 根据会话类型切换聊天
        if chat_type == "broadcast":
            self.switch_to_broadcast()
        elif chat_type == "personal":
            self.switch_to_personal_chat(chat_name)
        elif chat_type == "group":
            # 这里需要根据群组名找到群组ID
            # 简化处理：在实际应用中应该存储更多信息
            self.switch_to_group_chat(chat_name)
    
    def switch_to_broadcast(self):
        """切换到广播室"""
        if self.friend_manager:
            self.current_chat_id = self.friend_manager.get_broadcast_room_id()
        else:
            self.current_chat_id = "BROADCAST_ROOM"
        
        self.current_chat_name = "中考加油广播室"
        self.current_chat_type = "broadcast"
        
        self.update_chat_display()
        self.refresh_current_chat()
    
    def switch_to_personal_chat(self, friend_name):
        """切换到个人聊天"""
        if not self.friend_manager:
            messagebox.showerror("错误", "好友系统不可用")
            return
        
        self.current_chat_id = self.friend_manager.get_personal_chat_id(self.username, friend_name)
        self.current_chat_name = f"与 {friend_name} 的聊天"
        self.current_chat_type = "personal"
        
        self.update_chat_display()
        self.refresh_current_chat()
    
    def switch_to_group_chat(self, group_name):
        """切换到群组聊天"""
        # 这里需要根据群组名找到群组ID
        # 简化处理：在实际应用中应该存储更多信息
        if not self.friend_manager:
            messagebox.showerror("错误", "好友系统不可用")
            return
        
        # 获取用户所在的群组列表
        user_groups = self.friend_manager.get_group_list(self.username)
        target_group = None
        
        for group in user_groups:
            if group["name"] == group_name:
                target_group = group
                break
        
        if target_group:
            self.current_chat_id = target_group["id"]
            self.current_chat_name = group_name
            self.current_chat_type = "group"
            
            self.update_chat_display()
            self.refresh_current_chat()
        else:
            messagebox.showerror("错误", f"未找到群组: {group_name}")
    
    def update_chat_display(self):
        """更新聊天显示"""
        self.chat_title_label.config(text=self.current_chat_name)
        self.current_chat_label.config(text=f"当前会话: {self.current_chat_name}")
    
    def refresh_current_chat(self):
        """刷新当前聊天记录"""
        if not self.chat_manager or not self.current_chat_id:
            return
        
        try:
            # 获取当前会话的聊天记录
            messages = self.chat_manager.get_chat_history(self.current_chat_id)
            
            # 更新消息计数
            self.message_count_label.config(text=f"消息数: {len(messages)}")
            
            # 允许编辑
            self.chat_text.config(state='normal')
            self.chat_text.delete('1.0', tk.END)
            
            if not messages:
                # 显示欢迎信息
                if self.current_chat_type == "broadcast":
                    welcome_msg = """💬 欢迎来到中考加油广播室！

这里是所有同学都可以参与的公共聊天区域。

✨ 你可以在这里：
• 与所有同学交流学习心得
• 分享备考经验
• 互相鼓励支持
• 获取每日鼓励语录

发出第一条消息，开始你的中考加油之旅吧！"""
                elif self.current_chat_type == "personal":
                    welcome_msg = f"""💬 与好友的私密聊天

这里是您和好友的私人聊天空间。

💡 提示：
• 只有您和好友能看到这里的消息
• 可以畅所欲言，互相鼓励
• 共同进步，冲刺中考！"""
                else:  # group
                    welcome_msg = f"""💬 群组聊天: {self.current_chat_name}

这里是群组成员的专属聊天空间。

👥 群组成员可以：
• 讨论学习问题
• 分享学习资源
• 互相监督学习进度
• 共同备战中考！"""
                
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
            
            # 设置不同消息类型的样式
            self.chat_text.tag_config("welcome", 
                                     foreground="#7F8C8D", 
                                     font=('Microsoft YaHei', 10, 'italic'),
                                     justify='center')
            self.chat_text.tag_config("system", 
                                     foreground="#7F8C8D", 
                                     font=('Microsoft YaHei', 9, 'italic'))
            self.chat_text.tag_config("self", 
                                     foreground="#2C3E50", 
                                     font=('Microsoft YaHei', 10))
            self.chat_text.tag_config("other", 
                                     foreground="#2C3E50", 
                                     font=('Microsoft YaHei', 10))
            
            # 禁用编辑并滚动到底部
            self.chat_text.config(state='disabled')
            self.chat_text.see(tk.END)
            
        except Exception as e:
            print(f"刷新聊天记录时出错: {e}")
            self.chat_text.config(state='normal')
            self.chat_text.delete('1.0', tk.END)
            self.chat_text.insert(tk.END, f"❌ 加载聊天记录时出错: {e}\n")
            self.chat_text.config(state='disabled')
    
    # 以下方法保持不变，与基础版gui.py相同
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
                success, result = self.chat_manager.send_message(self.username, content, self.current_chat_id)
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
            self.refresh_current_chat()
            
            # 显示成功反馈
            self.send_btn.config(text="✅ 成功", bg="#2ECC71")
            self.master.after(1000, self.reset_send_button)
        else:
            messagebox.showerror("发送失败", result)
            self.reset_send_button()
    
    def reset_send_button(self):
        """重置发送按钮状态"""
        self.send_btn.config(state='normal', text="📤 发送", bg="#27AE60")
    
    def update_info_display(self):
        """更新顶部信息显示"""
        try:
            # 更新倒计时
            if COUNTDOWN_AVAILABLE:
                days = countdown.get_days_left()
                self.days_label.config(text=f"📅 距离中考还有 {days} 天")
            else:
                self.days_label.config(text="📅 倒计时功能暂不可用")
                
        except Exception as e:
            print(f"更新信息显示时出错: {e}")
    
    def toggle_auto_refresh(self):
        """切换自动刷新"""
        self.auto_refresh = self.auto_refresh_var.get()
    
    def start_auto_refresh(self):
        """开始自动刷新"""
        if self.auto_refresh and not self.is_closing:
            self.refresh_current_chat()
            self.master.after(30000, self.start_auto_refresh)  # 30秒后再次刷新
    
    def search_messages(self, event=None):
        """搜索消息"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("搜索", "请输入搜索关键词！")
            return
        
        try:
            if self.chat_manager:
                results = self.chat_manager.search_messages(keyword, self.current_chat_id)
                if results:
                    # 显示搜索结果
                    self.chat_text.config(state='normal')
                    self.chat_text.delete('1.0', tk.END)
                    
                    for msg in results:
                        sender = msg.get('sender', '未知用户')
                        content = msg.get('content', '')
                        timestamp = msg.get('timestamp', '')
                        
                        # 格式化时间
                        try:
                            time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                            display_time = time_obj.strftime("%m/%d %H:%M")
                        except:
                            display_time = timestamp
                        
                        display_line = f"[{display_time}] {sender}: {content}\n\n"
                        self.chat_text.insert(tk.END, display_line)
                    
                    self.chat_text.config(state='disabled')
                    messagebox.showinfo("搜索结果", f"找到 {len(results)} 条包含 '{keyword}' 的消息")
                else:
                    messagebox.showinfo("搜索结果", f"没有找到包含 '{keyword}' 的消息")
                    self.refresh_current_chat()  # 恢复显示所有消息
            else:
                messagebox.showerror("错误", "搜索功能暂不可用")
        except Exception as e:
            messagebox.showerror("搜索错误", f"搜索时出错: {e}")
    
    def show_add_friend_dialog(self):
        """显示添加好友对话框"""
        messagebox.showinfo("功能开发中", "添加好友功能正在开发中...")
    
    def show_create_group_dialog(self):
        """显示创建群组对话框"""
        messagebox.showinfo("功能开发中", "创建群组功能正在开发中...")
    
    def logout(self):
        """注销用户"""
        if messagebox.askyesno("确认注销", "确定要注销当前账号并返回登录界面吗？"):
            # 调用UserManager的logout方法记录注销事件
            try:
                from login import UserManager
                user_manager = UserManager()
                user_manager.logout(self.username)
            except Exception as e:
                print(f"⚠️ 记录注销事件时出错: {e}")
            
            print(f"👋 用户 {self.username} 注销")
            self.is_closing = True
            self.master.destroy()
            
            # 重新启动增强版登录界面
            try:
                from login_gui_enhanced import start_enhanced_login
                start_enhanced_login()
            except ImportError as e:
                print(f"❌ 无法启动增强版登录界面: {e}")
                # 尝试启动基础版作为备选
                try:
                    from login_gui import start_login_gui
                    start_login_gui()
                except ImportError as e2:
                    print(f"❌ 无法启动任何登录界面: {e2}")
                    messagebox.showerror("错误", "无法返回登录界面，请重新启动程序")
    
    def on_closing(self):
        """关闭窗口事件"""
        self.is_closing = True
        if messagebox.askokcancel("退出", "确定要退出中考加油聊天室吗？"):
            print("👋 退出中考加油聊天室")
            self.master.destroy()

def start_enhanced_app(username="同学"):
    """
    启动增强版应用程序
    """
    print(f"🎉 欢迎 {username} 使用增强版聊天室！")
    print("💡 新功能：多会话支持（广播室 + 个人聊天 + 群组聊天）")
    
    try:
        root = tk.Tk()
        
        # 设置窗口大小和位置
        root.geometry("1000x700")
        root.minsize(800, 500)
        
        # 创建应用
        app = EnhancedApplication(master=root, username=username)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("启动错误", f"启动增强版应用程序时出错: {e}")
        print(f"❌ 启动错误: {e}")

# 测试函数
def test_enhanced_gui():
    """测试增强版GUI"""
    start_enhanced_app("测试用户")

if __name__ == '__main__':
    test_enhanced_gui()