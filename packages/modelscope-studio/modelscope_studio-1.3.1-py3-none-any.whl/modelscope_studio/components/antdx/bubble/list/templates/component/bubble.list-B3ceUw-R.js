import { i as Yt, a as te, r as Qt, w as ce, g as Jt, c as q, b as Fe } from "./Index-CLhQYvxG.js";
const T = window.ms_globals.React, p = window.ms_globals.React, Wt = window.ms_globals.React.version, Ut = window.ms_globals.React.forwardRef, xt = window.ms_globals.React.useRef, Gt = window.ms_globals.React.useState, Kt = window.ms_globals.React.useEffect, qt = window.ms_globals.React.useCallback, he = window.ms_globals.React.useMemo, $e = window.ms_globals.ReactDOM.createPortal, Zt = window.ms_globals.internalContext.useContextPropsContext, Ye = window.ms_globals.internalContext.ContextPropsProvider, Ct = window.ms_globals.createItemsContext.createItemsContext, er = window.ms_globals.antd.ConfigProvider, De = window.ms_globals.antd.theme, tr = window.ms_globals.antd.Avatar, re = window.ms_globals.antdCssinjs.unit, Me = window.ms_globals.antdCssinjs.token2CSSVar, Qe = window.ms_globals.antdCssinjs.useStyleRegister, rr = window.ms_globals.antdCssinjs.useCSSVarRegister, nr = window.ms_globals.antdCssinjs.createTheme, or = window.ms_globals.antdCssinjs.useCacheToken, wt = window.ms_globals.antdCssinjs.Keyframes;
var sr = /\s/;
function ir(e) {
  for (var t = e.length; t-- && sr.test(e.charAt(t)); )
    ;
  return t;
}
var ar = /^\s+/;
function lr(e) {
  return e && e.slice(0, ir(e) + 1).replace(ar, "");
}
var Je = NaN, cr = /^[-+]0x[0-9a-f]+$/i, ur = /^0b[01]+$/i, fr = /^0o[0-7]+$/i, dr = parseInt;
function Ze(e) {
  if (typeof e == "number")
    return e;
  if (Yt(e))
    return Je;
  if (te(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = te(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = lr(e);
  var n = ur.test(e);
  return n || fr.test(e) ? dr(e.slice(2), n ? 2 : 8) : cr.test(e) ? Je : +e;
}
var Ie = function() {
  return Qt.Date.now();
}, hr = "Expected a function", gr = Math.max, mr = Math.min;
function pr(e, t, n) {
  var o, r, s, i, a, l, f = 0, c = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(hr);
  t = Ze(t) || 0, te(n) && (c = !!n.leading, u = "maxWait" in n, s = u ? gr(Ze(n.maxWait) || 0, t) : s, d = "trailing" in n ? !!n.trailing : d);
  function g(v) {
    var P = o, O = r;
    return o = r = void 0, f = v, i = e.apply(O, P), i;
  }
  function b(v) {
    return f = v, a = setTimeout(y, t), c ? g(v) : i;
  }
  function S(v) {
    var P = v - l, O = v - f, x = t - P;
    return u ? mr(x, s - O) : x;
  }
  function m(v) {
    var P = v - l, O = v - f;
    return l === void 0 || P >= t || P < 0 || u && O >= s;
  }
  function y() {
    var v = Ie();
    if (m(v))
      return w(v);
    a = setTimeout(y, S(v));
  }
  function w(v) {
    return a = void 0, d && o ? g(v) : (o = r = void 0, i);
  }
  function I() {
    a !== void 0 && clearTimeout(a), f = 0, o = l = r = a = void 0;
  }
  function h() {
    return a === void 0 ? i : w(Ie());
  }
  function _() {
    var v = Ie(), P = m(v);
    if (o = arguments, r = this, l = v, P) {
      if (a === void 0)
        return b(l);
      if (u)
        return clearTimeout(a), a = setTimeout(y, t), g(l);
    }
    return a === void 0 && (a = setTimeout(y, t)), i;
  }
  return _.cancel = I, _.flush = h, _;
}
var _t = {
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
var br = p, yr = Symbol.for("react.element"), vr = Symbol.for("react.fragment"), Sr = Object.prototype.hasOwnProperty, xr = br.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Cr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Tt(e, t, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (o in t) Sr.call(t, o) && !Cr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: yr,
    type: e,
    key: s,
    ref: i,
    props: r,
    _owner: xr.current
  };
}
pe.Fragment = vr;
pe.jsx = Tt;
pe.jsxs = Tt;
_t.exports = pe;
var H = _t.exports;
const {
  SvelteComponent: wr,
  assign: et,
  binding_callbacks: tt,
  check_outros: _r,
  children: Et,
  claim_element: Pt,
  claim_space: Tr,
  component_subscribe: rt,
  compute_slots: Er,
  create_slot: Pr,
  detach: Y,
  element: Ot,
  empty: nt,
  exclude_internal_props: ot,
  get_all_dirty_from_scope: Or,
  get_slot_changes: Mr,
  group_outros: Ir,
  init: Rr,
  insert_hydration: ue,
  safe_not_equal: jr,
  set_custom_element_data: Mt,
  space: kr,
  transition_in: fe,
  transition_out: Be,
  update_slot_base: Lr
} = window.__gradio__svelte__internal, {
  beforeUpdate: $r,
  getContext: Dr,
  onDestroy: Br,
  setContext: Hr
} = window.__gradio__svelte__internal;
function st(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = Pr(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Ot("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      t = Pt(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Et(t);
      r && r.l(i), i.forEach(Y), this.h();
    },
    h() {
      Mt(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      ue(s, t, i), r && r.m(t, null), e[9](t), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && Lr(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Mr(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Or(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (fe(r, s), n = !0);
    },
    o(s) {
      Be(r, s), n = !1;
    },
    d(s) {
      s && Y(t), r && r.d(s), e[9](null);
    }
  };
}
function zr(e) {
  let t, n, o, r, s = (
    /*$$slots*/
    e[4].default && st(e)
  );
  return {
    c() {
      t = Ot("react-portal-target"), n = kr(), s && s.c(), o = nt(), this.h();
    },
    l(i) {
      t = Pt(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Et(t).forEach(Y), n = Tr(i), s && s.l(i), o = nt(), this.h();
    },
    h() {
      Mt(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      ue(i, t, a), e[8](t), ue(i, n, a), s && s.m(i, a), ue(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && fe(s, 1)) : (s = st(i), s.c(), fe(s, 1), s.m(o.parentNode, o)) : s && (Ir(), Be(s, 1, 1, () => {
        s = null;
      }), _r());
    },
    i(i) {
      r || (fe(s), r = !0);
    },
    o(i) {
      Be(s), r = !1;
    },
    d(i) {
      i && (Y(t), Y(n), Y(o)), e[8](null), s && s.d(i);
    }
  };
}
function it(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Ar(e, t, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = Er(s);
  let {
    svelteInit: l
  } = t;
  const f = ce(it(t)), c = ce();
  rt(e, c, (h) => n(0, o = h));
  const u = ce();
  rt(e, u, (h) => n(1, r = h));
  const d = [], g = Dr("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: S,
    subSlotIndex: m
  } = Jt() || {}, y = l({
    parent: g,
    props: f,
    target: c,
    slot: u,
    slotKey: b,
    slotIndex: S,
    subSlotIndex: m,
    onDestroy(h) {
      d.push(h);
    }
  });
  Hr("$$ms-gr-react-wrapper", y), $r(() => {
    f.set(it(t));
  }), Br(() => {
    d.forEach((h) => h());
  });
  function w(h) {
    tt[h ? "unshift" : "push"](() => {
      o = h, c.set(o);
    });
  }
  function I(h) {
    tt[h ? "unshift" : "push"](() => {
      r = h, u.set(r);
    });
  }
  return e.$$set = (h) => {
    n(17, t = et(et({}, t), ot(h))), "svelteInit" in h && n(5, l = h.svelteInit), "$$scope" in h && n(6, i = h.$$scope);
  }, t = ot(t), [o, r, c, u, a, l, i, s, w, I];
}
class Fr extends wr {
  constructor(t) {
    super(), Rr(this, t, Ar, zr, jr, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: So
} = window.__gradio__svelte__internal, at = window.ms_globals.rerender, Re = window.ms_globals.tree;
function Xr(e, t = {}) {
  function n(o) {
    const r = ce(), s = new Fr({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? Re;
          return l.nodes = [...l.nodes, a], at({
            createPortal: $e,
            node: Re
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((f) => f.svelteInstance !== r), at({
              createPortal: $e,
              node: Re
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Nr = "1.2.0", Vr = /* @__PURE__ */ p.createContext({}), Wr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ur = (e) => {
  const t = p.useContext(Vr);
  return p.useMemo(() => ({
    ...Wr,
    ...t[e]
  }), [t[e]]);
};
function Q() {
  return Q = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, Q.apply(null, arguments);
}
function ge() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = p.useContext(er.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Gr(e) {
  var t = T.useRef();
  t.current = e;
  var n = T.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(s));
  }, []);
  return n;
}
function Kr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var lt = Kr() ? T.useLayoutEffect : T.useEffect, qr = function(t, n) {
  var o = T.useRef(!0);
  lt(function() {
    return t(o.current);
  }, n), lt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function ne(e) {
  "@babel/helpers - typeof";
  return ne = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, ne(e);
}
var E = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Xe = Symbol.for("react.element"), Ne = Symbol.for("react.portal"), be = Symbol.for("react.fragment"), ye = Symbol.for("react.strict_mode"), ve = Symbol.for("react.profiler"), Se = Symbol.for("react.provider"), xe = Symbol.for("react.context"), Yr = Symbol.for("react.server_context"), Ce = Symbol.for("react.forward_ref"), we = Symbol.for("react.suspense"), _e = Symbol.for("react.suspense_list"), Te = Symbol.for("react.memo"), Ee = Symbol.for("react.lazy"), Qr = Symbol.for("react.offscreen"), It;
It = Symbol.for("react.module.reference");
function z(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Xe:
        switch (e = e.type, e) {
          case be:
          case ve:
          case ye:
          case we:
          case _e:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Yr:
              case xe:
              case Ce:
              case Ee:
              case Te:
              case Se:
                return e;
              default:
                return t;
            }
        }
      case Ne:
        return t;
    }
  }
}
E.ContextConsumer = xe;
E.ContextProvider = Se;
E.Element = Xe;
E.ForwardRef = Ce;
E.Fragment = be;
E.Lazy = Ee;
E.Memo = Te;
E.Portal = Ne;
E.Profiler = ve;
E.StrictMode = ye;
E.Suspense = we;
E.SuspenseList = _e;
E.isAsyncMode = function() {
  return !1;
};
E.isConcurrentMode = function() {
  return !1;
};
E.isContextConsumer = function(e) {
  return z(e) === xe;
};
E.isContextProvider = function(e) {
  return z(e) === Se;
};
E.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Xe;
};
E.isForwardRef = function(e) {
  return z(e) === Ce;
};
E.isFragment = function(e) {
  return z(e) === be;
};
E.isLazy = function(e) {
  return z(e) === Ee;
};
E.isMemo = function(e) {
  return z(e) === Te;
};
E.isPortal = function(e) {
  return z(e) === Ne;
};
E.isProfiler = function(e) {
  return z(e) === ve;
};
E.isStrictMode = function(e) {
  return z(e) === ye;
};
E.isSuspense = function(e) {
  return z(e) === we;
};
E.isSuspenseList = function(e) {
  return z(e) === _e;
};
E.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === be || e === ve || e === ye || e === we || e === _e || e === Qr || typeof e == "object" && e !== null && (e.$$typeof === Ee || e.$$typeof === Te || e.$$typeof === Se || e.$$typeof === xe || e.$$typeof === Ce || e.$$typeof === It || e.getModuleId !== void 0);
};
E.typeOf = z;
Number(Wt.split(".")[0]);
function Jr(e, t) {
  if (ne(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (ne(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Zr(e) {
  var t = Jr(e, "string");
  return ne(t) == "symbol" ? t : t + "";
}
function en(e, t, n) {
  return (t = Zr(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function ct(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function tn(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ct(Object(n), !0).forEach(function(o) {
      en(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : ct(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function N(e) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, N(e);
}
function rn(e, t) {
  if (N(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (N(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Rt(e) {
  var t = rn(e, "string");
  return N(t) == "symbol" ? t : t + "";
}
function R(e, t, n) {
  return (t = Rt(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function ut(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function B(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ut(Object(n), !0).forEach(function(o) {
      R(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : ut(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function nn(e) {
  if (Array.isArray(e)) return e;
}
function on(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], l = !0, f = !1;
    try {
      if (s = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = s.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (c) {
      f = !0, r = c;
    } finally {
      try {
        if (!l && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (f) throw r;
      }
    }
    return a;
  }
}
function ft(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function sn(e, t) {
  if (e) {
    if (typeof e == "string") return ft(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ft(e, t) : void 0;
  }
}
function an() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function de(e, t) {
  return nn(e) || on(e, t) || sn(e, t) || an();
}
function Pe(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function ln(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Rt(o.key), o);
  }
}
function Oe(e, t, n) {
  return t && ln(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function He(e, t) {
  return He = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, He(e, t);
}
function jt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && He(e, t);
}
function me(e) {
  return me = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, me(e);
}
function kt() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (kt = function() {
    return !!e;
  })();
}
function ee(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function cn(e, t) {
  if (t && (N(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ee(e);
}
function Lt(e) {
  var t = kt();
  return function() {
    var n, o = me(e);
    if (t) {
      var r = me(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return cn(this, n);
  };
}
var $t = /* @__PURE__ */ Oe(function e() {
  Pe(this, e);
}), Dt = "CALC_UNIT", un = new RegExp(Dt, "g");
function je(e) {
  return typeof e == "number" ? "".concat(e).concat(Dt) : e;
}
var fn = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = Lt(n);
  function n(o, r) {
    var s;
    Pe(this, n), s = t.call(this), R(ee(s), "result", ""), R(ee(s), "unitlessCssVar", void 0), R(ee(s), "lowPriority", void 0);
    var i = N(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = je(o) : i === "string" && (s.result = o), s;
  }
  return Oe(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(je(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(je(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var s = this, i = r || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(f) {
        return s.result.includes(f);
      }) && (l = !1), this.result = this.result.replace(un, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}($t), dn = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = Lt(n);
  function n(o) {
    var r;
    return Pe(this, n), r = t.call(this), R(ee(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Oe(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}($t), hn = function(t, n) {
  var o = t === "css" ? fn : dn;
  return function(r) {
    return new o(r, n);
  };
}, dt = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ht(e, t, n, o) {
  var r = B({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var l = de(a, 2), f = l[0], c = l[1];
      if (r != null && r[f] || r != null && r[c]) {
        var u;
        (u = r[c]) !== null && u !== void 0 || (r[c] = r == null ? void 0 : r[f]);
      }
    });
  }
  var i = B(B({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var Bt = typeof CSSINJS_STATISTIC < "u", ze = !0;
function Ve() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!Bt)
    return Object.assign.apply(Object, [{}].concat(t));
  ze = !1;
  var o = {};
  return t.forEach(function(r) {
    if (N(r) === "object") {
      var s = Object.keys(r);
      s.forEach(function(i) {
        Object.defineProperty(o, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[i];
          }
        });
      });
    }
  }), ze = !0, o;
}
var gt = {};
function gn() {
}
var mn = function(t) {
  var n, o = t, r = gn;
  return Bt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(i, a) {
      if (ze) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var l;
    gt[i] = {
      global: Array.from(n),
      component: B(B({}, (l = gt[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function mt(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ve(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function pn(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return re(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return re(s);
      }).join(","), ")");
    }
  };
}
var bn = 1e3 * 60 * 10, yn = /* @__PURE__ */ function() {
  function e() {
    Pe(this, e), R(this, "map", /* @__PURE__ */ new Map()), R(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), R(this, "nextID", 0), R(this, "lastAccessBeat", /* @__PURE__ */ new Map()), R(this, "accessBeat", 0);
  }
  return Oe(e, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(s) {
        return s && N(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(N(s), "_").concat(s);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, s) {
          o - r > bn && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), pt = new yn();
function vn(e, t) {
  return p.useMemo(function() {
    var n = pt.get(t);
    if (n)
      return n;
    var o = e();
    return pt.set(t, o), o;
  }, t);
}
var Sn = function() {
  return {};
};
function xn(e) {
  var t = e.useCSP, n = t === void 0 ? Sn : t, o = e.useToken, r = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, g, b, S) {
    var m = Array.isArray(d) ? d[0] : d;
    function y(O) {
      return "".concat(String(m)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var w = (S == null ? void 0 : S.unitless) || {}, I = typeof a == "function" ? a(d) : {}, h = B(B({}, I), {}, R({}, y("zIndexPopup"), !0));
    Object.keys(w).forEach(function(O) {
      h[y(O)] = w[O];
    });
    var _ = B(B({}, S), {}, {
      unitless: h,
      prefixToken: y
    }), v = c(d, g, b, _), P = f(m, b, _);
    return function(O) {
      var x = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, M = v(O, x), A = de(M, 2), C = A[1], j = P(x), k = de(j, 2), L = k[0], D = k[1];
      return [L, C, D];
    };
  }
  function f(d, g, b) {
    var S = b.unitless, m = b.injectStyle, y = m === void 0 ? !0 : m, w = b.prefixToken, I = b.ignore, h = function(P) {
      var O = P.rootCls, x = P.cssVar, M = x === void 0 ? {} : x, A = o(), C = A.realToken;
      return rr({
        path: [d],
        prefix: M.prefix,
        key: M.key,
        unitless: S,
        ignore: I,
        token: C,
        scope: O
      }, function() {
        var j = mt(d, C, g), k = ht(d, C, j, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(j).forEach(function(L) {
          k[w(L)] = k[L], delete k[L];
        }), k;
      }), null;
    }, _ = function(P) {
      var O = o(), x = O.cssVar;
      return [function(M) {
        return y && x ? /* @__PURE__ */ p.createElement(p.Fragment, null, /* @__PURE__ */ p.createElement(h, {
          rootCls: P,
          cssVar: x,
          component: d
        }), M) : M;
      }, x == null ? void 0 : x.key];
    };
    return _;
  }
  function c(d, g, b) {
    var S = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], y = de(m, 1), w = y[0], I = m.join("-"), h = e.layer || {
      name: "antd"
    };
    return function(_) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, P = o(), O = P.theme, x = P.realToken, M = P.hashId, A = P.token, C = P.cssVar, j = r(), k = j.rootPrefixCls, L = j.iconPrefixCls, D = n(), F = C ? "css" : "js", U = vn(function() {
        var X = /* @__PURE__ */ new Set();
        return C && Object.keys(S.unitless || {}).forEach(function(W) {
          X.add(Me(W, C.prefix)), X.add(Me(W, dt(w, C.prefix)));
        }), hn(F, X);
      }, [F, w, C == null ? void 0 : C.prefix]), G = pn(F), oe = G.max, J = G.min, se = {
        theme: O,
        token: A,
        hashId: M,
        nonce: function() {
          return D.nonce;
        },
        clientOnly: S.clientOnly,
        layer: h,
        // antd is always at top of styles
        order: S.order || -999
      };
      typeof s == "function" && Qe(B(B({}, se), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return s(A, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: L
          },
          csp: D
        });
      });
      var ie = Qe(B(B({}, se), {}, {
        path: [I, _, L]
      }), function() {
        if (S.injectStyle === !1)
          return [];
        var X = mn(A), W = X.token, Ft = X.flush, K = mt(w, x, b), Xt = ".".concat(_), Ge = ht(w, x, K, {
          deprecatedTokens: S.deprecatedTokens
        });
        C && K && N(K) === "object" && Object.keys(K).forEach(function(qe) {
          K[qe] = "var(".concat(Me(qe, dt(w, C.prefix)), ")");
        });
        var Ke = Ve(W, {
          componentCls: Xt,
          prefixCls: _,
          iconCls: ".".concat(L),
          antCls: ".".concat(k),
          calc: U,
          // @ts-ignore
          max: oe,
          // @ts-ignore
          min: J
        }, C ? K : Ge), Nt = g(Ke, {
          hashId: M,
          prefixCls: _,
          rootPrefixCls: k,
          iconPrefixCls: L
        });
        Ft(w, Ge);
        var Vt = typeof i == "function" ? i(Ke, _, v, S.resetFont) : null;
        return [S.resetStyle === !1 ? null : Vt, Nt];
      });
      return [ie, M];
    };
  }
  function u(d, g, b) {
    var S = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = c(d, g, b, B({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, S)), y = function(I) {
      var h = I.prefixCls, _ = I.rootCls, v = _ === void 0 ? h : _;
      return m(h, v), null;
    };
    return y;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: c
  };
}
const $ = Math.round;
function ke(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const bt = (e, t, n) => n === 0 ? e : e / 100;
function Z(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class V {
  constructor(t) {
    R(this, "isValid", !0), R(this, "r", 0), R(this, "g", 0), R(this, "b", 0), R(this, "a", 1), R(this, "_h", void 0), R(this, "_s", void 0), R(this, "_l", void 0), R(this, "_v", void 0), R(this, "_max", void 0), R(this, "_min", void 0), R(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof V)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Z(t.r), this.g = Z(t.g), this.b = Z(t.b), this.a = typeof t.a == "number" ? Z(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
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
  darken(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: $(s("r")),
      g: $(s("g")),
      b: $(s("b")),
      a: $(s("a") * 100) / 100
    };
    return this._c(i);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (s) => $((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
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
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const s = $(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
    }
    return t;
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
    const t = this.getHue(), n = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
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
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = Z(n, o), r;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = $(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, f = (1 - Math.abs(2 * o - 1)) * n, c = f * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = f, i = c) : l >= 1 && l < 2 ? (s = c, i = f) : l >= 2 && l < 3 ? (i = f, a = c) : l >= 3 && l < 4 ? (i = c, a = f) : l >= 4 && l < 5 ? (s = c, a = f) : l >= 5 && l < 6 && (s = f, a = c);
    const u = o - f / 2;
    this.r = $((s + u) * 255), this.g = $((i + u) * 255), this.b = $((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = $(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, f = $(o * (1 - n) * 255), c = $(o * (1 - n * l) * 255), u = $(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = f;
        break;
      case 1:
        this.r = c, this.b = f;
        break;
      case 2:
        this.r = f, this.b = u;
        break;
      case 3:
        this.r = f, this.g = c;
        break;
      case 4:
        this.r = u, this.g = f;
        break;
      case 5:
      default:
        this.g = f, this.b = c;
        break;
    }
  }
  fromHsvString(t) {
    const n = ke(t, bt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = ke(t, bt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = ke(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Cn = {
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
}, wn = Object.assign(Object.assign({}, Cn), {
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
function Le(e) {
  return e >= 0 && e <= 255;
}
function ae(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new V(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new V(t).toRgb();
  for (let f = 0.01; f <= 1; f += 0.01) {
    const c = Math.round((n - i * (1 - f)) / f), u = Math.round((o - a * (1 - f)) / f), d = Math.round((r - l * (1 - f)) / f);
    if (Le(c) && Le(u) && Le(d))
      return new V({
        r: c,
        g: u,
        b: d,
        a: Math.round(f * 100) / 100
      }).toRgbString();
  }
  return new V({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var _n = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function Tn(e) {
  const {
    override: t
  } = e, n = _n(e, ["override"]), o = Object.assign({}, t);
  Object.keys(wn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, l = 992, f = 1200, c = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: ae(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: ae(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: ae(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: ae(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
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
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: f - 1,
    screenXL: f,
    screenXLMin: f,
    screenXLMax: c - 1,
    screenXXL: c,
    screenXXLMin: c,
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
const En = {
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
}, Pn = {
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
}, On = nr(De.defaultAlgorithm), Mn = {
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
}, Ht = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...s
  } = t;
  let i = {
    ...o,
    override: r
  };
  return i = Tn(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: f,
      ...c
    } = l;
    let u = c;
    f && (u = Ht({
      ...i,
      ...c
    }, {
      override: c
    }, f)), i[a] = u;
  }), i;
};
function In() {
  const {
    token: e,
    hashed: t,
    theme: n = On,
    override: o,
    cssVar: r
  } = p.useContext(De._internalContext), [s, i, a] = or(n, [De.defaultSeed, e], {
    salt: `${Nr}-${t || ""}`,
    override: o,
    getComputedToken: Ht,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: En,
      ignore: Pn,
      preserve: Mn
    }
  });
  return [n, a, t ? i : "", s, r];
}
const {
  genStyleHooks: Rn
} = xn({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = ge();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = In();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = ge();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var jn = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, kn = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Ln = "".concat(jn, " ").concat(kn).split(/[\s\n]+/), $n = "aria-", Dn = "data-";
function yt(e, t) {
  return e.indexOf(t) === 0;
}
function Bn(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = tn({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || yt(r, $n)) || // Data
    n.data && yt(r, Dn) || // Attr
    n.attr && Ln.includes(r)) && (o[r] = e[r]);
  }), o;
}
function le(e) {
  return typeof e == "string";
}
const Hn = (e, t, n, o) => {
  const r = T.useRef(""), [s, i] = T.useState(1), a = t && le(e);
  return qr(() => {
    !a && le(e) ? i(e.length) : le(e) && le(r.current) && e.indexOf(r.current) !== 0 && i(1), r.current = e;
  }, [e]), T.useEffect(() => {
    if (a && s < e.length) {
      const f = setTimeout(() => {
        i((c) => c + n);
      }, o);
      return () => {
        clearTimeout(f);
      };
    }
  }, [s, t, e]), [a ? e.slice(0, s) : e, a && s < e.length];
};
function zn(e) {
  return T.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const An = ({
  prefixCls: e
}) => /* @__PURE__ */ p.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ p.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), Fn = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: o
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${re(n)} ${re(o)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, Xn = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    padding: s,
    calc: i
  } = e, a = i(n).mul(o).div(2).add(r).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Nn = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto",
      "&::-webkit-scrollbar": {
        width: 8,
        backgroundColor: "transparent"
      },
      "&::-webkit-scrollbar-thumb": {
        backgroundColor: e.colorTextTertiary,
        borderRadius: e.borderRadiusSM
      },
      // For Firefox
      "&": {
        scrollbarWidth: "thin",
        scrollbarColor: `${e.colorTextTertiary} transparent`
      }
    }
  };
}, Vn = new wt("loadingMove", {
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
}), Wn = new wt("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Un = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: r,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Wn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: o,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: r
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(r).mul(2).add(i(o).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${re(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: Vn,
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
}, Gn = () => ({}), zt = Rn("Bubble", (e) => {
  const t = Ve(e, {});
  return [Un(t), Nn(t), Fn(t), Xn(t)];
}, Gn), At = /* @__PURE__ */ p.createContext({}), Kn = (e, t) => {
  const {
    prefixCls: n,
    className: o,
    rootClassName: r,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: f = "start",
    loading: c = !1,
    loadingRender: u,
    typing: d,
    content: g = "",
    messageRender: b,
    variant: S = "filled",
    shape: m,
    onTypingComplete: y,
    header: w,
    footer: I,
    ...h
  } = e, {
    onUpdate: _
  } = p.useContext(At), v = p.useRef(null);
  p.useImperativeHandle(t, () => ({
    nativeElement: v.current
  }));
  const {
    direction: P,
    getPrefixCls: O
  } = ge(), x = O("bubble", n), M = Ur("bubble"), [A, C, j, k] = zn(d), [L, D] = Hn(g, A, C, j);
  p.useEffect(() => {
    _ == null || _();
  }, [L]);
  const F = p.useRef(!1);
  p.useEffect(() => {
    !D && !c ? F.current || (F.current = !0, y == null || y()) : F.current = !1;
  }, [D, c]);
  const [U, G, oe] = zt(x), J = q(x, r, M.className, o, G, oe, `${x}-${f}`, {
    [`${x}-rtl`]: P === "rtl",
    [`${x}-typing`]: D && !c && !b && !k
  }), se = p.useMemo(() => /* @__PURE__ */ p.isValidElement(l) ? l : /* @__PURE__ */ p.createElement(tr, l), [l]), ie = p.useMemo(() => b ? b(L) : L, [L, b]);
  let X;
  c ? X = u ? u() : /* @__PURE__ */ p.createElement(An, {
    prefixCls: x
  }) : X = /* @__PURE__ */ p.createElement(p.Fragment, null, ie, D && k);
  let W = /* @__PURE__ */ p.createElement("div", {
    style: {
      ...M.styles.content,
      ...a.content
    },
    className: q(`${x}-content`, `${x}-content-${S}`, m && `${x}-content-${m}`, M.classNames.content, i.content)
  }, X);
  return (w || I) && (W = /* @__PURE__ */ p.createElement("div", {
    className: `${x}-content-wrapper`
  }, w && /* @__PURE__ */ p.createElement("div", {
    className: q(`${x}-header`, M.classNames.header, i.header),
    style: {
      ...M.styles.header,
      ...a.header
    }
  }, w), W, I && /* @__PURE__ */ p.createElement("div", {
    className: q(`${x}-footer`, M.classNames.footer, i.footer),
    style: {
      ...M.styles.footer,
      ...a.footer
    }
  }, typeof I == "function" ? I(ie) : I))), U(/* @__PURE__ */ p.createElement("div", Q({
    style: {
      ...M.style,
      ...s
    },
    className: J
  }, h, {
    ref: v
  }), l && /* @__PURE__ */ p.createElement("div", {
    style: {
      ...M.styles.avatar,
      ...a.avatar
    },
    className: q(`${x}-avatar`, M.classNames.avatar, i.avatar)
  }, se), W));
}, We = /* @__PURE__ */ p.forwardRef(Kn);
function qn(e, t) {
  const n = T.useCallback((o, r) => typeof t == "function" ? t(o, r) : t ? t[o.role] || {} : {}, [t]);
  return T.useMemo(() => (e || []).map((o, r) => {
    const s = o.key ?? `preset_${r}`;
    return {
      ...n(o, r),
      ...o,
      key: s
    };
  }), [e, n]);
}
const Yn = ({
  _key: e,
  ...t
}, n) => /* @__PURE__ */ T.createElement(We, Q({}, t, {
  ref: (o) => {
    var r;
    o ? n.current[e] = o : (r = n.current) == null || delete r[e];
  }
})), Qn = /* @__PURE__ */ T.memo(/* @__PURE__ */ T.forwardRef(Yn)), Jn = 1, Zn = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, f = Bn(l, {
    attr: !0,
    aria: !0
  }), c = T.useRef(null), u = T.useRef({}), {
    getPrefixCls: d
  } = ge(), g = d("bubble", n), b = `${g}-list`, [S, m, y] = zt(g), [w, I] = T.useState(!1);
  T.useEffect(() => (I(!0), () => {
    I(!1);
  }), []);
  const h = qn(s, a), [_, v] = T.useState(!0), [P, O] = T.useState(0), x = (C) => {
    const j = C.target;
    v(j.scrollHeight - Math.abs(j.scrollTop) - j.clientHeight <= Jn);
  };
  T.useEffect(() => {
    i && c.current && _ && c.current.scrollTo({
      top: c.current.scrollHeight
    });
  }, [P]), T.useEffect(() => {
    var C;
    if (i) {
      const j = (C = h[h.length - 2]) == null ? void 0 : C.key, k = u.current[j];
      if (k) {
        const {
          nativeElement: L
        } = k, {
          top: D,
          bottom: F
        } = L.getBoundingClientRect(), {
          top: U,
          bottom: G
        } = c.current.getBoundingClientRect();
        D < G && F > U && (O((J) => J + 1), v(!0));
      }
    }
  }, [h.length]), T.useImperativeHandle(t, () => ({
    nativeElement: c.current,
    scrollTo: ({
      key: C,
      offset: j,
      behavior: k = "smooth",
      block: L
    }) => {
      if (typeof j == "number")
        c.current.scrollTo({
          top: j,
          behavior: k
        });
      else if (C !== void 0) {
        const D = u.current[C];
        if (D) {
          const F = h.findIndex((U) => U.key === C);
          v(F === h.length - 1), D.nativeElement.scrollIntoView({
            behavior: k,
            block: L
          });
        }
      }
    }
  }));
  const M = Gr(() => {
    i && O((C) => C + 1);
  }), A = T.useMemo(() => ({
    onUpdate: M
  }), []);
  return S(/* @__PURE__ */ T.createElement(At.Provider, {
    value: A
  }, /* @__PURE__ */ T.createElement("div", Q({}, f, {
    className: q(b, o, r, m, y, {
      [`${b}-reach-end`]: _
    }),
    ref: c,
    onScroll: x
  }), h.map(({
    key: C,
    ...j
  }) => /* @__PURE__ */ T.createElement(Qn, Q({}, j, {
    key: C,
    _key: C,
    ref: u,
    typing: w ? j.typing : !1
  }))))));
}, eo = /* @__PURE__ */ T.forwardRef(Zn);
We.List = eo;
const to = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ro(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = no(n, o), t;
  }, {}) : {};
}
function no(e, t) {
  return typeof t == "number" && !to.includes(e) ? t + "px" : t;
}
function Ae(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = p.Children.toArray(e._reactElement.props.children).map((s) => {
      if (p.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = Ae(s.props.el);
        return p.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...p.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push($e(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, i, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = Ae(s);
      t.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function oo(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const vt = Ut(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = xt(), [a, l] = Gt([]), {
    forceClone: f
  } = Zt(), c = f ? !0 : t;
  return Kt(() => {
    var S;
    if (!i.current || !e)
      return;
    let u = e;
    function d() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), oo(s, m), n && m.classList.add(...n.split(" ")), o) {
        const y = ro(o);
        Object.keys(y).forEach((w) => {
          m.style[w] = y[w];
        });
      }
    }
    let g = null, b = null;
    if (c && window.MutationObserver) {
      let m = function() {
        var h, _, v;
        (h = i.current) != null && h.contains(u) && ((_ = i.current) == null || _.removeChild(u));
        const {
          portals: w,
          clonedElement: I
        } = Ae(e);
        u = I, l(w), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (v = i.current) == null || v.appendChild(u);
      };
      m();
      const y = pr(() => {
        m(), g == null || g.disconnect(), g == null || g.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      g = new window.MutationObserver(y), g.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (S = i.current) == null || S.appendChild(u);
    return () => {
      var m, y;
      u.style.display = "", (m = i.current) != null && m.contains(u) && ((y = i.current) == null || y.removeChild(u)), g == null || g.disconnect();
    };
  }, [e, c, n, o, s, r, f]), p.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
});
function St(e) {
  const t = xt(e);
  return t.current = e, qt((...n) => {
    var o;
    return (o = t.current) == null ? void 0 : o.call(t, ...n);
  }, []);
}
const so = ({
  children: e,
  ...t
}) => /* @__PURE__ */ H.jsx(H.Fragment, {
  children: e(t)
});
function io(e) {
  return p.createElement(so, {
    children: e
  });
}
function Ue(e, t, n) {
  const o = e.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var f;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((f = r.props) == null ? void 0 : f.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((c) => {
        if (!r.slots[c] || !(r.slots[c] instanceof Element) && !r.slots[c].el)
          return;
        const u = c.split(".");
        u.forEach((y, w) => {
          a[y] || (a[y] = {}), w !== u.length - 1 && (a = i[y]);
        });
        const d = r.slots[c];
        let g, b, S = (t == null ? void 0 : t.clone) ?? !1, m = t == null ? void 0 : t.forceClone;
        d instanceof Element ? g = d : (g = d.el, b = d.callback, S = d.clone ?? S, m = d.forceClone ?? m), m = m ?? !!b, a[u[u.length - 1]] = g ? b ? (...y) => (b(u[u.length - 1], y), /* @__PURE__ */ H.jsx(Ye, {
          ...r.ctx,
          params: y,
          forceClone: m,
          children: /* @__PURE__ */ H.jsx(vt, {
            slot: g,
            clone: S
          })
        })) : io((y) => /* @__PURE__ */ H.jsx(Ye, {
          ...r.ctx,
          forceClone: m,
          children: /* @__PURE__ */ H.jsx(vt, {
            ...y,
            slot: g,
            clone: S
          })
        })) : a[u[u.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return r[l] ? i[l] = Ue(r[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const {
  useItems: ao,
  withItemsContextProvider: lo,
  ItemHandler: xo
} = Ct("antdx-bubble.list-items"), {
  useItems: co,
  withItemsContextProvider: uo,
  ItemHandler: Co
} = Ct("antdx-bubble.list-roles");
function fo(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ho(e, t = !1) {
  try {
    if (Fe(e))
      return e;
    if (t && !fo(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function go(e, t) {
  return he(() => ho(e, t), [e, t]);
}
function mo(e, t) {
  return t((o, r) => Fe(o) ? r ? (...s) => o(...s, ...e) : o(...e) : o);
}
const po = Symbol();
function bo(e, t) {
  return mo(t, (n) => {
    var o, r;
    return {
      ...e,
      avatar: Fe(e.avatar) ? n(e.avatar) : te(e.avatar) ? {
        ...e.avatar,
        icon: n((o = e.avatar) == null ? void 0 : o.icon),
        src: n((r = e.avatar) == null ? void 0 : r.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function yo({
  roles: e,
  preProcess: t,
  postProcess: n
}, o = []) {
  const r = go(e), s = St(t), i = St(n), {
    items: {
      roles: a
    }
  } = co(), l = he(() => {
    var c;
    return e || ((c = Ue(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : c.reduce((u, d) => (d.role !== void 0 && (u[d.role] = d), u), {}));
  }, [a, e]), f = he(() => (c, u) => {
    const d = u ?? c[po], g = s(c, d) || c;
    if (g.role && (l || {})[g.role])
      return bo((l || {})[g.role], [g, d]);
    let b;
    return b = i(g, d), b || {
      messageRender(S) {
        return /* @__PURE__ */ H.jsx(H.Fragment, {
          children: te(S) ? JSON.stringify(S) : S
        });
      }
    };
  }, [l, i, s, ...o]);
  return r || f;
}
const wo = Xr(uo(["roles"], lo(["items", "default"], ({
  items: e,
  roles: t,
  children: n,
  ...o
}) => {
  const {
    items: r
  } = ao(), s = yo({
    roles: t
  }), i = r.items.length > 0 ? r.items : r.default;
  return /* @__PURE__ */ H.jsxs(H.Fragment, {
    children: [/* @__PURE__ */ H.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ H.jsx(We.List, {
      ...o,
      items: he(() => e || Ue(i), [e, i]),
      roles: s
    })]
  });
})));
export {
  wo as BubbleList,
  wo as default
};
