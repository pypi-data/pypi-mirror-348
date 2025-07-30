import markdown2
markdown_parsed=markdown2.Markdown().convert(r"$C_e^{(0)} = A + 0 = \{0, 1, 3\}$")

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