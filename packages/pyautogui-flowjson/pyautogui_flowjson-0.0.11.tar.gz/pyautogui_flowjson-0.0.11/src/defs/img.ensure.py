import asyncio
import json
from flowjson.utils.imgEnsure import imgEnsure
from utils.jsPy import getJsEnvArg, pyToJsArg


async def bootstrap():
    try:
        arg = await getJsEnvArg()
        res = await imgEnsure(arg)
        return await pyToJsArg(
            f"操作成功，检测到图片存在，点位信息：{json.dumps(res, ensure_ascii=False, indent=2)}"
        )
    except Exception as e:
        return await pyToJsArg(str(e))


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
