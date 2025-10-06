# login_gui_enhanced.py - 修复版
import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔐 加载增强版用户管理系统...")

class EnhancedLoginApp:
    """
    增强版用户管理GUI系统
    """
    
    def __init__(self, main_manager=None):
        self.root = tk.Tk()
        self.root.title("中考加油聊天室 - 增强版")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.center_window()
        
        self.main_manager = main_manager
        
        # 初始化用户管理器
        try:
            if main_manager is not None:
                # 在模块化环境中，从main_manager获取user_manager
                self.user_manager = main_manager.get_manager('user')
                print("✅ 从主管理器加载用户管理器成功")
            else:
                # 独立运行模式，直接导入UserManager
                from UserManager import UserManager
                self.user_manager = UserManager()
                print("✅ 独立加载用户管理器成功")
        except Exception as e:
            print(f"❌ 用户管理器加载失败: {e}")
            self.user_manager = None
        
        self.current_user = None
        self.create_welcome_screen()
    
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
        
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=40)
        main_frame.pack(fill="both", expand=True)
        
        # 图标和标题
        icon_label = tk.Label(main_frame, text="🚀", font=('Arial', 48), bg="#f5f5f5")
        icon_label.pack(pady=20)
        
        title_label = tk.Label(main_frame, 
                              text="中考加油聊天室",
                              font=('Microsoft YaHei', 24, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(main_frame,
                                 text="增强版 - 多会话聊天系统",
                                 font=('Microsoft YaHei', 12, 'bold'),
                                 fg="#3498DB",
                                 bg="#f5f5f5")
        subtitle_label.pack(pady=5)
        
        # 新功能特性
        features_frame = tk.Frame(main_frame, bg="#f5f5f5")
        features_frame.pack(pady=20, fill="x")
        
        features = [
            "🎯 广播室 - 与所有同学交流",
            "👥 个人聊天 - 与好友私密对话", 
            "👨‍👩‍👧‍👦 群组聊天 - 创建学习小组",
            "💬 多会话切换 - 同时管理多个聊天"
        ]
        
        for feature in features:
            feature_label = tk.Label(features_frame,
                                   text=feature,
                                   font=('Microsoft YaHei', 10),
                                   fg="#2C3E50",
                                   bg="#f5f5f5",
                                   anchor="w")
            feature_label.pack(fill="x", pady=3)
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(pady=30)
        
        # 登录按钮
        login_btn = tk.Button(button_frame,
                             text="🔐 登录账号",
                             command=self.show_login_form,
                             font=('Microsoft YaHei', 12, 'bold'),
                             bg="#3498DB",
                             fg="white",
                             width=20,
                             height=2)
        login_btn.pack(pady=10)
        
        # 注册按钮
        register_btn = tk.Button(button_frame,
                                text="📝 注册新账号",
                                command=self.show_register_form,
                                font=('Microsoft YaHei', 12),
                                bg="#27AE60",
                                fg="white",
                                width=20,
                                height=2)
        register_btn.pack(pady=10)
        
        # 游客体验
        guest_btn = tk.Button(button_frame,
                             text="👀 游客体验",
                             command=self.guest_login,
                             font=('Microsoft YaHei', 11),
                             bg="#95A5A6",
                             fg="white",
                             width=20,
                             height=2)
        guest_btn.pack(pady=10)
        
        # 统计信息
        info_frame = tk.Frame(main_frame, bg="#f5f5f5")
        info_frame.pack(pady=20)
        
        if self.user_manager:
            user_count = self.user_manager.get_user_count()
            count_label = tk.Label(info_frame,
                                  text=f"👥 已有 {user_count} 位同学加入",
                                  font=('Microsoft YaHei', 10),
                                  fg="#7F8C8D",
                                  bg="#f5f5f5")
            count_label.pack()
    
    def show_login_form(self):
        """显示登录表单"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # 返回按钮
        back_btn = tk.Button(main_frame,
                            text="← 返回",
                            command=self.create_welcome_screen,
                            font=('Microsoft YaHei', 9),
                            bg="#BDC3C7",
                            fg="white")
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # 标题
        title_label = tk.Label(main_frame,
                              text="🔐 登录账号",
                              font=('Microsoft YaHei', 20, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=20)
        
        # 登录表单
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(pady=20)
        
        # 用户名
        user_frame = tk.Frame(form_frame, bg="#f5f5f5")
        user_frame.pack(fill="x", pady=15)
        
        tk.Label(user_frame, text="用户名:", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.login_username = tk.Entry(user_frame, 
                                      font=('Microsoft YaHei', 12))
        self.login_username.pack(fill="x", pady=5, ipady=8)
        self.login_username.focus()
        
        # 密码
        pass_frame = tk.Frame(form_frame, bg="#f5f5f5")
        pass_frame.pack(fill="x", pady=15)
        
        tk.Label(pass_frame, text="密码:", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.login_password = tk.Entry(pass_frame, 
                                      font=('Microsoft YaHei', 12),
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
                                  height=2)
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
        
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # 返回按钮
        back_btn = tk.Button(main_frame,
                            text="← 返回",
                            command=self.create_welcome_screen,
                            font=('Microsoft YaHei', 9),
                            bg="#BDC3C7",
                            fg="white")
        back_btn.pack(anchor="w", pady=(0, 20))
        
        # 标题
        title_label = tk.Label(main_frame,
                              text="📝 注册新账号",
                              font=('Microsoft YaHei', 20, 'bold'),
                              fg="#2C3E50",
                              bg="#f5f5f5")
        title_label.pack(pady=20)
        
        # 注册表单
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(pady=20)
        
        # 用户名
        user_frame = tk.Frame(form_frame, bg="#f5f5f5")
        user_frame.pack(fill="x", pady=10)
        
        tk.Label(user_frame, text="用户名 (3-15个字符):", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.register_username = tk.Entry(user_frame, 
                                        font=('Microsoft YaHei', 12))
        self.register_username.pack(fill="x", pady=5, ipady=8)
        self.register_username.focus()
        
        # 密码
        pass_frame = tk.Frame(form_frame, bg="#f5f5f5")
        pass_frame.pack(fill="x", pady=10)
        
        tk.Label(pass_frame, text="密码 (至少4个字符):", 
                font=('Microsoft YaHei', 11),
                bg="#f5f5f5").pack(anchor="w")
        
        self.register_password = tk.Entry(pass_frame, 
                                        font=('Microsoft YaHei', 12),
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
                                     height=2)
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
        
        self.login_btn.config(state='disabled', text="登录中...")
        
        thread = threading.Thread(target=self._login_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _login_thread(self, username, password):
        """后台登录线程"""
        try:
            success, message = self.user_manager.login(username, password)
            self.root.after(0, lambda: self._login_complete(success, message, username))
        except Exception as e:
            self.root.after(0, lambda: self._login_complete(False, str(e), username))
    
    def _login_complete(self, success, message, username):
        """登录完成处理"""
        if success:
            self.current_user = username
            messagebox.showinfo("登录成功", f"{message}\n\n欢迎使用增强版聊天室！")
            self.enter_enhanced_chatroom()
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
        
        self.register_btn.config(state='disabled', text="注册中...")
        
        thread = threading.Thread(target=self._register_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _register_thread(self, username, password):
        """后台注册线程"""
        try:
            success, message = self.user_manager.register(username, password)
            self.root.after(0, lambda: self._register_complete(success, message, username))
        except Exception as e:
            self.root.after(0, lambda: self._register_complete(False, str(e), username))
    
    def _register_complete(self, success, message, username):
        """注册完成处理"""
        if success:
            messagebox.showinfo("注册成功", f"{message}\n\n已自动登录！")
            self.current_user = username
            self.enter_enhanced_chatroom()
        else:
            messagebox.showerror("注册失败", message)
            self.register_btn.config(state='normal', text="注册")
    
    def guest_login(self):
        """游客登录"""
        if messagebox.askyesno("游客模式", "将以游客身份体验增强版功能，确定继续吗？"):
            self.current_user = "游客"
            self.enter_enhanced_chatroom()
    
    def enter_enhanced_chatroom(self):
        """进入增强版聊天室"""
        if not self.current_user:
            return
        
        print(f"🚀 用户 {self.current_user} 进入增强版聊天室")
        self.root.destroy()
        
        # 导入并启动增强版GUI
        try:
            # 先检查增强版GUI是否存在
            if not os.path.exists('gui_enhanced.py'):
                raise ImportError("增强版GUI文件不存在")
                
            from gui_enhanced import start_enhanced_app
            start_enhanced_app(self.current_user)
        except ImportError as e:
            print(f"❌ 无法启动增强版: {e}")
            # 尝试启动基础版
            try:
                from gui import start_main_app
                messagebox.showinfo("提示", "增强版不可用，正在启动基础版...")
                start_main_app(self.current_user)
            except ImportError as e2:
                messagebox.showerror("错误", f"所有版本都启动失败: {e2}")
        except Exception as e:
            messagebox.showerror("启动错误", f"启动增强版时出错: {e}")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

# 添加缺失的 start_enhanced_login 函数
def start_enhanced_login(main_manager=None):
    """
    启动增强版登录系统
    
    参数:
    - main_manager: 可选的主管理器实例，用于在模块化环境中运行
    """
    print("🎯 中考加油聊天室 - 增强版")
    app = EnhancedLoginApp(main_manager)
    app.run()

if __name__ == '__main__':
    start_enhanced_login()