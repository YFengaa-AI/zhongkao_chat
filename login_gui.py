# login_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import threading
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔐 加载用户管理系统...")

# 初始化主管理器
try:
    from MainManager import MainManager
    main_manager = MainManager()
    print("✅ 主管理器加载成功")
except Exception as e:
    print(f"❌ 主管理器加载失败: {e}")
    main_manager = None

class LoginApp:
    """
    完整的用户管理GUI系统 - 登录、注册、用户管理
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("中考加油聊天室 - 用户系统")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # 设置图标和位置
        self.center_window()
        
        # 初始化用户管理器 - 使用模块化系统或降级方案
        if main_manager:
            self.user_manager = main_manager.get_manager('login')
            print("✅ 使用模块化用户管理器")
        else:
            # 降级方案：尝试直接使用UserManager
            try:
                from UserManager import UserManager
                self.user_manager = UserManager()
                print("✅ 降级模式：用户管理器加载成功")
            except Exception as e:
                print(f"❌ 降级模式：用户管理器加载失败: {e}")
                self.user_manager = None
                messagebox.showerror("错误", f"用户系统初始化失败: {e}")
        
        # 当前用户信息
        self.current_user = None
        
        # 创建界面
        self.create_welcome_screen()
        
        # 检查系统状态
        self.check_system_status()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_window(self):
        """清空窗口内容"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_welcome_screen(self):
        """创建欢迎屏幕"""
        self.clear_window()
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=40)
        main_frame.pack(fill="both", expand=True)
        
        # 应用图标和标题
        icon_label = tk.Label(main_frame, text="🎯", font=('Arial', 48), bg="#f5f5f5")
        icon_label.pack(pady=20)
        
        title_label = tk.Label(main_frame, 
                              text="中考加油聊天室",
                              font=('Microsoft YaHei', 24, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(main_frame,
                                 text="与同学一起加油，冲刺中考！",
                                 font=('Microsoft YaHei', 12),
                                 fg="#7F8C8D",
                                 bg="#f5f5f5")
        subtitle_label.pack(pady=5)
        
        # 功能按钮框架
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(pady=40)
        
        # 登录按钮
        login_btn = tk.Button(button_frame,
                             text="🔐 登录账号",
                             command=self.show_login_form,
                             font=('Microsoft YaHei', 12, 'bold'),
                             bg="#3498DB",
                             fg="white",
                             width=20,
                             height=2,
                             cursor="hand2")
        login_btn.pack(pady=10)
        
        # 注册按钮
        register_btn = tk.Button(button_frame,
                                text="📝 注册新账号",
                                command=self.show_register_form,
                                font=('Microsoft YaHei', 12),
                                bg="#27AE60",
                                fg="white",
                                width=20,
                                height=2,
                                cursor="hand2")
        register_btn.pack(pady=10)
        
        # 游客体验按钮
        guest_btn = tk.Button(button_frame,
                             text="👀 游客体验",
                             command=self.guest_login,
                             font=('Microsoft YaHei', 11),
                             bg="#95A5A6",
                             fg="white",
                             width=20,
                             height=2,
                             cursor="hand2")
        guest_btn.pack(pady=10)
        
        # 系统信息
        info_frame = tk.Frame(main_frame, bg="#f5f5f5")
        info_frame.pack(pady=20)
        
        # 显示用户统计
        if self.user_manager:
            user_count = self.user_manager.get_user_count()
            count_label = tk.Label(info_frame,
                                  text=f"👥 已有 {user_count} 位同学加入",
                                  font=('Microsoft YaHei', 10),
                                  fg="#7F8C8D",
                                  bg="#f5f5f5")
            count_label.pack()
        
        # 版本信息
        version_label = tk.Label(info_frame,
                                text="版本 1.0 | 中考加油！",
                                font=('Microsoft YaHei', 9),
                                fg="#BDC3C7",
                                bg="#f5f5f5")
        version_label.pack(pady=5)
    
    def show_login_form(self):
        """显示登录表单"""
        self.clear_window()
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # 返回按钮
        back_btn = tk.Button(main_frame,
                            text="← 返回",
                            command=self.create_welcome_screen,
                            font=('Microsoft YaHei', 9),
                            bg="#BDC3C7",
                            fg="white",
                            cursor="hand2")
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # 标题
        title_label = tk.Label(main_frame,
                              text="🔐 登录账号",
                              font=('Microsoft YaHei', 20, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=20)
        
        # 登录表单容器
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(pady=20)
        
        # 用户名输入
        user_frame = tk.Frame(form_frame, bg="#f5f5f5")
        user_frame.pack(fill="x", pady=15)
        
        tk.Label(user_frame, text="用户名:", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.login_username = tk.Entry(user_frame, 
                                      font=('Microsoft YaHei', 12),
                                      width=25)
        self.login_username.pack(fill="x", pady=5, ipady=8)
        self.login_username.focus()
        
        # 密码输入
        pass_frame = tk.Frame(form_frame, bg="#f5f5f5")
        pass_frame.pack(fill="x", pady=15)
        
        tk.Label(pass_frame, text="密码:", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.login_password = tk.Entry(pass_frame, 
                                      font=('Microsoft YaHei', 12),
                                      width=25,
                                      show="•")
        self.login_password.pack(fill="x", pady=5, ipady=8)
        
        # 登录按钮
        self.login_btn = tk.Button(form_frame,
                                  text="登录",
                                  command=self.login,
                                  font=('Microsoft YaHei', 12, 'bold'),
                                  bg="#3498DB",
                                  fg="white",
                                  width=20,
                                  height=2,
                                  cursor="hand2")
        self.login_btn.pack(pady=20)
        
        # 绑定回车键
        self.root.bind('<Return>', lambda e: self.login())
        
        # 注册提示
        register_label = tk.Label(main_frame,
                                 text="还没有账号？点击注册",
                                 font=('Microsoft YaHei', 10),
                                 fg="#3498DB",
                                 bg="#f5f5f5",
                                 cursor="hand2")
        register_label.pack(pady=10)
        register_label.bind("<Button-1>", lambda e: self.show_register_form())
    
    def show_register_form(self):
        """显示注册表单"""
        self.clear_window()
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # 返回按钮
        back_btn = tk.Button(main_frame,
                            text="← 返回",
                            command=self.create_welcome_screen,
                            font=('Microsoft YaHei', 9),
                            bg="#BDC3C7",
                            fg="white",
                            cursor="hand2")
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # 标题
        title_label = tk.Label(main_frame,
                              text="📝 注册新账号",
                              font=('Microsoft YaHei', 20, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=20)
        
        # 注册表单容器
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(pady=20)
        
        # 用户名输入
        user_frame = tk.Frame(form_frame, bg="#f5f5f5")
        user_frame.pack(fill="x", pady=10)
        
        tk.Label(user_frame, text="用户名 (3-15个字符):", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.register_username = tk.Entry(user_frame, 
                                        font=('Microsoft YaHei', 12),
                                        width=25)
        self.register_username.pack(fill="x", pady=5, ipady=8)
        self.register_username.focus()
        
        # 密码输入
        pass_frame = tk.Frame(form_frame, bg="#f5f5f5")
        pass_frame.pack(fill="x", pady=10)
        
        tk.Label(pass_frame, text="密码 (至少4个字符):", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.register_password = tk.Entry(pass_frame, 
                                        font=('Microsoft YaHei', 12),
                                        width=25,
                                        show="•")
        self.register_password.pack(fill="x", pady=5, ipady=8)
        
        # 确认密码
        confirm_frame = tk.Frame(form_frame, bg="#f5f5f5")
        confirm_frame.pack(fill="x", pady=10)
        
        tk.Label(confirm_frame, text="确认密码:", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.register_confirm = tk.Entry(confirm_frame, 
                                       font=('Microsoft YaHei', 12),
                                       width=25,
                                       show="•")
        self.register_confirm.pack(fill="x", pady=5, ipady=8)
        
        # 注册按钮
        self.register_btn = tk.Button(form_frame,
                                     text="注册",
                                     command=self.register,
                                     font=('Microsoft YaHei', 12, 'bold'),
                                     bg="#27AE60",
                                     fg="white",
                                     width=20,
                                     height=2,
                                     cursor="hand2")
        self.register_btn.pack(pady=20)
        
        # 绑定回车键
        self.root.bind('<Return>', lambda e: self.register())
        
        # 登录提示
        login_label = tk.Label(main_frame,
                              text="已有账号？点击登录",
                              font=('Microsoft YaHei', 10),
                              fg="#3498DB",
                              bg="#f5f5f5",
                              cursor="hand2")
        login_label.pack(pady=10)
        login_label.bind("<Button-1>", lambda e: self.show_login_form())
    
    def show_user_profile(self):
        """显示用户个人信息页面"""
        self.clear_window()
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # 返回按钮
        back_btn = tk.Button(main_frame,
                            text="← 返回",
                            command=self.create_welcome_screen,
                            font=('Microsoft YaHei', 9),
                            bg="#BDC3C7",
                            fg="white",
                            cursor="hand2")
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # 标题
        title_label = tk.Label(main_frame,
                              text="👤 个人信息",
                              font=('Microsoft YaHei', 20, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=20)
        
        # 信息卡片
        card_frame = tk.Frame(main_frame, bg="white", relief="raised", bd=1)
        card_frame.pack(fill="x", pady=20, ipadx=20, ipady=20)
        
        # 用户头像和基本信息
        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(fill="x", pady=10)
        
        # 头像
        avatar_label = tk.Label(info_frame, text="👤", font=('Arial', 24), bg="white")
        avatar_label.pack(side="left", padx=20)
        
        # 用户信息
        user_info_frame = tk.Frame(info_frame, bg="white")
        user_info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = tk.Label(user_info_frame, 
                             text=self.current_user,
                             font=('Microsoft YaHei', 16, 'bold'),
                             bg="white",
                             fg="#2C3E50")
        name_label.pack(anchor="w")
        
        join_label = tk.Label(user_info_frame,
                             text=f"注册时间: {datetime.now().strftime('%Y-%m-%d')}",
                             font=('Microsoft YaHei', 10),
                             bg="white",
                             fg="#7F8C8D")
        join_label.pack(anchor="w", pady=(5, 0))
        
        # 统计信息
        stats_frame = tk.Frame(card_frame, bg="white")
        stats_frame.pack(fill="x", pady=20)
        
        # 消息统计
        try:
            from chat import ChatManager
            chat_mgr = ChatManager()
            user_messages = chat_mgr.get_user_messages(self.current_user)
            message_count = len(user_messages)
        except:
            message_count = 0
        
        stats_text = f"📊 已发送 {message_count} 条消息"
        stats_label = tk.Label(stats_frame,
                              text=stats_text,
                              font=('Microsoft YaHei', 11),
                              bg="white",
                              fg="#2C3E50")
        stats_label.pack()
        
        # 操作按钮
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(pady=30)
        
        # 进入聊天室按钮
        chat_btn = tk.Button(button_frame,
                            text="💬 进入聊天室",
                            command=self.enter_chatroom,
                            font=('Microsoft YaHei', 12, 'bold'),
                            bg="#3498DB",
                            fg="white",
                            width=20,
                            height=2,
                            cursor="hand2")
        chat_btn.pack(pady=10)
        
        # 注销按钮
        logout_btn = tk.Button(button_frame,
                              text="🚪 注销账号",
                              command=self.logout,
                              font=('Microsoft YaHei', 11),
                              bg="#E74C3C",
                              fg="white",
                              width=15,
                              height=1,
                              cursor="hand2")
        logout_btn.pack(pady=5)
    
    def login(self):
        """登录操作"""
        if not self.user_manager:
            messagebox.showerror("错误", "用户系统不可用")
            return
        
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("输入提示", "请输入用户名和密码")
            return
        
        # 禁用登录按钮
        self.login_btn.config(state='disabled', text="登录中...")
        
        # 在后台线程中登录
        thread = threading.Thread(target=self._login_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _login_thread(self, username, password):
        """后台登录线程"""
        try:
            # 兼容不同的登录方法名
            if hasattr(self.user_manager, 'login_user'):
                success, message = self.user_manager.login_user(username, password)
            elif hasattr(self.user_manager, 'login'):
                success, message = self.user_manager.login(username, password)
            elif hasattr(self.user_manager, 'verify_user'):
                # 最简单的验证方法
                if self.user_manager.verify_user(username, password):
                    success, message = True, f"欢迎回来，{username}！"
                else:
                    success, message = False, "用户名或密码错误！"
            else:
                success, message = False, "登录方法不支持"
            
            self.root.after(0, lambda: self._login_complete(success, message, username))
        except Exception as e:
            self.root.after(0, lambda: self._login_complete(False, str(e), username))
    
    def _login_complete(self, success, message, username):
        """登录完成处理"""
        if success:
            self.current_user = username
            messagebox.showinfo("登录成功", message)
            self.show_user_profile()
        else:
            messagebox.showerror("登录失败", message)
            self.login_btn.config(state='normal', text="登录")
    
    def register(self):
        """注册操作"""
        if not self.user_manager:
            messagebox.showerror("错误", "用户系统不可用")
            return
        
        username = self.register_username.get().strip()
        password = self.register_password.get().strip()
        confirm = self.register_confirm.get().strip()
        
        # 输入验证
        if not username or not password:
            messagebox.showwarning("输入提示", "请输入用户名和密码")
            return
        
        if len(username) < 3 or len(username) > 15:
            messagebox.showwarning("输入提示", "用户名长度应为3-15个字符")
            return
        
        if len(password) < 4:
            messagebox.showwarning("输入提示", "密码长度至少为4个字符")
            return
        
        if password != confirm:
            messagebox.showwarning("输入提示", "两次输入的密码不一致")
            return
        
        # 禁用注册按钮
        self.register_btn.config(state='disabled', text="注册中...")
        
        # 在后台线程中注册
        thread = threading.Thread(target=self._register_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _register_thread(self, username, password):
        """后台注册线程"""
        try:
            # 兼容不同的注册方法名
            if hasattr(self.user_manager, 'register_user'):
                success, message = self.user_manager.register_user(username, password)
            elif hasattr(self.user_manager, 'register'):
                success, message = self.user_manager.register(username, password)
            elif hasattr(self.user_manager, 'add_user'):
                # 最简单的添加用户方法
                if not hasattr(self.user_manager, 'is_username_taken') or not self.user_manager.is_username_taken(username):
                    self.user_manager.add_user(username, password)
                    success, message = True, "注册成功！"
                else:
                    success, message = False, "用户名已存在！"
            else:
                success, message = False, "注册方法不支持"
            
            self.root.after(0, lambda: self._register_complete(success, message, username))
        except Exception as e:
            self.root.after(0, lambda: self._register_complete(False, str(e), username))
    
    def _register_complete(self, success, message, username):
        """注册完成处理"""
        if success:
            messagebox.showinfo("注册成功", message)
            # 自动登录
            self.current_user = username
            self.show_user_profile()
        else:
            messagebox.showerror("注册失败", message)
            self.register_btn.config(state='normal', text="注册")
    
    def guest_login(self):
        """游客登录"""
        if messagebox.askyesno("游客模式", 
                              "将以游客身份进入聊天室：\n\n• 可以体验基本功能\n• 无法保存个人消息记录\n• 部分功能可能受限\n\n确定继续吗？"):
            self.current_user = "游客"
            self.enter_chatroom()
    
    def enter_chatroom(self):
        """进入聊天室"""
        if not self.current_user:
            messagebox.showwarning("提示", "请先登录或选择游客模式")
            return
        
        print(f"🚀 用户 {self.current_user} 进入聊天室")
        self.root.destroy()
        
        # 启动主聊天应用
        try:
            # 优先使用模块化方式
            if main_manager:
                main_manager.login.current_user = self.current_user
                print("✅ 使用模块化方式启动聊天室")
            
            # 尝试启动不同的聊天应用入口
            try:
                from gui import start_main_app
                start_main_app(self.current_user)
            except ImportError:
                # 尝试其他入口
                from gui import start_chat_gui
                start_chat_gui(self.current_user)
        except Exception as e:
            messagebox.showerror("启动错误", f"无法启动聊天室: {e}")
    
    def logout(self):
        """注销账号"""
        if messagebox.askyesno("确认注销", "确定要注销当前账号吗？"):
            # 调用Logout模块进行注销处理
            if main_manager:
                logout_manager = main_manager.get_manager('logout')
                if logout_manager:
                    logout_manager.logout_user(self.current_user)
            
            self.current_user = None
            self.create_welcome_screen()
    
    def check_system_status(self):
        """检查系统状态"""
        status_messages = []
        
        # 检查模块化文件结构
        module_files = [
            'MainManager.py', 'UserManager.py', 'ChatManager.py', 'FriendManager.py', 
            'GUIManager.py', 'Login.py', 'Logout.py', 'Register.py', 
            'Chat.py', 'Friend.py', 'Group.py', 'Countdown.py', 'Encouragement.py'
        ]
        
        for file in module_files:
            if os.path.exists(file):
                status_messages.append(f"✅ {file}")
            else:
                status_messages.append(f"❌ {file} 缺失")
        
        # 检查基础功能文件
        basic_files = ['countdown.py', 'encouragement.py', 'chat.py', 'login.py', 'gui.py']
        for file in basic_files:
            if file not in module_files:
                if os.path.exists(file):
                    status_messages.append(f"✅ 基础文件: {file}")
                else:
                    status_messages.append(f"❌ 基础文件: {file} 缺失")
        
        # 检查数据目录
        if not os.path.exists('data'):
            try:
                os.makedirs('data')
                status_messages.append("✅ 创建数据目录")
            except Exception as e:
                status_messages.append(f"❌ 创建数据目录失败: {e}")
        else:
            status_messages.append("✅ 数据目录正常")
        
        # 如果有严重错误，显示警告
        if any("❌" in msg for msg in status_messages):
            print("⚠️ 系统状态警告:")
            for msg in status_messages:
                if "❌" in msg:
                    print(f"   {msg}")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

def start_login_gui():
    """
    启动登录GUI系统
    """
    print("🎯 中考加油聊天室 - 用户管理系统")
    print("💡 正在启动登录界面...")
    
    app = LoginApp()
    app.run()

if __name__ == '__main__':
    start_login_gui()