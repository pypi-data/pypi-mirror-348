from solidipes_core_plugin.loaders.code_snippet import CodeSnippet


class AbaqusPythonCode(CodeSnippet):
    supported_mime_types = {"text/x-script.python": "jnl"}
