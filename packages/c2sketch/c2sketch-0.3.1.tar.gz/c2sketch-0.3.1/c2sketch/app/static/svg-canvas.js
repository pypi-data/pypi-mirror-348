class SVGCanvas extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
        
        const style = document.createElement('style');
        const slot = document.createElement('slot');
        const block = document.createElement('div');
        block.classList.add('block');

        style.innerHTML = ':host {position: relative; overflow: clip;} div.block {position: absolute; width: content-height; height: content-width;}';
        this.shadowRoot.append(style);
        this.shadowRoot.append(block);
        block.appendChild(slot);

        var last_pos = null;
        block.addEventListener('mousedown', e => {
            last_pos = [e.clientX,e.clientY];
            document.body.style.cursor = 'move';
        });
        block.addEventListener('mousemove', e => {
            if( last_pos !== null) {
                const cur_left_px = getComputedStyle(block).left;
                const cur_left = parseInt(cur_left_px.substring(0,cur_left_px.length -2));
                const new_left = cur_left + (e.clientX - last_pos[0]);
                const cur_top_px = getComputedStyle(block).top;
                const cur_top = parseInt(cur_top_px.substring(0,cur_top_px.length -2));
                const new_top = cur_top + (e.clientY - last_pos[1]);
                
                block.style.left = `${new_left}px`;
                block.style.top = `${new_top}px`;
                
                last_pos = [e.clientX,e.clientY];
            }
        });
        block.addEventListener('mouseup', e => {
            last_pos = null;
            document.body.style.removeProperty('cursor');
        });
    }
}

customElements.define('svg-canvas',SVGCanvas);