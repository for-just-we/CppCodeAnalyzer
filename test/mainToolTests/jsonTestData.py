
data = {
  "nodes": [
    {
      "contents": [
        [
          "Parameter",
          "int a"
        ],
        [
          "ParameterType",
          "int"
        ],
        [
          "Identifier",
          "a"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          0,
          2
        ]
      ],
      "lines": 1
    },
    {
      "contents": [
        [
          "IdentifierDeclStatement",
          "char * data ;"
        ],
        [
          "IdentifierDecl",
          "* data"
        ],
        [
          "IdentifierDeclType",
          "char *"
        ],
        [
          "Identifier",
          "data"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 3
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "data = NULL ;"
        ],
        [
          "AssignmentExpr",
          "data = NULL"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "PointerExpression",
          "NULL"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 4
    },
    {
      "contents": [
        [
          "Condition",
          "6"
        ],
        [
          "IntergerExpression",
          "6"
        ]
      ],
      "edges": [
        [
          0,
          1
        ]
      ],
      "lines": 5
    },
    {
      "contents": [
        [
          "Label",
          "case 6 :"
        ],
        [
          "IntergerExpression",
          "6"
        ]
      ],
      "edges": [
        [
          0,
          1
        ]
      ],
      "lines": 7
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "data = ( char * ) malloc ( 100 * sizeof ( char ) ) ;"
        ],
        [
          "AssignmentExpr",
          "data = ( char * ) malloc ( 100 * sizeof ( char ) )"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "CastExpression",
          "( char * ) malloc ( 100 * sizeof ( char ) )"
        ],
        [
          "CastTarget",
          "char *"
        ],
        [
          "CallExpression",
          "malloc ( 100 * sizeof ( char ) )"
        ],
        [
          "Callee",
          "malloc"
        ],
        [
          "ArgumentList",
          "100 * sizeof ( char )"
        ],
        [
          "Identifier",
          "malloc"
        ],
        [
          "Argument",
          "100 * sizeof ( char )"
        ],
        [
          "MultiplicativeExpression",
          "100 * sizeof ( char )"
        ],
        [
          "IntergerExpression",
          "100"
        ],
        [
          "SizeofExpr",
          "sizeof ( char )"
        ],
        [
          "Sizeof",
          "sizeof"
        ],
        [
          "SizeofOperand",
          "char"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          3,
          4
        ],
        [
          3,
          5
        ],
        [
          5,
          6
        ],
        [
          5,
          7
        ],
        [
          6,
          8
        ],
        [
          7,
          9
        ],
        [
          9,
          10
        ],
        [
          10,
          11
        ],
        [
          10,
          12
        ],
        [
          12,
          13
        ],
        [
          12,
          14
        ]
      ],
      "lines": 9
    },
    {
      "contents": [
        [
          "Condition",
          "data == NULL"
        ],
        [
          "EqualityExpression",
          "data == NULL"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "PointerExpression",
          "NULL"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 10
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "exit ( - 1 ) ;"
        ],
        [
          "CallExpression",
          "exit ( - 1 )"
        ],
        [
          "Callee",
          "exit"
        ],
        [
          "ArgumentList",
          "- 1"
        ],
        [
          "Identifier",
          "exit"
        ],
        [
          "Argument",
          "- 1"
        ],
        [
          "UnaryOp",
          "- 1"
        ],
        [
          "UnaryOperator",
          ""
        ],
        [
          "IntergerExpression",
          "1"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          5
        ],
        [
          5,
          6
        ],
        [
          6,
          7
        ],
        [
          6,
          8
        ]
      ],
      "lines": 10
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "data [ 0 ] = '\\0' ;"
        ],
        [
          "AssignmentExpr",
          "data [ 0 ] = '\\0'"
        ],
        [
          "ArrayIndexing",
          "data [ 0 ]"
        ],
        [
          "CharExpression",
          "'\\0'"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "IntergerExpression",
          "0"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          2,
          5
        ]
      ],
      "lines": 11
    },
    {
      "contents": [
        [
          "BreakStatement",
          "break ;"
        ]
      ],
      "edges": [],
      "lines": 12
    },
    {
      "contents": [
        [
          "Label",
          "default :"
        ]
      ],
      "edges": [],
      "lines": 13
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "printLine ( \"Benign, fixed string\" ) ;"
        ],
        [
          "CallExpression",
          "printLine ( \"Benign, fixed string\" )"
        ],
        [
          "Callee",
          "printLine"
        ],
        [
          "ArgumentList",
          "\"Benign, fixed string\""
        ],
        [
          "Identifier",
          "printLine"
        ],
        [
          "Argument",
          "\"Benign, fixed string\""
        ],
        [
          "StringExpression",
          "\"Benign, fixed string\""
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          5
        ],
        [
          5,
          6
        ]
      ],
      "lines": 15
    },
    {
      "contents": [
        [
          "BreakStatement",
          "break ;"
        ]
      ],
      "edges": [],
      "lines": 16
    },
    {
      "contents": [
        [
          "IdentifierDeclStatement",
          "size_t i ;"
        ],
        [
          "IdentifierDecl",
          "i"
        ],
        [
          "IdentifierDeclType",
          "size_t"
        ],
        [
          "Identifier",
          "i"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 19
    },
    {
      "contents": [
        [
          "IdentifierDeclStatement",
          "char source [ 100 ] ;"
        ],
        [
          "IdentifierDecl",
          "source [ 100 ]"
        ],
        [
          "IdentifierDeclType",
          "char *"
        ],
        [
          "Identifier",
          "source"
        ],
        [
          "IntergerExpression",
          "100"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          1,
          4
        ]
      ],
      "lines": 20
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "memset ( source , 'C' , 100 - 1 ) ;"
        ],
        [
          "CallExpression",
          "memset ( source , 'C' , 100 - 1 )"
        ],
        [
          "Callee",
          "memset"
        ],
        [
          "ArgumentList",
          "source"
        ],
        [
          "Identifier",
          "memset"
        ],
        [
          "Argument",
          "source"
        ],
        [
          "Argument",
          "'C'"
        ],
        [
          "Argument",
          "100 - 1"
        ],
        [
          "Identifier",
          "source"
        ],
        [
          "CharExpression",
          "'C'"
        ],
        [
          "AdditiveExpression",
          "100 - 1"
        ],
        [
          "IntergerExpression",
          "100"
        ],
        [
          "IntergerExpression",
          "1"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          5
        ],
        [
          3,
          6
        ],
        [
          3,
          7
        ],
        [
          5,
          8
        ],
        [
          6,
          9
        ],
        [
          7,
          10
        ],
        [
          10,
          11
        ],
        [
          10,
          12
        ]
      ],
      "lines": 21
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "source [ 100 - 1 ] = '\\0' ;"
        ],
        [
          "AssignmentExpr",
          "source [ 100 - 1 ] = '\\0'"
        ],
        [
          "ArrayIndexing",
          "source [ 100 - 1 ]"
        ],
        [
          "CharExpression",
          "'\\0'"
        ],
        [
          "Identifier",
          "source"
        ],
        [
          "AdditiveExpression",
          "100 - 1"
        ],
        [
          "IntergerExpression",
          "100"
        ],
        [
          "IntergerExpression",
          "1"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          2,
          5
        ],
        [
          5,
          6
        ],
        [
          5,
          7
        ]
      ],
      "lines": 22
    },
    {
      "contents": [
        [
          "ForInit",
          "i = 0 ;"
        ],
        [
          "AssignmentExpr",
          "i = 0"
        ],
        [
          "Identifier",
          "i"
        ],
        [
          "IntergerExpression",
          "0"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 24
    },
    {
      "contents": [
        [
          "Condition",
          "i < 100"
        ],
        [
          "RelationalExpression",
          "i < 100"
        ],
        [
          "Identifier",
          "i"
        ],
        [
          "IntergerExpression",
          "100"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ]
      ],
      "lines": 24
    },
    {
      "contents": [
        [
          "IncDecOp",
          "i ++"
        ],
        [
          "Identifier",
          "i"
        ],
        [
          "IncDec",
          ""
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          0,
          2
        ]
      ],
      "lines": 24
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "data [ i ] = source [ i ] ;"
        ],
        [
          "AssignmentExpr",
          "data [ i ] = source [ i ]"
        ],
        [
          "ArrayIndexing",
          "data [ i ]"
        ],
        [
          "ArrayIndexing",
          "source [ i ]"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "Identifier",
          "i"
        ],
        [
          "Identifier",
          "source"
        ],
        [
          "Identifier",
          "i"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          2,
          5
        ],
        [
          3,
          6
        ],
        [
          3,
          7
        ]
      ],
      "lines": 26
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "data [ 100 - 1 ] = '\\0' ;"
        ],
        [
          "AssignmentExpr",
          "data [ 100 - 1 ] = '\\0'"
        ],
        [
          "ArrayIndexing",
          "data [ 100 - 1 ]"
        ],
        [
          "CharExpression",
          "'\\0'"
        ],
        [
          "Identifier",
          "data"
        ],
        [
          "AdditiveExpression",
          "100 - 1"
        ],
        [
          "IntergerExpression",
          "100"
        ],
        [
          "IntergerExpression",
          "1"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          2,
          5
        ],
        [
          5,
          6
        ],
        [
          5,
          7
        ]
      ],
      "lines": 28
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "printLine ( data ) ;"
        ],
        [
          "CallExpression",
          "printLine ( data )"
        ],
        [
          "Callee",
          "printLine"
        ],
        [
          "ArgumentList",
          "data"
        ],
        [
          "Identifier",
          "printLine"
        ],
        [
          "Argument",
          "data"
        ],
        [
          "Identifier",
          "data"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          5
        ],
        [
          5,
          6
        ]
      ],
      "lines": 29
    },
    {
      "contents": [
        [
          "ExpressionStatement",
          "free ( data ) ;"
        ],
        [
          "CallExpression",
          "free ( data )"
        ],
        [
          "Callee",
          "free"
        ],
        [
          "ArgumentList",
          "data"
        ],
        [
          "Identifier",
          "free"
        ],
        [
          "Argument",
          "data"
        ],
        [
          "Identifier",
          "data"
        ]
      ],
      "edges": [
        [
          0,
          1
        ],
        [
          1,
          2
        ],
        [
          1,
          3
        ],
        [
          2,
          4
        ],
        [
          3,
          5
        ],
        [
          5,
          6
        ]
      ],
      "lines": 30
    }
  ],
  "cfgEdges": [
    [
      0,
      1,
      ""
    ],
    [
      1,
      2,
      ""
    ],
    [
      2,
      3,
      ""
    ],
    [
      3,
      4,
      "case 6"
    ],
    [
      3,
      10,
      "default"
    ],
    [
      4,
      5,
      ""
    ],
    [
      5,
      6,
      ""
    ],
    [
      6,
      7,
      "True"
    ],
    [
      6,
      8,
      "False"
    ],
    [
      7,
      8,
      ""
    ],
    [
      8,
      9,
      ""
    ],
    [
      9,
      13,
      ""
    ],
    [
      10,
      11,
      ""
    ],
    [
      11,
      12,
      ""
    ],
    [
      12,
      13,
      ""
    ],
    [
      13,
      14,
      ""
    ],
    [
      14,
      15,
      ""
    ],
    [
      15,
      16,
      ""
    ],
    [
      16,
      17,
      ""
    ],
    [
      18,
      20,
      "True"
    ],
    [
      18,
      21,
      "False"
    ],
    [
      17,
      18,
      ""
    ],
    [
      19,
      18,
      ""
    ],
    [
      20,
      19,
      ""
    ],
    [
      21,
      22,
      ""
    ],
    [
      22,
      23,
      ""
    ]
  ],
  "cdgEdges": [
    [
      18,
      19
    ],
    [
      18,
      20
    ],
    [
      3,
      12
    ],
    [
      3,
      11
    ],
    [
      3,
      10
    ],
    [
      3,
      9
    ],
    [
      3,
      8
    ],
    [
      3,
      6
    ],
    [
      3,
      5
    ],
    [
      3,
      4
    ],
    [
      6,
      7
    ]
  ],
  "ddgEdges": [
    [
      14,
      16,
      "source"
    ],
    [
      14,
      15,
      "source"
    ],
    [
      14,
      20,
      "source"
    ],
    [
      19,
      18,
      "i"
    ],
    [
      17,
      19,
      "i"
    ],
    [
      17,
      20,
      "i"
    ],
    [
      19,
      20,
      "i"
    ],
    [
      17,
      18,
      "i"
    ],
    [
      5,
      8,
      "data"
    ],
    [
      5,
      6,
      "data"
    ],
    [
      2,
      20,
      "data"
    ],
    [
      5,
      20,
      "data"
    ],
    [
      2,
      21,
      "data"
    ],
    [
      5,
      21,
      "data"
    ],
    [
      5,
      22,
      "data"
    ],
    [
      2,
      23,
      "data"
    ],
    [
      16,
      20,
      "* source"
    ],
    [
      5,
      23,
      "data"
    ],
    [
      2,
      22,
      "data"
    ]
  ]
}