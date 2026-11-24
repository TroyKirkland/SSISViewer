# SSIS Visualiser

A read-only viewer for SSIS `.dtsx` packages. It's a single HTML file with no install, no server and no internet connection needed. Packages are parsed locally in the browser.

## Use it

**Option 1: open the viewer and drop files on it**

```sh
open viewer.html
```

Then drag one or more `.dtsx` files onto the window, or click **Open .dtsx…** (⌘O).

**Option 2: bake packages into a standalone HTML file you can share**

```sh
./dtsx2html.py path/to/Package.dtsx --open          # -> Package.html
./dtsx2html.py path/to/SSISProject/ -o project.html # every .dtsx in a folder
```

## What you get

- **Control Flow**: tasks and containers (Sequence, For Loop, Foreach) drawn with nesting. Precedence constraints are colour-coded (green success, red failure, blue completion). A dashed line is an OR constraint, and **fx** marks an expression.
- **Data Flow**: components coloured by role (source, transform, destination), with named outputs (Lookup no-match, Conditional Split branches) and error paths.
- **Event Handlers**: shown as their own diagrams.
- **Details panel**: SQL statements (highlighted), Derived Column and Conditional Split expressions, column lists, destination column mappings, script task code, Foreach enumerator settings, property expressions and precedence logic.
- **Connection managers, variables and parameters**: each one shows *Used by*, i.e. which tasks and components reference it. Passwords in connection strings are masked.
- Search, pan (drag or two-finger scroll), zoom (pinch or ⌘-scroll), **Fit** (`f`), collapsing containers (double-click), and **Export SVG**.

Supports both the SSIS 2012+ package format and the older 2008 format.

## Files

| File | Purpose |
|---|---|
| `viewer.html` | The whole app |
| `dtsx2html.py` | CLI that embeds packages into a copy of `viewer.html` |
| `samples/SalesLoad.dtsx` | Example package for testing |
