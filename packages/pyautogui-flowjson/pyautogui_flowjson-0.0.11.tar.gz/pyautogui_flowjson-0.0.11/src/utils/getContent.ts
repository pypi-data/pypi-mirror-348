import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js'

export async function getContent(text: any): Promise<CallToolResult> {
  return {
    content: [
      {
        type: 'text',
        text: typeof text === 'string' ? text : JSON.stringify(text),
      },
    ],
  }
}
