import logging
import logging.config
import yaml

from taker.TrailingSLTaker import TrailingSLTaker
from taker.TrailingSLAndTPTaker import TrailingSLAndTPTaker
from taker.ThreeLineTradingTaker import ThreeLineTradingTaker
from taker.SMCSLAndTPTaker import SMCSLAndTPTaker
from pyfiglet import Figlet
    
def read_config_file(file_path):
    try:
        # 打开 YAML 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用 yaml.safe_load 方法解析 YAML 文件内容
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        raise Exception(f"文件 {file_path} 未找到。")
    except yaml.YAMLError as e:
        raise Exception(f"解析 {file_path} 文件时出错: {e}")


def main():
    import importlib.metadata
    version = importlib.metadata.version("openfund-taker")

    package_name = __package__ or "taker" 
    
    openfund_config_path = 'taker_config.yaml'
    config_data = read_config_file(openfund_config_path)
    

    platform_config = config_data['platform']["okx"]
    common_config = config_data['common']
    taker = common_config.get('actived_taker', 'SMCSLAndTPTaker')
    feishu_webhook_url = common_config['feishu_webhook']
    monitor_interval = common_config.get("monitor_interval", 60)  # 默认值为60秒
    
    logging.config.dictConfig(config_data["Logger"])
    logger = logging.getLogger("openfund-taker")
    
    f = Figlet(font="standard")  # 字体可选（如 "block", "bubble"）
    logger.info(f"\n{f.renderText("OpenFund Taker")}")
            
    logger.info(f" ++ {package_name}.{taker}:{version} is doing...")
    # 根据配置动态创建策略实例
    strategy_class = globals()[taker]
    bot = strategy_class(config_data, platform_config, common_config, feishu_webhook=feishu_webhook_url, monitor_interval=monitor_interval,logger=logger)


    bot.monitor_total_profit()
    # bot = ThreeLineTradingBot(platform_config, feishu_webhook=feishu_webhook_url, monitor_interval=monitor_interval)
    # bot.monitor_klines()

if __name__ == "__main__":
    main()
