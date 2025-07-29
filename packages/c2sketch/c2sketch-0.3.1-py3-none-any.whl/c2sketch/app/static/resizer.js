
let resize_start = 0;
let resize_width = 0;
let resize_element = null;

class FlexResizer extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.attachShadow({mode: 'open'});
        const sizer = document.createElement('div');
        sizer.classList.add('resizer');
        sizer.setAttribute('style','cursor: ew-resize');
        sizer.innerHTML = '&nbsp;'
        this.shadowRoot.append(sizer);

        this.addEventListener('mousedown', (e) => {
            resize_element = e.target.previousElementSibling;
            resize_start = e.clientX;
            resize_width = resize_element.getBoundingClientRect().width;
            document.body.style.cursor = 'ew-resize';
        });
        document.addEventListener('mousemove', e => {
            if( resize_element !== null) {
                resize_element.style.width = `${resize_width+(e.clientX - resize_start)}px`;
            }
        });
        document.addEventListener('mouseup', el => {
            resize_element = null;
            document.body.style.removeProperty('cursor');
        });
    }
}
customElements.define('flex-resizer',FlexResizer);
