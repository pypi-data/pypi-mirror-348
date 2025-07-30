import { i as Gt, a as he, r as Kt, w as le, g as qt, c as Y, b as Yt } from "./Index-pnW_-s4y.js";
const _ = window.ms_globals.React, g = window.ms_globals.React, Xt = window.ms_globals.React.forwardRef, Nt = window.ms_globals.React.useRef, Vt = window.ms_globals.React.useState, Wt = window.ms_globals.React.useEffect, Ut = window.ms_globals.React.version, vt = window.ms_globals.React.useMemo, $e = window.ms_globals.ReactDOM.createPortal, Qt = window.ms_globals.internalContext.useContextPropsContext, Jt = window.ms_globals.internalContext.ContextPropsProvider, Zt = window.ms_globals.antd.ConfigProvider, De = window.ms_globals.antd.theme, er = window.ms_globals.antd.Avatar, re = window.ms_globals.antdCssinjs.unit, Me = window.ms_globals.antdCssinjs.token2CSSVar, Ke = window.ms_globals.antdCssinjs.useStyleRegister, tr = window.ms_globals.antdCssinjs.useCSSVarRegister, rr = window.ms_globals.antdCssinjs.createTheme, nr = window.ms_globals.antdCssinjs.useCacheToken, St = window.ms_globals.antdCssinjs.Keyframes;
var or = /\s/;
function ir(t) {
  for (var e = t.length; e-- && or.test(t.charAt(e)); )
    ;
  return e;
}
var sr = /^\s+/;
function ar(t) {
  return t && t.slice(0, ir(t) + 1).replace(sr, "");
}
var qe = NaN, cr = /^[-+]0x[0-9a-f]+$/i, lr = /^0b[01]+$/i, ur = /^0o[0-7]+$/i, fr = parseInt;
function Ye(t) {
  if (typeof t == "number")
    return t;
  if (Gt(t))
    return qe;
  if (he(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = he(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = ar(t);
  var r = lr.test(t);
  return r || ur.test(t) ? fr(t.slice(2), r ? 2 : 8) : cr.test(t) ? qe : +t;
}
var Re = function() {
  return Kt.Date.now();
}, dr = "Expected a function", hr = Math.max, gr = Math.min;
function mr(t, e, r) {
  var o, n, i, s, a, c, l = 0, u = !1, f = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(dr);
  e = Ye(e) || 0, he(r) && (u = !!r.leading, f = "maxWait" in r, i = f ? hr(Ye(r.maxWait) || 0, e) : i, d = "trailing" in r ? !!r.trailing : d);
  function v(m) {
    var P = o, O = n;
    return o = n = void 0, l = m, s = t.apply(O, P), s;
  }
  function S(m) {
    return l = m, a = setTimeout(x, e), u ? v(m) : s;
  }
  function E(m) {
    var P = m - c, O = m - l, b = e - P;
    return f ? gr(b, i - O) : b;
  }
  function p(m) {
    var P = m - c, O = m - l;
    return c === void 0 || P >= e || P < 0 || f && O >= i;
  }
  function x() {
    var m = Re();
    if (p(m))
      return C(m);
    a = setTimeout(x, E(m));
  }
  function C(m) {
    return a = void 0, d && o ? v(m) : (o = n = void 0, s);
  }
  function R() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = n = a = void 0;
  }
  function h() {
    return a === void 0 ? s : C(Re());
  }
  function w() {
    var m = Re(), P = p(m);
    if (o = arguments, n = this, c = m, P) {
      if (a === void 0)
        return S(c);
      if (f)
        return clearTimeout(a), a = setTimeout(x, e), v(c);
    }
    return a === void 0 && (a = setTimeout(x, e)), s;
  }
  return w.cancel = R, w.flush = h, w;
}
var xt = {
  exports: {}
}, pe = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var pr = g, br = Symbol.for("react.element"), yr = Symbol.for("react.fragment"), vr = Object.prototype.hasOwnProperty, Sr = pr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, xr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Ct(t, e, r) {
  var o, n = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) vr.call(e, o) && !xr.hasOwnProperty(o) && (n[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) n[o] === void 0 && (n[o] = e[o]);
  return {
    $$typeof: br,
    type: t,
    key: i,
    ref: s,
    props: n,
    _owner: Sr.current
  };
}
pe.Fragment = yr;
pe.jsx = Ct;
pe.jsxs = Ct;
xt.exports = pe;
var D = xt.exports;
const {
  SvelteComponent: Cr,
  assign: Qe,
  binding_callbacks: Je,
  check_outros: wr,
  children: wt,
  claim_element: _t,
  claim_space: _r,
  component_subscribe: Ze,
  compute_slots: Tr,
  create_slot: Er,
  detach: Q,
  element: Tt,
  empty: et,
  exclude_internal_props: tt,
  get_all_dirty_from_scope: Pr,
  get_slot_changes: Or,
  group_outros: Mr,
  init: Rr,
  insert_hydration: ue,
  safe_not_equal: jr,
  set_custom_element_data: Et,
  space: Ir,
  transition_in: fe,
  transition_out: Be,
  update_slot_base: kr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Lr,
  getContext: $r,
  onDestroy: Dr,
  setContext: Br
} = window.__gradio__svelte__internal;
function rt(t) {
  let e, r;
  const o = (
    /*#slots*/
    t[7].default
  ), n = Er(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Tt("svelte-slot"), n && n.c(), this.h();
    },
    l(i) {
      e = _t(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = wt(e);
      n && n.l(s), s.forEach(Q), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      ue(i, e, s), n && n.m(e, null), t[9](e), r = !0;
    },
    p(i, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && kr(
        n,
        o,
        i,
        /*$$scope*/
        i[6],
        r ? Or(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Pr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (fe(n, i), r = !0);
    },
    o(i) {
      Be(n, i), r = !1;
    },
    d(i) {
      i && Q(e), n && n.d(i), t[9](null);
    }
  };
}
function Hr(t) {
  let e, r, o, n, i = (
    /*$$slots*/
    t[4].default && rt(t)
  );
  return {
    c() {
      e = Tt("react-portal-target"), r = Ir(), i && i.c(), o = et(), this.h();
    },
    l(s) {
      e = _t(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), wt(e).forEach(Q), r = _r(s), i && i.l(s), o = et(), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ue(s, e, a), t[8](e), ue(s, r, a), i && i.m(s, a), ue(s, o, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && fe(i, 1)) : (i = rt(s), i.c(), fe(i, 1), i.m(o.parentNode, o)) : i && (Mr(), Be(i, 1, 1, () => {
        i = null;
      }), wr());
    },
    i(s) {
      n || (fe(i), n = !0);
    },
    o(s) {
      Be(i), n = !1;
    },
    d(s) {
      s && (Q(e), Q(r), Q(o)), t[8](null), i && i.d(s);
    }
  };
}
function nt(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function zr(t, e, r) {
  let o, n, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = Tr(i);
  let {
    svelteInit: c
  } = e;
  const l = le(nt(e)), u = le();
  Ze(t, u, (h) => r(0, o = h));
  const f = le();
  Ze(t, f, (h) => r(1, n = h));
  const d = [], v = $r("$$ms-gr-react-wrapper"), {
    slotKey: S,
    slotIndex: E,
    subSlotIndex: p
  } = qt() || {}, x = c({
    parent: v,
    props: l,
    target: u,
    slot: f,
    slotKey: S,
    slotIndex: E,
    subSlotIndex: p,
    onDestroy(h) {
      d.push(h);
    }
  });
  Br("$$ms-gr-react-wrapper", x), Lr(() => {
    l.set(nt(e));
  }), Dr(() => {
    d.forEach((h) => h());
  });
  function C(h) {
    Je[h ? "unshift" : "push"](() => {
      o = h, u.set(o);
    });
  }
  function R(h) {
    Je[h ? "unshift" : "push"](() => {
      n = h, f.set(n);
    });
  }
  return t.$$set = (h) => {
    r(17, e = Qe(Qe({}, e), tt(h))), "svelteInit" in h && r(5, c = h.svelteInit), "$$scope" in h && r(6, s = h.$$scope);
  }, e = tt(e), [o, n, u, f, a, c, s, i, C, R];
}
class Ar extends Cr {
  constructor(e) {
    super(), Rr(this, e, zr, Hr, jr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: lo
} = window.__gradio__svelte__internal, ot = window.ms_globals.rerender, je = window.ms_globals.tree;
function Fr(t, e = {}) {
  function r(o) {
    const n = le(), i = new Ar({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? je;
          return c.nodes = [...c.nodes, a], ot({
            createPortal: $e,
            node: je
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== n), ot({
              createPortal: $e,
              node: je
            });
          }), a;
        },
        ...o.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(r);
    });
  });
}
const Xr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Nr(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const o = t[r];
    return e[r] = Vr(r, o), e;
  }, {}) : {};
}
function Vr(t, e) {
  return typeof e == "number" && !Xr.includes(t) ? e + "px" : e;
}
function He(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement) {
    const n = g.Children.toArray(t._reactElement.props.children).map((i) => {
      if (g.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = He(i.props.el);
        return g.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...g.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return n.originalChildren = t._reactElement.props.children, e.push($e(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: n
    }), r)), {
      clonedElement: r,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((n) => {
    t.getEventListeners(n).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const o = Array.from(t.childNodes);
  for (let n = 0; n < o.length; n++) {
    const i = o[n];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = He(i);
      e.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Wr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const U = Xt(({
  slot: t,
  clone: e,
  className: r,
  style: o,
  observeAttributes: n
}, i) => {
  const s = Nt(), [a, c] = Vt([]), {
    forceClone: l
  } = Qt(), u = l ? !0 : e;
  return Wt(() => {
    var E;
    if (!s.current || !t)
      return;
    let f = t;
    function d() {
      let p = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (p = f.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), Wr(i, p), r && p.classList.add(...r.split(" ")), o) {
        const x = Nr(o);
        Object.keys(x).forEach((C) => {
          p.style[C] = x[C];
        });
      }
    }
    let v = null, S = null;
    if (u && window.MutationObserver) {
      let p = function() {
        var h, w, m;
        (h = s.current) != null && h.contains(f) && ((w = s.current) == null || w.removeChild(f));
        const {
          portals: C,
          clonedElement: R
        } = He(t);
        f = R, c(C), f.style.display = "contents", S && clearTimeout(S), S = setTimeout(() => {
          d();
        }, 50), (m = s.current) == null || m.appendChild(f);
      };
      p();
      const x = mr(() => {
        p(), v == null || v.disconnect(), v == null || v.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: n
        });
      }, 50);
      v = new window.MutationObserver(x), v.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (E = s.current) == null || E.appendChild(f);
    return () => {
      var p, x;
      f.style.display = "", (p = s.current) != null && p.contains(f) && ((x = s.current) == null || x.removeChild(f)), v == null || v.disconnect();
    };
  }, [t, u, r, o, i, n, l]), g.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Ur = "1.2.0", Gr = /* @__PURE__ */ g.createContext({}), Kr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, qr = (t) => {
  const e = g.useContext(Gr);
  return g.useMemo(() => ({
    ...Kr,
    ...e[t]
  }), [e[t]]);
};
function J() {
  return J = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var r = arguments[e];
      for (var o in r) ({}).hasOwnProperty.call(r, o) && (t[o] = r[o]);
    }
    return t;
  }, J.apply(null, arguments);
}
function ge() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: r,
    iconPrefixCls: o,
    theme: n
  } = g.useContext(Zt.ConfigContext);
  return {
    theme: n,
    getPrefixCls: t,
    direction: e,
    csp: r,
    iconPrefixCls: o
  };
}
function Yr(t) {
  var e = _.useRef();
  e.current = t;
  var r = _.useCallback(function() {
    for (var o, n = arguments.length, i = new Array(n), s = 0; s < n; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return r;
}
function Qr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var it = Qr() ? _.useLayoutEffect : _.useEffect, Jr = function(e, r) {
  var o = _.useRef(!0);
  it(function() {
    return e(o.current);
  }, r), it(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function ne(t) {
  "@babel/helpers - typeof";
  return ne = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, ne(t);
}
var T = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Fe = Symbol.for("react.element"), Xe = Symbol.for("react.portal"), be = Symbol.for("react.fragment"), ye = Symbol.for("react.strict_mode"), ve = Symbol.for("react.profiler"), Se = Symbol.for("react.provider"), xe = Symbol.for("react.context"), Zr = Symbol.for("react.server_context"), Ce = Symbol.for("react.forward_ref"), we = Symbol.for("react.suspense"), _e = Symbol.for("react.suspense_list"), Te = Symbol.for("react.memo"), Ee = Symbol.for("react.lazy"), en = Symbol.for("react.offscreen"), Pt;
Pt = Symbol.for("react.module.reference");
function z(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case Fe:
        switch (t = t.type, t) {
          case be:
          case ve:
          case ye:
          case we:
          case _e:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case Zr:
              case xe:
              case Ce:
              case Ee:
              case Te:
              case Se:
                return t;
              default:
                return e;
            }
        }
      case Xe:
        return e;
    }
  }
}
T.ContextConsumer = xe;
T.ContextProvider = Se;
T.Element = Fe;
T.ForwardRef = Ce;
T.Fragment = be;
T.Lazy = Ee;
T.Memo = Te;
T.Portal = Xe;
T.Profiler = ve;
T.StrictMode = ye;
T.Suspense = we;
T.SuspenseList = _e;
T.isAsyncMode = function() {
  return !1;
};
T.isConcurrentMode = function() {
  return !1;
};
T.isContextConsumer = function(t) {
  return z(t) === xe;
};
T.isContextProvider = function(t) {
  return z(t) === Se;
};
T.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === Fe;
};
T.isForwardRef = function(t) {
  return z(t) === Ce;
};
T.isFragment = function(t) {
  return z(t) === be;
};
T.isLazy = function(t) {
  return z(t) === Ee;
};
T.isMemo = function(t) {
  return z(t) === Te;
};
T.isPortal = function(t) {
  return z(t) === Xe;
};
T.isProfiler = function(t) {
  return z(t) === ve;
};
T.isStrictMode = function(t) {
  return z(t) === ye;
};
T.isSuspense = function(t) {
  return z(t) === we;
};
T.isSuspenseList = function(t) {
  return z(t) === _e;
};
T.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === be || t === ve || t === ye || t === we || t === _e || t === en || typeof t == "object" && t !== null && (t.$$typeof === Ee || t.$$typeof === Te || t.$$typeof === Se || t.$$typeof === xe || t.$$typeof === Ce || t.$$typeof === Pt || t.getModuleId !== void 0);
};
T.typeOf = z;
Number(Ut.split(".")[0]);
function tn(t, e) {
  if (ne(t) != "object" || !t) return t;
  var r = t[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(t, e);
    if (ne(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function rn(t) {
  var e = tn(t, "string");
  return ne(e) == "symbol" ? e : e + "";
}
function nn(t, e, r) {
  return (e = rn(e)) in t ? Object.defineProperty(t, e, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = r, t;
}
function st(t, e) {
  var r = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(t, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function on(t) {
  for (var e = 1; e < arguments.length; e++) {
    var r = arguments[e] != null ? arguments[e] : {};
    e % 2 ? st(Object(r), !0).forEach(function(o) {
      nn(t, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : st(Object(r)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return t;
}
function N(t) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, N(t);
}
function sn(t, e) {
  if (N(t) != "object" || !t) return t;
  var r = t[Symbol.toPrimitive];
  if (r !== void 0) {
    var o = r.call(t, e);
    if (N(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function Ot(t) {
  var e = sn(t, "string");
  return N(e) == "symbol" ? e : e + "";
}
function j(t, e, r) {
  return (e = Ot(e)) in t ? Object.defineProperty(t, e, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = r, t;
}
function at(t, e) {
  var r = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(n) {
      return Object.getOwnPropertyDescriptor(t, n).enumerable;
    })), r.push.apply(r, o);
  }
  return r;
}
function H(t) {
  for (var e = 1; e < arguments.length; e++) {
    var r = arguments[e] != null ? arguments[e] : {};
    e % 2 ? at(Object(r), !0).forEach(function(o) {
      j(t, o, r[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : at(Object(r)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(r, o));
    });
  }
  return t;
}
function an(t) {
  if (Array.isArray(t)) return t;
}
function cn(t, e) {
  var r = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (r != null) {
    var o, n, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (r = r.call(t)).next, e === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (o = i.call(r)).done) && (a.push(o.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, n = u;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw n;
      }
    }
    return a;
  }
}
function ct(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var r = 0, o = Array(e); r < e; r++) o[r] = t[r];
  return o;
}
function ln(t, e) {
  if (t) {
    if (typeof t == "string") return ct(t, e);
    var r = {}.toString.call(t).slice(8, -1);
    return r === "Object" && t.constructor && (r = t.constructor.name), r === "Map" || r === "Set" ? Array.from(t) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? ct(t, e) : void 0;
  }
}
function un() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function de(t, e) {
  return an(t) || cn(t, e) || ln(t, e) || un();
}
function Pe(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function fn(t, e) {
  for (var r = 0; r < e.length; r++) {
    var o = e[r];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, Ot(o.key), o);
  }
}
function Oe(t, e, r) {
  return e && fn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function ze(t, e) {
  return ze = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, o) {
    return r.__proto__ = o, r;
  }, ze(t, e);
}
function Mt(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && ze(t, e);
}
function me(t) {
  return me = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, me(t);
}
function Rt() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Rt = function() {
    return !!t;
  })();
}
function te(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function dn(t, e) {
  if (e && (N(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return te(t);
}
function jt(t) {
  var e = Rt();
  return function() {
    var r, o = me(t);
    if (e) {
      var n = me(this).constructor;
      r = Reflect.construct(o, arguments, n);
    } else r = o.apply(this, arguments);
    return dn(this, r);
  };
}
var It = /* @__PURE__ */ Oe(function t() {
  Pe(this, t);
}), kt = "CALC_UNIT", hn = new RegExp(kt, "g");
function Ie(t) {
  return typeof t == "number" ? "".concat(t).concat(kt) : t;
}
var gn = /* @__PURE__ */ function(t) {
  Mt(r, t);
  var e = jt(r);
  function r(o, n) {
    var i;
    Pe(this, r), i = e.call(this), j(te(i), "result", ""), j(te(i), "unitlessCssVar", void 0), j(te(i), "lowPriority", void 0);
    var s = N(o);
    return i.unitlessCssVar = n, o instanceof r ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = Ie(o) : s === "string" && (i.result = o), i;
  }
  return Oe(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " + ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " + ").concat(Ie(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result = "".concat(this.result, " - ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " - ").concat(Ie(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof r ? this.result = "".concat(this.result, " * ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " * ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof r ? this.result = "".concat(this.result, " / ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " / ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(n) {
      return this.lowPriority || n ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(n) {
      var i = this, s = n || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return i.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(hn, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(It), mn = /* @__PURE__ */ function(t) {
  Mt(r, t);
  var e = jt(r);
  function r(o) {
    var n;
    return Pe(this, r), n = e.call(this), j(te(n), "result", 0), o instanceof r ? n.result = o.result : typeof o == "number" && (n.result = o), n;
  }
  return Oe(r, [{
    key: "add",
    value: function(n) {
      return n instanceof r ? this.result += n.result : typeof n == "number" && (this.result += n), this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof r ? this.result -= n.result : typeof n == "number" && (this.result -= n), this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return n instanceof r ? this.result *= n.result : typeof n == "number" && (this.result *= n), this;
    }
  }, {
    key: "div",
    value: function(n) {
      return n instanceof r ? this.result /= n.result : typeof n == "number" && (this.result /= n), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(It), pn = function(e, r) {
  var o = e === "css" ? gn : mn;
  return function(n) {
    return new o(n, r);
  };
}, lt = function(e, r) {
  return "".concat([r, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ut(t, e, r, o) {
  var n = H({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var c = de(a, 2), l = c[0], u = c[1];
      if (n != null && n[l] || n != null && n[u]) {
        var f;
        (f = n[u]) !== null && f !== void 0 || (n[u] = n == null ? void 0 : n[l]);
      }
    });
  }
  var s = H(H({}, r), n);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Lt = typeof CSSINJS_STATISTIC < "u", Ae = !0;
function Ne() {
  for (var t = arguments.length, e = new Array(t), r = 0; r < t; r++)
    e[r] = arguments[r];
  if (!Lt)
    return Object.assign.apply(Object, [{}].concat(e));
  Ae = !1;
  var o = {};
  return e.forEach(function(n) {
    if (N(n) === "object") {
      var i = Object.keys(n);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return n[s];
          }
        });
      });
    }
  }), Ae = !0, o;
}
var ft = {};
function bn() {
}
var yn = function(e) {
  var r, o = e, n = bn;
  return Lt && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if (Ae) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), n = function(s, a) {
    var c;
    ft[s] = {
      global: Array.from(r),
      component: H(H({}, (c = ft[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: r,
    flush: n
  };
};
function dt(t, e, r) {
  if (typeof r == "function") {
    var o;
    return r(Ne(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return r ?? {};
}
function vn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "max(".concat(o.map(function(i) {
        return re(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, o = new Array(r), n = 0; n < r; n++)
        o[n] = arguments[n];
      return "min(".concat(o.map(function(i) {
        return re(i);
      }).join(","), ")");
    }
  };
}
var Sn = 1e3 * 60 * 10, xn = /* @__PURE__ */ function() {
  function t() {
    Pe(this, t), j(this, "map", /* @__PURE__ */ new Map()), j(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), j(this, "nextID", 0), j(this, "lastAccessBeat", /* @__PURE__ */ new Map()), j(this, "accessBeat", 0);
  }
  return Oe(t, [{
    key: "set",
    value: function(r, o) {
      this.clear();
      var n = this.getCompositeKey(r);
      this.map.set(n, o), this.lastAccessBeat.set(n, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var o = this.getCompositeKey(r), n = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, n;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var o = this, n = r.map(function(i) {
        return i && N(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(N(i), "_").concat(i);
      });
      return n.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var o = this.nextID;
      return this.objectIDMap.set(r, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(n, i) {
          o - n > Sn && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), ht = new xn();
function Cn(t, e) {
  return g.useMemo(function() {
    var r = ht.get(e);
    if (r)
      return r;
    var o = t();
    return ht.set(e, o), o;
  }, e);
}
var wn = function() {
  return {};
};
function _n(t) {
  var e = t.useCSP, r = e === void 0 ? wn : e, o = t.useToken, n = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function c(d, v, S, E) {
    var p = Array.isArray(d) ? d[0] : d;
    function x(O) {
      return "".concat(String(p)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var C = (E == null ? void 0 : E.unitless) || {}, R = typeof a == "function" ? a(d) : {}, h = H(H({}, R), {}, j({}, x("zIndexPopup"), !0));
    Object.keys(C).forEach(function(O) {
      h[x(O)] = C[O];
    });
    var w = H(H({}, E), {}, {
      unitless: h,
      prefixToken: x
    }), m = u(d, v, S, w), P = l(p, S, w);
    return function(O) {
      var b = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, M = m(O, b), A = de(M, 2), y = A[1], I = P(b), k = de(I, 2), L = k[0], B = k[1];
      return [L, y, B];
    };
  }
  function l(d, v, S) {
    var E = S.unitless, p = S.injectStyle, x = p === void 0 ? !0 : p, C = S.prefixToken, R = S.ignore, h = function(P) {
      var O = P.rootCls, b = P.cssVar, M = b === void 0 ? {} : b, A = o(), y = A.realToken;
      return tr({
        path: [d],
        prefix: M.prefix,
        key: M.key,
        unitless: E,
        ignore: R,
        token: y,
        scope: O
      }, function() {
        var I = dt(d, y, v), k = ut(d, y, I, {
          deprecatedTokens: S == null ? void 0 : S.deprecatedTokens
        });
        return Object.keys(I).forEach(function(L) {
          k[C(L)] = k[L], delete k[L];
        }), k;
      }), null;
    }, w = function(P) {
      var O = o(), b = O.cssVar;
      return [function(M) {
        return x && b ? /* @__PURE__ */ g.createElement(g.Fragment, null, /* @__PURE__ */ g.createElement(h, {
          rootCls: P,
          cssVar: b,
          component: d
        }), M) : M;
      }, b == null ? void 0 : b.key];
    };
    return w;
  }
  function u(d, v, S) {
    var E = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], x = de(p, 1), C = x[0], R = p.join("-"), h = t.layer || {
      name: "antd"
    };
    return function(w) {
      var m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : w, P = o(), O = P.theme, b = P.realToken, M = P.hashId, A = P.token, y = P.cssVar, I = n(), k = I.rootPrefixCls, L = I.iconPrefixCls, B = r(), F = y ? "css" : "js", G = Cn(function() {
        var X = /* @__PURE__ */ new Set();
        return y && Object.keys(E.unitless || {}).forEach(function(W) {
          X.add(Me(W, y.prefix)), X.add(Me(W, lt(C, y.prefix)));
        }), pn(F, X);
      }, [F, C, y == null ? void 0 : y.prefix]), K = vn(F), oe = K.max, Z = K.min, ie = {
        theme: O,
        token: A,
        hashId: M,
        nonce: function() {
          return B.nonce;
        },
        clientOnly: E.clientOnly,
        layer: h,
        // antd is always at top of styles
        order: E.order || -999
      };
      typeof i == "function" && Ke(H(H({}, ie), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return i(A, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: L
          },
          csp: B
        });
      });
      var se = Ke(H(H({}, ie), {}, {
        path: [R, w, L]
      }), function() {
        if (E.injectStyle === !1)
          return [];
        var X = yn(A), W = X.token, Ht = X.flush, q = dt(C, b, S), zt = ".".concat(w), We = ut(C, b, q, {
          deprecatedTokens: E.deprecatedTokens
        });
        y && q && N(q) === "object" && Object.keys(q).forEach(function(Ge) {
          q[Ge] = "var(".concat(Me(Ge, lt(C, y.prefix)), ")");
        });
        var Ue = Ne(W, {
          componentCls: zt,
          prefixCls: w,
          iconCls: ".".concat(L),
          antCls: ".".concat(k),
          calc: G,
          // @ts-ignore
          max: oe,
          // @ts-ignore
          min: Z
        }, y ? q : We), At = v(Ue, {
          hashId: M,
          prefixCls: w,
          rootPrefixCls: k,
          iconPrefixCls: L
        });
        Ht(C, We);
        var Ft = typeof s == "function" ? s(Ue, w, m, E.resetFont) : null;
        return [E.resetStyle === !1 ? null : Ft, At];
      });
      return [se, M];
    };
  }
  function f(d, v, S) {
    var E = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = u(d, v, S, H({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, E)), x = function(R) {
      var h = R.prefixCls, w = R.rootCls, m = w === void 0 ? h : w;
      return p(h, m), null;
    };
    return x;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: u
  };
}
const $ = Math.round;
function ke(t, e) {
  const r = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = r.map((n) => parseFloat(n));
  for (let n = 0; n < 3; n += 1)
    o[n] = e(o[n] || 0, r[n] || "", n);
  return r[3] ? o[3] = r[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const gt = (t, e, r) => r === 0 ? t : t / 100;
function ee(t, e) {
  const r = e || 255;
  return t > r ? r : t < 0 ? 0 : t;
}
class V {
  constructor(e) {
    j(this, "isValid", !0), j(this, "r", 0), j(this, "g", 0), j(this, "b", 0), j(this, "a", 1), j(this, "_h", void 0), j(this, "_s", void 0), j(this, "_l", void 0), j(this, "_v", void 0), j(this, "_max", void 0), j(this, "_min", void 0), j(this, "_brightness", void 0);
    function r(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let n = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : n("rgb") ? this.fromRgbString(o) : n("hsl") ? this.fromHslString(o) : (n("hsv") || n("hsb")) && this.fromHsvString(o);
    } else if (e instanceof V)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (r("rgb"))
      this.r = ee(e.r), this.g = ee(e.g), this.b = ee(e.b), this.a = typeof e.a == "number" ? ee(e.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(e);
    else if (r("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const r = this.toHsv();
    return r.h = e, this._c(r);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const r = e(this.r), o = e(this.g), n = e(this.b);
    return 0.2126 * r + 0.7152 * o + 0.0722 * n;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(e = 10) {
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() - e / 100;
    return n < 0 && (n = 0), this._c({
      h: r,
      s: o,
      l: n,
      a: this.a
    });
  }
  lighten(e = 10) {
    const r = this.getHue(), o = this.getSaturation();
    let n = this.getLightness() + e / 100;
    return n > 1 && (n = 1), this._c({
      h: r,
      s: o,
      l: n,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, r = 50) {
    const o = this._c(e), n = r / 100, i = (a) => (o[a] - this[a]) * n + this[a], s = {
      r: $(i("r")),
      g: $(i("g")),
      b: $(i("b")),
      a: $(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const r = this._c(e), o = this.a + r.a * (1 - this.a), n = (i) => $((this[i] * this.a + r[i] * r.a * (1 - this.a)) / o);
    return this._c({
      r: n("r"),
      g: n("g"),
      b: n("b"),
      a: o
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const r = (this.r || 0).toString(16);
    e += r.length === 2 ? r : "0" + r;
    const o = (this.g || 0).toString(16);
    e += o.length === 2 ? o : "0" + o;
    const n = (this.b || 0).toString(16);
    if (e += n.length === 2 ? n : "0" + n, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = $(this.a * 255).toString(16);
      e += i.length === 2 ? i : "0" + i;
    }
    return e;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const e = this.getHue(), r = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${r}%,${o}%,${this.a})` : `hsl(${e},${r}%,${o}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(e, r, o) {
    const n = this.clone();
    return n[e] = ee(r, o), n;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const r = e.replace("#", "");
    function o(n, i) {
      return parseInt(r[n] + r[i || n], 16);
    }
    r.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = r[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = r[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: r,
    l: o,
    a: n
  }) {
    if (this._h = e % 360, this._s = r, this._l = o, this.a = typeof n == "number" ? n : 1, r <= 0) {
      const d = $(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * o - 1)) * r, u = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = l, s = u) : c >= 1 && c < 2 ? (i = u, s = l) : c >= 2 && c < 3 ? (s = l, a = u) : c >= 3 && c < 4 ? (s = u, a = l) : c >= 4 && c < 5 ? (i = u, a = l) : c >= 5 && c < 6 && (i = l, a = u);
    const f = o - l / 2;
    this.r = $((i + f) * 255), this.g = $((s + f) * 255), this.b = $((a + f) * 255);
  }
  fromHsv({
    h: e,
    s: r,
    v: o,
    a: n
  }) {
    this._h = e % 360, this._s = r, this._v = o, this.a = typeof n == "number" ? n : 1;
    const i = $(o * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = e / 60, a = Math.floor(s), c = s - a, l = $(o * (1 - r) * 255), u = $(o * (1 - r * c) * 255), f = $(o * (1 - r * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = l;
        break;
      case 1:
        this.r = u, this.b = l;
        break;
      case 2:
        this.r = l, this.b = f;
        break;
      case 3:
        this.r = l, this.g = u;
        break;
      case 4:
        this.r = f, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = u;
        break;
    }
  }
  fromHsvString(e) {
    const r = ke(e, gt);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(e) {
    const r = ke(e, gt);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(e) {
    const r = ke(e, (o, n) => (
      // Convert percentage to number. e.g. 50% -> 128
      n.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const Tn = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, En = Object.assign(Object.assign({}, Tn), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Le(t) {
  return t >= 0 && t <= 255;
}
function ae(t, e) {
  const {
    r,
    g: o,
    b: n,
    a: i
  } = new V(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: c
  } = new V(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const u = Math.round((r - s * (1 - l)) / l), f = Math.round((o - a * (1 - l)) / l), d = Math.round((n - c * (1 - l)) / l);
    if (Le(u) && Le(f) && Le(d))
      return new V({
        r: u,
        g: f,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new V({
    r,
    g: o,
    b: n,
    a: 1
  }).toRgbString();
}
var Pn = function(t, e) {
  var r = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (r[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var n = 0, o = Object.getOwnPropertySymbols(t); n < o.length; n++)
    e.indexOf(o[n]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[n]) && (r[o[n]] = t[o[n]]);
  return r;
};
function On(t) {
  const {
    override: e
  } = t, r = Pn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(En).forEach((d) => {
    delete o[d];
  });
  const n = Object.assign(Object.assign({}, r), o), i = 480, s = 576, a = 768, c = 992, l = 1200, u = 1600;
  if (n.motion === !1) {
    const d = "0s";
    n.motionDurationFast = d, n.motionDurationMid = d, n.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, n), {
    // ============== Background ============== //
    colorFillContent: n.colorFillSecondary,
    colorFillContentHover: n.colorFill,
    colorFillAlter: n.colorFillQuaternary,
    colorBgContainerDisabled: n.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: n.colorBgContainer,
    colorSplit: ae(n.colorBorderSecondary, n.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: n.colorTextQuaternary,
    colorTextDisabled: n.colorTextQuaternary,
    colorTextHeading: n.colorText,
    colorTextLabel: n.colorTextSecondary,
    colorTextDescription: n.colorTextTertiary,
    colorTextLightSolid: n.colorWhite,
    colorHighlight: n.colorError,
    colorBgTextHover: n.colorFillSecondary,
    colorBgTextActive: n.colorFill,
    colorIcon: n.colorTextTertiary,
    colorIconHover: n.colorText,
    colorErrorOutline: ae(n.colorErrorBg, n.colorBgContainer),
    colorWarningOutline: ae(n.colorWarningBg, n.colorBgContainer),
    // Font
    fontSizeIcon: n.fontSizeSM,
    // Line
    lineWidthFocus: n.lineWidth * 3,
    // Control
    lineWidth: n.lineWidth,
    controlOutlineWidth: n.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: n.controlHeight / 2,
    controlItemBgHover: n.colorFillTertiary,
    controlItemBgActive: n.colorPrimaryBg,
    controlItemBgActiveHover: n.colorPrimaryBgHover,
    controlItemBgActiveDisabled: n.colorFill,
    controlTmpOutline: n.colorFillQuaternary,
    controlOutline: ae(n.colorPrimaryBg, n.colorBgContainer),
    lineType: n.lineType,
    borderRadius: n.borderRadius,
    borderRadiusXS: n.borderRadiusXS,
    borderRadiusSM: n.borderRadiusSM,
    borderRadiusLG: n.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: n.sizeXXS,
    paddingXS: n.sizeXS,
    paddingSM: n.sizeSM,
    padding: n.size,
    paddingMD: n.sizeMD,
    paddingLG: n.sizeLG,
    paddingXL: n.sizeXL,
    paddingContentHorizontalLG: n.sizeLG,
    paddingContentVerticalLG: n.sizeMS,
    paddingContentHorizontal: n.sizeMS,
    paddingContentVertical: n.sizeSM,
    paddingContentHorizontalSM: n.size,
    paddingContentVerticalSM: n.sizeXS,
    marginXXS: n.sizeXXS,
    marginXS: n.sizeXS,
    marginSM: n.sizeSM,
    margin: n.size,
    marginMD: n.sizeMD,
    marginLG: n.sizeLG,
    marginXL: n.sizeXL,
    marginXXL: n.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new V("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new V("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new V("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), o);
}
const Mn = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, Rn = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, jn = rr(De.defaultAlgorithm), In = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, $t = (t, e, r) => {
  const o = r.getDerivativeToken(t), {
    override: n,
    ...i
  } = e;
  let s = {
    ...o,
    override: n
  };
  return s = On(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: l,
      ...u
    } = c;
    let f = u;
    l && (f = $t({
      ...s,
      ...u
    }, {
      override: u
    }, l)), s[a] = f;
  }), s;
};
function kn() {
  const {
    token: t,
    hashed: e,
    theme: r = jn,
    override: o,
    cssVar: n
  } = g.useContext(De._internalContext), [i, s, a] = nr(r, [De.defaultSeed, t], {
    salt: `${Ur}-${e || ""}`,
    override: o,
    getComputedToken: $t,
    cssVar: n && {
      prefix: n.prefix,
      key: n.key,
      unitless: Mn,
      ignore: Rn,
      preserve: In
    }
  });
  return [r, a, e ? s : "", i, n];
}
const {
  genStyleHooks: Ln
} = _n({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = ge();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, r, o, n] = kn();
    return {
      theme: t,
      realToken: e,
      hashId: r,
      token: o,
      cssVar: n
    };
  },
  useCSP: () => {
    const {
      csp: t
    } = ge();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var $n = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, Dn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Bn = "".concat($n, " ").concat(Dn).split(/[\s\n]+/), Hn = "aria-", zn = "data-";
function mt(t, e) {
  return t.indexOf(e) === 0;
}
function An(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, r;
  e === !1 ? r = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? r = {
    aria: !0
  } : r = on({}, e);
  var o = {};
  return Object.keys(t).forEach(function(n) {
    // Aria
    (r.aria && (n === "role" || mt(n, Hn)) || // Data
    r.data && mt(n, zn) || // Attr
    r.attr && Bn.includes(n)) && (o[n] = t[n]);
  }), o;
}
function ce(t) {
  return typeof t == "string";
}
const Fn = (t, e, r, o) => {
  const n = _.useRef(""), [i, s] = _.useState(1), a = e && ce(t);
  return Jr(() => {
    !a && ce(t) ? s(t.length) : ce(t) && ce(n.current) && t.indexOf(n.current) !== 0 && s(1), n.current = t;
  }, [t]), _.useEffect(() => {
    if (a && i < t.length) {
      const l = setTimeout(() => {
        s((u) => u + r);
      }, o);
      return () => {
        clearTimeout(l);
      };
    }
  }, [i, e, t]), [a ? t.slice(0, i) : t, a && i < t.length];
};
function Xn(t) {
  return _.useMemo(() => {
    if (!t)
      return [!1, 0, 0, null];
    let e = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof t == "object" && (e = {
      ...e,
      ...t
    }), [!0, e.step, e.interval, e.suffix];
  }, [t]);
}
const Nn = ({
  prefixCls: t
}) => /* @__PURE__ */ g.createElement("span", {
  className: `${t}-dot`
}, /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ g.createElement("i", {
  className: `${t}-dot-item`,
  key: "item-3"
})), Vn = (t) => {
  const {
    componentCls: e,
    paddingSM: r,
    padding: o
  } = t;
  return {
    [e]: {
      [`${e}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${re(r)} ${re(o)}`,
          borderRadius: t.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: t.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${t.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: t.boxShadowTertiary
        }
      }
    }
  };
}, Wn = (t) => {
  const {
    componentCls: e,
    fontSize: r,
    lineHeight: o,
    paddingSM: n,
    padding: i,
    calc: s
  } = t, a = s(r).mul(o).div(2).add(n).equal(), c = `${e}-content`;
  return {
    [e]: {
      [c]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: s(i).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${c}-corner`]: {
        borderStartStartRadius: t.borderRadiusXS
      },
      [`&-end ${c}-corner`]: {
        borderStartEndRadius: t.borderRadiusXS
      }
    }
  };
}, Un = (t) => {
  const {
    componentCls: e,
    padding: r
  } = t;
  return {
    [`${e}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: r,
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: 8,
        backgroundColor: "transparent"
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: t.colorTextTertiary,
        borderRadius: t.borderRadiusSM
      },
      // For Firefox
      "&": {
        scrollbarWidth: "thin",
        scrollbarColor: `${t.colorTextTertiary} transparent`
      }
    }
  };
}, Gn = new St("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), Kn = new St("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), qn = (t) => {
  const {
    componentCls: e,
    fontSize: r,
    lineHeight: o,
    paddingSM: n,
    colorText: i,
    calc: s
  } = t;
  return {
    [e]: {
      display: "flex",
      columnGap: n,
      [`&${e}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${e}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      [`&${e}-typing ${e}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Kn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${e}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${e}-header, & ${e}-footer`]: {
        fontSize: r,
        lineHeight: o,
        color: t.colorText
      },
      [`& ${e}-header`]: {
        marginBottom: t.paddingXXS
      },
      [`& ${e}-footer`]: {
        marginTop: n
      },
      // =========================== Content =============================
      [`& ${e}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${e}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: i,
        fontSize: t.fontSize,
        lineHeight: t.lineHeight,
        minHeight: s(n).mul(2).add(s(o).mul(r)).equal(),
        wordBreak: "break-word",
        [`& ${e}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: t.marginXS,
          padding: `0 ${re(t.paddingXXS)}`,
          "&-item": {
            backgroundColor: t.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Gn,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Yn = () => ({}), Dt = Ln("Bubble", (t) => {
  const e = Ne(t, {});
  return [qn(e), Un(e), Vn(e), Wn(e)];
}, Yn), Bt = /* @__PURE__ */ g.createContext({}), Qn = (t, e) => {
  const {
    prefixCls: r,
    className: o,
    rootClassName: n,
    style: i,
    classNames: s = {},
    styles: a = {},
    avatar: c,
    placement: l = "start",
    loading: u = !1,
    loadingRender: f,
    typing: d,
    content: v = "",
    messageRender: S,
    variant: E = "filled",
    shape: p,
    onTypingComplete: x,
    header: C,
    footer: R,
    ...h
  } = t, {
    onUpdate: w
  } = g.useContext(Bt), m = g.useRef(null);
  g.useImperativeHandle(e, () => ({
    nativeElement: m.current
  }));
  const {
    direction: P,
    getPrefixCls: O
  } = ge(), b = O("bubble", r), M = qr("bubble"), [A, y, I, k] = Xn(d), [L, B] = Fn(v, A, y, I);
  g.useEffect(() => {
    w == null || w();
  }, [L]);
  const F = g.useRef(!1);
  g.useEffect(() => {
    !B && !u ? F.current || (F.current = !0, x == null || x()) : F.current = !1;
  }, [B, u]);
  const [G, K, oe] = Dt(b), Z = Y(b, n, M.className, o, K, oe, `${b}-${l}`, {
    [`${b}-rtl`]: P === "rtl",
    [`${b}-typing`]: B && !u && !S && !k
  }), ie = g.useMemo(() => /* @__PURE__ */ g.isValidElement(c) ? c : /* @__PURE__ */ g.createElement(er, c), [c]), se = g.useMemo(() => S ? S(L) : L, [L, S]);
  let X;
  u ? X = f ? f() : /* @__PURE__ */ g.createElement(Nn, {
    prefixCls: b
  }) : X = /* @__PURE__ */ g.createElement(g.Fragment, null, se, B && k);
  let W = /* @__PURE__ */ g.createElement("div", {
    style: {
      ...M.styles.content,
      ...a.content
    },
    className: Y(`${b}-content`, `${b}-content-${E}`, p && `${b}-content-${p}`, M.classNames.content, s.content)
  }, X);
  return (C || R) && (W = /* @__PURE__ */ g.createElement("div", {
    className: `${b}-content-wrapper`
  }, C && /* @__PURE__ */ g.createElement("div", {
    className: Y(`${b}-header`, M.classNames.header, s.header),
    style: {
      ...M.styles.header,
      ...a.header
    }
  }, C), W, R && /* @__PURE__ */ g.createElement("div", {
    className: Y(`${b}-footer`, M.classNames.footer, s.footer),
    style: {
      ...M.styles.footer,
      ...a.footer
    }
  }, typeof R == "function" ? R(se) : R))), G(/* @__PURE__ */ g.createElement("div", J({
    style: {
      ...M.style,
      ...i
    },
    className: Z
  }, h, {
    ref: m
  }), c && /* @__PURE__ */ g.createElement("div", {
    style: {
      ...M.styles.avatar,
      ...a.avatar
    },
    className: Y(`${b}-avatar`, M.classNames.avatar, s.avatar)
  }, ie), W));
}, Ve = /* @__PURE__ */ g.forwardRef(Qn);
function Jn(t, e) {
  const r = _.useCallback((o, n) => typeof e == "function" ? e(o, n) : e ? e[o.role] || {} : {}, [e]);
  return _.useMemo(() => (t || []).map((o, n) => {
    const i = o.key ?? `preset_${n}`;
    return {
      ...r(o, n),
      ...o,
      key: i
    };
  }), [t, r]);
}
const Zn = ({
  _key: t,
  ...e
}, r) => /* @__PURE__ */ _.createElement(Ve, J({}, e, {
  ref: (o) => {
    var n;
    o ? r.current[t] = o : (n = r.current) == null || delete n[t];
  }
})), eo = /* @__PURE__ */ _.memo(/* @__PURE__ */ _.forwardRef(Zn)), to = 1, ro = (t, e) => {
  const {
    prefixCls: r,
    rootClassName: o,
    className: n,
    items: i,
    autoScroll: s = !0,
    roles: a,
    ...c
  } = t, l = An(c, {
    attr: !0,
    aria: !0
  }), u = _.useRef(null), f = _.useRef({}), {
    getPrefixCls: d
  } = ge(), v = d("bubble", r), S = `${v}-list`, [E, p, x] = Dt(v), [C, R] = _.useState(!1);
  _.useEffect(() => (R(!0), () => {
    R(!1);
  }), []);
  const h = Jn(i, a), [w, m] = _.useState(!0), [P, O] = _.useState(0), b = (y) => {
    const I = y.target;
    m(I.scrollHeight - Math.abs(I.scrollTop) - I.clientHeight <= to);
  };
  _.useEffect(() => {
    s && u.current && w && u.current.scrollTo({
      top: u.current.scrollHeight
    });
  }, [P]), _.useEffect(() => {
    var y;
    if (s) {
      const I = (y = h[h.length - 2]) == null ? void 0 : y.key, k = f.current[I];
      if (k) {
        const {
          nativeElement: L
        } = k, {
          top: B,
          bottom: F
        } = L.getBoundingClientRect(), {
          top: G,
          bottom: K
        } = u.current.getBoundingClientRect();
        B < K && F > G && (O((Z) => Z + 1), m(!0));
      }
    }
  }, [h.length]), _.useImperativeHandle(e, () => ({
    nativeElement: u.current,
    scrollTo: ({
      key: y,
      offset: I,
      behavior: k = "smooth",
      block: L
    }) => {
      if (typeof I == "number")
        u.current.scrollTo({
          top: I,
          behavior: k
        });
      else if (y !== void 0) {
        const B = f.current[y];
        if (B) {
          const F = h.findIndex((G) => G.key === y);
          m(F === h.length - 1), B.nativeElement.scrollIntoView({
            behavior: k,
            block: L
          });
        }
      }
    }
  }));
  const M = Yr(() => {
    s && O((y) => y + 1);
  }), A = _.useMemo(() => ({
    onUpdate: M
  }), []);
  return E(/* @__PURE__ */ _.createElement(Bt.Provider, {
    value: A
  }, /* @__PURE__ */ _.createElement("div", J({}, l, {
    className: Y(S, o, n, p, x, {
      [`${S}-reach-end`]: w
    }),
    ref: u,
    onScroll: b
  }), h.map(({
    key: y,
    ...I
  }) => /* @__PURE__ */ _.createElement(eo, J({}, I, {
    key: y,
    _key: y,
    ref: f,
    typing: C ? I.typing : !1
  }))))));
}, no = /* @__PURE__ */ _.forwardRef(ro);
Ve.List = no;
function oo(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function io(t, e = !1) {
  try {
    if (Yt(t))
      return t;
    if (e && !oo(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function pt(t, e) {
  return vt(() => io(t, e), [t, e]);
}
const so = ({
  children: t,
  ...e
}) => /* @__PURE__ */ D.jsx(D.Fragment, {
  children: t(e)
});
function ao(t) {
  return g.createElement(so, {
    children: t
  });
}
function bt(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ao((r) => /* @__PURE__ */ D.jsx(Jt, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ D.jsx(U, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...r
    })
  })) : /* @__PURE__ */ D.jsx(U, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function yt({
  key: t,
  slots: e,
  targets: r
}, o) {
  return e[t] ? (...n) => r ? r.map((i, s) => /* @__PURE__ */ D.jsx(g.Fragment, {
    children: bt(i, {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ D.jsx(D.Fragment, {
    children: bt(e[t], {
      clone: !0,
      params: n,
      forceClone: !0
    })
  }) : void 0;
}
const uo = Fr(({
  loadingRender: t,
  messageRender: e,
  slots: r,
  setSlotParams: o,
  children: n,
  ...i
}) => {
  const s = pt(t), a = pt(e), c = vt(() => {
    var l, u;
    return r.avatar ? /* @__PURE__ */ D.jsx(U, {
      slot: r.avatar
    }) : r["avatar.icon"] || r["avatar.src"] ? {
      ...i.avatar || {},
      icon: r["avatar.icon"] ? /* @__PURE__ */ D.jsx(U, {
        slot: r["avatar.icon"]
      }) : (l = i.avatar) == null ? void 0 : l.icon,
      src: r["avatar.src"] ? /* @__PURE__ */ D.jsx(U, {
        slot: r["avatar.src"]
      }) : (u = i.avatar) == null ? void 0 : u.src
    } : i.avatar;
  }, [i.avatar, r]);
  return /* @__PURE__ */ D.jsxs(D.Fragment, {
    children: [/* @__PURE__ */ D.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ D.jsx(Ve, {
      ...i,
      avatar: c,
      typing: r["typing.suffix"] ? {
        ...he(i.typing) ? i.typing : {},
        suffix: /* @__PURE__ */ D.jsx(U, {
          slot: r["typing.suffix"]
        })
      } : i.typing,
      content: r.content ? /* @__PURE__ */ D.jsx(U, {
        slot: r.content
      }) : i.content,
      footer: r.footer ? /* @__PURE__ */ D.jsx(U, {
        slot: r.footer
      }) : i.footer,
      loadingRender: r.loadingRender ? yt({
        slots: r,
        key: "loadingRender"
      }) : s,
      messageRender: r.messageRender ? yt({
        slots: r,
        key: "messageRender"
      }) : a
    })]
  });
});
export {
  uo as Bubble,
  uo as default
};
