import asyncio
from utils.jsPy import getJsEnvArg, pyToJsArg
from flowjson.utils.imgOcr import imgOcr


async def bootstrap():
    try:
        arg = await getJsEnvArg()
        res = await imgOcr(**arg)
        return await pyToJsArg({"message": "操作成功", "result": " ".join(res)})
    except Exception as e:
        return await pyToJsArg(str(e))


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
