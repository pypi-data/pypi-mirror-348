;; Scopes
(function_body) @scope
(jsx_block) @scope

;; Definitions
(function_definition
  name: (identifier) @definition.function)
(variable_declaration
  (identifier) @definition.var)
(const_declaration
  (identifier) @definition.var)
; Parameters are not currently defined in the grammar

;; References
(identifier) @reference
(component_identifier) @reference
(jsx_identifier) @reference
