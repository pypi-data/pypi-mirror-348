import 'https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.min.js';

ace.config.set('basePath', 'https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/');

class C2SEditor extends(HTMLElement) {
    constructor() {
        super();
    }
    connectedCallback() {
        this.attachShadow({mode: 'open'});
        
        const style = document.createElement('style');
        style.textContent = `
        :host { display: flex;}
        :host > div {
            flex: 1 1 auto;
            align-self: stretch;
        }
        .code-error {
            position:absolute;
            background-color: #ef2e55;
        }
        `;
        this.shadowRoot.append(style);
        const container = document.createElement('div');
        this.shadowRoot.append(container);
        
        this.codeContainer = this.querySelector('c2s-code');

        this.editor = ace.edit(container,{value: this.codeContainer.textContent.trim()});
        this.editor.renderer.attachToShadowRoot();
        
        ace.config.setModuleUrl("ace/mode/c2sketch","/static/c2s_mode.js");
        this.editor.setOption("mode","ace/mode/c2sketch");
        this.editor.setOption("theme","ace/theme/tomorrow");

        const enabled = this.getAttribute("enabled");
        if(enabled === "false") {
            this.editor.setOptions({
                readOnly: true,
                highlightActiveLine: false,
                highlightGutterLine: false,
            });
            this.editor.container.style.opacity=0.5;
        }

        if(this.hasAttribute("onchange")) {
            const handler = this.getAttribute("onchange");
            this.editor.addEventListener('change', (e) => {
                eval(handler);
            });
        }

        this.problems = this.querySelectorAll('c2s-problem');
        var annotations = [];
        for(var problem of this.problems) {
            const start = parseInt(problem.getAttribute("start"));
            const end = parseInt(problem.getAttribute("end"));
            annotations.push({
                row: start - 1,
                text: problem.textContent, 
                type: 'error'
            });
            this.editor.session.addMarker(new ace.Range(start - 1,null,end,null), 'code-error', 'text');
        }
        this.editor.getSession().setAnnotations(annotations);
    }
    get name() {
        return this.getAttribute('name');
    }
    get value() {
        return this.editor.getValue();
    }
}
customElements.define('c2s-editor',C2SEditor);