# run_enhanced_fixed.py
#!/usr/bin/env python3
"""
中考加油聊天室 - 修复版增强启动脚本
"""
import sys
import os

def main():
    print("🚀 启动中考加油聊天室 - 增强版")
    print("=" * 50)
    
    try:
        # 确保当前目录在Python路径中
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # 导入主管理器
        from MainManager import MainManager
        
        # 创建主管理器实例，明确指定数据目录
        data_dir = os.path.join(current_dir, "data")
        main_manager = MainManager(data_dir)
        
        # 调试：检查main_manager的属性
        print(f"🔧 主管理器实例创建成功，数据目录: {data_dir}")
        print(f"🔧 主管理器包含的属性: {dir(main_manager)}")
        
        # 启动应用程序
        main_manager.start_application()
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("请确保所有必需的模块文件都存在于当前目录中")
        input("按回车键退出...")
    
    except Exception as e:
        import traceback
        print(f"❌ 启动时发生错误: {e}")
        print(f"📋 错误详情: {traceback.format_exc()}")
        input("按回车键退出...")

if __name__ == '__main__':
    main()