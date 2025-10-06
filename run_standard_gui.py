#!/usr/bin/env python3
"""
中考加油聊天室 - 标准GUI启动脚本
专门用于启动标准登录界面（用户提供的截图版本）
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """检查系统依赖"""
    print("🔍 检查系统依赖...")
    
    dependencies = {
        'countdown.py': '倒计时功能',
        'encouragement.py': '鼓励语录功能', 
        'login.py': '用户登录功能',
        'chat.py': '聊天功能',
        'gui.py': '聊天界面',
        'login_gui.py': '用户管理界面（标准版）'
    }
    
    all_ok = True
    for file, description in dependencies.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
        else:
            print(f"❌ {file} - {description} 缺失")
            all_ok = False
    
    # 检查数据目录
    if not os.path.exists('data'):
        print("📁 创建数据目录...")
        try:
            os.makedirs('data')
            print("✅ 数据目录创建成功")
        except Exception as e:
            print(f"❌ 创建数据目录失败: {e}")
            all_ok = False
    else:
        print("✅ 数据目录已存在")
    
    return all_ok

def main():
    """主函数"""
    print("🚀 启动中考加油聊天室 - 标准GUI版本")
    print("=" * 50)
    
    # 确保当前目录在Python路径中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # 检查依赖
    if not check_dependencies():
        print("\n⚠️ 系统依赖不完整，部分功能可能无法使用")
        if not messagebox.askyesno("依赖警告", "系统检测到部分文件缺失，是否继续启动？"):
            return
    
    # 启动标准用户管理GUI
    try:
        from login_gui import start_login_gui
        print("🎯 正在启动标准登录界面...")
        start_login_gui()
    except ImportError as e:
        print(f"❌ 无法启动标准用户界面: {e}")
        messagebox.showerror("启动错误", f"无法启动标准用户界面: {e}")
    except Exception as e:
        import traceback
        print(f"❌ 启动时发生错误: {e}")
        print(f"📋 错误详情: {traceback.format_exc()}")
        messagebox.showerror("启动错误", f"启动时发生错误: {e}\n\n详情请查看控制台输出。")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        input("按回车键退出...")