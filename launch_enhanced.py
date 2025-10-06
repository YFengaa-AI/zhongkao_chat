# launch_enhanced.py
#!/usr/bin/env python3
"""
中考加油聊天室 - 备用启动器
直接启动增强版登录界面
"""
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 启动中考加油聊天室 - 增强版")
    print("=" * 50)
    
    try:
        # 检查必要文件
        if not os.path.exists('login_gui_enhanced.py'):
            raise ImportError("增强版登录界面文件不存在")
        
        # 导入并启动增强版登录系统
        from login_gui_enhanced import start_enhanced_login
        start_enhanced_login()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        
        # 尝试启动基础版
        try:
            if os.path.exists('login_gui.py'):
                from login_gui import start_login_gui
                print("🔄 启动基础版系统...")
                start_login_gui()
            else:
                raise ImportError("基础版系统也不可用")
        except ImportError as e2:
            print(f"❌ 所有版本都启动失败: {e2}")
            input("按回车键退出...")
            
    except Exception as e:
        print(f"❌ 启动时发生错误: {e}")
        input("按回车键退出...")

if __name__ == '__main__':
    main()