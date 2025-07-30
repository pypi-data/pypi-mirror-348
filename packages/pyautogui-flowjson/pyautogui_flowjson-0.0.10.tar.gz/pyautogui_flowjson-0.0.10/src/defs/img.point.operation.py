import asyncio
import json
import pyautogui
import pydash
from typing import Optional
from flowjson.types.workflows import Image, Shot
from flowjson.utils.formatArgument import toArr
from flowjson.utils.findOnScreen import findOnScreen
from utils.jsPy import getJsEnvArg, pyToJsArg


async def analyzeShot(shot: Optional[Shot]):
    if shot is None:
        return await asyncio.sleep(0)
    URI_KEY = "uri"
    # 统一格式
    screenShot = {URI_KEY: shot} if isinstance(shot, str) else shot
    otherArg = {k: v for k, v in screenShot.items() if k != URI_KEY}
    return await findOnScreen(
        targetImage=pydash.get(screenShot, URI_KEY),
        **otherArg,
    )


async def analyzeImage(image: Optional[Image]):
    if image is None:
        return {"isPass": True}
    (positionRes, includesRes, excludesRes) = await asyncio.gather(
        (analyzeShot(pydash.get(image, "position"))),
        (
            asyncio.gather(
                # 展开
                *[
                    # 列表推导式
                    analyzeShot(v)
                    # 通用转换为数组
                    for v in toArr(pydash.get(image, "includes"))
                ]
            )
        ),
        (
            asyncio.gather(
                *[analyzeShot(v) for v in toArr(pydash.get(image, "excludes"))]
            )
        ),
    )
    # 给了 position 的值 就应该解析出坐标
    positionPass = (
        (positionRes is not None) if pydash.get(image, "position") is not None else True
    )
    includesPass = all(v is not None for v in includesRes)
    excludesPass = all(v is None for v in excludesRes)
    return {
        "position": positionRes,
        "includes": includesRes,
        "excludes": excludesRes,
        "isPass": positionPass and includesPass and excludesPass,
    }


async def bootstrap():
    arg = await getJsEnvArg()
    ACTION_KEY = "action"
    otherArg = {k: v for k, v in arg.items() if k != ACTION_KEY}
    imageRes = await analyzeImage(otherArg)

    if pydash.get(imageRes, "isPass"):
        pyautoguiActionFn = getattr(pyautogui, pydash.get(arg, "action.type"))
        (x, y) = (
            (None, None)
            if pydash.get(imageRes, "position") is None
            else (
                pydash.get(imageRes, "position[0]"),
                pydash.get(imageRes, "position[1]"),
            )
        )
        xyArguments = {"x": x, "y": y} if all(v is not None for v in (x, y)) else {}
        actionArguments: dict | list = pydash.get(arg, "action.arguments", {})
        # pyautogui.move(xOffset=0, yOffset=-100) 参数非 xy 一般不需要兼容
        (
            # 确保 actionArguments 会覆盖 xyArguments
            pyautoguiActionFn(**{**xyArguments, **actionArguments})
            if isinstance(actionArguments, dict)
            else pyautoguiActionFn(*actionArguments, **xyArguments)
        )
        return await pyToJsArg("操作成功")

    return await pyToJsArg(
        f"图片整体查找 验证不通过 {json.dumps(imageRes, ensure_ascii=False, indent=2)}"
    )


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
