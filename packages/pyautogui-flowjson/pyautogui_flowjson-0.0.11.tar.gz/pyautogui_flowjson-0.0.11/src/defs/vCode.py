import asyncio
import json
import pydash
from flowjson.utils.vCode import vCodeClickType, vCodeFillType, vCodeScrollType
from utils.jsPy import getJsEnvArg, pyToJsArg


async def bootstrap():
    try:
        arg = await getJsEnvArg()
        match pydash.get(arg, "type"):
            case "fill":
                res = await vCodeFillType(pydash.get(arg, "source"))
                return await pyToJsArg(
                    f"操作成功，{json.dumps(res, ensure_ascii=False, indent=2)}"
                )
            case "click":
                res = await vCodeClickType(pydash.get(arg, "source"))
                return await pyToJsArg(
                    f"操作成功，{json.dumps(res, ensure_ascii=False, indent=2)}"
                )
            case "scroll":
                res = await vCodeScrollType(
                    targetSource=pydash.get(arg, "source"),
                    backgroundSource=pydash.get(arg, "backgroundSource"),
                    simple_target=pydash.get(arg, "simple_target"),
                )
                return await pyToJsArg(
                    f"操作成功，{json.dumps(res, ensure_ascii=False, indent=2)}"
                )
    except Exception as e:
        return await pyToJsArg(str(e))


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
