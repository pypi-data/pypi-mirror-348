import io
import pyautogui
from .img import toBase64


async def getScreenshot():
    # 捕获 屏幕截图
    screenshot = pyautogui.screenshot()
    # 将 PIL.Image 转换为 bytes
    imgbytes = io.BytesIO()
    screenshot.save(imgbytes, format="png")
    imgbytes.seek(0)  # 重置指针到开头 确保后续 从开头读取数据
    return await toBase64(imgbytes.read())
