import { def, execPyFile, lfJoin } from '../utils'

export const screenshotDef = def({
  name: 'screenshot',
  description: lfJoin('获取当前屏幕截图 返回 base64 字符串'),
  argsSchema: {},
  async requestHandler(arg, extra) {
    const res = await execPyFile('src/defs/screenshot.py', arg)
    return res
  },
})
