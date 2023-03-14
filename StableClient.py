import asyncio
# 本文提供 Stable Diffcusion（以下简称 SD） 画图接口
# 设想如下：
#   bot部署到服务器上
#   SD放在本地 PC 上（需要显卡，云服务器没有）
#   使用异步 TCP进行通信
#   通信逻辑：
#       PC -> 云服务器, 云服务器对PC进行请求，PC响应请求        


# 后续有时间更新