; Keywords
(page_declaration "page" @keyword)
(layout_section "layout:" @keyword)
(render_section "render:" @keyword)
(functions_section "functions:" @keyword)
(import_statement "import" @keyword "from" @keyword)

; Variables and identifiers
(identifier) @variable
(component_identifier) @type
(jsx_identifier) @tag

; Functions
(function_definition name: (identifier) @function)

; Literals
(string_literal) @string
(boolean_literal) @boolean

; Comments
(comment) @comment

; JSX
(jsx_element (jsx_identifier) @tag)
(jsx_self_closing_element (jsx_identifier) @tag)
(jsx_attribute (identifier) @property)
(text_content) @text

; Operators and punctuation
["(" ")" "{" "}" "[" "]" "<" ">" "," "=" ":"] @punctuation.delimiter
["+" "-" "*" "/" "&&" "||" "==" "!="] @operator

; Control flow
(if_statement "if" @conditional "else" @conditional)
(return_statement "return" @keyword.return)

; Variables declarations
(variable_declaration "const" @keyword)
(const_declaration "let" @keyword)
