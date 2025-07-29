![Mobvoi Logo](https://raw.githubusercontent.com/mobvoi/mobvoi-mcp/master/.assets/logo.jpeg)
<p align="center">
<a href="https://pypi.org/project/mobvoi-mcp/"><img src="https://img.shields.io/badge/pypi-mobvoimcp-green" alt="version"></a>
<a href="https://openapi.moyin.com/index/"><img src="https://img.shields.io/badge/openapi-SeqMonkey-orange" alt="version"></a>
<a href="https://www.moyin.com/"><img src="https://img.shields.io/badge/魔音工坊-出门问问-red" alt="version"></a>
<a href="https://www.dupdub.com/"><img src="https://img.shields.io/badge/dupdub-Mobvoi-yellow" alt="version"></a>
<a href="https://sparkaudio.github.io/spark-tts/"><img src="https://img.shields.io/badge/github-sparktts-blue" alt="version"></a>
</p>

<p align="center">
  Official Mobvoi <a href="https://github.com/modelcontextprotocol">Model Context Protocol (MCP)</a> server that enables interaction with Mobvoi powerful Text to Speech, Voice Clone APIs. This server allows MCP clients like <a href="https://www.cursor.so">Cursor</a>, <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://cline.bot/">Cline</a> </a>, <a href="https://windsurf.com/editor">Windsurf</a> and other Client to generate speech, clone voices, and more. The mobvoi-tts-mcp server is built based on Python. Our PyPI package is published at Pypi, you can click on <a href="https://pypi.org/project/mobvoi-mcp/">Pypi</a> to view the latest version.
</p>

## Prerequisite

1. python 3.10+;
2. Get your APP_KEY and APP_SECRET from [Mobvoi Sequence Monkey open platform](https://openapi.moyin.com/user/mine-app-detail). New users can claim a free quota.
3. Install `uv` (Python package manager), install with `pip install uv` or see the `uv` [repo](https://github.com/astral-sh/uv) for additional install methods.

## What can Mobvoi MCP do?

Mobvoi MCP currently supports the following functions:

1. Voice Clone: Clone the voice according to the URL audio file link or the local audio file provided by you, and return the speaker ID. You can use this speaker ID to generate speech.
2. Speech Synthesis: You can specify the speaker ID to generate speech from the specified text content. In addition, you can also adjust speech attributes such as speech speed and volume. For detailed information, please refer to the documentation of our [Mobvoi Sequence Monkey open platform TTS part](https://openapi.moyin.com/document?name=%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90%EF%BC%88TTS%EF%BC%89).
3. Voice broadcasting: Play the specified audio file.

## Quickstart with Cursor

Go to Cursor -> Cursor Settings -> MCP, click `Add new global MCP server`, and mcp.json will open, paste the following config content:

```
"Mobvoi": {
        "command": "uvx",
        "args": [
          "mobvoi-mcp"
        ],
        "env": {
          "APP_KEY": "<insert-your-APP_KEY-here>",
          "APP_SECRET": "<insert-your-APP_SECRET-here>"
        },
      },
```

## Quickstart with Claude Desktop

Go to Claude Desktop -> Settings -> Developer, click `Edit Config` and open `claude_desktop_config.json`, paste the following config content:

```
"Mobvoi": {
        "command": "uvx",
        "args": [
          "mobvoi-mcp"
        ],
        "env": {
          "APP_KEY": "<insert-your-APP_KEY-here>",
          "APP_SECRET": "<insert-your-APP_SECRET-here>"
        },
      },
```

## Quickstart with Cline

Install Cline extension on VSCode EXTENSIONS, and go to Cline -> MCP Servers -> Installed, click `Config MCP Servers` and  `cline_mcp_settings.json` will be opened, paste the following config content:

```
"Mobvoi": {
        "command": "uvx",
        "args": [
          "mobvoi-mcp"
        ],
        "env": {
          "APP_KEY": "<insert-your-APP_KEY-here>",
          "APP_SECRET": "<insert-your-APP_SECRET-here>"
        },
        "transportType": "stdio"
      },
```

For MacOS and Linux systems, you can refer to the above for configuration. We haven't tested the Windows system yet.

## Source Code Test

If you want to conduct tests based on the source code or perform secondary development based on this repository, you can configure it in the following way:

```
"MobvoiLocal": {
      "disabled": false,
      "timeout": 60,
      "command": "uv",
      "args": [
        "--directory",
        "<path-to-mobvoi-mcp>/mobvoi_mcp",
        "run",
        "server.py"
      ],
      "env": {
          "APP_KEY": "<insert-your-APP_KEY-here>",
          "APP_SECRET": "<insert-your-APP_SECRET-here>"
      },
      "transportType": "stdio"
    },
```

Take Cline as an example, and the configuration of other clients is similar.

## Example usage

1. Try cloning a voice from your audio file(local or remote), enter the following content in the Cursor agent mode: "[https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav](https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav), clone this voice"
2. Specify the speaker, synthesize speech from the text and play it aloud. Prompt the model like the following: "Use the sound cloned just now to broadcast: 'Welcome to experience Mobvoi TTS MCP."
3. A demonstration video:
   ![TTS Demo](https://raw.githubusercontent.com/mobvoi/mobvoi-mcp/master/.assets/Mobvoi_TTS_Demo.gif)

## Troubleshooting

### spawn uvx ENOENT

If you encounter the error "MCP Mobvoi: spawn uvx ENOENT", confirm its absolute path by running this command in your terminal:
`which uvx`
Once you obtain the absolute path (e.g., /usr/local/bin/uvx), update your configuration to use that path (e.g., "command": "/usr/local/bin/uvx"). This ensures that the correct executable is referenced.

### MCP error -32001: Request timed out

If you encounter this error, this indicates that there is a problem with your network. If you are in mainland China, we strongly recommend that you configure extra pypi sources in the following way:

```
"Mobvoi": {
        ...
        "args": [
          "--index", 
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "mobvoi-mcp"
        ],
       ...
      },
```

Note that the extra pypi source needs to be configured at the very front of the args.

### Unable to synchronize the latest PyPI package

If you encounter this situation, it may be caused by the following reasons: 1) Network problems; 2) Cache problems; 3) The specified mirror source has not synchronized the mobvoi-mcp package.
If you are using a mirror source, you should first check whether the mobvoi-mcp package is synchronized on the mirror source you are using, in the following way:
`pip index versions --index-url https://pypi.tuna.tsinghua.edu.cn/simple mobvoi-mcp`
If you can see that the LATEST version number is consistent with that on PyPI, you can use the mirror source to update the latest mobvoi-mcp package. Otherwise, you can only use https://pypi.org/simple for the update. Usually, after a new package is released on PyPI, there will be a delay of dozens of minutes for the mirror source to synchronize.
At the same time, you can refer to the following configuration to update and clear the cache.

```
"Mobvoi": {
        ...
        "args": [
          "--upgrade",
          "--no-cache-dir",
          "--index", 
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "mobvoi-mcp"
        ],
       ...
      },
```

