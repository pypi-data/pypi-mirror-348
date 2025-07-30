import asyncio
import json
from flowjson.utils.pointOperation import pointOperation
from utils.jsPy import getJsEnvArg, pyToJsArg


async def bootstrap():
    try:
        arg = await getJsEnvArg()
        imageRes = await pointOperation(arg)
        if imageRes:
            return await pyToJsArg(
                f"图片整体查找 验证不通过 {json.dumps(imageRes, ensure_ascii=False, indent=2)}"
            )
        return await pyToJsArg("操作成功")
    except Exception as e:
        return await pyToJsArg(str(e))


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
