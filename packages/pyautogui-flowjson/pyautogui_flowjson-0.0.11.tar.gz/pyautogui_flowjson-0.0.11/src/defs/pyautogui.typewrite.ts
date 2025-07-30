import { PythonShell } from 'python-shell'
import z from 'zod'
import {
  def,
  getContent,
  KEYBOARD_KEYS,
  lfJoin,
  PythonShellOptions,
  toPyStrArg,
} from '../utils'

export const typewriteDef = def({
  name: 'typewrite',
  description: lfJoin(
    '模拟按键输入文本字符串的过程，message 中的每个字符执行一个按键按下，然后释放。',
    '也可用于粘贴文本，message 为要粘贴的字符串。',
    '不能用于执行键盘快捷键',
    '示例：',
    '1. 键盘输入 你好',
    `${JSON.stringify(
      {
        "message": "你好"
      },
      null,
      2
    )}`
  ),
  argsSchema: {
    message: z
      .union([z.string(), z.array(z.string())])
      .describe(
        lfJoin(
          '如果是一个字符串，则是需要按下的字符。',
          '如果是一个数组，则是按键名称的列表，按键顺序按下。',
          `有效的名称: ${KEYBOARD_KEYS.join(', ')}`
        )
      ),

    interval: z
      .number()
      .optional()
      .describe(lfJoin('每个按键之间等待的时间，以秒为单位', '默认为 0')),
  },
  async requestHandler(arg) {
    const pyArgument = toPyStrArg(arg)
    await PythonShell.runString(
      lfJoin(
        'import asyncio',
        'from flowjson.utils.typewrite import typewrite',
        `asyncio.run(typewrite(${pyArgument}))`
      ),
      PythonShellOptions
    )
    return getContent('操作成功')
  },
})
