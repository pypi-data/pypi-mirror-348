import { defineComponent as d, ref as l, watch as u, createElementBlock as g, openBlock as _ } from "vue";
import o from "mermaid";
const v = "instaui-mermaid_svg-";
let h = 0;
function k() {
  return `${v}${h++}`;
}
const C = /* @__PURE__ */ d({
  __name: "Mermaid",
  props: {
    graph: {},
    initConfig: {}
  },
  emits: ["update:graph"],
  setup(a, { emit: s }) {
    const r = a, c = s, {
      initConfig: m = {
        securityLevel: "loose"
      }
    } = r;
    o.initialize({
      ...m,
      startOnLoad: !1
    });
    const i = l(), p = k();
    return u([() => r.graph, i], async ([t, e]) => {
      if (e) {
        const { svg: f, bindFunctions: n } = await o.render(
          p,
          t,
          e
        );
        e.innerHTML = f, n == null || n(e), c("update:graph", t);
      }
    }), (t, e) => (_(), g("div", {
      ref_key: "container",
      ref: i
    }, null, 512));
  }
});
export {
  C as default
};
