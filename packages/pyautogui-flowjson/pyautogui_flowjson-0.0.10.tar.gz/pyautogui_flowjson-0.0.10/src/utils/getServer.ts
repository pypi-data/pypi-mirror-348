import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'
import pkg from '../../package.json'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import * as defs from '../defs'
import { ServerType } from '../types'
import { def } from './def'

export function getServer(serverType: ServerType = ServerType.mcpServer) {
  const coreDefs = Object.keys(defs)
    .filter((key) => key.includes('Def'))
    // @ts-expect-error
    .map((key) => defs[key] as ReturnType<typeof def>)

  switch (serverType) {
    case ServerType.mcpServer:
      const mcpServer = new McpServer({
        name: pkg.name,
        version: pkg.version,
        capabilities: {
          resources: {},
          tools: {},
        },
      })
      for (const v of coreDefs) {
        mcpServer.tool(v.name, v.description, v.argsSchema, v.requestHandler)
      }
      return mcpServer
    case ServerType.server:
      const server = new Server(
        {
          name: pkg.name,
          version: pkg.version,
        },
        {
          capabilities: {
            tools: {},
          },
        }
      )
      // Define available tools
      server.setRequestHandler(ListToolsRequestSchema, async () => {
        return {
          tools: coreDefs.map((v) => ({
            name: v.name,
            description: v.description,
            inputSchema: zodToJsonSchema(
              z.object(v.argsSchema)
              // .strict() // 默认 additionalProperties: false,
              // .passthrough() // additionalProperties: true,
            ),
          })),
        }
      })
      // Handle tool execution
      server.setRequestHandler(CallToolRequestSchema, async (request) => {
        try {
          const { name, arguments: args } = request.params
          const item = coreDefs.find((v) => name === v.name)
          if (!item) throw new Error(`Unknown tool: ${name}`)
          // @ts-expect-error
          const res = await item.requestHandler(args)
          return res
        } catch (error) {
          const errorMessage =
            error instanceof Error ? error.message : String(error)
          return {
            content: [{ type: 'text', text: `Error: ${errorMessage}` }],
            isError: true,
          }
        }
      })
      return server
    default:
      throw new Error('Unknown server type')
  }
}
