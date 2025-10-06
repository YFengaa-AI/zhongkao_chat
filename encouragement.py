# Encouragement.py
import random

class Encouragement:
    """
    鼓励语录功能模块
    提供随机鼓励语录
    支持模块化系统
    """
    
    def __init__(self, main_manager=None):
        """
        初始化鼓励语录模块
        
        参数:
        - main_manager: 模块化系统的主管理器，用于在模块化环境中获取其他管理器
        """
        self.main_manager = main_manager
        # 鼓励语录列表
        self.encouragements = [
            "今天也要加油哦！",
            "相信自己，你可以的！",
            "每一份努力都不会被辜负！",
            "中考加油，未来可期！",
            "只有努力，才能改变命运！",
            "再坚持一下，胜利就在眼前！",
            "祝你今天学习效率超高！",
            "数学题做不对？多练几遍就会了！",
            "语文作文写不好？多读多写一定行！",
            "英语单词记不住？每天背10个就是进步！",
            "加油！你一定可以的！",
            "每一次努力都不会白费！",
            "坚持就是胜利！",
            "相信自己，你比想象中更强大！",
            "今天的努力，明天的收获！",
            "不要放弃，成功就在前方！",
            "付出多少，就会收获多少！",
            "中考必胜！我能行！",
            "越努力，越幸运！",
            "困难是暂时的，胜利是属于你的！",
            "每一小步都在靠近成功！",
            "你已经很棒了，继续加油！",
            "专注当下，未来可期！",
            "学习虽苦，但结果很甜！",
            "不要畏惧困难，它是成功的垫脚石！",
            "现在的辛苦是为了将来的幸福！",
            "相信自己的能力，你一定能做到！",
            "每一次坚持都是成长的机会！",
            "中考只是人生的一个小挑战，你能轻松应对！",
            "保持积极的心态，一切都会好起来的！"
        ]
    
    def get_encouragement(self):
        """
        获取一条随机的鼓励语录
        """
        if not self.encouragements:
            return "加油！你一定可以的！"
        return random.choice(self.encouragements)
    
    def add_encouragement(self, quote):
        """
        添加新的鼓励语录
        """
        if quote and quote.strip() and quote not in self.encouragements:
            self.encouragements.append(quote.strip())
            return True, "鼓励语录添加成功！"
        return False, "无效的鼓励语录或已存在！"
    
    def get_all_encouragements(self):
        """
        获取所有鼓励语录
        """
        return self.encouragements.copy()
    
    def get_count(self):
        """
        获取鼓励语录的数量
        """
        return len(self.encouragements)

# 为保持向后兼容性，保留原有的变量和函数接口
ENCOURAGING_WORDS = Encouragement().get_all_encouragements()
encouragement_instance = Encouragement()

def get_encouragement():
    """
    从语录列表中随机选择一条鼓励信息并返回。
    保持向后兼容性的函数接口
    """
    return encouragement_instance.get_encouragement()

# 测试代码
if __name__ == '__main__':
    encouragement = Encouragement()
    print("随机鼓励语录：")
    for i in range(3):
        print(f"测试 {i+1}: {encouragement.get_encouragement()}")
    print(f"共有{encouragement.get_count()}条鼓励语录")
