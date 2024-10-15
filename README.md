# AST Viewer

An ast tree visualization tool (currently supports XML representations only). Will improve in the future, very simple for now.

## How To
ASTs must be of the form:
```xml
<Node val="Node value">
  <!-- Terminal Nodes -->
  <Node val="Terminal node value" />
</Node>
```

`&`, `<`, and `>` must be esacped when used in values.
