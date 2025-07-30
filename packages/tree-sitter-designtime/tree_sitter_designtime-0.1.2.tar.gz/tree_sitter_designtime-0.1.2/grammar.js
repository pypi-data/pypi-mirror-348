// fuck this, am going to rewrite this soon.

module.exports = grammar({
  name: 'designtime',

  extras: $ => [
    $.comment,
    /\s/
  ],

  keywords: $ => [
    'page',
    'layout',
    'render',
    'functions',
    'self',
    'import',
    'from',
    'const',
    'let',
    'if',
    'else',
    'return',
    'true',
    'false'
  ],

  conflicts: $ => [
    [$.jsx_element, $.expression],
    [$.jsx_element, $.jsx_self_closing_element],
    [$.member_expression, $.jsx_identifier],
    [$.jsx_block, $.expression],
    [$.expression, $.object_property],
    [$.function_body, $.statement],
    [$.conditional_expression, $.binary_expression],
    [$.jsx_expression, $.jsx_expression_block],
  ],

  word: $ => $.identifier,

  rules: {
    source_file: $ => repeat(choice(
      $.import_statement,
      $.page_declaration,
      $.comment,
    )),

    import_statement: $ => seq(
      'import',
      choice(
        seq('{', commaSep($.component_identifier), '}'),
        $.component_identifier,
      ),
      'from',
      $.string_literal,
      optional(';'),
    ),

    page_declaration: $ => seq(
      'page',
      $.identifier,
      '{',
      repeat(choice(
        $.layout_section,
        $.render_section,
        $.functions_section,
        $.comment,
      )),
      '}',
    ),

    layout_section: $ => seq(
      'layout:',
      $.component_reference,
      ',',
      $.parameter_block
    ),

    render_section: $ => seq(
      'render:',
      prec(1, $.jsx_block)
    ),

    functions_section: $ => seq(
      'functions:',
      '{',
      repeat(choice(
        $.function_definition,
        $.comment,
      )),
      '}',
    ),

    component_reference: $ => choice(
      $.component_identifier,
      $.member_expression,
    ),

    jsx_block: $ => prec(2, seq(
      '{',
      choice(
        prec.right(1, $.expression),
        repeat(choice(
          prec.right(2, $.jsx_element),
          prec.right(2, $.jsx_self_closing_element),
          $.text_content,
          $.jsx_expression,
          $.comment,
        )),
      ),
      '}',
    )),

    jsx_element: $ => seq(
      '<',
      field('name', $.jsx_identifier),
      repeat($.jsx_attribute),
      '>',
      repeat(choice(
        $.jsx_element,
        $.jsx_self_closing_element,
        $.jsx_expression,
        $.text_content,
        $.comment,
      )),
      '</',
      field('name', $.jsx_identifier),
      '>',
    ),

    jsx_self_closing_element: $ => seq(
      '<',
      $.jsx_identifier,
      repeat($.jsx_attribute),
      '/>',
    ),

    jsx_attribute: $ => seq(
      $.identifier,
      optional(seq(
        '=',
        choice(
          $.string_literal,
          $.jsx_expression,
          $.jsx_expression_block,
        ),
      )),
    ),

    jsx_identifier: $ => choice($.component_identifier, $.identifier,),

    jsx_expression: $ => prec(3, seq('{', $.expression, '}')),

    jsx_expression_block: $ => seq(
      '{',
      $.expression,
      '}',
    ),

    function_definition: $ => seq(
      field('name', $.identifier),
      ':',
      field('body', $.function_body),
    ),

    function_body: $ => prec(2, seq(
      '{',
      repeat(choice($.statement, $.comment)),
      '}',
    )),

    statement: $ => choice(
      $.if_statement,
      $.return_statement,
      $.assignment,
      $.expression,
      $.comment,
      $.variable_declaration,
      $.const_declaration,
      seq($.expression, ';'),
    ),

    variable_declaration: $ => seq(
      'const',
      $.identifier,
      '=',
      $.expression,
      optional(';'),
    ),

    const_declaration: $ => seq(
      'let',
      $.identifier,
      '=',
      $.expression,
      optional(';'),
    ),

    if_statement: $ => seq(
      'if',
      '(',
      $.expression,
      ')',
      $.statement_block,
      optional(seq(
        'else',
        choice($.statement_block, $.if_statement),
      )),
    ),

    statement_block: $ => seq('{', repeat($.statement), '}',),

    return_statement: $ => prec.right(seq(
      'return',
      optional(seq($.expression, optional(';'))),
    )),

    parameter_block: $ => seq(
      '{',
      repeat(choice($.assignment, $.comment)),
      '}',
    ),

    assignment: $ => seq(
      $.identifier,
      ':',
      $.expression,
      optional(','),
    ),

    expression: $ => choice(
      $.conditional_expression,
      $.binary_expression,
      $.member_expression,
      $.call_expression,
      $.jsx_element,
      $.jsx_self_closing_element,
      $.self_expression,
      $.array_literal,
      $.object_literal,
      $.identifier,
      $.string_literal,
      $.numeric_literal,
      $.boolean_literal,
      seq('(', $.expression, ')'),
    ),

    conditional_expression: $ => prec.right(10, seq(
      field('condition', $.expression),
      '?',
      field('consequent', $.expression),
      ':',
      field('alternate', $.expression),
    )),

    binary_expression: $ => choice(
      ...[['?', 1]].map(([operator, precedence]) =>
        prec.right(precedence, seq(
          field('condition', $.expression),
          field('operator', operator),
          field('consequent', $.expression),
          ':',
          field('alternate', $.expression),
        )),
      ),
      ...[
        ['||', 1],
        ['&&', 2],
        ['==', 3],
        ['!=', 3],
        ['<', 4],
        ['<=', 4],
        ['>', 4],
        ['>=', 4],
        ['+', 5],
        ['-', 5],
        ['*', 6],
        ['/', 6],
        ['%', 6],
      ].map(([operator, precedence]) =>
        prec.left(precedence, seq(
          field('left', $.expression),
          field('operator', token(operator)),
          field('right', $.expression),
        )),
      )
    ),

    member_expression: $ => prec.left(7, seq(
      $.expression,
      '.',
      choice(
        $.identifier,
        $.component_identifier,
      ),
    )),

    call_expression: $ => prec.left(8, seq(
      $.expression,
      '(',
      optional(commaSep1($.expression)),
      ')',
    )),

    self_expression: $ => 'self',

    array_literal: $ => seq(
      '[',
      optional(commaSep1($.expression)),
      ']',
    ),

    object_literal: $ => seq(
      '{',
      optional(commaSep1($.object_property)),
      '}',
    ),

    object_property: $ => prec(9, choice(
      seq(
        choice($.identifier, $.string_literal),
        ':',
        $.expression,
      ),
      $.identifier,
    )),

    component_identifier: $ => token(prec(2, /[A-Z][a-zA-Z0-9]*/)),

    identifier: $ => {
      const alpha = /[a-zA-Z_]/;
      const alphaNumeric = /[a-zA-Z0-9_]/;
      return token(seq(
        alpha,
        repeat(alphaNumeric),
      ));
    },

    string_literal: $ => choice(
      seq(
        '"',
        repeat(choice(
          token.immediate(/[^"\\]+/),
          seq('\\', choice(
            /[^xu0-7]/,
            /[0-7]{1,3}/,
            /x[0-9a-fA-F]{2}/,
            /u[0-9a-fA-F]{4}/,
            /u\{[0-9a-fA-F]+\}/
          ))
        )),
        '"'
      ),
      seq(
        "'",
        repeat(choice(
          token.immediate(/[^'\\]+/),
          seq('\\', choice(
            /[^xu0-7]/,
            /[0-7]{1,3}/,
            /x[0-9a-fA-F]{2}/,
            /u[0-9a-fA-F]{4}/,
            /u\{[0-9a-fA-F]+\}/
          ))
        )),
        "'"
      ),
      seq(
        '`',
        repeat(choice(
          token.immediate(/[^`\\$]+/),
          seq('\\', choice(
            /[^xu0-7]/,
            /[0-7]{1,3}/,
            /x[0-9a-fA-F]{2}/,
            /u[0-9a-fA-F]{4}/,
            /u\{[0-9a-fA-F]+\}/
          )),
          $.template_substitution
        )),
        '`'
      )
    ),

    template_substitution: $ => seq('${', $.expression, '}'),

    numeric_literal: $ => token(choice(
      /\d+(\.\d+)?([eE][+-]?\d+)?/,
      /0[xX][0-9a-fA-F]+/,
      /0[oO][0-7]+/,
      /0[bB][01]+/
    )),

    boolean_literal: $ => choice('true', 'false'),

    text_content: $ => token(/[^<>{}\s][^<>{}]*/),

    comment: $ => token(choice(
      seq('//', /.*/),
      seq(
        '/*',
        /[^*]*\*+([^/*][^*]*\*+)*/,
        '/',
      ),
    )),
  }
});

function commaSep(rule) {
  return optional(commaSep1(rule));
}

function commaSep1(rule) {
  return seq(rule, repeat(seq(',', rule)));
}
