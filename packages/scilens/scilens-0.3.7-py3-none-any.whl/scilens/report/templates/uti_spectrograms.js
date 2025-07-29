((w_1, undef) => {
//
// tmp
//
function resize22(obj, parent, dir) { // ASSUMPTIONS : obj.size int, "js-plotly-plot"
  // size
  const size = obj.size + (dir * obj.size * 0.1); // new size
  obj.size = obj.size + (dir * obj.size * 0.1); // save
  // update widgets
  const update = { width: size, height: size };
  const nodes = dom.q(parent, ".js-plotly-plot");
  nodes.forEach((node) => {
    node.style.width  = size + "px";
    node.style.height = size + "px";
    Plotly.relayout(node, update); // update plotly
  });
}
//
//
//
const PREFIX = "spectrograms_"; // section prefix
const DEFAULT_SIZE = 300;
const COLORSCALE = "Viridis"; // plotly
const COLORSCALE_DIFF = "RdBu"; // plotly
//
class Spectrograms {
  constructor(index, arr_mat) {
    console.log("index data", index);
    // data
    this.size = DEFAULT_SIZE;
    this.arr_mat = arr_mat;
    this.elt = dom.get(PREFIX+(1+index));
    // init
    this.init();
  }
  init() {
    // resize
    const that = this;
    //
    const tmpls = []
    this.arr_mat.forEach((mat, i) => { tmpls.push({tag:"button", html: mat.name, click: function() { that.var_toogle(i); } }) });
    //
    dom.tree(
      this.elt,
      {tag:"div", children: [
        {tag:"div", attrs:{class:"py-2"}, children: [
          {tag:"button", html: '+ Increase', click: function() { resize22(that, that.elt, 1); }},
          {tag:"button", html: '- Decrease', click: function() { resize22(that, that.elt, -1); }},
        ]},
        {tag:"div", attrs:{class:"py-2"}, children: tmpls},  
      ]},
    );
    // toogle
    // Show all
    this.arr_mat.forEach((mat, i) => { this.var_add(i); });
  }
  var_get_id(idx) {
    return PREFIX+"block_"+idx;
  }
  var_toogle(idx) {
    if (dom.get(this.var_get_id(idx))) { this.var_rmv(idx); }
    else { this.var_add(idx); }
  }
  var_add(idx) {
    const mat = this.arr_mat[idx];
    //
    const style = "width:"+this.size+"px;height:"+this.size+"px;";
    const attrs = { class: "m-1 shadow-lg" };
    //
    const templs = [{out:"var", tag:"div", attrs: attrs, style:style} ];
    if (mat.ref) {
      templs.push({out:"ref", tag:"div", attrs: attrs, style:style});
      templs.push({out:"dif", tag:"div", attrs: attrs, style:style});
    }
    const e = {};
    dom.tree(
      this.elt,
      {tag:"div", attrs: {id: this.var_get_id(idx)}, children: [
          {tag:"div", style:"display: flex; flex-wrap: wrap;", children: templs},
      ]},
      e
    );

    this.add_widget(e["var"], mat.data);
    if (mat.ref) {
      this.add_widget(e["ref"], mat.ref);
      this.add_widget(e["dif"], mat.ref_diff_data(), COLORSCALE_DIFF);
    }
  }
  var_rmv(idx) {
    dom.get(this.var_get_id(idx)).remove();
  }
  add_widget(elt, mat, colorscale=COLORSCALE) {
    const data = [{
        z: mat,
        type: 'heatmap',
        colorscale: colorscale,
    }];

    const layout = {
        // title: mat.name,
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };

    Plotly.newPlot(elt, data, layout);        
  }
}
w_1.Spectrograms = Spectrograms;
})(window);