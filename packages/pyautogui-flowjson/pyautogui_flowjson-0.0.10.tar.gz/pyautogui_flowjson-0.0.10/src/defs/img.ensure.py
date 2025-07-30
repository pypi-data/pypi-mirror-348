import asyncio
import json
import time
import pyautogui
import pydash
from flowjson.utils.findOnScreen import findOnScreen
from utils.jsPy import getJsEnvArg, pyToJsArg


async def bootstrap():
    arg = await getJsEnvArg()

    async def task():
        while True:
            res = await findOnScreen(
                targetImage=pydash.get(arg, "uri"),
                confidence=pydash.get(arg, "confidence"),
            )
            if res is None:
                await asyncio.sleep(0.3)
            else:
                return res

    try:
        result = await asyncio.wait_for(task(), timeout=pydash.get(arg, "timeout"))
        return await pyToJsArg(
            f"操作成功，检测到图片存在，点位信息：{json.dumps(result, ensure_ascii=False, indent=2)}"
        )
    except asyncio.TimeoutError:
        return await pyToJsArg(
            f"操作失败，已经超过最大执行时间 {pydash.get(arg, 'timeout')} 秒"
        )


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
