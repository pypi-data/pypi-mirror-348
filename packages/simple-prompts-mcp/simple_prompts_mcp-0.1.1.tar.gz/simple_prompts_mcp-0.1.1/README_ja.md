# simple-prompts-mcp

## 概要

- Promptを利用するためのシンプルなMCPサーバーです。
- Promptは事前にyamlファイルで定義します。

## プロンプトファイルの定義

プロンプトは1つずつ個別のyamlファイルで定義してください。

### スキーマ詳細

- `name`: string型。プロンプトの識別名。
- `description`: string型。プロンプトの説明文。
- `arguments`: 配列。各要素は以下のプロパティを持つオブジェクト。
    - `name`: string型。引数名。
    - `description`: string型。引数の説明。
    - `required`: boolean型。必須かどうか。
- `prompt`: string型。プロンプト本文。  
  プロンプト本文（`prompt`）は、Pythonの`str.format()`を使い、名前付き引数で動的に生成されます。  
  例のように`{user_name}`のようなプレースホルダを記述し、引数で与えた値が埋め込まれます。

### 例

```yaml
name: example
description: これはサンプルプロンプトです
arguments:
  - name: user_name
    description: ユーザーの名前
    required: true
prompt: |
  こんにちは、{user_name}さん！
```

各yamlファイルはこのスキーマに従って作成してください.

## MCPサーバーの登録

MCPサーバーとして`simple-prompts-mcp`を登録するには、設定ファイルに以下のように記述します。

> **注意:**  
> `uv` でPython 3.11以降を使用してください。

```json
{
    "mcpServers": {
        "simple-prompts-mcp": {
            "command": "uvx",
            "args": ["simple-prompts-mcp"]
        }
    }
}
```

### 設定

| 環境変数    | 目的                       | デフォルト値                  |
|-------------|----------------------------|------------------------------|
| `PROMPTS_DIR` | プロンプトファイルの保存先 | ~/.config/simple-prompts-mcp |


```json
{
    "mcpServers": {
        "simple-prompts-mcp": {
            "command": "uvx",
            "args": ["simple-prompts-mcp"],
            "env": {
                "PROMPTS_DIR": "/full-path/to/prompts/dir"
            }
        }
    }
}
```

## ライセンス

本プロジェクトはMITライセンスです。詳細はLICENSEファイルをご覧ください。
