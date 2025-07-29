define('ace/mode/c2sketch', function(require, exports, module) {

var oop = require("ace/lib/oop");
var TextMode = require("ace/mode/text").Mode;
var C2SketchHighlightRules = require("ace/mode/c2sketch_highlight_rules").C2SketchHighlightRules;

var Mode = function() {
    this.HighlightRules = C2SketchHighlightRules;
};
oop.inherits(Mode, TextMode);
exports.Mode = Mode;
});

define('ace/mode/c2sketch_highlight_rules', function(require, exports, module) {

var oop = require("ace/lib/oop");
var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

var C2SketchHighlightRules = function() {
    this.$rules = {
        "start": [
            {token : "comment.line.number-sign.c2sketch",
            regex : "#.*$"
            },
            {token :"keyword.operator.new.c2sketch"
			,regex : "(<->|->|<-)"
            },
            {token : "keyword.control.c2sketch"
            ,regex:"\\b(import|actor|member|group|location|at-location|task-def|task-instance|task-ref|task|info-req|info-space|trigger|record-type|record|field-mode|field|key-limit|age-limit)\\b"
            },
            {token : "variable.name.c2sketch"
            ,regex: "\\@[a-zA-Z0-9_\\-]+"
            },
            { token: "constant.language.c2sketch"
		    , regex: "\\b(key|first|last|min|max)\\b"
			},
            {token: "variable.name.c2sketch"
			,regex: "\\@[a-zA-Z0-9_\\-]+"
            },
            {token: "support.function.c2sketch"
			,regex: "![a-zA-Z0-9_\\-]+"
            },
            {token: "constant.numeric.c2sketch"
			,regex: "[\\+\\-]?[0-9]+"
            },
            {token: "punctuation.quote.c2sketch"
            ,regex: '"'
            ,push: [{token: "punctuation.quote.c2sketch"
                    ,regex: '"'
                    ,next: 'pop'
                },{defaultToken: 'string'}]
            }
        ]
    }
    this.normalizeRules();
}
oop.inherits(C2SketchHighlightRules, TextHighlightRules);
exports.C2SketchHighlightRules = C2SketchHighlightRules;
});