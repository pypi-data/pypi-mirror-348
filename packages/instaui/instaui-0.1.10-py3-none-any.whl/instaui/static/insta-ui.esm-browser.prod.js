var Bn = Object.defineProperty;
var Ln = (e, t, n) => t in e ? Bn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var B = (e, t, n) => Ln(e, typeof t != "symbol" ? t + "" : t, n);
import * as Wn from "vue";
import { customRef as Ae, toValue as q, unref as L, watch as G, nextTick as Ne, isRef as Kt, shallowRef as J, ref as Z, watchEffect as Gt, computed as W, readonly as Un, provide as Ve, inject as ee, shallowReactive as Kn, defineComponent as F, reactive as Gn, h as A, getCurrentInstance as qt, normalizeStyle as qn, normalizeClass as ze, toDisplayString as Ht, onUnmounted as je, Fragment as $e, vModelDynamic as Hn, vShow as zn, resolveDynamicComponent as ut, normalizeProps as Jn, withDirectives as Qn, onErrorCaptured as Yn, openBlock as de, createElementBlock as Pe, createElementVNode as Xn, createVNode as Zn, withCtx as er, renderList as tr, createBlock as nr, TransitionGroup as zt, KeepAlive as rr } from "vue";
let Jt;
function or(e) {
  Jt = e;
}
function Je() {
  return Jt;
}
function ye() {
  const { queryPath: e, pathParams: t, queryParams: n } = Je();
  return {
    path: e,
    ...t === void 0 ? {} : { params: t },
    ...n === void 0 ? {} : { queryParams: n }
  };
}
class sr extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function we(e) {
  return new sr(e);
}
function Et(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function Ee(e, t) {
  return Qt(e, {
    valueFn: t
  });
}
function Qt(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s], i) => [
      r ? r(o, s) : o,
      n(s, o, i)
    ])
  );
}
function Yt(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = Xt(t, n);
  return e[r];
}
function Xt(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function _e(e, t, n) {
  return t.reduce(
    (r, o) => Yt(r, o, n),
    e
  );
}
function Qe(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[Xt(s, r)] = n;
    else
      return Yt(o, s, r);
  }, e);
}
function Zt(e) {
  return JSON.parse(JSON.stringify(e));
}
function _t(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : Ae(() => ({
    get() {
      try {
        return _e(
          q(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(c) {
      Qe(
        q(e),
        s || r,
        c,
        i
      );
    }
  }));
}
function en(e) {
  return Ae((t, n) => ({
    get() {
      return t(), e;
    },
    set(r) {
      JSON.stringify(r) !== JSON.stringify(e) && (e = r, n());
    }
  }));
}
function he(e) {
  return typeof e == "function" ? e() : L(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const Ye = () => {
};
function Xe(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function Ze(e, t = !1) {
  function n(u, { flush: f = "sync", deep: h = !1, timeout: v, throwOnTimeout: p } = {}) {
    let g = null;
    const _ = [new Promise((O) => {
      g = G(
        e,
        (R) => {
          u(R) !== t && (g ? g() : Ne(() => g == null ? void 0 : g()), O(R));
        },
        {
          flush: f,
          deep: h,
          immediate: !0
        }
      );
    })];
    return v != null && _.push(
      Xe(v, p).then(() => he(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(u, f) {
    if (!Kt(u))
      return n((R) => R === u, f);
    const { flush: h = "sync", deep: v = !1, timeout: p, throwOnTimeout: g } = f ?? {};
    let y = null;
    const O = [new Promise((R) => {
      y = G(
        [e, u],
        ([D, C]) => {
          t !== (D === C) && (y ? y() : Ne(() => y == null ? void 0 : y()), R(D));
        },
        {
          flush: h,
          deep: v,
          immediate: !0
        }
      );
    })];
    return p != null && O.push(
      Xe(p, g).then(() => he(e)).finally(() => (y == null || y(), he(e)))
    ), Promise.race(O);
  }
  function o(u) {
    return n((f) => !!f, u);
  }
  function s(u) {
    return r(null, u);
  }
  function i(u) {
    return r(void 0, u);
  }
  function c(u) {
    return n(Number.isNaN, u);
  }
  function l(u, f) {
    return n((h) => {
      const v = Array.from(h);
      return v.includes(u) || v.includes(he(u));
    }, f);
  }
  function d(u) {
    return a(1, u);
  }
  function a(u = 1, f) {
    let h = -1;
    return n(() => (h += 1, h >= u), f);
  }
  return Array.isArray(he(e)) ? {
    toMatch: n,
    toContains: l,
    changed: d,
    changedTimes: a,
    get not() {
      return Ze(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: c,
    toBeUndefined: i,
    changed: d,
    changedTimes: a,
    get not() {
      return Ze(e, !t);
    }
  };
}
function ir(e) {
  return Ze(e);
}
function ar(e, t, n) {
  let r;
  Kt(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: c = Ye
  } = r, l = Z(!o), d = i ? J(t) : Z(t);
  let a = 0;
  return Gt(async (u) => {
    if (!l.value)
      return;
    a++;
    const f = a;
    let h = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const v = await e((p) => {
        u(() => {
          s && (s.value = !1), h || p();
        });
      });
      f === a && (d.value = v);
    } catch (v) {
      c(v);
    } finally {
      s && f === a && (s.value = !1), h = !0;
    }
  }), o ? W(() => (l.value = !0, d.value)) : d;
}
function cr(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = Ye,
    onSuccess: i = Ye,
    resetOnExecute: c = !0,
    shallow: l = !0,
    throwError: d
  } = {}, a = l ? J(t) : Z(t), u = Z(!1), f = Z(!1), h = J(void 0);
  async function v(y = 0, ..._) {
    c && (a.value = t), h.value = void 0, u.value = !1, f.value = !0, y > 0 && await Xe(y);
    const O = typeof e == "function" ? e(..._) : e;
    try {
      const R = await O;
      a.value = R, u.value = !0, i(R);
    } catch (R) {
      if (h.value = R, s(R), d)
        throw R;
    } finally {
      f.value = !1;
    }
    return a.value;
  }
  r && v(o);
  const p = {
    state: a,
    isReady: u,
    isLoading: f,
    error: h,
    execute: v
  };
  function g() {
    return new Promise((y, _) => {
      ir(f).toBe(!1).then(() => y(p)).catch(_);
    });
  }
  return {
    ...p,
    then(y, _) {
      return g().then(y, _);
    }
  };
}
function U(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Wn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function ur(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return U(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function tn(e) {
  return e.constructor.name === "AsyncFunction";
}
function lr(e, t) {
  return Z(e.value);
}
function fr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((a, u) => s[u] === 1 ? a : t.getVueRefObjectOrValue(a));
  if (tn(new Function(o)))
    return ar(
      async () => {
        const a = Object.fromEntries(
          Object.keys(r).map((u, f) => [u, i[f]])
        );
        return await U(o, a)();
      },
      null,
      { lazy: !0 }
    );
  const c = Object.fromEntries(
    Object.keys(r).map((a, u) => [a, i[u]])
  ), l = U(o, c);
  return W(l);
}
function dr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: c = null,
    deepEqOnInput: l = 0
  } = e, d = s || Array(r.length).fill(0), a = i || Array(r.length).fill(0), u = r.filter((g, y) => d[y] === 0 && a[y] === 0).map((g) => t.getVueRefObject(g));
  function f() {
    return r.map(
      (g, y) => a[y] === 1 ? g : t.getObjectToValue(g)
    );
  }
  const h = U(o), v = l === 0 ? J(null) : en(null), p = { immediate: !0, deep: !0 };
  return tn(h) ? (v.value = c, G(
    u,
    async () => {
      v.value = await h(...f());
    },
    p
  )) : G(
    u,
    () => {
      v.value = h(...f());
    },
    p
  ), Un(v);
}
var N;
((e) => {
  function t(f) {
    return f.type === "var";
  }
  e.isVar = t;
  function n(f) {
    return f.type === "routePar";
  }
  e.isRouterParams = n;
  function r(f) {
    return f.type === "routeAct";
  }
  e.isRouterAction = r;
  function o(f) {
    return f.type === "js";
  }
  e.isJs = o;
  function s(f) {
    return f.type === "jsOutput";
  }
  e.isJsOutput = s;
  function i(f) {
    return f.type === "vf";
  }
  e.isVForItem = i;
  function c(f) {
    return f.type === "vf-i";
  }
  e.isVForIndex = c;
  function l(f) {
    return f.type === "sp";
  }
  e.isSlotProp = l;
  function d(f) {
    return f.type === "event";
  }
  e.isEventContext = d;
  function a(f) {
    return f.type === "ele_ref";
  }
  e.isElementRef = a;
  function u(f) {
    return f.type !== void 0;
  }
  e.IsBinding = u;
})(N || (N = {}));
class hr {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = Je().webServerInfo, c = s !== void 0 ? { key: s } : {}, l = r === "sync" ? i.event_url : i.event_async_url;
    let d = {};
    const a = await fetch(l, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: n,
        hKey: o,
        ...c,
        page: ye(),
        ...d
      })
    });
    if (!a.ok)
      throw new Error(`HTTP error! status: ${a.status}`);
    return await a.json();
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = Je().webServerInfo, i = r === "sync" ? s.watch_url : s.watch_async_url, c = t.getServerInputs(), l = {
      key: o,
      input: c,
      page: ye()
    };
    return await (await fetch(i, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(l)
    })).json();
  }
}
class pr {
  async eventSend(t, n) {
    const { fType: r, hKey: o, key: s } = t, i = s !== void 0 ? { key: s } : {};
    let c = {};
    const l = {
      bind: n,
      fType: r,
      hKey: o,
      ...i,
      page: ye(),
      ...c
    };
    return await window.pywebview.api.event_call(l);
  }
  async watchSend(t) {
    const { outputs: n, fType: r, key: o } = t.watchConfig, s = t.getServerInputs(), i = {
      key: o,
      input: s,
      fType: r,
      page: ye()
    };
    return await window.pywebview.api.watch_call(i);
  }
}
let et;
function mr(e) {
  switch (e.mode) {
    case "web":
      et = new hr();
      break;
    case "webview":
      et = new pr();
      break;
  }
}
function nn() {
  return et;
}
class gr {
  toString() {
    return "";
  }
}
const tt = new gr();
function vr(e) {
  return e === tt;
}
function yr(e, t, n) {
  return new wr(e, t, n);
}
class wr {
  constructor(t, n, r) {
    B(this, "taskQueue", []);
    B(this, "id2TaskMap", /* @__PURE__ */ new Map());
    B(this, "input2TaskIdMap", we(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const c = new Er(i, r);
      return this.id2TaskMap.set(c.id, c), (l = i.inputs) == null || l.forEach((d, a) => {
        var f, h;
        if (((f = i.data) == null ? void 0 : f[a]) === 0 && ((h = i.slient) == null ? void 0 : h[a]) === 0) {
          const v = `${d.sid}-${d.id}`;
          this.input2TaskIdMap.getOrDefault(v).push(c.id);
        }
      }), c;
    };
    t == null || t.forEach((i) => {
      const c = s(i);
      o.push(c);
    }), n == null || n.forEach((i) => {
      const c = {
        type: "var",
        sid: i.sid,
        id: i.id
      }, l = {
        ...i,
        immediate: !0,
        outputs: [c, ...i.outputs || []]
      }, d = s(l);
      o.push(d);
    }), o.forEach((i) => {
      const {
        deep: c = !0,
        once: l,
        flush: d,
        immediate: a = !0
      } = i.watchConfig, u = {
        immediate: a,
        deep: c,
        once: l,
        flush: d
      }, f = this._getWatchTargets(i);
      G(
        f,
        (h) => {
          h.some(vr) || (i.modify = !0, this.taskQueue.push(new _r(i)), this._scheduleNextTick());
        },
        u
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs, r = t.constDataInputs;
    return t.watchConfig.inputs.filter(
      (s, i) => !r[i] && (N.isVar(s) || N.isVForItem(s) || N.isRouterParams(s)) && !n[i]
    ).map((s) => this.snapshots.getVueRefObjectOrValue(s));
  }
  _scheduleNextTick() {
    Ne(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((i) => n.add(i));
    }), n;
  }
}
class Er {
  constructor(t, n) {
    B(this, "modify", !0);
    B(this, "_running", !1);
    B(this, "id");
    B(this, "_runningPromise", null);
    B(this, "_runningPromiseResolve", null);
    B(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  get constDataInputs() {
    return this._inputInfos.const_data;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class _r {
  /**
   *
   */
  constructor(t) {
    B(this, "prevNodes", []);
    B(this, "nextNodes", []);
    B(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await Or(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function Or(e) {
  const { snapshot: t } = e, { outputs: n } = e.watchConfig, r = await nn().watchSend(e);
  r && t.updateOutputsRefFromServer(r, n);
}
function br() {
  return [];
}
const Oe = we(br);
function rn(e, t) {
  var s, i, c, l, d;
  const n = Oe.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  n.push(r), t.replaceSnapshot({
    scopeSnapshot: on()
  });
  const o = (a, u) => {
    r.set(a.id, u);
  };
  return (s = e.refs) == null || s.forEach((a) => {
    o(a, lr(a));
  }), (i = e.web_computed) == null || i.forEach((a) => {
    const { init: u } = a, f = a.deepEqOnInput === void 0 ? J(u ?? tt) : en(u ?? tt);
    o(a, f);
  }), (c = e.vue_computed) == null || c.forEach((a) => {
    o(
      a,
      fr(a, t)
    );
  }), (l = e.js_computed) == null || l.forEach((a) => {
    o(
      a,
      dr(a, t)
    );
  }), (d = e.data) == null || d.forEach((a) => {
    o(a, a.value);
  }), n.length - 1;
}
function on() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Oe) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return sn(n, e);
  }
  return {
    getVueRef: t
  };
}
function Sr(e) {
  return sn(e, Oe);
}
function sn(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function Rr(e) {
  Oe.delete(e);
}
function an(e, t) {
  const n = Oe.get(e);
  n && n.splice(t, 1);
}
const lt = we(() => []);
function Pr(e) {
  var r;
  const t = /* @__PURE__ */ new Map(), n = lt.getOrDefault(e.id).push(t);
  return (r = e.eRefs) == null || r.forEach((o) => {
    const s = J();
    t.set(o.id, s);
  }), n;
}
function kr(e, t) {
  const n = lt.get(e);
  n && n.splice(t, 1);
}
function cn() {
  const e = new Map(
    Array.from(lt.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid).get(n.id);
  }
  return {
    getRef: t
  };
}
const Ce = we(() => []);
function Vr(e) {
  const t = Ce.getOrDefault(e);
  return t.push(J({})), t.length - 1;
}
function Nr(e, t, n) {
  Ce.get(e)[t].value = n;
}
function Ir(e) {
  Ce.delete(e);
}
function Tr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Ce) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
const un = /* @__PURE__ */ new Map(), ft = we(() => /* @__PURE__ */ new Map()), ln = /* @__PURE__ */ new Set(), fn = Symbol("vfor");
function Ar(e) {
  const t = dn() ?? {};
  Ve(fn, { ...t, [e.fid]: e.key });
}
function dn() {
  return ee(fn, void 0);
}
function jr() {
  const e = dn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function $r(e, t, n, r) {
  if (r) {
    ln.add(e);
    return;
  }
  let o;
  if (n)
    o = new Lr(t);
  else {
    const s = Array.isArray(t) ? t : Object.entries(t).map(([i, c], l) => [c, i, l]);
    o = new Br(s);
  }
  un.set(e, o);
}
function Cr(e, t, n) {
  const r = ft.getOrDefault(e);
  r.has(t) || r.set(t, Z(n)), r.get(t).value = n;
}
function xr(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = ft.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function Dr(e) {
  const t = e, n = jr();
  function r(o) {
    const s = n.get(o) ?? t;
    return ft.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function Mr(e) {
  return un.get(e.binding.fid).createRefObjectWithPaths(e);
}
function Fr(e) {
  return ln.has(e);
}
class Br {
  constructor(t) {
    this.array = t;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { snapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), Ae(() => ({
      get: () => _e(
        this.array,
        s,
        r.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class Lr {
  constructor(t) {
    B(this, "_isDictSource");
    this.binding = t;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = q(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { snapshot: s } = t, i = s.getVueRefObject(this.binding), c = this.isDictSource(i), l = s.getVForIndex(n.fid), d = c && o.length === 0 ? [0] : [];
    return o.unshift(l, ...d), Ae(() => ({
      get: () => {
        const a = q(i), u = c ? Object.entries(a).map(([f, h], v) => [
          h,
          f,
          v
        ]) : a;
        try {
          return _e(
            q(u),
            o,
            s.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (a) => {
        const u = q(i);
        if (c) {
          const f = Object.keys(u);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const h = f[l];
          Qe(
            u,
            [h],
            a,
            s.getObjectToValue
          );
          return;
        }
        Qe(
          u,
          o,
          a,
          s.getObjectToValue
        );
      }
    }));
  }
}
function Wr(e, t, n = !1) {
  return n && (e = `$computed(${e})`, t = { ...t, $computed: W }), U(e, t);
}
function Ot(e) {
  return e == null;
}
function Ur() {
  return hn().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function hn() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const Kr = typeof Proxy == "function", Gr = "devtools-plugin:setup", qr = "plugin:settings:set";
let ie, nt;
function Hr() {
  var e;
  return ie !== void 0 || (typeof window < "u" && window.performance ? (ie = !0, nt = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ie = !0, nt = globalThis.perf_hooks.performance) : ie = !1), ie;
}
function zr() {
  return Hr() ? nt.now() : Date.now();
}
class Jr {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const i in t.settings) {
        const c = t.settings[i];
        r[i] = c.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const i = localStorage.getItem(o), c = JSON.parse(i);
      Object.assign(s, c);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(i) {
        try {
          localStorage.setItem(o, JSON.stringify(i));
        } catch {
        }
        s = i;
      },
      now() {
        return zr();
      }
    }, n && n.on(qr, (i, c) => {
      i === this.plugin.id && this.fallbacks.setSettings(c);
    }), this.proxiedOn = new Proxy({}, {
      get: (i, c) => this.target ? this.target.on[c] : (...l) => {
        this.onQueue.push({
          method: c,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (i, c) => this.target ? this.target[c] : c === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(c) ? (...l) => (this.targetQueue.push({
        method: c,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[c](...l)) : (...l) => new Promise((d) => {
        this.targetQueue.push({
          method: c,
          args: l,
          resolve: d
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Qr(e, t) {
  const n = e, r = hn(), o = Ur(), s = Kr && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(Gr, e, t);
  else {
    const i = s ? new Jr(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var S = {};
const z = typeof document < "u";
function pn(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Yr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && pn(e.default);
}
const I = Object.assign;
function Ke(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = K(o) ? o.map(e) : e(o);
  }
  return n;
}
const ve = () => {
}, K = Array.isArray;
function P(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const mn = /#/g, Xr = /&/g, Zr = /\//g, eo = /=/g, to = /\?/g, gn = /\+/g, no = /%5B/g, ro = /%5D/g, vn = /%5E/g, oo = /%60/g, yn = /%7B/g, so = /%7C/g, wn = /%7D/g, io = /%20/g;
function dt(e) {
  return encodeURI("" + e).replace(so, "|").replace(no, "[").replace(ro, "]");
}
function ao(e) {
  return dt(e).replace(yn, "{").replace(wn, "}").replace(vn, "^");
}
function rt(e) {
  return dt(e).replace(gn, "%2B").replace(io, "+").replace(mn, "%23").replace(Xr, "%26").replace(oo, "`").replace(yn, "{").replace(wn, "}").replace(vn, "^");
}
function co(e) {
  return rt(e).replace(eo, "%3D");
}
function uo(e) {
  return dt(e).replace(mn, "%23").replace(to, "%3F");
}
function lo(e) {
  return e == null ? "" : uo(e).replace(Zr, "%2F");
}
function ae(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    S.NODE_ENV !== "production" && P(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const fo = /\/$/, ho = (e) => e.replace(fo, "");
function Ge(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const c = t.indexOf("#");
  let l = t.indexOf("?");
  return c < l && c >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, c > -1 ? c : t.length), o = e(s)), c > -1 && (r = r || t.slice(0, c), i = t.slice(c, t.length)), r = go(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ae(i)
  };
}
function po(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function bt(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function St(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && te(t.matched[r], n.matched[o]) && En(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function te(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function En(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!mo(e[n], t[n]))
      return !1;
  return !0;
}
function mo(e, t) {
  return K(e) ? Rt(e, t) : K(t) ? Rt(t, e) : e === t;
}
function Rt(e, t) {
  return K(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function go(e, t) {
  if (e.startsWith("/"))
    return e;
  if (S.NODE_ENV !== "production" && !t.startsWith("/"))
    return P(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, i, c;
  for (i = 0; i < r.length; i++)
    if (c = r[i], c !== ".")
      if (c === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(i).join("/");
}
const Y = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ce;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ce || (ce = {}));
var oe;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(oe || (oe = {}));
const qe = "";
function _n(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), ho(e);
}
const vo = /^[^#]+#/;
function On(e, t) {
  return e.replace(vo, "#") + t;
}
function yo(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const xe = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function wo(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (S.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          P(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        P(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      S.NODE_ENV !== "production" && P(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = yo(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Pt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const ot = /* @__PURE__ */ new Map();
function Eo(e, t) {
  ot.set(e, t);
}
function _o(e) {
  const t = ot.get(e);
  return ot.delete(e), t;
}
let Oo = () => location.protocol + "//" + location.host;
function bn(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let c = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(c);
    return l[0] !== "/" && (l = "/" + l), bt(l, "");
  }
  return bt(n, e) + r + o;
}
function bo(e, t, n, r) {
  let o = [], s = [], i = null;
  const c = ({ state: f }) => {
    const h = bn(e, location), v = n.value, p = t.value;
    let g = 0;
    if (f) {
      if (n.value = h, t.value = f, i && i === v) {
        i = null;
        return;
      }
      g = p ? f.position - p.position : 0;
    } else
      r(h);
    o.forEach((y) => {
      y(n.value, v, {
        delta: g,
        type: ce.pop,
        direction: g ? g > 0 ? oe.forward : oe.back : oe.unknown
      });
    });
  };
  function l() {
    i = n.value;
  }
  function d(f) {
    o.push(f);
    const h = () => {
      const v = o.indexOf(f);
      v > -1 && o.splice(v, 1);
    };
    return s.push(h), h;
  }
  function a() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: xe() }), "");
  }
  function u() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", c), window.removeEventListener("beforeunload", a);
  }
  return window.addEventListener("popstate", c), window.addEventListener("beforeunload", a, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: d,
    destroy: u
  };
}
function kt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? xe() : null
  };
}
function So(e) {
  const { history: t, location: n } = window, r = {
    value: bn(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, d, a) {
    const u = e.indexOf("#"), f = u > -1 ? (n.host && document.querySelector("base") ? e : e.slice(u)) + l : Oo() + e + l;
    try {
      t[a ? "replaceState" : "pushState"](d, "", f), o.value = d;
    } catch (h) {
      S.NODE_ENV !== "production" ? P("Error with push/replace State", h) : console.error(h), n[a ? "replace" : "assign"](f);
    }
  }
  function i(l, d) {
    const a = I({}, t.state, kt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), d, { position: o.value.position });
    s(l, a, !0), r.value = l;
  }
  function c(l, d) {
    const a = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: xe()
      }
    );
    S.NODE_ENV !== "production" && !t.state && P(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(a.current, a, !0);
    const u = I({}, kt(r.value, l, null), { position: a.position + 1 }, d);
    s(l, u, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: c,
    replace: i
  };
}
function Sn(e) {
  e = _n(e);
  const t = So(e), n = bo(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: On.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function Ro(e = "") {
  let t = [], n = [qe], r = 0;
  e = _n(e);
  function o(c) {
    r++, r !== n.length && n.splice(r), n.push(c);
  }
  function s(c, l, { direction: d, delta: a }) {
    const u = {
      direction: d,
      delta: a,
      type: ce.pop
    };
    for (const f of t)
      f(c, l, u);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: qe,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: On.bind(null, e),
    replace(c) {
      n.splice(r--, 1), o(c);
    },
    push(c, l) {
      o(c);
    },
    listen(c) {
      return t.push(c), () => {
        const l = t.indexOf(c);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [qe], r = 0;
    },
    go(c, l = !0) {
      const d = this.location, a = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        c < 0 ? oe.back : oe.forward
      );
      r = Math.max(0, Math.min(r + c, n.length - 1)), l && s(this.location, d, {
        direction: a,
        delta: c
      });
    }
  };
  return Object.defineProperty(i, "location", {
    enumerable: !0,
    get: () => n[r]
  }), i;
}
function Po(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), S.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && P(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), Sn(e);
}
function Ie(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function Rn(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const st = Symbol(S.NODE_ENV !== "production" ? "navigation failure" : "");
var Vt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(Vt || (Vt = {}));
const ko = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${No(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function ue(e, t) {
  return S.NODE_ENV !== "production" ? I(new Error(ko[e](t)), {
    type: e,
    [st]: !0
  }, t) : I(new Error(), {
    type: e,
    [st]: !0
  }, t);
}
function H(e, t) {
  return e instanceof Error && st in e && (t == null || !!(e.type & t));
}
const Vo = ["params", "query", "hash"];
function No(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Vo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Nt = "[^/]+?", Io = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, To = /[.+*?^${}()[\]/\\]/g;
function Ao(e, t) {
  const n = I({}, Io, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const d of e) {
    const a = d.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !d.length && (o += "/");
    for (let u = 0; u < d.length; u++) {
      const f = d[u];
      let h = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        u || (o += "/"), o += f.value.replace(To, "\\$&"), h += 40;
      else if (f.type === 1) {
        const { value: v, repeatable: p, optional: g, regexp: y } = f;
        s.push({
          name: v,
          repeatable: p,
          optional: g
        });
        const _ = y || Nt;
        if (_ !== Nt) {
          h += 10;
          try {
            new RegExp(`(${_})`);
          } catch (R) {
            throw new Error(`Invalid custom RegExp for param "${v}" (${_}): ` + R.message);
          }
        }
        let O = p ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        u || (O = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && d.length < 2 ? `(?:/${O})` : "/" + O), g && (O += "?"), o += O, h += 20, g && (h += -8), p && (h += -20), _ === ".*" && (h += -50);
      }
      a.push(h);
    }
    r.push(a);
  }
  if (n.strict && n.end) {
    const d = r.length - 1;
    r[d][r[d].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function c(d) {
    const a = d.match(i), u = {};
    if (!a)
      return null;
    for (let f = 1; f < a.length; f++) {
      const h = a[f] || "", v = s[f - 1];
      u[v.name] = h && v.repeatable ? h.split("/") : h;
    }
    return u;
  }
  function l(d) {
    let a = "", u = !1;
    for (const f of e) {
      (!u || !a.endsWith("/")) && (a += "/"), u = !1;
      for (const h of f)
        if (h.type === 0)
          a += h.value;
        else if (h.type === 1) {
          const { value: v, repeatable: p, optional: g } = h, y = v in d ? d[v] : "";
          if (K(y) && !p)
            throw new Error(`Provided param "${v}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = K(y) ? y.join("/") : y;
          if (!_)
            if (g)
              f.length < 2 && (a.endsWith("/") ? a = a.slice(0, -1) : u = !0);
            else
              throw new Error(`Missing required param "${v}"`);
          a += _;
        }
    }
    return a || "/";
  }
  return {
    re: i,
    score: r,
    keys: s,
    parse: c,
    stringify: l
  };
}
function jo(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Pn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = jo(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (It(r))
      return 1;
    if (It(o))
      return -1;
  }
  return o.length - r.length;
}
function It(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const $o = {
  type: 0,
  value: ""
}, Co = /[a-zA-Z0-9_]/;
function xo(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[$o]];
  if (!e.startsWith("/"))
    throw new Error(S.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(h) {
    throw new Error(`ERR (${n})/"${d}": ${h}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let c = 0, l, d = "", a = "";
  function u() {
    d && (n === 0 ? s.push({
      type: 0,
      value: d
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${d}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: d,
      regexp: a,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), d = "");
  }
  function f() {
    d += l;
  }
  for (; c < e.length; ) {
    if (l = e[c++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (d && u(), i()) : l === ":" ? (u(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : Co.test(l) ? f() : (u(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--);
        break;
      case 2:
        l === ")" ? a[a.length - 1] == "\\" ? a = a.slice(0, -1) + l : n = 3 : a += l;
        break;
      case 3:
        u(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--, a = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${d}"`), u(), i(), o;
}
function Do(e, t, n) {
  const r = Ao(xo(e.path), n);
  if (S.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && P(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function Mo(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = $t({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(u) {
    return r.get(u);
  }
  function s(u, f, h) {
    const v = !h, p = At(u);
    S.NODE_ENV !== "production" && Wo(p, f), p.aliasOf = h && h.record;
    const g = $t(t, u), y = [p];
    if ("alias" in u) {
      const R = typeof u.alias == "string" ? [u.alias] : u.alias;
      for (const D of R)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          At(I({}, p, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: h ? h.record.components : p.components,
            path: D,
            // we might be the child of an alias
            aliasOf: h ? h.record : p
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, O;
    for (const R of y) {
      const { path: D } = R;
      if (f && D[0] !== "/") {
        const C = f.record.path, x = C[C.length - 1] === "/" ? "" : "/";
        R.path = f.record.path + (D && x + D);
      }
      if (S.NODE_ENV !== "production" && R.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = Do(R, f, g), S.NODE_ENV !== "production" && f && D[0] === "/" && Ko(_, f), h ? (h.alias.push(_), S.NODE_ENV !== "production" && Lo(h, _)) : (O = O || _, O !== _ && O.alias.push(_), v && u.name && !jt(_) && (S.NODE_ENV !== "production" && Uo(u, f), i(u.name))), kn(_) && l(_), p.children) {
        const C = p.children;
        for (let x = 0; x < C.length; x++)
          s(C[x], _, h && h.children[x]);
      }
      h = h || _;
    }
    return O ? () => {
      i(O);
    } : ve;
  }
  function i(u) {
    if (Rn(u)) {
      const f = r.get(u);
      f && (r.delete(u), n.splice(n.indexOf(f), 1), f.children.forEach(i), f.alias.forEach(i));
    } else {
      const f = n.indexOf(u);
      f > -1 && (n.splice(f, 1), u.record.name && r.delete(u.record.name), u.children.forEach(i), u.alias.forEach(i));
    }
  }
  function c() {
    return n;
  }
  function l(u) {
    const f = Go(u, n);
    n.splice(f, 0, u), u.record.name && !jt(u) && r.set(u.record.name, u);
  }
  function d(u, f) {
    let h, v = {}, p, g;
    if ("name" in u && u.name) {
      if (h = r.get(u.name), !h)
        throw ue(1, {
          location: u
        });
      if (S.NODE_ENV !== "production") {
        const O = Object.keys(u.params || {}).filter((R) => !h.keys.find((D) => D.name === R));
        O.length && P(`Discarded invalid param(s) "${O.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = h.record.name, v = I(
        // paramsFromLocation is a new object
        Tt(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          h.keys.filter((O) => !O.optional).concat(h.parent ? h.parent.keys.filter((O) => O.optional) : []).map((O) => O.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        u.params && Tt(u.params, h.keys.map((O) => O.name))
      ), p = h.stringify(v);
    } else if (u.path != null)
      p = u.path, S.NODE_ENV !== "production" && !p.startsWith("/") && P(`The Matcher cannot resolve relative paths but received "${p}". Unless you directly called \`matcher.resolve("${p}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), h = n.find((O) => O.re.test(p)), h && (v = h.parse(p), g = h.record.name);
    else {
      if (h = f.name ? r.get(f.name) : n.find((O) => O.re.test(f.path)), !h)
        throw ue(1, {
          location: u,
          currentLocation: f
        });
      g = h.record.name, v = I({}, f.params, u.params), p = h.stringify(v);
    }
    const y = [];
    let _ = h;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: p,
      params: v,
      matched: y,
      meta: Bo(y)
    };
  }
  e.forEach((u) => s(u));
  function a() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: d,
    removeRoute: i,
    clearRoutes: a,
    getRoutes: c,
    getRecordMatcher: o
  };
}
function Tt(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function At(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Fo(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function Fo(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function jt(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Bo(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function $t(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function it(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Lo(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(it.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(it.bind(null, n)))
      return P(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function Wo(e, t) {
  t && t.record.name && !e.name && !e.path && P(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function Uo(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function Ko(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(it.bind(null, n)))
      return P(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function Go(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Pn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = qo(e);
  return o && (r = t.lastIndexOf(o, r - 1), S.NODE_ENV !== "production" && r < 0 && P(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function qo(e) {
  let t = e;
  for (; t = t.parent; )
    if (kn(t) && Pn(e, t) === 0)
      return t;
}
function kn({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Ho(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(gn, " "), i = s.indexOf("="), c = ae(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ae(s.slice(i + 1));
    if (c in t) {
      let d = t[c];
      K(d) || (d = t[c] = [d]), d.push(l);
    } else
      t[c] = l;
  }
  return t;
}
function Ct(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = co(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (K(r) ? r.map((s) => s && rt(s)) : [r && rt(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function zo(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = K(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Jo = Symbol(S.NODE_ENV !== "production" ? "router view location matched" : ""), xt = Symbol(S.NODE_ENV !== "production" ? "router view depth" : ""), De = Symbol(S.NODE_ENV !== "production" ? "router" : ""), ht = Symbol(S.NODE_ENV !== "production" ? "route location" : ""), at = Symbol(S.NODE_ENV !== "production" ? "router view location" : "");
function pe() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function X(e, t, n, r, o, s = (i) => i()) {
  const i = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((c, l) => {
    const d = (f) => {
      f === !1 ? l(ue(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ie(f) ? l(ue(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), c());
    }, a = s(() => e.call(r && r.instances[o], t, n, S.NODE_ENV !== "production" ? Qo(d, t, n) : d));
    let u = Promise.resolve(a);
    if (e.length < 3 && (u = u.then(d)), S.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof a == "object" && "then" in a)
        u = u.then((h) => d._called ? h : (P(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (a !== void 0 && !d._called) {
        P(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    u.catch((f) => l(f));
  });
}
function Qo(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && P(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function He(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    S.NODE_ENV !== "production" && !i.components && !i.children.length && P(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const c in i.components) {
      let l = i.components[c];
      if (S.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw P(`Component "${c}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          P(`Component "${c}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const d = l;
          l = () => d;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, P(`Component "${c}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[c]))
        if (pn(l)) {
          const a = (l.__vccOpts || l)[t];
          a && s.push(X(a, n, r, i, c, o));
        } else {
          let d = l();
          S.NODE_ENV !== "production" && !("catch" in d) && (P(`Component "${c}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), d = Promise.resolve(d)), s.push(() => d.then((a) => {
            if (!a)
              throw new Error(`Couldn't resolve component "${c}" at "${i.path}"`);
            const u = Yr(a) ? a.default : a;
            i.mods[c] = a, i.components[c] = u;
            const h = (u.__vccOpts || u)[t];
            return h && X(h, n, r, i, c, o)();
          }));
        }
    }
  }
  return s;
}
function Dt(e) {
  const t = ee(De), n = ee(ht);
  let r = !1, o = null;
  const s = W(() => {
    const a = L(e.to);
    return S.NODE_ENV !== "production" && (!r || a !== o) && (Ie(a) || (r ? P(`Invalid value for prop "to" in useLink()
- to:`, a, `
- previous to:`, o, `
- props:`, e) : P(`Invalid value for prop "to" in useLink()
- to:`, a, `
- props:`, e)), o = a, r = !0), t.resolve(a);
  }), i = W(() => {
    const { matched: a } = s.value, { length: u } = a, f = a[u - 1], h = n.matched;
    if (!f || !h.length)
      return -1;
    const v = h.findIndex(te.bind(null, f));
    if (v > -1)
      return v;
    const p = Mt(a[u - 2]);
    return (
      // we are dealing with nested routes
      u > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Mt(f) === p && // avoid comparing the child with its parent
      h[h.length - 1].path !== p ? h.findIndex(te.bind(null, a[u - 2])) : v
    );
  }), c = W(() => i.value > -1 && ts(n.params, s.value.params)), l = W(() => i.value > -1 && i.value === n.matched.length - 1 && En(n.params, s.value.params));
  function d(a = {}) {
    if (es(a)) {
      const u = t[L(e.replace) ? "replace" : "push"](
        L(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ve);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => u), u;
    }
    return Promise.resolve();
  }
  if (S.NODE_ENV !== "production" && z) {
    const a = qt();
    if (a) {
      const u = {
        route: s.value,
        isActive: c.value,
        isExactActive: l.value,
        error: null
      };
      a.__vrl_devtools = a.__vrl_devtools || [], a.__vrl_devtools.push(u), Gt(() => {
        u.route = s.value, u.isActive = c.value, u.isExactActive = l.value, u.error = Ie(L(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: W(() => s.value.href),
    isActive: c,
    isExactActive: l,
    navigate: d
  };
}
function Yo(e) {
  return e.length === 1 ? e[0] : e;
}
const Xo = /* @__PURE__ */ F({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Dt,
  setup(e, { slots: t }) {
    const n = Gn(Dt(e)), { options: r } = ee(De), o = W(() => ({
      [Ft(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Ft(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Yo(t.default(n));
      return e.custom ? s : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Zo = Xo;
function es(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function ts(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!K(o) || o.length !== r.length || r.some((s, i) => s !== o[i]))
      return !1;
  }
  return !0;
}
function Mt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Ft = (e, t, n) => e ?? t ?? n, ns = /* @__PURE__ */ F({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    S.NODE_ENV !== "production" && os();
    const r = ee(at), o = W(() => e.route || r.value), s = ee(xt, 0), i = W(() => {
      let d = L(s);
      const { matched: a } = o.value;
      let u;
      for (; (u = a[d]) && !u.components; )
        d++;
      return d;
    }), c = W(() => o.value.matched[i.value]);
    Ve(xt, W(() => i.value + 1)), Ve(Jo, c), Ve(at, o);
    const l = Z();
    return G(() => [l.value, c.value, e.name], ([d, a, u], [f, h, v]) => {
      a && (a.instances[u] = d, h && h !== a && d && d === f && (a.leaveGuards.size || (a.leaveGuards = h.leaveGuards), a.updateGuards.size || (a.updateGuards = h.updateGuards))), d && a && // if there is no instance but to and from are the same this might be
      // the first visit
      (!h || !te(a, h) || !f) && (a.enterCallbacks[u] || []).forEach((p) => p(d));
    }, { flush: "post" }), () => {
      const d = o.value, a = e.name, u = c.value, f = u && u.components[a];
      if (!f)
        return Bt(n.default, { Component: f, route: d });
      const h = u.props[a], v = h ? h === !0 ? d.params : typeof h == "function" ? h(d) : h : null, g = A(f, I({}, v, t, {
        onVnodeUnmounted: (y) => {
          y.component.isUnmounted && (u.instances[a] = null);
        },
        ref: l
      }));
      if (S.NODE_ENV !== "production" && z && g.ref) {
        const y = {
          depth: i.value,
          name: u.name,
          path: u.path,
          meta: u.meta
        };
        (K(g.ref) ? g.ref.map((O) => O.i) : [g.ref.i]).forEach((O) => {
          O.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Bt(n.default, { Component: g, route: d }) || g
      );
    };
  }
});
function Bt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const rs = ns;
function os() {
  const e = qt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    P(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function me(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => ms(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function ke(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let ss = 0;
function is(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = ss++;
  Qr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((a, u) => {
      a.instanceData && a.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: me(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: a, componentInstance: u }) => {
      if (u.__vrv_devtools) {
        const f = u.__vrv_devtools;
        a.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: Vn
        });
      }
      K(u.__vrl_devtools) && (u.__devtoolsApi = o, u.__vrl_devtools.forEach((f) => {
        let h = f.route.path, v = Tn, p = "", g = 0;
        f.error ? (h = f.error, v = fs, g = ds) : f.isExactActive ? (v = In, p = "This is exactly active") : f.isActive && (v = Nn, p = "This link is active"), a.tags.push({
          label: h,
          textColor: g,
          tooltip: p,
          backgroundColor: v
        });
      }));
    }), G(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(c), o.sendInspectorState(c);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((a, u) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: u.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: a },
          groupId: u.meta.__navigationId
        }
      });
    });
    let i = 0;
    t.beforeEach((a, u) => {
      const f = {
        guard: ke("beforeEach"),
        from: me(u, "Current Location during this navigation"),
        to: me(a, "Target location")
      };
      Object.defineProperty(a.meta, "__navigationId", {
        value: i++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: a.fullPath,
          data: f,
          groupId: a.meta.__navigationId
        }
      });
    }), t.afterEach((a, u, f) => {
      const h = {
        guard: ke("afterEach")
      };
      f ? (h.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, h.status = ke("❌")) : h.status = ke("✅"), h.from = me(u, "Current Location during this navigation"), h.to = me(a, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: a.fullPath,
          time: o.now(),
          data: h,
          logType: f ? "warning" : "default",
          groupId: a.meta.__navigationId
        }
      });
    });
    const c = "router-inspector:" + r;
    o.addInspector({
      id: c,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!d)
        return;
      const a = d;
      let u = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      u.forEach($n), a.filter && (u = u.filter((f) => (
        // save matches state based on the payload
        ct(f, a.filter.toLowerCase())
      ))), u.forEach((f) => jn(f, t.currentRoute.value)), a.rootNodes = u.map(An);
    }
    let d;
    o.on.getInspectorTree((a) => {
      d = a, a.app === e && a.inspectorId === c && l();
    }), o.on.getInspectorState((a) => {
      if (a.app === e && a.inspectorId === c) {
        const f = n.getRoutes().find((h) => h.record.__vd_id === a.nodeId);
        f && (a.state = {
          options: cs(f)
        });
      }
    }), o.sendInspectorTree(c), o.sendInspectorState(c);
  });
}
function as(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function cs(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${as(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const Vn = 15485081, Nn = 2450411, In = 8702998, us = 2282478, Tn = 16486972, ls = 6710886, fs = 16704226, ds = 12131356;
function An(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: us
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: Tn
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: Vn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: In
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: Nn
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: ls
  });
  let r = n.__vd_id;
  return r == null && (r = String(hs++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(An)
  };
}
let hs = 0;
const ps = /^\/(.*)\/([a-z]*)$/;
function jn(e, t) {
  const n = t.matched.length && te(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => te(r, e.record))), e.children.forEach((r) => jn(r, t));
}
function $n(e) {
  e.__vd_match = !1, e.children.forEach($n);
}
function ct(e, t) {
  const n = String(e.re).match(ps);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => ct(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ae(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => ct(i, t));
}
function ms(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function gs(e) {
  const t = Mo(e.routes, e), n = e.parseQuery || Ho, r = e.stringifyQuery || Ct, o = e.history;
  if (S.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = pe(), i = pe(), c = pe(), l = J(Y);
  let d = Y;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const a = Ke.bind(null, (m) => "" + m), u = Ke.bind(null, lo), f = (
    // @ts-expect-error: intentionally avoid the type check
    Ke.bind(null, ae)
  );
  function h(m, E) {
    let w, b;
    return Rn(m) ? (w = t.getRecordMatcher(m), S.NODE_ENV !== "production" && !w && P(`Parent route "${String(m)}" not found when adding child route`, E), b = E) : b = m, t.addRoute(b, w);
  }
  function v(m) {
    const E = t.getRecordMatcher(m);
    E ? t.removeRoute(E) : S.NODE_ENV !== "production" && P(`Cannot remove non-existent route "${String(m)}"`);
  }
  function p() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, E) {
    if (E = I({}, E || l.value), typeof m == "string") {
      const k = Ge(n, m, E.path), j = t.resolve({ path: k.path }, E), re = o.createHref(k.fullPath);
      return S.NODE_ENV !== "production" && (re.startsWith("//") ? P(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : j.matched.length || P(`No match found for location with path "${m}"`)), I(k, j, {
        params: f(j.params),
        hash: ae(k.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (S.NODE_ENV !== "production" && !Ie(m))
      return P(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let w;
    if (m.path != null)
      S.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && P(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), w = I({}, m, {
        path: Ge(n, m.path, E.path).path
      });
    else {
      const k = I({}, m.params);
      for (const j in k)
        k[j] == null && delete k[j];
      w = I({}, m, {
        params: u(k)
      }), E.params = u(E.params);
    }
    const b = t.resolve(w, E), T = m.hash || "";
    S.NODE_ENV !== "production" && T && !T.startsWith("#") && P(`A \`hash\` should always start with the character "#". Replace "${T}" with "#${T}".`), b.params = a(f(b.params));
    const $ = po(r, I({}, m, {
      hash: ao(T),
      path: b.path
    })), V = o.createHref($);
    return S.NODE_ENV !== "production" && (V.startsWith("//") ? P(`Location "${m}" resolved to "${V}". A resolved location cannot start with multiple slashes.`) : b.matched.length || P(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: $,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: T,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === Ct ? zo(m.query) : m.query || {}
      )
    }, b, {
      redirectedFrom: void 0,
      href: V
    });
  }
  function _(m) {
    return typeof m == "string" ? Ge(n, m, l.value.path) : I({}, m);
  }
  function O(m, E) {
    if (d !== m)
      return ue(8, {
        from: E,
        to: m
      });
  }
  function R(m) {
    return x(m);
  }
  function D(m) {
    return R(I(_(m), { replace: !0 }));
  }
  function C(m) {
    const E = m.matched[m.matched.length - 1];
    if (E && E.redirect) {
      const { redirect: w } = E;
      let b = typeof w == "function" ? w(m) : w;
      if (typeof b == "string" && (b = b.includes("?") || b.includes("#") ? b = _(b) : (
        // force empty params
        { path: b }
      ), b.params = {}), S.NODE_ENV !== "production" && b.path == null && !("name" in b))
        throw P(`Invalid redirect found:
${JSON.stringify(b, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: b.path != null ? {} : m.params
      }, b);
    }
  }
  function x(m, E) {
    const w = d = y(m), b = l.value, T = m.state, $ = m.force, V = m.replace === !0, k = C(w);
    if (k)
      return x(
        I(_(k), {
          state: typeof k == "object" ? I({}, T, k.state) : T,
          force: $,
          replace: V
        }),
        // keep original redirectedFrom if it exists
        E || w
      );
    const j = w;
    j.redirectedFrom = E;
    let re;
    return !$ && St(r, b, w) && (re = ue(16, { to: j, from: b }), yt(
      b,
      b,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : pt(j, b)).catch((M) => H(M) ? (
      // navigation redirects still mark the router as ready
      H(
        M,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? M : Le(M)
    ) : (
      // reject any unknown error
      Be(M, j, b)
    )).then((M) => {
      if (M) {
        if (H(
          M,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return S.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          St(r, y(M.to), j) && // and we have done it a couple of times
          E && // @ts-expect-error: added only in dev
          (E._count = E._count ? (
            // @ts-expect-error
            E._count + 1
          ) : 1) > 30 ? (P(`Detected a possibly infinite redirection in a navigation guard when going from "${b.fullPath}" to "${j.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : x(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: V
            }, _(M.to), {
              state: typeof M.to == "object" ? I({}, T, M.to.state) : T,
              force: $
            }),
            // preserve the original redirectedFrom if any
            E || j
          );
      } else
        M = gt(j, b, !0, V, T);
      return mt(j, b, M), M;
    });
  }
  function Me(m, E) {
    const w = O(m, E);
    return w ? Promise.reject(w) : Promise.resolve();
  }
  function le(m) {
    const E = Re.values().next().value;
    return E && typeof E.runWithContext == "function" ? E.runWithContext(m) : m();
  }
  function pt(m, E) {
    let w;
    const [b, T, $] = vs(m, E);
    w = He(b.reverse(), "beforeRouteLeave", m, E);
    for (const k of b)
      k.leaveGuards.forEach((j) => {
        w.push(X(j, m, E));
      });
    const V = Me.bind(null, m, E);
    return w.push(V), se(w).then(() => {
      w = [];
      for (const k of s.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).then(() => {
      w = He(T, "beforeRouteUpdate", m, E);
      for (const k of T)
        k.updateGuards.forEach((j) => {
          w.push(X(j, m, E));
        });
      return w.push(V), se(w);
    }).then(() => {
      w = [];
      for (const k of $)
        if (k.beforeEnter)
          if (K(k.beforeEnter))
            for (const j of k.beforeEnter)
              w.push(X(j, m, E));
          else
            w.push(X(k.beforeEnter, m, E));
      return w.push(V), se(w);
    }).then(() => (m.matched.forEach((k) => k.enterCallbacks = {}), w = He($, "beforeRouteEnter", m, E, le), w.push(V), se(w))).then(() => {
      w = [];
      for (const k of i.list())
        w.push(X(k, m, E));
      return w.push(V), se(w);
    }).catch((k) => H(
      k,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? k : Promise.reject(k));
  }
  function mt(m, E, w) {
    c.list().forEach((b) => le(() => b(m, E, w)));
  }
  function gt(m, E, w, b, T) {
    const $ = O(m, E);
    if ($)
      return $;
    const V = E === Y, k = z ? history.state : {};
    w && (b || V ? o.replace(m.fullPath, I({
      scroll: V && k && k.scroll
    }, T)) : o.push(m.fullPath, T)), l.value = m, yt(m, E, w, V), Le();
  }
  let fe;
  function Mn() {
    fe || (fe = o.listen((m, E, w) => {
      if (!wt.listening)
        return;
      const b = y(m), T = C(b);
      if (T) {
        x(I(T, { replace: !0, force: !0 }), b).catch(ve);
        return;
      }
      d = b;
      const $ = l.value;
      z && Eo(Pt($.fullPath, w.delta), xe()), pt(b, $).catch((V) => H(
        V,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? V : H(
        V,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (x(
        I(_(V.to), {
          force: !0
        }),
        b
        // avoid an uncaught rejection, let push call triggerError
      ).then((k) => {
        H(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !w.delta && w.type === ce.pop && o.go(-1, !1);
      }).catch(ve), Promise.reject()) : (w.delta && o.go(-w.delta, !1), Be(V, b, $))).then((V) => {
        V = V || gt(
          // after navigation, all matched components are resolved
          b,
          $,
          !1
        ), V && (w.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !H(
          V,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-w.delta, !1) : w.type === ce.pop && H(
          V,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), mt(b, $, V);
      }).catch(ve);
    }));
  }
  let Fe = pe(), vt = pe(), Se;
  function Be(m, E, w) {
    Le(m);
    const b = vt.list();
    return b.length ? b.forEach((T) => T(m, E, w)) : (S.NODE_ENV !== "production" && P("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Fn() {
    return Se && l.value !== Y ? Promise.resolve() : new Promise((m, E) => {
      Fe.add([m, E]);
    });
  }
  function Le(m) {
    return Se || (Se = !m, Mn(), Fe.list().forEach(([E, w]) => m ? w(m) : E()), Fe.reset()), m;
  }
  function yt(m, E, w, b) {
    const { scrollBehavior: T } = e;
    if (!z || !T)
      return Promise.resolve();
    const $ = !w && _o(Pt(m.fullPath, 0)) || (b || !w) && history.state && history.state.scroll || null;
    return Ne().then(() => T(m, E, $)).then((V) => V && wo(V)).catch((V) => Be(V, m, E));
  }
  const We = (m) => o.go(m);
  let Ue;
  const Re = /* @__PURE__ */ new Set(), wt = {
    currentRoute: l,
    listening: !0,
    addRoute: h,
    removeRoute: v,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: p,
    resolve: y,
    options: e,
    push: R,
    replace: D,
    go: We,
    back: () => We(-1),
    forward: () => We(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: c.add,
    onError: vt.add,
    isReady: Fn,
    install(m) {
      const E = this;
      m.component("RouterLink", Zo), m.component("RouterView", rs), m.config.globalProperties.$router = E, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => L(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !Ue && l.value === Y && (Ue = !0, R(o.location).catch((T) => {
        S.NODE_ENV !== "production" && P("Unexpected error when starting the router:", T);
      }));
      const w = {};
      for (const T in Y)
        Object.defineProperty(w, T, {
          get: () => l.value[T],
          enumerable: !0
        });
      m.provide(De, E), m.provide(ht, Kn(w)), m.provide(at, l);
      const b = m.unmount;
      Re.add(m), m.unmount = function() {
        Re.delete(m), Re.size < 1 && (d = Y, fe && fe(), fe = null, l.value = Y, Ue = !1, Se = !1), b();
      }, S.NODE_ENV !== "production" && z && is(m, E, t);
    }
  };
  function se(m) {
    return m.reduce((E, w) => E.then(() => le(w)), Promise.resolve());
  }
  return wt;
}
function vs(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const c = t.matched[i];
    c && (e.matched.find((d) => te(d, c)) ? r.push(c) : n.push(c));
    const l = e.matched[i];
    l && (t.matched.find((d) => te(d, l)) || o.push(l));
  }
  return [n, r, o];
}
function ys() {
  return ee(De);
}
function ws(e) {
  return ee(ht);
}
function ne(e) {
  let t = on(), n = Tr(), r = Dr(e), o = cn(), s = ys(), i = ws();
  function c(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return q(d(p));
    if (N.isVForItem(p))
      return Fr(p.fid) ? r.getVForIndex(p.fid) : q(d(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJs(p)) {
      const { code: g, bind: y } = p, _ = Ee(y, (O) => a(O));
      return Wr(g, _)();
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return q(d(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function d(p) {
    if (N.isVar(p)) {
      const g = t.getVueRef(p) || Sr(p);
      return _t(g, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Mr({
        binding: p,
        snapshot: v
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: g = "params" } = p;
      return _t(() => i[g], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function a(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return d(p);
    if (N.isVForIndex(p))
      return l(p);
    if (N.isJs(p))
      return null;
    if (N.isRouterParams(p))
      return d(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function u(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJs(p))
      return null;
  }
  function f(p) {
    var g, y;
    (g = p.vars) == null || g.forEach((_) => {
      d({ type: "var", ..._ }).value = _.val;
    }), (y = p.ele_refs) == null || y.forEach((_) => {
      o.getRef({
        sid: _.sid,
        id: _.id
      }).value[_.method](..._.args);
    });
  }
  function h(p, g) {
    if (Ot(g) || Ot(p.values))
      return;
    g = g;
    const y = p.values, _ = p.skips || new Array(g.length).fill(0);
    g.forEach((O, R) => {
      if (_[R] === 1)
        return;
      if (N.isVar(O)) {
        const C = d(O);
        C.value = y[R];
        return;
      }
      if (N.isRouterAction(O)) {
        const C = y[R], x = s[C.fn];
        x(...C.args);
        return;
      }
      if (N.isElementRef(O)) {
        const C = o.getRef(O).value, x = y[R], { method: Me, args: le = [] } = x;
        C[Me](...le);
        return;
      }
      if (N.isJsOutput(O)) {
        const C = y[R], x = U(C);
        typeof x == "function" && x();
        return;
      }
      const D = d(O);
      D.value = y[R];
    });
  }
  const v = {
    getVForIndex: r.getVForIndex,
    getObjectToValue: l,
    getVueRefObject: d,
    getVueRefObjectOrValue: a,
    getBindingServerInfo: u,
    updateRefFromServer: f,
    updateOutputsRefFromServer: h,
    replaceSnapshot: c
  };
  return v;
}
function Es(e, t) {
  const {
    on: n,
    code: r,
    immediate: o,
    deep: s,
    once: i,
    flush: c,
    bind: l = {},
    onData: d,
    bindData: a
  } = e, u = d || new Array(n.length).fill(0), f = a || new Array(Object.keys(l).length).fill(0), h = Ee(
    l,
    (g, y, _) => f[_] === 0 ? t.getVueRefObject(g) : g
  ), v = U(r, h), p = n.length === 1 ? Lt(u[0] === 1, n[0], t) : n.map(
    (g, y) => Lt(u[y] === 1, g, t)
  );
  return G(p, v, { immediate: o, deep: s, once: i, flush: c });
}
function Lt(e, t, n) {
  return e ? () => t : n.getVueRefObject(t);
}
function _s(e, t) {
  const {
    inputs: n = [],
    outputs: r,
    slient: o,
    data: s,
    code: i,
    immediate: c = !0,
    deep: l,
    once: d,
    flush: a
  } = e, u = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), h = U(i), v = n.filter((g, y) => u[y] === 0 && f[y] === 0).map((g) => t.getVueRefObject(g));
  function p() {
    return n.map((g, y) => f[y] === 0 ? Zt(q(t.getVueRefObject(g))) : g);
  }
  G(
    v,
    () => {
      let g = h(...p());
      if (!r)
        return;
      const _ = r.length === 1 ? [g] : g, O = _.map((R) => R === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer(
        { values: _, skips: O },
        r
      );
    },
    { immediate: c, deep: l, once: d, flush: a }
  );
}
function Os(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((c) => {
        if (c.type === "web") {
          const l = bs(c.bind, t);
          return Ss(c, l, t);
        } else {
          if (c.type === "vue")
            return Ps(c, t);
          if (c.type === "js")
            return Rs(c, t);
        }
        throw new Error(`unknown event type ${c}`);
      }), i = U(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...c) => o.map(async (l) => {
            await l(...c);
          })
        }
      );
      return { [n]: i };
    })
  );
}
function bs(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return U(o)(...n);
      }
      return _e(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function Ss(e, t, n) {
  async function r(...o) {
    const s = t(...o), i = await nn().eventSend(e, s);
    i && n.updateOutputsRefFromServer(i, e.set);
  }
  return r;
}
function Rs(e, t) {
  const { code: n, inputs: r = [], set: o } = e, s = U(n);
  function i(...c) {
    const l = (r ?? []).map((a) => {
      if (N.isEventContext(a)) {
        if (a.path.startsWith(":")) {
          const u = a.path.slice(1);
          return U(u)(...c);
        }
        return _e(c[0], a.path.split("."));
      }
      return N.IsBinding(a) ? Zt(t.getObjectToValue(a)) : a;
    }), d = s(...l);
    if (o !== void 0) {
      const u = o.length === 1 ? [d] : d, f = u.map((h) => h === void 0 ? 1 : 0);
      t.updateOutputsRefFromServer({ values: u, skips: f }, o);
    }
  }
  return i;
}
function Ps(e, t) {
  const { code: n, bind: r = {}, bindData: o } = e, s = o || new Array(Object.keys(r).length).fill(0), i = Ee(
    r,
    (d, a, u) => s[u] === 0 ? t.getVueRefObject(d) : d
  ), c = U(n, i);
  function l(...d) {
    c(...d);
  }
  return l;
}
function ks(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      Ee(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = qn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Vs(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return ze(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    Ee(
      o,
      (c) => t.getObjectToValue(c)
    )
  ), s && i.push(...s.map((c) => t.getObjectToValue(c))), ze(i);
}
function Ns(e, t) {
  var r;
  const n = {};
  return Et(e.bProps || {}, (o, s) => {
    n[s] = Is(t.getObjectToValue(o), s);
  }), (r = e.proxyProps) == null || r.forEach((o) => {
    const s = t.getObjectToValue(o);
    typeof s == "object" && Et(s, (i, c) => {
      n[c] = i;
    });
  }), { ...e.props || {}, ...n };
}
function Is(e, t) {
  return t === "innerText" ? Ht(e) : e;
}
function Ts(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Vr(n);
  return je(() => {
    Ir(n);
  }), () => {
    const s = e.propsValue;
    return Nr(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A($e, null, t.default());
  };
}
const As = F(Ts, {
  props: ["propsInfo", "propsValue"]
});
function js(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ge(n) : () => ge(n) : Qt(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: c } = i;
    return (l) => {
      if (i.scope) {
        const d = () => i.props ? Wt(i.props, l, c) : ge(c);
        return A(be, { scope: i.scope }, d);
      }
      return i.props ? Wt(i.props, l, c) : ge(c);
    };
  } });
}
function Wt(e, t, n) {
  return A(
    As,
    { propsInfo: e, propsValue: t },
    () => ge(n)
  );
}
function ge(e) {
  const t = (e ?? []).map((n) => A(Q, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function $s(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: c, value: l, mf: d } = o;
    if (i === "vmodel") {
      const a = t.getVueRefObject(l);
      if (n[`onUpdate:${c}`] = (u) => {
        a.value = u;
      }, s === 1) {
        const u = d ? Object.fromEntries(d.map((f) => [f, !0])) : {};
        r.push([Hn, a.value, void 0, u]);
      } else
        n[c] = a.value;
    } else if (i === "vshow") {
      const a = t.getVueRefObject(l);
      r.push([zn, a.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function Cs(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function xs(e) {
  const t = ne(), n = cn();
  return () => {
    const { tag: r } = e.component, o = N.IsBinding(r) ? t.getObjectToValue(r) : r, s = ut(o), i = typeof s == "string", c = Vs(e.component, t), { styles: l, hasStyle: d } = ks(e.component, t), a = Os(e.component.events ?? {}, t), u = js(e.component, i), f = Ns(e.component, t), { newProps: h, directiveArray: v } = $s(
      e.component.dir,
      t
    ), p = Cs(
      e.component,
      n
    ), g = Jn({
      ...f,
      ...a,
      ...h,
      ...p
    }) || {};
    d && (g.style = l), c && (g.class = c);
    const y = A(s, { ...g }, u);
    return v.length > 0 ? Qn(
      // @ts-ignore
      y,
      v
    ) : y;
  };
}
const Q = F(xs, {
  props: ["component"]
});
function Cn(e, t) {
  var n, r;
  if (e) {
    const o = Pr(e), s = rn(e, ne(t)), i = ne(t);
    yr(e.py_watch, e.web_computed, i), (n = e.vue_watch) == null || n.forEach((c) => Es(c, i)), (r = e.js_watch) == null || r.forEach((c) => _s(c, i)), je(() => {
      an(e.id, s), kr(e.id, o);
    });
  }
}
function Ds(e, { slots: t }) {
  const { scope: n } = e;
  return Cn(n), () => A($e, null, t.default());
}
const be = F(Ds, {
  props: ["scope"]
}), Ms = F(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Ar(r), Cn(t, r.key), n.length === 1 ? () => A(Q, {
      component: n[0]
    }) : () => n.map(
      (s) => A(Q, {
        component: s
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Fs(e, t) {
  const { state: n, isReady: r, isLoading: o } = cr(async () => {
    let s = e;
    const i = t;
    if (!s && !i)
      throw new Error("Either config or configUrl must be provided");
    if (!s && i && (s = await (await fetch(i)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Bs(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Ls = { class: "app-box" }, Ws = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Us = /* @__PURE__ */ F({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = Fs(
      t.config,
      t.configUrl
    );
    let o = null;
    return G(n, (s) => {
      o = s, s.url && (or({
        mode: s.mode,
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params,
        webServerInfo: s.webInfo
      }), mr(s));
    }), Yn(Bs), (s, i) => (de(), Pe("div", Ls, [
      L(r) ? (de(), Pe("div", Ws, i[0] || (i[0] = [
        Xn("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (de(), Pe("div", {
        key: 1,
        class: ze(["insta-main", L(n).class])
      }, [
        Zn(L(be), {
          scope: L(o).scope
        }, {
          default: er(() => [
            (de(!0), Pe($e, null, tr(L(o).items, (c) => (de(), nr(L(Q), { component: c }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
});
function Ks(e) {
  const { on: t, scope: n, items: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t);
    return A(be, { scope: n }, () => s ? r.map(
      (c) => A(Q, { component: c })
    ) : void 0);
  };
}
const Gs = F(Ks, {
  props: ["on", "scope", "items"]
});
function qs(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
function Hs(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scope: i, num: c, tsGroup: l = {} } = e, d = t === void 0, a = c !== void 0, u = d ? n : t, f = ne();
  $r(s, u, d, a);
  const v = Xs(o ?? "index");
  return je(() => {
    Rr(i.id);
  }), () => {
    const p = Js(
      a,
      d,
      u,
      f,
      c
    ), g = xr(s), y = p.map((_, O) => {
      const R = v(_, O);
      return g.add(R), Cr(s, R, O), A(Ms, {
        scope: e.scope,
        items: r,
        vforInfo: {
          fid: s,
          key: R
        },
        key: R
      });
    });
    return g.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(zt, l, {
      default: () => y
    }) : y;
  };
}
const zs = F(Hs, {
  props: ["array", "items", "fid", "bArray", "scope", "num", "fkey", "tsGroup"]
});
function Js(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, qs({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const Qs = (e) => e, Ys = (e, t) => t;
function Xs(e) {
  const t = ur(e);
  return typeof t == "function" ? t : e === "item" ? Qs : Ys;
}
function Zs(e) {
  return e.map((n) => {
    if (n.tag)
      return A(Q, { component: n });
    const r = ut(xn);
    return A(r, {
      scope: n
    });
  });
}
const xn = F(
  (e) => {
    const t = e.scope;
    return () => Zs(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function ei(e) {
  return e.map((t) => {
    if (t.tag)
      return A(Q, { component: t });
    const n = ut(xn);
    return A(n, {
      scope: t
    });
  });
}
const ti = F(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = J(r), s = rn(t), i = ne();
    return Te.createDynamicWatchRefresh(n, i, async () => {
      const { items: c, on: l } = await Te.fetchRemote(e, i);
      return o.value = c, l;
    }), je(() => {
      an(t.id, s);
    }), () => ei(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var Te;
((e) => {
  function t(r, o, s) {
    let i = null, c = r, l = c.map((a) => o.getVueRefObject(a));
    function d() {
      i && i(), i = G(
        l,
        async () => {
          c = await s(), l = c.map((a) => o.getVueRefObject(a)), d();
        },
        { deep: !0 }
      );
    }
    return d(), () => {
      i && i();
    };
  }
  e.createDynamicWatchRefresh = t;
  async function n(r, o) {
    const s = Object.values(r.bind).map((a) => ({
      sid: a.sid,
      id: a.id,
      value: o.getObjectToValue(a)
    })), i = {
      sid: r.sid,
      bind: s,
      hKey: r.hKey,
      page: ye()
    }, c = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(i)
    }, l = await fetch(r.url, c);
    if (!l.ok)
      throw new Error("Failed to fetch data");
    return await l.json();
  }
  e.fetchRemote = n;
})(Te || (Te = {}));
function ni(e) {
  const { scope: t, items: n } = e;
  return () => {
    const r = n.map((o) => A(Q, { component: o }));
    return A(be, { scope: t }, () => r);
  };
}
const Ut = F(ni, {
  props: ["scope", "items"]
});
function ri(e) {
  const { on: t, case: n, default: r } = e, o = ne();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((c) => {
      const { value: l, items: d, scope: a } = c.props;
      if (s === l)
        return A(Ut, {
          scope: a,
          items: d,
          key: ["case", l].join("-")
        });
    }).filter((c) => c);
    if (r && !i.length) {
      const { items: c, scope: l } = r.props;
      i.push(A(Ut, { scope: l, items: c, key: "default" }));
    }
    return A($e, i);
  };
}
const oi = F(ri, {
  props: ["case", "on", "default"]
});
function si(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    zt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const ii = F(si, {
  props: ["name", "tag"]
});
function ai(e) {
  const { content: t, r: n = 0 } = e, r = ne(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Ht(o());
}
const ci = F(ai, {
  props: ["content", "r"]
});
function ui(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Dn(o, n)
  );
}
function Dn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scope: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(li(r, o, t));
  }, i = (l = r.children) == null ? void 0 : l.map(
    (d) => Dn(d, t)
  ), c = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete c.component, i === void 0 && delete c.children, c;
}
function li(e, t, n) {
  const { path: r, component: o } = e, s = A(
    be,
    { scope: t, key: r },
    () => o.map((c) => A(Q, { component: c }))
  );
  return n ? A(rr, null, () => s) : s;
}
function fi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? Po() : n === "memory" ? Ro() : Sn();
  e.use(
    gs({
      history: r,
      routes: ui(t)
    })
  );
}
function pi(e, t) {
  e.component("insta-ui", Us), e.component("vif", Gs), e.component("vfor", zs), e.component("match", oi), e.component("refresh", ti), e.component("ts-group", ii), e.component("content", ci), t.router && fi(e, t);
}
export {
  pi as default
};
//# sourceMappingURL=insta-ui.js.map
