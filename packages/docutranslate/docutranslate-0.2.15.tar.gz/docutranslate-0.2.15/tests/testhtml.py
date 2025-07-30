import markdown2
markdowner = markdown2.Markdown(extras=['tables', 'fenced-code-blocks', 'mermaid', "code-friendly"])
markdown_parsed=markdowner.convert(r"""
$C_e^{(0)} = A + 0 = \{0, 1, 3\}$")
请注意，当领导者 \( L \) 收到针对前一轮编码 \( R(s+1)e \) 的 \( n' - f' \) 个 code-finish 消息时，它将开始为下一轮编码 \( R(s+1)e+1 \) 重新编码块。为了确保所有备份节点意识到诚实节点已完成对编码轮次 \( R(s+1)e \) 的重新编码，领导者 \( L \) 广播已收到的 \( n' - f' \) 个 code-finish 消息以及下一轮编码 \( R(s+1)e+1 \) 的重新编码消息。当一个备份节点通过验证签名集合 \( V \) 确认 \( n' - f' \) 个节点已完成重新编码后，它会删除使用旧方案的块数据。通过这种方法，在重新编码之前，所有块仍然保持可用。
```mermaid
sequenceDiagram
participant 用户
participant 客户端
participant 服务端

用户->>客户端: 输入用户名和密码
客户端->>服务端: 发送用户名和密码
服务端->>服务端: 验证用户名和密码
服务端-->>客户端: 返回session_id
客户端->>服务端: 请求资源（携带session_id）
服务端->>服务端: 验证session_id
服务端-->>客户端: 认证成功，返回资源
```
""".replace("\\","\\\\"))

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>title</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css">
        <style>
        html {{
            padding:2vh 10vw;
            font-size: 15px;
        }}
    </style>
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({{
        messageStyle: "none",
        tex2jax: {{
          inlineMath: [ ['$','$'], ["\\\\(","\\\\)"] ],
          processEscapes: true
        }}
      }});
    </script>

    <script type="text/javascript"
            src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
</head>
<body>
{markdown_parsed}
</body>
<script type="module" defer>
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{
    securityLevel: 'loose',
    startOnLoad: true
  }});
  let observer = new MutationObserver(mutations => {{
    for(let mutation of mutations) {{
      mutation.target.style.visibility = "visible";
    }}
  }});
  document.querySelectorAll("pre.mermaid-pre div.mermaid").forEach(item => {{
    observer.observe(item, {{ 
      attributes: true, 
      attributeFilter: ['data-processed'] 
    }});
  }});
</script>

</html>
"""

print(html)