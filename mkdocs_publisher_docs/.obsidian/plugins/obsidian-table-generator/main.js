"use strict";
var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => {
  __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
  return value;
};
const obsidian = require("obsidian");
function noop() {
}
function assign(tar, src) {
  for (const k in src)
    tar[k] = src[k];
  return tar;
}
function add_location(element2, file2, line, column, char) {
  element2.__svelte_meta = {
    loc: { file: file2, line, column, char }
  };
}
function run(fn) {
  return fn();
}
function blank_object() {
  return /* @__PURE__ */ Object.create(null);
}
function run_all(fns) {
  fns.forEach(run);
}
function is_function(thing) {
  return typeof thing === "function";
}
function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || (a && typeof a === "object" || typeof a === "function");
}
function is_empty(obj) {
  return Object.keys(obj).length === 0;
}
function create_slot(definition, ctx, $$scope, fn) {
  if (definition) {
    const slot_ctx = get_slot_context(definition, ctx, $$scope, fn);
    return definition[0](slot_ctx);
  }
}
function get_slot_context(definition, ctx, $$scope, fn) {
  return definition[1] && fn ? assign($$scope.ctx.slice(), definition[1](fn(ctx))) : $$scope.ctx;
}
function get_slot_changes(definition, $$scope, dirty, fn) {
  if (definition[2] && fn) {
    const lets = definition[2](fn(dirty));
    if ($$scope.dirty === void 0) {
      return lets;
    }
    if (typeof lets === "object") {
      const merged = [];
      const len = Math.max($$scope.dirty.length, lets.length);
      for (let i = 0; i < len; i += 1) {
        merged[i] = $$scope.dirty[i] | lets[i];
      }
      return merged;
    }
    return $$scope.dirty | lets;
  }
  return $$scope.dirty;
}
function update_slot_base(slot, slot_definition, ctx, $$scope, slot_changes, get_slot_context_fn) {
  if (slot_changes) {
    const slot_context = get_slot_context(slot_definition, ctx, $$scope, get_slot_context_fn);
    slot.p(slot_context, slot_changes);
  }
}
function get_all_dirty_from_scope($$scope) {
  if ($$scope.ctx.length > 32) {
    const dirty = [];
    const length = $$scope.ctx.length / 32;
    for (let i = 0; i < length; i++) {
      dirty[i] = -1;
    }
    return dirty;
  }
  return -1;
}
function append(target, node) {
  target.appendChild(node);
}
function insert(target, node, anchor) {
  target.insertBefore(node, anchor || null);
}
function detach(node) {
  node.parentNode.removeChild(node);
}
function element(name) {
  return document.createElement(name);
}
function text(data) {
  return document.createTextNode(data);
}
function space() {
  return text(" ");
}
function empty() {
  return text("");
}
function listen(node, event, handler, options) {
  node.addEventListener(event, handler, options);
  return () => node.removeEventListener(event, handler, options);
}
function attr(node, attribute, value) {
  if (value == null)
    node.removeAttribute(attribute);
  else if (node.getAttribute(attribute) !== value)
    node.setAttribute(attribute, value);
}
function children(element2) {
  return Array.from(element2.childNodes);
}
function set_input_value(input, value) {
  input.value = value == null ? "" : value;
}
function set_style(node, key, value, important) {
  if (value === null) {
    node.style.removeProperty(key);
  } else {
    node.style.setProperty(key, value, important ? "important" : "");
  }
}
function toggle_class(element2, name, toggle) {
  element2.classList[toggle ? "add" : "remove"](name);
}
function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
  const e = document.createEvent("CustomEvent");
  e.initCustomEvent(type, bubbles, cancelable, detail);
  return e;
}
let current_component;
function set_current_component(component) {
  current_component = component;
}
function get_current_component() {
  if (!current_component)
    throw new Error("Function called outside component initialization");
  return current_component;
}
function onMount(fn) {
  get_current_component().$$.on_mount.push(fn);
}
function createEventDispatcher() {
  const component = get_current_component();
  return (type, detail, { cancelable = false } = {}) => {
    const callbacks = component.$$.callbacks[type];
    if (callbacks) {
      const event = custom_event(type, detail, { cancelable });
      callbacks.slice().forEach((fn) => {
        fn.call(component, event);
      });
      return !event.defaultPrevented;
    }
    return true;
  };
}
const dirty_components = [];
const binding_callbacks = [];
const render_callbacks = [];
const flush_callbacks = [];
const resolved_promise = Promise.resolve();
let update_scheduled = false;
function schedule_update() {
  if (!update_scheduled) {
    update_scheduled = true;
    resolved_promise.then(flush);
  }
}
function add_render_callback(fn) {
  render_callbacks.push(fn);
}
function add_flush_callback(fn) {
  flush_callbacks.push(fn);
}
const seen_callbacks = /* @__PURE__ */ new Set();
let flushidx = 0;
function flush() {
  const saved_component = current_component;
  do {
    while (flushidx < dirty_components.length) {
      const component = dirty_components[flushidx];
      flushidx++;
      set_current_component(component);
      update(component.$$);
    }
    set_current_component(null);
    dirty_components.length = 0;
    flushidx = 0;
    while (binding_callbacks.length)
      binding_callbacks.pop()();
    for (let i = 0; i < render_callbacks.length; i += 1) {
      const callback = render_callbacks[i];
      if (!seen_callbacks.has(callback)) {
        seen_callbacks.add(callback);
        callback();
      }
    }
    render_callbacks.length = 0;
  } while (dirty_components.length);
  while (flush_callbacks.length) {
    flush_callbacks.pop()();
  }
  update_scheduled = false;
  seen_callbacks.clear();
  set_current_component(saved_component);
}
function update($$) {
  if ($$.fragment !== null) {
    $$.update();
    run_all($$.before_update);
    const dirty = $$.dirty;
    $$.dirty = [-1];
    $$.fragment && $$.fragment.p($$.ctx, dirty);
    $$.after_update.forEach(add_render_callback);
  }
}
const outroing = /* @__PURE__ */ new Set();
let outros;
function transition_in(block, local) {
  if (block && block.i) {
    outroing.delete(block);
    block.i(local);
  }
}
function transition_out(block, local, detach2, callback) {
  if (block && block.o) {
    if (outroing.has(block))
      return;
    outroing.add(block);
    outros.c.push(() => {
      outroing.delete(block);
      if (callback) {
        if (detach2)
          block.d(1);
        callback();
      }
    });
    block.o(local);
  } else if (callback) {
    callback();
  }
}
const globals = typeof window !== "undefined" ? window : typeof globalThis !== "undefined" ? globalThis : global;
function destroy_block(block, lookup) {
  block.d(1);
  lookup.delete(block.key);
}
function update_keyed_each(old_blocks, dirty, get_key, dynamic, ctx, list, lookup, node, destroy, create_each_block2, next, get_context) {
  let o = old_blocks.length;
  let n = list.length;
  let i = o;
  const old_indexes = {};
  while (i--)
    old_indexes[old_blocks[i].key] = i;
  const new_blocks = [];
  const new_lookup = /* @__PURE__ */ new Map();
  const deltas = /* @__PURE__ */ new Map();
  i = n;
  while (i--) {
    const child_ctx = get_context(ctx, list, i);
    const key = get_key(child_ctx);
    let block = lookup.get(key);
    if (!block) {
      block = create_each_block2(key, child_ctx);
      block.c();
    } else if (dynamic) {
      block.p(child_ctx, dirty);
    }
    new_lookup.set(key, new_blocks[i] = block);
    if (key in old_indexes)
      deltas.set(key, Math.abs(i - old_indexes[key]));
  }
  const will_move = /* @__PURE__ */ new Set();
  const did_move = /* @__PURE__ */ new Set();
  function insert2(block) {
    transition_in(block, 1);
    block.m(node, next);
    lookup.set(block.key, block);
    next = block.first;
    n--;
  }
  while (o && n) {
    const new_block = new_blocks[n - 1];
    const old_block = old_blocks[o - 1];
    const new_key = new_block.key;
    const old_key = old_block.key;
    if (new_block === old_block) {
      next = new_block.first;
      o--;
      n--;
    } else if (!new_lookup.has(old_key)) {
      destroy(old_block, lookup);
      o--;
    } else if (!lookup.has(new_key) || will_move.has(new_key)) {
      insert2(new_block);
    } else if (did_move.has(old_key)) {
      o--;
    } else if (deltas.get(new_key) > deltas.get(old_key)) {
      did_move.add(new_key);
      insert2(new_block);
    } else {
      will_move.add(old_key);
      o--;
    }
  }
  while (o--) {
    const old_block = old_blocks[o];
    if (!new_lookup.has(old_block.key))
      destroy(old_block, lookup);
  }
  while (n)
    insert2(new_blocks[n - 1]);
  return new_blocks;
}
function validate_each_keys(ctx, list, get_context, get_key) {
  const keys = /* @__PURE__ */ new Set();
  for (let i = 0; i < list.length; i++) {
    const key = get_key(get_context(ctx, list, i));
    if (keys.has(key)) {
      throw new Error("Cannot have duplicate keys in a keyed each");
    }
    keys.add(key);
  }
}
function bind(component, name, callback) {
  const index = component.$$.props[name];
  if (index !== void 0) {
    component.$$.bound[index] = callback;
    callback(component.$$.ctx[index]);
  }
}
function create_component(block) {
  block && block.c();
}
function mount_component(component, target, anchor, customElement) {
  const { fragment, on_mount, on_destroy, after_update } = component.$$;
  fragment && fragment.m(target, anchor);
  if (!customElement) {
    add_render_callback(() => {
      const new_on_destroy = on_mount.map(run).filter(is_function);
      if (on_destroy) {
        on_destroy.push(...new_on_destroy);
      } else {
        run_all(new_on_destroy);
      }
      component.$$.on_mount = [];
    });
  }
  after_update.forEach(add_render_callback);
}
function destroy_component(component, detaching) {
  const $$ = component.$$;
  if ($$.fragment !== null) {
    run_all($$.on_destroy);
    $$.fragment && $$.fragment.d(detaching);
    $$.on_destroy = $$.fragment = null;
    $$.ctx = [];
  }
}
function make_dirty(component, i) {
  if (component.$$.dirty[0] === -1) {
    dirty_components.push(component);
    schedule_update();
    component.$$.dirty.fill(0);
  }
  component.$$.dirty[i / 31 | 0] |= 1 << i % 31;
}
function init(component, options, instance2, create_fragment2, not_equal, props, append_styles, dirty = [-1]) {
  const parent_component = current_component;
  set_current_component(component);
  const $$ = component.$$ = {
    fragment: null,
    ctx: null,
    props,
    update: noop,
    not_equal,
    bound: blank_object(),
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
    callbacks: blank_object(),
    dirty,
    skip_bound: false,
    root: options.target || parent_component.$$.root
  };
  append_styles && append_styles($$.root);
  let ready = false;
  $$.ctx = instance2 ? instance2(component, options.props || {}, (i, ret, ...rest) => {
    const value = rest.length ? rest[0] : ret;
    if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
      if (!$$.skip_bound && $$.bound[i])
        $$.bound[i](value);
      if (ready)
        make_dirty(component, i);
    }
    return ret;
  }) : [];
  $$.update();
  ready = true;
  run_all($$.before_update);
  $$.fragment = create_fragment2 ? create_fragment2($$.ctx) : false;
  if (options.target) {
    if (options.hydrate) {
      const nodes = children(options.target);
      $$.fragment && $$.fragment.l(nodes);
      nodes.forEach(detach);
    } else {
      $$.fragment && $$.fragment.c();
    }
    if (options.intro)
      transition_in(component.$$.fragment);
    mount_component(component, options.target, options.anchor, options.customElement);
    flush();
  }
  set_current_component(parent_component);
}
class SvelteComponent {
  $destroy() {
    destroy_component(this, 1);
    this.$destroy = noop;
  }
  $on(type, callback) {
    const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
    callbacks.push(callback);
    return () => {
      const index = callbacks.indexOf(callback);
      if (index !== -1)
        callbacks.splice(index, 1);
    };
  }
  $set($$props) {
    if (this.$$set && !is_empty($$props)) {
      this.$$.skip_bound = true;
      this.$$set($$props);
      this.$$.skip_bound = false;
    }
  }
}
function dispatch_dev(type, detail) {
  document.dispatchEvent(custom_event(type, Object.assign({ version: "3.50.1" }, detail), { bubbles: true }));
}
function append_dev(target, node) {
  dispatch_dev("SvelteDOMInsert", { target, node });
  append(target, node);
}
function insert_dev(target, node, anchor) {
  dispatch_dev("SvelteDOMInsert", { target, node, anchor });
  insert(target, node, anchor);
}
function detach_dev(node) {
  dispatch_dev("SvelteDOMRemove", { node });
  detach(node);
}
function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation) {
  const modifiers = options === true ? ["capture"] : options ? Array.from(Object.keys(options)) : [];
  if (has_prevent_default)
    modifiers.push("preventDefault");
  if (has_stop_propagation)
    modifiers.push("stopPropagation");
  dispatch_dev("SvelteDOMAddEventListener", { node, event, handler, modifiers });
  const dispose = listen(node, event, handler, options);
  return () => {
    dispatch_dev("SvelteDOMRemoveEventListener", { node, event, handler, modifiers });
    dispose();
  };
}
function attr_dev(node, attribute, value) {
  attr(node, attribute, value);
  if (value == null)
    dispatch_dev("SvelteDOMRemoveAttribute", { node, attribute });
  else
    dispatch_dev("SvelteDOMSetAttribute", { node, attribute, value });
}
function set_data_dev(text2, data) {
  data = "" + data;
  if (text2.wholeText === data)
    return;
  dispatch_dev("SvelteDOMSetData", { node: text2, data });
  text2.data = data;
}
function validate_each_argument(arg) {
  if (typeof arg !== "string" && !(arg && typeof arg === "object" && "length" in arg)) {
    let msg = "{#each} only iterates over array-like objects.";
    if (typeof Symbol === "function" && arg && Symbol.iterator in arg) {
      msg += " You can use a spread to convert this iterable into an array.";
    }
    throw new Error(msg);
  }
}
function validate_slots(name, slot, keys) {
  for (const slot_key of Object.keys(slot)) {
    if (!~keys.indexOf(slot_key)) {
      console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
    }
  }
}
class SvelteComponentDev extends SvelteComponent {
  constructor(options) {
    if (!options || !options.target && !options.$$inline) {
      throw new Error("'target' is a required option");
    }
    super();
  }
  $destroy() {
    super.$destroy();
    this.$destroy = () => {
      console.warn("Component was already destroyed");
    };
  }
  $capture_state() {
  }
  $inject_state() {
  }
}
function __awaiter(thisArg, _arguments, P, generator) {
  function adopt(value) {
    return value instanceof P ? value : new P(function(resolve) {
      resolve(value);
    });
  }
  return new (P || (P = Promise))(function(resolve, reject) {
    function fulfilled(value) {
      try {
        step(generator.next(value));
      } catch (e) {
        reject(e);
      }
    }
    function rejected(value) {
      try {
        step(generator["throw"](value));
      } catch (e) {
        reject(e);
      }
    }
    function step(result) {
      result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected);
    }
    step((generator = generator.apply(thisArg, _arguments || [])).next());
  });
}
const Table_svelte_svelte_type_style_lang = "";
const file$3 = "E:/obdev/.obsidian/plugins/Obsidian-Table-Generator/src/ui/basic/Table.svelte";
function get_each_context$1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[20] = list[i];
  child_ctx[22] = i;
  return child_ctx;
}
function get_each_context_1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[20] = list[i];
  child_ctx[24] = i;
  return child_ctx;
}
function create_each_block_1(key_1, ctx) {
  let div;
  let mounted;
  let dispose;
  function mouseenter_handler() {
    return ctx[12](ctx[22], ctx[24]);
  }
  function click_handler() {
    return ctx[13](ctx[22], ctx[24]);
  }
  const block = {
    key: key_1,
    first: null,
    c: function create() {
      div = element("div");
      attr_dev(div, "class", "table-generator-cell s-VU35bhriycJk");
      toggle_class(div, "active", ctx[0][ctx[22]][ctx[24]]);
      add_location(div, file$3, 43, 12, 1276);
      this.first = div;
    },
    m: function mount(target, anchor) {
      insert_dev(target, div, anchor);
      if (!mounted) {
        dispose = [
          listen_dev(div, "mouseenter", mouseenter_handler, false, false, false),
          listen_dev(div, "click", click_handler, false, false, false)
        ];
        mounted = true;
      }
    },
    p: function update2(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & 9) {
        toggle_class(div, "active", ctx[0][ctx[22]][ctx[24]]);
      }
    },
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div);
      mounted = false;
      run_all(dispose);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_each_block_1.name,
    type: "each",
    source: "(43:8) {#each {length: grid[1]} as _, j (j)}",
    ctx
  });
  return block;
}
function create_each_block$1(key_1, ctx) {
  let first;
  let each_blocks = [];
  let each_1_lookup = /* @__PURE__ */ new Map();
  let each_1_anchor;
  let each_value_1 = { length: ctx[3][1] };
  validate_each_argument(each_value_1);
  const get_key = (ctx2) => ctx2[24];
  validate_each_keys(ctx, each_value_1, get_each_context_1, get_key);
  for (let i = 0; i < each_value_1.length; i += 1) {
    let child_ctx = get_each_context_1(ctx, each_value_1, i);
    let key = get_key(child_ctx);
    each_1_lookup.set(key, each_blocks[i] = create_each_block_1(key, child_ctx));
  }
  const block = {
    key: key_1,
    first: null,
    c: function create() {
      first = empty();
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      each_1_anchor = empty();
      this.first = first;
    },
    m: function mount(target, anchor) {
      insert_dev(target, first, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].m(target, anchor);
      }
      insert_dev(target, each_1_anchor, anchor);
    },
    p: function update2(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & 89) {
        each_value_1 = { length: ctx[3][1] };
        validate_each_argument(each_value_1);
        validate_each_keys(ctx, each_value_1, get_each_context_1, get_key);
        each_blocks = update_keyed_each(each_blocks, dirty, get_key, 1, ctx, each_value_1, each_1_lookup, each_1_anchor.parentNode, destroy_block, create_each_block_1, each_1_anchor, get_each_context_1);
      }
    },
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(first);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].d(detaching);
      }
      if (detaching)
        detach_dev(each_1_anchor);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_each_block$1.name,
    type: "each",
    source: "(42:4) {#each {length: grid[0]} as _, i (i)}",
    ctx
  });
  return block;
}
function create_fragment$5(ctx) {
  let div;
  let each_blocks = [];
  let each_1_lookup = /* @__PURE__ */ new Map();
  let mounted;
  let dispose;
  let each_value = { length: ctx[3][0] };
  validate_each_argument(each_value);
  const get_key = (ctx2) => ctx2[22];
  validate_each_keys(ctx, each_value, get_each_context$1, get_key);
  for (let i = 0; i < each_value.length; i += 1) {
    let child_ctx = get_each_context$1(ctx, each_value, i);
    let key = get_key(child_ctx);
    each_1_lookup.set(key, each_blocks[i] = create_each_block$1(key, child_ctx));
  }
  const block = {
    c: function create() {
      div = element("div");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr_dev(div, "class", "table-container s-VU35bhriycJk");
      set_style(div, "grid-template-rows", ctx[1], false);
      set_style(div, "grid-template-columns", ctx[2], false);
      add_location(div, file$3, 39, 0, 1014);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      insert_dev(target, div, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].m(div, null);
      }
      if (!mounted) {
        dispose = [
          listen_dev(div, "mouseleave", ctx[14], false, false, false),
          listen_dev(div, "blur", ctx[15], false, false, false)
        ];
        mounted = true;
      }
    },
    p: function update2(ctx2, [dirty]) {
      if (dirty & 89) {
        each_value = { length: ctx2[3][0] };
        validate_each_argument(each_value);
        validate_each_keys(ctx2, each_value, get_each_context$1, get_key);
        each_blocks = update_keyed_each(each_blocks, dirty, get_key, 1, ctx2, each_value, each_1_lookup, div, destroy_block, create_each_block$1, null, get_each_context$1);
      }
      if (dirty & 2) {
        set_style(div, "grid-template-rows", ctx2[1], false);
      }
      if (dirty & 4) {
        set_style(div, "grid-template-columns", ctx2[2], false);
      }
    },
    i: noop,
    o: noop,
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].d();
      }
      mounted = false;
      run_all(dispose);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment$5.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance$5($$self, $$props, $$invalidate) {
  let col;
  let row;
  let is_active;
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("Table", slots, []);
  let { plugin } = $$props;
  let { rowNum = 8 } = $$props;
  let { colNum = 8 } = $$props;
  let { hoverTableEnd } = $$props;
  let { insertTable } = $$props;
  let grid = [rowNum, colNum];
  let start = [];
  let end = [];
  function hover(i, j) {
    start = [0, 0];
    end = [i, j];
    $$invalidate(7, hoverTableEnd = [i + 1, j + 1]);
    checkActive(end);
  }
  function unHover() {
    start = end = [-1, -1];
    setTimeout(
      () => {
        $$invalidate(7, hoverTableEnd = [0, 0]);
        checkActive(end);
      },
      1e3
    );
  }
  function click(i, j) {
    if (j === 0)
      return;
    insertTable([i + 1, j + 1]);
    plugin.hideTable();
  }
  function isInRange([i, j], [i2, j2]) {
    return (i - start[0]) * (i - i2) <= 0 && (j - start[1]) * (j - j2) <= 0;
  }
  function checkActive(end2) {
    $$invalidate(0, is_active = is_active.map((a, i) => a.map((_, j) => isInRange([i, j], end2))));
  }
  const writable_props = ["plugin", "rowNum", "colNum", "hoverTableEnd", "insertTable"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console.warn(`<Table> was created with unknown prop '${key}'`);
  });
  const mouseenter_handler = (i, j) => hover(i, j);
  const click_handler = (i, j) => click(i, j);
  const mouseleave_handler = () => unHover();
  const blur_handler = () => unHover();
  $$self.$$set = ($$props2) => {
    if ("plugin" in $$props2)
      $$invalidate(8, plugin = $$props2.plugin);
    if ("rowNum" in $$props2)
      $$invalidate(9, rowNum = $$props2.rowNum);
    if ("colNum" in $$props2)
      $$invalidate(10, colNum = $$props2.colNum);
    if ("hoverTableEnd" in $$props2)
      $$invalidate(7, hoverTableEnd = $$props2.hoverTableEnd);
    if ("insertTable" in $$props2)
      $$invalidate(11, insertTable = $$props2.insertTable);
  };
  $$self.$capture_state = () => ({
    plugin,
    rowNum,
    colNum,
    hoverTableEnd,
    insertTable,
    grid,
    start,
    end,
    hover,
    unHover,
    click,
    isInRange,
    checkActive,
    is_active,
    row,
    col
  });
  $$self.$inject_state = ($$props2) => {
    if ("plugin" in $$props2)
      $$invalidate(8, plugin = $$props2.plugin);
    if ("rowNum" in $$props2)
      $$invalidate(9, rowNum = $$props2.rowNum);
    if ("colNum" in $$props2)
      $$invalidate(10, colNum = $$props2.colNum);
    if ("hoverTableEnd" in $$props2)
      $$invalidate(7, hoverTableEnd = $$props2.hoverTableEnd);
    if ("insertTable" in $$props2)
      $$invalidate(11, insertTable = $$props2.insertTable);
    if ("grid" in $$props2)
      $$invalidate(3, grid = $$props2.grid);
    if ("start" in $$props2)
      start = $$props2.start;
    if ("end" in $$props2)
      end = $$props2.end;
    if ("is_active" in $$props2)
      $$invalidate(0, is_active = $$props2.is_active);
    if ("row" in $$props2)
      $$invalidate(1, row = $$props2.row);
    if ("col" in $$props2)
      $$invalidate(2, col = $$props2.col);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  $$invalidate(2, col = `repeat(${grid[1]}, 1fr)`);
  $$invalidate(1, row = `repeat(${grid[0]}, 1fr)`);
  $$invalidate(0, is_active = Array(grid[0]).fill(0).map((_) => Array(grid[1]).fill(false)));
  return [
    is_active,
    row,
    col,
    grid,
    hover,
    unHover,
    click,
    hoverTableEnd,
    plugin,
    rowNum,
    colNum,
    insertTable,
    mouseenter_handler,
    click_handler,
    mouseleave_handler,
    blur_handler
  ];
}
class Table extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance$5, create_fragment$5, safe_not_equal, {
      plugin: 8,
      rowNum: 9,
      colNum: 10,
      hoverTableEnd: 7,
      insertTable: 11
    });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "Table",
      options,
      id: create_fragment$5.name
    });
    const { ctx } = this.$$;
    const props = options.props || {};
    if (ctx[8] === void 0 && !("plugin" in props)) {
      console.warn("<Table> was created without expected prop 'plugin'");
    }
    if (ctx[7] === void 0 && !("hoverTableEnd" in props)) {
      console.warn("<Table> was created without expected prop 'hoverTableEnd'");
    }
    if (ctx[11] === void 0 && !("insertTable" in props)) {
      console.warn("<Table> was created without expected prop 'insertTable'");
    }
  }
  get plugin() {
    throw new Error("<Table>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set plugin(value) {
    throw new Error("<Table>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get rowNum() {
    throw new Error("<Table>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set rowNum(value) {
    throw new Error("<Table>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get colNum() {
    throw new Error("<Table>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set colNum(value) {
    throw new Error("<Table>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get hoverTableEnd() {
    throw new Error("<Table>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set hoverTableEnd(value) {
    throw new Error("<Table>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get insertTable() {
    throw new Error("<Table>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set insertTable(value) {
    throw new Error("<Table>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
const TableGeneratorComponent_svelte_svelte_type_style_lang = "";
const file$2 = "E:/obdev/.obsidian/plugins/Obsidian-Table-Generator/src/ui/basic/TableGeneratorComponent.svelte";
const get_sizeControls_slot_changes = (dirty) => ({});
const get_sizeControls_slot_context = (ctx) => ({});
const get_headerControls_slot_changes = (dirty) => ({});
const get_headerControls_slot_context = (ctx) => ({});
function create_fragment$4(ctx) {
  let div5;
  let div1;
  let div0;
  let t0;
  let t1;
  let t2;
  let table;
  let updating_hoverTableEnd;
  let t3;
  let div4;
  let div2;
  let t4;
  let input0;
  let t5;
  let div3;
  let t6;
  let input1;
  let t7;
  let t8;
  let button;
  let current;
  let mounted;
  let dispose;
  const headerControls_slot_template = ctx[8].headerControls;
  const headerControls_slot = create_slot(headerControls_slot_template, ctx, ctx[7], get_headerControls_slot_context);
  function table_hoverTableEnd_binding(value) {
    ctx[9](value);
  }
  let table_props = {
    rowNum: ctx[6].rowNum,
    colNum: ctx[6].colNum,
    insertTable: ctx[2],
    plugin: ctx[1]
  };
  if (ctx[3] !== void 0) {
    table_props.hoverTableEnd = ctx[3];
  }
  table = new Table({ props: table_props, $$inline: true });
  binding_callbacks.push(() => bind(table, "hoverTableEnd", table_hoverTableEnd_binding));
  const sizeControls_slot_template = ctx[8].sizeControls;
  const sizeControls_slot = create_slot(sizeControls_slot_template, ctx, ctx[7], get_sizeControls_slot_context);
  const block = {
    c: function create() {
      div5 = element("div");
      div1 = element("div");
      div0 = element("div");
      t0 = text(ctx[0]);
      t1 = space();
      if (headerControls_slot)
        headerControls_slot.c();
      t2 = space();
      create_component(table.$$.fragment);
      t3 = space();
      div4 = element("div");
      div2 = element("div");
      t4 = text("ROW:\r\n            ");
      input0 = element("input");
      t5 = space();
      div3 = element("div");
      t6 = text("COL:\r\n            ");
      input1 = element("input");
      t7 = space();
      if (sizeControls_slot)
        sizeControls_slot.c();
      t8 = space();
      button = element("button");
      button.textContent = "Insert";
      attr_dev(div0, "class", "H1 s-YxLKubgSvLDy");
      add_location(div0, file$2, 31, 8, 927);
      attr_dev(div1, "class", "table-generator-header s-YxLKubgSvLDy");
      add_location(div1, file$2, 30, 4, 881);
      attr_dev(input0, "class", "row-input s-YxLKubgSvLDy");
      add_location(input0, file$2, 41, 12, 1302);
      attr_dev(div2, "class", "input-table-generator-row s-YxLKubgSvLDy");
      add_location(div2, file$2, 39, 8, 1231);
      attr_dev(input1, "class", "col-input s-YxLKubgSvLDy");
      add_location(input1, file$2, 45, 12, 1445);
      attr_dev(div3, "class", "input-table-generator-col s-YxLKubgSvLDy");
      add_location(div3, file$2, 43, 8, 1374);
      attr_dev(div4, "class", "input-table-generator s-YxLKubgSvLDy");
      add_location(div4, file$2, 38, 4, 1186);
      attr_dev(button, "class", "s-YxLKubgSvLDy");
      add_location(button, file$2, 49, 4, 1564);
      attr_dev(div5, "class", "table-generator s-YxLKubgSvLDy");
      add_location(div5, file$2, 29, 0, 846);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      insert_dev(target, div5, anchor);
      append_dev(div5, div1);
      append_dev(div1, div0);
      append_dev(div0, t0);
      append_dev(div1, t1);
      if (headerControls_slot) {
        headerControls_slot.m(div1, null);
      }
      append_dev(div5, t2);
      mount_component(table, div5, null);
      append_dev(div5, t3);
      append_dev(div5, div4);
      append_dev(div4, div2);
      append_dev(div2, t4);
      append_dev(div2, input0);
      set_input_value(input0, ctx[4]);
      append_dev(div4, t5);
      append_dev(div4, div3);
      append_dev(div3, t6);
      append_dev(div3, input1);
      set_input_value(input1, ctx[5]);
      append_dev(div5, t7);
      if (sizeControls_slot) {
        sizeControls_slot.m(div5, null);
      }
      append_dev(div5, t8);
      append_dev(div5, button);
      current = true;
      if (!mounted) {
        dispose = [
          listen_dev(input0, "input", ctx[10]),
          listen_dev(input1, "input", ctx[11]),
          listen_dev(button, "click", ctx[12], false, false, false)
        ];
        mounted = true;
      }
    },
    p: function update2(ctx2, [dirty]) {
      if (!current || dirty & 1)
        set_data_dev(t0, ctx2[0]);
      if (headerControls_slot) {
        if (headerControls_slot.p && (!current || dirty & 128)) {
          update_slot_base(
            headerControls_slot,
            headerControls_slot_template,
            ctx2,
            ctx2[7],
            !current ? get_all_dirty_from_scope(ctx2[7]) : get_slot_changes(headerControls_slot_template, ctx2[7], dirty, get_headerControls_slot_changes),
            get_headerControls_slot_context
          );
        }
      }
      const table_changes = {};
      if (dirty & 4)
        table_changes.insertTable = ctx2[2];
      if (dirty & 2)
        table_changes.plugin = ctx2[1];
      if (!updating_hoverTableEnd && dirty & 8) {
        updating_hoverTableEnd = true;
        table_changes.hoverTableEnd = ctx2[3];
        add_flush_callback(() => updating_hoverTableEnd = false);
      }
      table.$set(table_changes);
      if (dirty & 16 && input0.value !== ctx2[4]) {
        set_input_value(input0, ctx2[4]);
      }
      if (dirty & 32 && input1.value !== ctx2[5]) {
        set_input_value(input1, ctx2[5]);
      }
      if (sizeControls_slot) {
        if (sizeControls_slot.p && (!current || dirty & 128)) {
          update_slot_base(
            sizeControls_slot,
            sizeControls_slot_template,
            ctx2,
            ctx2[7],
            !current ? get_all_dirty_from_scope(ctx2[7]) : get_slot_changes(sizeControls_slot_template, ctx2[7], dirty, get_sizeControls_slot_changes),
            get_sizeControls_slot_context
          );
        }
      }
    },
    i: function intro(local) {
      if (current)
        return;
      transition_in(headerControls_slot, local);
      transition_in(table.$$.fragment, local);
      transition_in(sizeControls_slot, local);
      current = true;
    },
    o: function outro(local) {
      transition_out(headerControls_slot, local);
      transition_out(table.$$.fragment, local);
      transition_out(sizeControls_slot, local);
      current = false;
    },
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div5);
      if (headerControls_slot)
        headerControls_slot.d(detaching);
      destroy_component(table);
      if (sizeControls_slot)
        sizeControls_slot.d(detaching);
      mounted = false;
      run_all(dispose);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment$4.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance$4($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("TableGeneratorComponent", slots, ["headerControls", "sizeControls"]);
  var _a, _b;
  let { title } = $$props;
  let { plugin } = $$props;
  let { onInsert } = $$props;
  let hoverTableEnd;
  let gridRow;
  let gridCol;
  let settings = {
    rowNum: (_a = plugin === null || plugin === void 0 ? void 0 : plugin.settings.rowCount) !== null && _a !== void 0 ? _a : 8,
    colNum: (_b = plugin === null || plugin === void 0 ? void 0 : plugin.settings.columnCount) !== null && _b !== void 0 ? _b : 8
  };
  function setRowAndCol(end) {
    if (end.length === 0) {
      $$invalidate(4, gridRow = 0);
      $$invalidate(5, gridCol = 0);
      return;
    }
    if (!(hoverTableEnd[0] === 0 && hoverTableEnd[1] === 0)) {
      $$invalidate(4, gridRow = hoverTableEnd[0]);
      $$invalidate(5, gridCol = hoverTableEnd[1]);
    }
  }
  const writable_props = ["title", "plugin", "onInsert"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console.warn(`<TableGeneratorComponent> was created with unknown prop '${key}'`);
  });
  function table_hoverTableEnd_binding(value) {
    hoverTableEnd = value;
    $$invalidate(3, hoverTableEnd);
  }
  function input0_input_handler() {
    gridRow = this.value;
    $$invalidate(4, gridRow);
  }
  function input1_input_handler() {
    gridCol = this.value;
    $$invalidate(5, gridCol);
  }
  const click_handler = () => {
    if (/^\d+$/.test(gridRow.toString()) && /^\d+$/.test(gridCol.toString())) {
      onInsert([gridRow, gridCol]);
    } else {
      new obsidian.Notice("Please enter a valid number");
    }
  };
  $$self.$$set = ($$props2) => {
    if ("title" in $$props2)
      $$invalidate(0, title = $$props2.title);
    if ("plugin" in $$props2)
      $$invalidate(1, plugin = $$props2.plugin);
    if ("onInsert" in $$props2)
      $$invalidate(2, onInsert = $$props2.onInsert);
    if ("$$scope" in $$props2)
      $$invalidate(7, $$scope = $$props2.$$scope);
  };
  $$self.$capture_state = () => ({
    _a,
    _b,
    Table,
    Notice: obsidian.Notice,
    title,
    plugin,
    onInsert,
    hoverTableEnd,
    gridRow,
    gridCol,
    settings,
    setRowAndCol
  });
  $$self.$inject_state = ($$props2) => {
    if ("_a" in $$props2)
      _a = $$props2._a;
    if ("_b" in $$props2)
      _b = $$props2._b;
    if ("title" in $$props2)
      $$invalidate(0, title = $$props2.title);
    if ("plugin" in $$props2)
      $$invalidate(1, plugin = $$props2.plugin);
    if ("onInsert" in $$props2)
      $$invalidate(2, onInsert = $$props2.onInsert);
    if ("hoverTableEnd" in $$props2)
      $$invalidate(3, hoverTableEnd = $$props2.hoverTableEnd);
    if ("gridRow" in $$props2)
      $$invalidate(4, gridRow = $$props2.gridRow);
    if ("gridCol" in $$props2)
      $$invalidate(5, gridCol = $$props2.gridCol);
    if ("settings" in $$props2)
      $$invalidate(6, settings = $$props2.settings);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 8) {
      if (hoverTableEnd) {
        setRowAndCol(hoverTableEnd);
      }
    }
  };
  return [
    title,
    plugin,
    onInsert,
    hoverTableEnd,
    gridRow,
    gridCol,
    settings,
    $$scope,
    slots,
    table_hoverTableEnd_binding,
    input0_input_handler,
    input1_input_handler,
    click_handler
  ];
}
class TableGeneratorComponent extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance$4, create_fragment$4, safe_not_equal, { title: 0, plugin: 1, onInsert: 2 });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "TableGeneratorComponent",
      options,
      id: create_fragment$4.name
    });
    const { ctx } = this.$$;
    const props = options.props || {};
    if (ctx[0] === void 0 && !("title" in props)) {
      console.warn("<TableGeneratorComponent> was created without expected prop 'title'");
    }
    if (ctx[1] === void 0 && !("plugin" in props)) {
      console.warn("<TableGeneratorComponent> was created without expected prop 'plugin'");
    }
    if (ctx[2] === void 0 && !("onInsert" in props)) {
      console.warn("<TableGeneratorComponent> was created without expected prop 'onInsert'");
    }
  }
  get title() {
    throw new Error("<TableGeneratorComponent>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set title(value) {
    throw new Error("<TableGeneratorComponent>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get plugin() {
    throw new Error("<TableGeneratorComponent>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set plugin(value) {
    throw new Error("<TableGeneratorComponent>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get onInsert() {
    throw new Error("<TableGeneratorComponent>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set onInsert(value) {
    throw new Error("<TableGeneratorComponent>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
const alignLineText = (align) => {
  switch (align) {
    case "left":
      return "|:-----";
    case "center":
      return "|:----:";
    case "right":
      return "|-----:";
    default:
      return "";
  }
};
const generateMarkdownTable = (selectedGrid, align) => {
  let table = "";
  let secondLine = "";
  let normalLine = "";
  const alignText = alignLineText(align);
  if (selectedGrid.length === 0)
    return table;
  for (let i = 0; i < Number(selectedGrid[1]); i++) {
    secondLine += alignText;
  }
  for (let i = 0; i < Number(selectedGrid[1]); i++) {
    normalLine += "|      ";
  }
  if (!selectedGrid[0]) {
    table = normalLine + "|\n" + secondLine + "|\n";
    return table;
  }
  for (let i = 0; i < Number(selectedGrid[0]) + 1; i++) {
    if (!i)
      table = table + normalLine + "|\n";
    if (i === 1)
      table = table + secondLine + "|\n";
    if (i > 1)
      table = table + normalLine + "|\n";
  }
  return table.trim();
};
function checkBlankLine(editor, line) {
  const getLine = editor.getLine(line);
  if (getLine.trim().length > 0)
    return false;
  return true;
}
const AlignItems_svelte_svelte_type_style_lang = "";
const file$1 = "E:/obdev/.obsidian/plugins/Obsidian-Table-Generator/src/ui/basic/AlignItems.svelte";
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[7] = list[i];
  child_ctx[8] = list;
  child_ctx[9] = i;
  return child_ctx;
}
function create_each_block(key_1, ctx) {
  let div;
  let alignment = ctx[7];
  let mounted;
  let dispose;
  const assign_div = () => ctx[4](div, alignment);
  const unassign_div = () => ctx[4](null, alignment);
  function click_handler() {
    return ctx[5](ctx[7]);
  }
  const block = {
    key: key_1,
    first: null,
    c: function create() {
      div = element("div");
      attr_dev(div, "class", "table-generator-align-icon s-XNB-qso0yOHJ");
      toggle_class(div, "active", ctx[0] === ctx[7]);
      add_location(div, file$1, 19, 8, 598);
      this.first = div;
    },
    m: function mount(target, anchor) {
      insert_dev(target, div, anchor);
      assign_div();
      if (!mounted) {
        dispose = listen_dev(div, "click", click_handler, false, false, false);
        mounted = true;
      }
    },
    p: function update2(new_ctx, dirty) {
      ctx = new_ctx;
      if (alignment !== ctx[7]) {
        unassign_div();
        alignment = ctx[7];
        assign_div();
      }
      if (dirty & 5) {
        toggle_class(div, "active", ctx[0] === ctx[7]);
      }
    },
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div);
      unassign_div();
      mounted = false;
      dispose();
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_each_block.name,
    type: "each",
    source: "(19:4) {#each alignments as alignment (alignment)}",
    ctx
  });
  return block;
}
function create_fragment$3(ctx) {
  let div;
  let each_blocks = [];
  let each_1_lookup = /* @__PURE__ */ new Map();
  let each_value = ctx[2];
  validate_each_argument(each_value);
  const get_key = (ctx2) => ctx2[7];
  validate_each_keys(ctx, each_value, get_each_context, get_key);
  for (let i = 0; i < each_value.length; i += 1) {
    let child_ctx = get_each_context(ctx, each_value, i);
    let key = get_key(child_ctx);
    each_1_lookup.set(key, each_blocks[i] = create_each_block(key, child_ctx));
  }
  const block = {
    c: function create() {
      div = element("div");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      attr_dev(div, "class", "table-generator-align-group s-XNB-qso0yOHJ");
      add_location(div, file$1, 17, 0, 498);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      insert_dev(target, div, anchor);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].m(div, null);
      }
    },
    p: function update2(ctx2, [dirty]) {
      if (dirty & 15) {
        each_value = ctx2[2];
        validate_each_argument(each_value);
        validate_each_keys(ctx2, each_value, get_each_context, get_key);
        each_blocks = update_keyed_each(each_blocks, dirty, get_key, 1, ctx2, each_value, each_1_lookup, div, destroy_block, create_each_block, null, get_each_context);
      }
    },
    i: noop,
    o: noop,
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div);
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].d();
      }
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment$3.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance$3($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("AlignItems", slots, []);
  let { align = "left" } = $$props;
  const dispatch = createEventDispatcher();
  const alignments = ["left", "center", "right"];
  let refs = {};
  onMount(() => {
    obsidian.setIcon(refs["left"], "align-left");
    obsidian.setIcon(refs["center"], "align-center");
    obsidian.setIcon(refs["right"], "align-right");
  });
  function click(update2) {
    $$invalidate(0, align = update2);
    dispatch("update", align);
  }
  const writable_props = ["align"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console.warn(`<AlignItems> was created with unknown prop '${key}'`);
  });
  function div_binding($$value, alignment) {
    binding_callbacks[$$value ? "unshift" : "push"](() => {
      refs[alignment] = $$value;
      $$invalidate(1, refs);
    });
  }
  const click_handler = (alignment) => click(alignment);
  $$self.$$set = ($$props2) => {
    if ("align" in $$props2)
      $$invalidate(0, align = $$props2.align);
  };
  $$self.$capture_state = () => ({
    onMount,
    createEventDispatcher,
    setIcon: obsidian.setIcon,
    align,
    dispatch,
    alignments,
    refs,
    click
  });
  $$self.$inject_state = ($$props2) => {
    if ("align" in $$props2)
      $$invalidate(0, align = $$props2.align);
    if ("refs" in $$props2)
      $$invalidate(1, refs = $$props2.refs);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  return [align, refs, alignments, click, div_binding, click_handler];
}
class AlignItems extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance$3, create_fragment$3, safe_not_equal, { align: 0 });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "AlignItems",
      options,
      id: create_fragment$3.name
    });
  }
  get align() {
    throw new Error("<AlignItems>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set align(value) {
    throw new Error("<AlignItems>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
function create_headerControls_slot(ctx) {
  let alignitems;
  let current;
  alignitems = new AlignItems({
    props: {
      align: ctx[1],
      slot: "headerControls"
    },
    $$inline: true
  });
  alignitems.$on("update", ctx[2]);
  const block = {
    c: function create() {
      create_component(alignitems.$$.fragment);
    },
    m: function mount(target, anchor) {
      mount_component(alignitems, target, anchor);
      current = true;
    },
    p: function update2(ctx2, dirty) {
      const alignitems_changes = {};
      if (dirty & 2)
        alignitems_changes.align = ctx2[1];
      alignitems.$set(alignitems_changes);
    },
    i: function intro(local) {
      if (current)
        return;
      transition_in(alignitems.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      transition_out(alignitems.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      destroy_component(alignitems, detaching);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_headerControls_slot.name,
    type: "slot",
    source: "(47:4) ",
    ctx
  });
  return block;
}
function create_fragment$2(ctx) {
  let tablegeneratorcomponent;
  let current;
  tablegeneratorcomponent = new TableGeneratorComponent({
    props: {
      title: "Table Generator",
      plugin: ctx[0],
      onInsert: ctx[3],
      $$slots: {
        headerControls: [create_headerControls_slot]
      },
      $$scope: { ctx }
    },
    $$inline: true
  });
  const block = {
    c: function create() {
      create_component(tablegeneratorcomponent.$$.fragment);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      mount_component(tablegeneratorcomponent, target, anchor);
      current = true;
    },
    p: function update2(ctx2, [dirty]) {
      const tablegeneratorcomponent_changes = {};
      if (dirty & 1)
        tablegeneratorcomponent_changes.plugin = ctx2[0];
      if (dirty & 66) {
        tablegeneratorcomponent_changes.$$scope = { dirty, ctx: ctx2 };
      }
      tablegeneratorcomponent.$set(tablegeneratorcomponent_changes);
    },
    i: function intro(local) {
      if (current)
        return;
      transition_in(tablegeneratorcomponent.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      transition_out(tablegeneratorcomponent.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      destroy_component(tablegeneratorcomponent, detaching);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment$2.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance$2($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("TableGenerator", slots, []);
  var _a;
  let { editor } = $$props;
  let { plugin } = $$props;
  let currentAlign = (_a = plugin === null || plugin === void 0 ? void 0 : plugin.settings.defaultAlignment) !== null && _a !== void 0 ? _a : "left";
  function handleAlignModeUpdate(event) {
    var _a2;
    return __awaiter(this, void 0, void 0, function* () {
      $$invalidate(1, currentAlign = event.detail);
      (_a2 = plugin === null || plugin === void 0 ? void 0 : plugin.settings) === null || _a2 === void 0 ? void 0 : _a2.defaultAlignment = currentAlign;
      yield plugin === null || plugin === void 0 ? void 0 : plugin.saveSettings();
    });
  }
  function insertTable(selectedGrid) {
    if (selectedGrid.length === 0 || selectedGrid[1] < 2)
      return;
    const basicTable = generateMarkdownTable(selectedGrid, currentAlign);
    let markdownTable = basicTable;
    const cursor = editor.getCursor("from");
    const line = editor.getLine(cursor.line);
    if (cursor.line !== 0 && line.trim().length !== 0) {
      markdownTable = "\n" + markdownTable;
    }
    if (cursor.line !== editor.lastLine() && !checkBlankLine(editor, cursor.line + 1)) {
      markdownTable = markdownTable + "\n";
    } else if (cursor.line === editor.lastLine()) {
      markdownTable = "\n" + markdownTable;
    }
    if (line.trim().length > 0) {
      editor.replaceRange(markdownTable, { line: cursor.line + 1, ch: 0 }, { line: cursor.line + 1, ch: 0 });
    } else {
      editor.replaceRange(markdownTable, { line: cursor.line, ch: 0 }, { line: cursor.line, ch: 0 });
    }
  }
  const writable_props = ["editor", "plugin"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console.warn(`<TableGenerator> was created with unknown prop '${key}'`);
  });
  $$self.$$set = ($$props2) => {
    if ("editor" in $$props2)
      $$invalidate(4, editor = $$props2.editor);
    if ("plugin" in $$props2)
      $$invalidate(0, plugin = $$props2.plugin);
  };
  $$self.$capture_state = () => ({
    _a,
    __awaiter,
    TableGeneratorComponent,
    checkBlankLine,
    generateMarkdownTable,
    AlignItems,
    editor,
    plugin,
    currentAlign,
    handleAlignModeUpdate,
    insertTable
  });
  $$self.$inject_state = ($$props2) => {
    if ("_a" in $$props2)
      _a = $$props2._a;
    if ("editor" in $$props2)
      $$invalidate(4, editor = $$props2.editor);
    if ("plugin" in $$props2)
      $$invalidate(0, plugin = $$props2.plugin);
    if ("currentAlign" in $$props2)
      $$invalidate(1, currentAlign = $$props2.currentAlign);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  return [plugin, currentAlign, handleAlignModeUpdate, insertTable, editor];
}
class TableGenerator extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance$2, create_fragment$2, safe_not_equal, { editor: 4, plugin: 0 });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "TableGenerator",
      options,
      id: create_fragment$2.name
    });
    const { ctx } = this.$$;
    const props = options.props || {};
    if (ctx[4] === void 0 && !("editor" in props)) {
      console.warn("<TableGenerator> was created without expected prop 'editor'");
    }
    if (ctx[0] === void 0 && !("plugin" in props)) {
      console.warn("<TableGenerator> was created without expected prop 'plugin'");
    }
  }
  get editor() {
    throw new Error("<TableGenerator>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set editor(value) {
    throw new Error("<TableGenerator>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get plugin() {
    throw new Error("<TableGenerator>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set plugin(value) {
    throw new Error("<TableGenerator>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
const tableGeneratorDefault = "";
function getLineHeight(editor, pos) {
  const lineInfo = editor.cm.state.doc.lineAt(pos);
  const lineDOM = editor.cm.domAtPos(lineInfo.from);
  return lineDOM.node.offsetHeight;
}
const random = (e) => {
  const t = [];
  for (let n = 0; n < e; n++) {
    t.push((16 * Math.random() | 0).toString(16));
  }
  return t.join("");
};
function reverseCalculation(n, t) {
  const r = t.scale;
  const cx = t.canvasRect.cx;
  const cy = t.canvasRect.cy;
  const x = t.x;
  const y = t.y;
  const eClientX = (n.x - x) * r + cx;
  const eClientY = (n.y - y) * r + cy;
  return {
    clientX: eClientX,
    clientY: eClientY
  };
}
function calculateEditor(editor, tableGeneratorBoard) {
  var _a, _b, _c, _d;
  if (!tableGeneratorBoard)
    return;
  const cursor = editor.getCursor("from");
  let coords;
  if (editor.cursorCoords) {
    coords = editor.cursorCoords(true, "window");
  } else if (editor.coordsAtPos) {
    const offset = editor.posToOffset(cursor);
    coords = (_c = (_b = (_a = editor.cm).coordsAtPos) == null ? void 0 : _b.call(_a, offset)) != null ? _c : editor.coordsAtPos(offset);
  } else {
    return;
  }
  const lineHeight = getLineHeight(editor, editor.posToOffset(cursor));
  const calculateTop = ((_d = obsidian.requireApiVersion("0.15.0") ? activeDocument : document) == null ? void 0 : _d.body.getBoundingClientRect().height) - (coords.top || 0) - (coords.height || lineHeight);
  return {
    top: calculateTop || 0,
    left: coords.left || 0,
    bottom: coords.bottom || 0,
    height: coords.height || lineHeight
  };
}
function around(obj, factories) {
  const removers = Object.keys(factories).map((key) => around1(obj, key, factories[key]));
  return removers.length === 1 ? removers[0] : function() {
    removers.forEach((r) => r());
  };
}
function around1(obj, method, createWrapper) {
  const original = obj[method], hadOwn = obj.hasOwnProperty(method);
  let current = createWrapper(original);
  if (original)
    Object.setPrototypeOf(current, original);
  Object.setPrototypeOf(wrapper, current);
  obj[method] = wrapper;
  return remove;
  function wrapper(...args) {
    if (current === original && obj[method] === wrapper)
      remove();
    return current.apply(this, args);
  }
  function remove() {
    if (obj[method] === wrapper) {
      if (hadOwn)
        obj[method] = original;
      else
        delete obj[method];
    }
    if (current === original)
      return;
    current = original;
    Object.setPrototypeOf(wrapper, original || Function);
  }
}
const SizeControls_svelte_svelte_type_style_lang = "";
const file = "E:/obdev/.obsidian/plugins/Obsidian-Table-Generator/src/ui/basic/SizeControls.svelte";
function create_fragment$1(ctx) {
  let div2;
  let div0;
  let t0;
  let input0;
  let t1;
  let div1;
  let t2;
  let input1;
  let mounted;
  let dispose;
  const block = {
    c: function create() {
      div2 = element("div");
      div0 = element("div");
      t0 = text("H:\r\n        ");
      input0 = element("input");
      t1 = space();
      div1 = element("div");
      t2 = text("W:\r\n        ");
      input1 = element("input");
      attr_dev(input0, "class", "height-input s-b7dfVi8Mj3e3");
      add_location(input0, file, 12, 8, 374);
      attr_dev(div0, "class", "input-table-generator-height s-b7dfVi8Mj3e3");
      add_location(div0, file, 10, 4, 310);
      attr_dev(input1, "class", "width-input s-b7dfVi8Mj3e3");
      add_location(input1, file, 16, 8, 503);
      attr_dev(div1, "class", "input-table-generator-width s-b7dfVi8Mj3e3");
      add_location(div1, file, 14, 4, 440);
      attr_dev(div2, "class", "input-table-generator s-b7dfVi8Mj3e3");
      add_location(div2, file, 9, 0, 269);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      insert_dev(target, div2, anchor);
      append_dev(div2, div0);
      append_dev(div0, t0);
      append_dev(div0, input0);
      set_input_value(input0, ctx[0]);
      append_dev(div2, t1);
      append_dev(div2, div1);
      append_dev(div1, t2);
      append_dev(div1, input1);
      set_input_value(input1, ctx[1]);
      if (!mounted) {
        dispose = [
          listen_dev(input0, "input", ctx[2]),
          listen_dev(input1, "input", ctx[3])
        ];
        mounted = true;
      }
    },
    p: function update2(ctx2, [dirty]) {
      if (dirty & 1 && input0.value !== ctx2[0]) {
        set_input_value(input0, ctx2[0]);
      }
      if (dirty & 2 && input1.value !== ctx2[1]) {
        set_input_value(input1, ctx2[1]);
      }
    },
    i: noop,
    o: noop,
    d: function destroy(detaching) {
      if (detaching)
        detach_dev(div2);
      mounted = false;
      run_all(dispose);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment$1.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance$1($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("SizeControls", slots, []);
  const dispatch = createEventDispatcher();
  let { height = 160 } = $$props;
  let { width = 160 } = $$props;
  const writable_props = ["height", "width"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console.warn(`<SizeControls> was created with unknown prop '${key}'`);
  });
  function input0_input_handler() {
    height = this.value;
    $$invalidate(0, height);
  }
  function input1_input_handler() {
    width = this.value;
    $$invalidate(1, width);
  }
  $$self.$$set = ($$props2) => {
    if ("height" in $$props2)
      $$invalidate(0, height = $$props2.height);
    if ("width" in $$props2)
      $$invalidate(1, width = $$props2.width);
  };
  $$self.$capture_state = () => ({
    createEventDispatcher,
    dispatch,
    height,
    width
  });
  $$self.$inject_state = ($$props2) => {
    if ("height" in $$props2)
      $$invalidate(0, height = $$props2.height);
    if ("width" in $$props2)
      $$invalidate(1, width = $$props2.width);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  $$self.$$.update = () => {
    if ($$self.$$.dirty & 3) {
      dispatch("sizeUpdate", { height, width });
    }
  };
  return [height, width, input0_input_handler, input1_input_handler];
}
class SizeControls extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance$1, create_fragment$1, safe_not_equal, { height: 0, width: 1 });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "SizeControls",
      options,
      id: create_fragment$1.name
    });
  }
  get height() {
    throw new Error("<SizeControls>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set height(value) {
    throw new Error("<SizeControls>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get width() {
    throw new Error("<SizeControls>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set width(value) {
    throw new Error("<SizeControls>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
const { console: console_1 } = globals;
function create_sizeControls_slot(ctx) {
  let sizecontrols;
  let current;
  sizecontrols = new SizeControls({
    props: {
      slot: "sizeControls",
      width: ctx[1],
      height: ctx[2]
    },
    $$inline: true
  });
  sizecontrols.$on("sizeUpdate", ctx[3]);
  const block = {
    c: function create() {
      create_component(sizecontrols.$$.fragment);
    },
    m: function mount(target, anchor) {
      mount_component(sizecontrols, target, anchor);
      current = true;
    },
    p: function update2(ctx2, dirty) {
      const sizecontrols_changes = {};
      if (dirty & 2)
        sizecontrols_changes.width = ctx2[1];
      if (dirty & 4)
        sizecontrols_changes.height = ctx2[2];
      sizecontrols.$set(sizecontrols_changes);
    },
    i: function intro(local) {
      if (current)
        return;
      transition_in(sizecontrols.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      transition_out(sizecontrols.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      destroy_component(sizecontrols, detaching);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_sizeControls_slot.name,
    type: "slot",
    source: "(47:4) ",
    ctx
  });
  return block;
}
function create_fragment(ctx) {
  let tablegeneratorcomponent;
  let current;
  tablegeneratorcomponent = new TableGeneratorComponent({
    props: {
      title: "Card Generator",
      plugin: ctx[0],
      onInsert: ctx[4],
      $$slots: { sizeControls: [create_sizeControls_slot] },
      $$scope: { ctx }
    },
    $$inline: true
  });
  const block = {
    c: function create() {
      create_component(tablegeneratorcomponent.$$.fragment);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      mount_component(tablegeneratorcomponent, target, anchor);
      current = true;
    },
    p: function update2(ctx2, [dirty]) {
      const tablegeneratorcomponent_changes = {};
      if (dirty & 1)
        tablegeneratorcomponent_changes.plugin = ctx2[0];
      if (dirty & 134) {
        tablegeneratorcomponent_changes.$$scope = { dirty, ctx: ctx2 };
      }
      tablegeneratorcomponent.$set(tablegeneratorcomponent_changes);
    },
    i: function intro(local) {
      if (current)
        return;
      transition_in(tablegeneratorcomponent.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      transition_out(tablegeneratorcomponent.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      destroy_component(tablegeneratorcomponent, detaching);
    }
  };
  dispatch_dev("SvelteRegisterBlock", {
    block,
    id: create_fragment.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}
function instance($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  validate_slots("CardGenerator", slots, []);
  let { canvas } = $$props;
  let { coords } = $$props;
  let { plugin } = $$props;
  let width = plugin.settings.defaultCardWidth || 160;
  let height = plugin.settings.defaultCardHeight || 160;
  function handleSizeUpdate(event) {
    $$invalidate(2, height = parseInt(event.detail.height, 10));
    $$invalidate(1, width = parseInt(event.detail.width, 10));
    $$invalidate(0, plugin.settings.defaultCardHeight = height, plugin);
    $$invalidate(0, plugin.settings.defaultCardWidth = width, plugin);
    plugin.saveSettings();
  }
  function insertTable(selectedGrid) {
    return __awaiter(this, void 0, void 0, function* () {
      if (selectedGrid.length === 0 || selectedGrid[1] < 2)
        return;
      const canvasFile = yield plugin.app.vault.cachedRead(canvas.view.file);
      const canvasFileData = JSON.parse(canvasFile);
      console.log(selectedGrid);
      for (let i = 0; i < selectedGrid[0]; i++) {
        for (let j = 0; j < selectedGrid[1]; j++) {
          canvasFileData.nodes.push({
            id: random(16),
            x: coords.x + j * (width + 10) + 40,
            y: coords.y + i * (height + 10) + 40,
            width,
            height,
            type: "text",
            text: ""
          });
        }
      }
      console.log(canvasFileData);
      setTimeout(
        () => {
          canvas.setData(canvasFileData);
          canvas.requestSave();
        },
        100
      );
    });
  }
  const writable_props = ["canvas", "coords", "plugin"];
  Object.keys($$props).forEach((key) => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$" && key !== "slot")
      console_1.warn(`<CardGenerator> was created with unknown prop '${key}'`);
  });
  $$self.$$set = ($$props2) => {
    if ("canvas" in $$props2)
      $$invalidate(5, canvas = $$props2.canvas);
    if ("coords" in $$props2)
      $$invalidate(6, coords = $$props2.coords);
    if ("plugin" in $$props2)
      $$invalidate(0, plugin = $$props2.plugin);
  };
  $$self.$capture_state = () => ({
    __awaiter,
    random,
    TableGeneratorComponent,
    SizeControls,
    canvas,
    coords,
    plugin,
    width,
    height,
    handleSizeUpdate,
    insertTable
  });
  $$self.$inject_state = ($$props2) => {
    if ("canvas" in $$props2)
      $$invalidate(5, canvas = $$props2.canvas);
    if ("coords" in $$props2)
      $$invalidate(6, coords = $$props2.coords);
    if ("plugin" in $$props2)
      $$invalidate(0, plugin = $$props2.plugin);
    if ("width" in $$props2)
      $$invalidate(1, width = $$props2.width);
    if ("height" in $$props2)
      $$invalidate(2, height = $$props2.height);
  };
  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }
  return [plugin, width, height, handleSizeUpdate, insertTable, canvas, coords];
}
class CardGenerator extends SvelteComponentDev {
  constructor(options) {
    super(options);
    init(this, options, instance, create_fragment, safe_not_equal, { canvas: 5, coords: 6, plugin: 0 });
    dispatch_dev("SvelteRegisterComponent", {
      component: this,
      tagName: "CardGenerator",
      options,
      id: create_fragment.name
    });
    const { ctx } = this.$$;
    const props = options.props || {};
    if (ctx[5] === void 0 && !("canvas" in props)) {
      console_1.warn("<CardGenerator> was created without expected prop 'canvas'");
    }
    if (ctx[6] === void 0 && !("coords" in props)) {
      console_1.warn("<CardGenerator> was created without expected prop 'coords'");
    }
    if (ctx[0] === void 0 && !("plugin" in props)) {
      console_1.warn("<CardGenerator> was created without expected prop 'plugin'");
    }
  }
  get canvas() {
    throw new Error("<CardGenerator>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set canvas(value) {
    throw new Error("<CardGenerator>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get coords() {
    throw new Error("<CardGenerator>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set coords(value) {
    throw new Error("<CardGenerator>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  get plugin() {
    throw new Error("<CardGenerator>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
  set plugin(value) {
    throw new Error("<CardGenerator>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }
}
function setTableGeneratorMenuPosition(tableGeneratorBoard, coords, displayMode) {
  if (!tableGeneratorBoard)
    return;
  setTimeout(() => {
    tableGeneratorBoard.style.display = "block";
    switch (displayMode) {
      case "canvas":
        tableGeneratorBoard.style.top = `${coords.top}px`;
        tableGeneratorBoard.style.left = `${coords.left}px`;
        break;
      case "editor":
        tableGeneratorBoard.style.transform = `translate(${coords.left}px,-${coords.top}px`;
        break;
    }
  });
}
function handleHideTableGeneratorMenu(evt, tableGeneratorEl) {
  var _a;
  const target = evt.target;
  if (!tableGeneratorEl || !target)
    return;
  if (target.classList.contains("table-generator-menu") || ((_a = target.parentElement) == null ? void 0 : _a.classList.contains("table-generator-menu")) || target.tagName == "BUTTON")
    return;
  if (tableGeneratorEl == null ? void 0 : tableGeneratorEl.contains(target))
    return;
  if (!document.body.contains(tableGeneratorEl))
    return;
  tableGeneratorEl.detach();
}
const DEFAULT_SETTINGS = {
  rowCount: 8,
  columnCount: 8,
  defaultAlignment: "left",
  defaultCardWidth: 160,
  defaultCardHeight: 160
};
class TableGeneratorPlugin extends obsidian.Plugin {
  constructor() {
    super(...arguments);
    __publicField(this, "tableGeneratorEl", null);
    __publicField(this, "tableGeneratorComponent");
    __publicField(this, "settings");
  }
  async onload() {
    this.registerEvent(
      this.app.workspace.on("editor-menu", (menu, editor, view) => this.handleCreateTableGeneratorInMenu(menu, editor, view))
    );
    await this.registerSettings();
    this.registerDomEvent(window, "click", (evt) => handleHideTableGeneratorMenu(evt, this.tableGeneratorEl));
    if (obsidian.requireApiVersion("0.15.0"))
      this.registerTableGeneratorMenu();
    this.registerCommands();
    this.registerCanvasMenu();
  }
  hideTable() {
    var _a;
    (_a = this.tableGeneratorEl) == null ? void 0 : _a.detach();
  }
  handleCreateTableGeneratorInMenu(menu, editor, view) {
    menu.addItem((item) => {
      const itemDom = item.dom;
      itemDom.addClass("table-generator-menu");
      item.setTitle("Add Markdown Table").setIcon("table").setSection("action").onClick(async () => {
        this.createGeneratorMenu("table", { editor }, this);
        const coords = calculateEditor(editor, this.tableGeneratorEl);
        if (!coords)
          return;
        setTableGeneratorMenuPosition(this.tableGeneratorEl, coords, "editor");
      });
    });
  }
  createGeneratorMenu(type, context, plugin) {
    var _a;
    if (this.tableGeneratorEl)
      this.tableGeneratorEl.detach();
    this.tableGeneratorEl = (_a = obsidian.requireApiVersion("0.15.0") ? activeDocument : document) == null ? void 0 : _a.body.createEl("div", { cls: "table-generator-view" });
    this.tableGeneratorEl.hide();
    if (type === "table") {
      this.tableGeneratorComponent = new TableGenerator({
        target: this.tableGeneratorEl,
        props: { editor: context.editor, plugin }
      });
    } else if (type === "card") {
      this.tableGeneratorComponent = new CardGenerator({
        target: this.tableGeneratorEl,
        props: { canvas: context.canvas, coords: context.coords, plugin }
      });
    }
  }
  async registerSettings() {
    await this.loadSettings();
    this.addSettingTab(new TableGeneratorSettingTab(this.app, this));
    this.registerInterval(
      window.setTimeout(() => {
        this.saveSettings();
      }, 100)
    );
  }
  registerCanvasMenu() {
    const createCardTable = (canvas, e, t, a) => {
      const { top, left } = e.dom.getBoundingClientRect();
      const data = reverseCalculation(t, canvas);
      console.log(data);
      setTimeout(() => {
        this.createGeneratorMenu("card", { canvas, coords: t }, this);
        setTableGeneratorMenuPosition(this.tableGeneratorEl, { top, left, bottom: 0, height: 0 }, "canvas");
      }, 0);
    };
    const patchNode = () => {
      var _a;
      const canvasView = (_a = this.app.workspace.getLeavesOfType("canvas").first()) == null ? void 0 : _a.view;
      const canvas = canvasView == null ? void 0 : canvasView.canvas;
      if (!canvas)
        return false;
      const uninstaller = around(canvas.constructor.prototype, {
        showCreationMenu: (next) => function(e, t, a) {
          const result = next.call(this, e, t, a);
          e.addSeparator().addItem((item) => {
            item.setSection("create").setTitle("Add Card Table").setIcon("table").onClick(async () => {
              createCardTable(this, e, t);
            });
          });
          return result;
        }
      });
      this.register(uninstaller);
      console.log("Obsidian-Canvas-MindMap: canvas node patched");
      return true;
    };
    this.app.workspace.onLayoutReady(() => {
      if (!patchNode()) {
        const evt = this.app.workspace.on("layout-change", () => {
          patchNode() && this.app.workspace.offref(evt);
        });
        this.registerEvent(evt);
      }
    });
  }
  registerCommands() {
    this.addCommand({
      id: "create-table-genertator",
      name: "Create Table Generator",
      editorCallback: (editor, view) => {
        var _a;
        if ((_a = obsidian.requireApiVersion("0.15.0") ? activeDocument : document) == null ? void 0 : _a.body.contains(this.tableGeneratorEl))
          return;
        this.createGeneratorMenu("table", { editor }, this);
        const coords = calculateEditor(editor, this.tableGeneratorEl);
        if (!coords)
          return;
        setTableGeneratorMenuPosition(this.tableGeneratorEl, coords, "editor");
      }
    });
  }
  registerTableGeneratorMenu() {
    this.app.workspace.on("window-open", (leaf) => {
      this.registerDomEvent(leaf.doc, "click", (evt) => {
        var _a, _b;
        const target = evt.target;
        if (!this.tableGeneratorEl || !target)
          return;
        if (target.classList.contains("table-generator-menu") || ((_a = target.parentElement) == null ? void 0 : _a.classList.contains("table-generator-menu")) || target.tagName == "BUTTON")
          return;
        if ((_b = this.tableGeneratorEl) == null ? void 0 : _b.contains(target))
          return;
        if (!activeDocument.body.contains(this.tableGeneratorEl))
          return;
        this.tableGeneratorEl.detach();
      });
    });
  }
  onunload() {
    if (this.tableGeneratorEl) {
      this.tableGeneratorComponent.$destroy();
      this.tableGeneratorEl.detach();
    }
  }
  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
}
class TableGeneratorSettingTab extends obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    __publicField(this, "plugin");
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Table Generator" });
    let rowText;
    new obsidian.Setting(containerEl).setName("Row Count").setDesc("The number of rows in the table").addSlider(
      (slider) => slider.setLimits(2, 12, 1).setValue(this.plugin.settings.rowCount).onChange(async (value) => {
        rowText.innerText = ` ${value.toString()}`;
        this.plugin.settings.rowCount = value;
      })
    ).settingEl.createDiv("", (el) => {
      rowText = el;
      el.className = "table-generator-setting-text";
      el.innerText = ` ${this.plugin.settings.rowCount.toString()}`;
    });
    let columnText;
    new obsidian.Setting(containerEl).setName("Columns Count").setDesc("The number of columns in the table").addSlider(
      (slider) => slider.setLimits(2, 12, 1).setValue(this.plugin.settings.columnCount).onChange(async (value) => {
        columnText.innerText = ` ${value.toString()}`;
        this.plugin.settings.columnCount = value;
      })
    ).settingEl.createDiv("", (el) => {
      columnText = el;
      el.className = "table-generator-setting-text";
      el.innerText = ` ${this.plugin.settings.columnCount.toString()}`;
    });
    this.containerEl.createEl("h2", { text: "Say Thank You" });
    new obsidian.Setting(containerEl).setName("Donate").setDesc("If you like this plugin, consider donating to support continued development:").addButton((bt) => {
      bt.buttonEl.outerHTML = `<a href="https://www.buymeacoffee.com/boninall"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=boninall&button_colour=6495ED&font_colour=ffffff&font_family=Inter&outline_colour=000000&coffee_colour=FFDD00"></a>`;
    });
  }
}
module.exports = TableGeneratorPlugin;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWFpbi5qcyIsInNvdXJjZXMiOlsibm9kZV9tb2R1bGVzLy5wbnBtL3N2ZWx0ZUAzLjUwLjEvbm9kZV9tb2R1bGVzL3N2ZWx0ZS9pbnRlcm5hbC9pbmRleC5tanMiLCJub2RlX21vZHVsZXMvLnBucG0vdHNsaWJAMi40LjAvbm9kZV9tb2R1bGVzL3RzbGliL3RzbGliLmVzNi5qcyIsInNyYy91aS9iYXNpYy9UYWJsZS5zdmVsdGUiLCJzcmMvdWkvYmFzaWMvVGFibGVHZW5lcmF0b3JDb21wb25lbnQuc3ZlbHRlIiwic3JjL3V0aWxzL21hcmtkb3duVGFibGUudHMiLCJzcmMvdWkvYmFzaWMvQWxpZ25JdGVtcy5zdmVsdGUiLCJzcmMvdWkvVGFibGVHZW5lcmF0b3Iuc3ZlbHRlIiwic3JjL3V0aWxzL3RhYmxlUE9TLnRzIiwibm9kZV9tb2R1bGVzLy5wbnBtL21vbmtleS1hcm91bmRAMi4zLjAvbm9kZV9tb2R1bGVzL21vbmtleS1hcm91bmQvbWpzL2luZGV4LmpzIiwic3JjL3VpL2Jhc2ljL1NpemVDb250cm9scy5zdmVsdGUiLCJzcmMvdWkvQ2FyZEdlbmVyYXRvci5zdmVsdGUiLCJzcmMvdXRpbHMvdGFibGVET00udHMiLCJzcmMvdGFibGVHZW5lcmF0b3JJbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBub29wKCkgeyB9XG5jb25zdCBpZGVudGl0eSA9IHggPT4geDtcbmZ1bmN0aW9uIGFzc2lnbih0YXIsIHNyYykge1xuICAgIC8vIEB0cy1pZ25vcmVcbiAgICBmb3IgKGNvbnN0IGsgaW4gc3JjKVxuICAgICAgICB0YXJba10gPSBzcmNba107XG4gICAgcmV0dXJuIHRhcjtcbn1cbmZ1bmN0aW9uIGlzX3Byb21pc2UodmFsdWUpIHtcbiAgICByZXR1cm4gdmFsdWUgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgdmFsdWUudGhlbiA9PT0gJ2Z1bmN0aW9uJztcbn1cbmZ1bmN0aW9uIGFkZF9sb2NhdGlvbihlbGVtZW50LCBmaWxlLCBsaW5lLCBjb2x1bW4sIGNoYXIpIHtcbiAgICBlbGVtZW50Ll9fc3ZlbHRlX21ldGEgPSB7XG4gICAgICAgIGxvYzogeyBmaWxlLCBsaW5lLCBjb2x1bW4sIGNoYXIgfVxuICAgIH07XG59XG5mdW5jdGlvbiBydW4oZm4pIHtcbiAgICByZXR1cm4gZm4oKTtcbn1cbmZ1bmN0aW9uIGJsYW5rX29iamVjdCgpIHtcbiAgICByZXR1cm4gT2JqZWN0LmNyZWF0ZShudWxsKTtcbn1cbmZ1bmN0aW9uIHJ1bl9hbGwoZm5zKSB7XG4gICAgZm5zLmZvckVhY2gocnVuKTtcbn1cbmZ1bmN0aW9uIGlzX2Z1bmN0aW9uKHRoaW5nKSB7XG4gICAgcmV0dXJuIHR5cGVvZiB0aGluZyA9PT0gJ2Z1bmN0aW9uJztcbn1cbmZ1bmN0aW9uIHNhZmVfbm90X2VxdWFsKGEsIGIpIHtcbiAgICByZXR1cm4gYSAhPSBhID8gYiA9PSBiIDogYSAhPT0gYiB8fCAoKGEgJiYgdHlwZW9mIGEgPT09ICdvYmplY3QnKSB8fCB0eXBlb2YgYSA9PT0gJ2Z1bmN0aW9uJyk7XG59XG5sZXQgc3JjX3VybF9lcXVhbF9hbmNob3I7XG5mdW5jdGlvbiBzcmNfdXJsX2VxdWFsKGVsZW1lbnRfc3JjLCB1cmwpIHtcbiAgICBpZiAoIXNyY191cmxfZXF1YWxfYW5jaG9yKSB7XG4gICAgICAgIHNyY191cmxfZXF1YWxfYW5jaG9yID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYScpO1xuICAgIH1cbiAgICBzcmNfdXJsX2VxdWFsX2FuY2hvci5ocmVmID0gdXJsO1xuICAgIHJldHVybiBlbGVtZW50X3NyYyA9PT0gc3JjX3VybF9lcXVhbF9hbmNob3IuaHJlZjtcbn1cbmZ1bmN0aW9uIG5vdF9lcXVhbChhLCBiKSB7XG4gICAgcmV0dXJuIGEgIT0gYSA/IGIgPT0gYiA6IGEgIT09IGI7XG59XG5mdW5jdGlvbiBpc19lbXB0eShvYmopIHtcbiAgICByZXR1cm4gT2JqZWN0LmtleXMob2JqKS5sZW5ndGggPT09IDA7XG59XG5mdW5jdGlvbiB2YWxpZGF0ZV9zdG9yZShzdG9yZSwgbmFtZSkge1xuICAgIGlmIChzdG9yZSAhPSBudWxsICYmIHR5cGVvZiBzdG9yZS5zdWJzY3JpYmUgIT09ICdmdW5jdGlvbicpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGAnJHtuYW1lfScgaXMgbm90IGEgc3RvcmUgd2l0aCBhICdzdWJzY3JpYmUnIG1ldGhvZGApO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHN1YnNjcmliZShzdG9yZSwgLi4uY2FsbGJhY2tzKSB7XG4gICAgaWYgKHN0b3JlID09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIG5vb3A7XG4gICAgfVxuICAgIGNvbnN0IHVuc3ViID0gc3RvcmUuc3Vic2NyaWJlKC4uLmNhbGxiYWNrcyk7XG4gICAgcmV0dXJuIHVuc3ViLnVuc3Vic2NyaWJlID8gKCkgPT4gdW5zdWIudW5zdWJzY3JpYmUoKSA6IHVuc3ViO1xufVxuZnVuY3Rpb24gZ2V0X3N0b3JlX3ZhbHVlKHN0b3JlKSB7XG4gICAgbGV0IHZhbHVlO1xuICAgIHN1YnNjcmliZShzdG9yZSwgXyA9PiB2YWx1ZSA9IF8pKCk7XG4gICAgcmV0dXJuIHZhbHVlO1xufVxuZnVuY3Rpb24gY29tcG9uZW50X3N1YnNjcmliZShjb21wb25lbnQsIHN0b3JlLCBjYWxsYmFjaykge1xuICAgIGNvbXBvbmVudC4kJC5vbl9kZXN0cm95LnB1c2goc3Vic2NyaWJlKHN0b3JlLCBjYWxsYmFjaykpO1xufVxuZnVuY3Rpb24gY3JlYXRlX3Nsb3QoZGVmaW5pdGlvbiwgY3R4LCAkJHNjb3BlLCBmbikge1xuICAgIGlmIChkZWZpbml0aW9uKSB7XG4gICAgICAgIGNvbnN0IHNsb3RfY3R4ID0gZ2V0X3Nsb3RfY29udGV4dChkZWZpbml0aW9uLCBjdHgsICQkc2NvcGUsIGZuKTtcbiAgICAgICAgcmV0dXJuIGRlZmluaXRpb25bMF0oc2xvdF9jdHgpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGdldF9zbG90X2NvbnRleHQoZGVmaW5pdGlvbiwgY3R4LCAkJHNjb3BlLCBmbikge1xuICAgIHJldHVybiBkZWZpbml0aW9uWzFdICYmIGZuXG4gICAgICAgID8gYXNzaWduKCQkc2NvcGUuY3R4LnNsaWNlKCksIGRlZmluaXRpb25bMV0oZm4oY3R4KSkpXG4gICAgICAgIDogJCRzY29wZS5jdHg7XG59XG5mdW5jdGlvbiBnZXRfc2xvdF9jaGFuZ2VzKGRlZmluaXRpb24sICQkc2NvcGUsIGRpcnR5LCBmbikge1xuICAgIGlmIChkZWZpbml0aW9uWzJdICYmIGZuKSB7XG4gICAgICAgIGNvbnN0IGxldHMgPSBkZWZpbml0aW9uWzJdKGZuKGRpcnR5KSk7XG4gICAgICAgIGlmICgkJHNjb3BlLmRpcnR5ID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgIHJldHVybiBsZXRzO1xuICAgICAgICB9XG4gICAgICAgIGlmICh0eXBlb2YgbGV0cyA9PT0gJ29iamVjdCcpIHtcbiAgICAgICAgICAgIGNvbnN0IG1lcmdlZCA9IFtdO1xuICAgICAgICAgICAgY29uc3QgbGVuID0gTWF0aC5tYXgoJCRzY29wZS5kaXJ0eS5sZW5ndGgsIGxldHMubGVuZ3RoKTtcbiAgICAgICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgbGVuOyBpICs9IDEpIHtcbiAgICAgICAgICAgICAgICBtZXJnZWRbaV0gPSAkJHNjb3BlLmRpcnR5W2ldIHwgbGV0c1tpXTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBtZXJnZWQ7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuICQkc2NvcGUuZGlydHkgfCBsZXRzO1xuICAgIH1cbiAgICByZXR1cm4gJCRzY29wZS5kaXJ0eTtcbn1cbmZ1bmN0aW9uIHVwZGF0ZV9zbG90X2Jhc2Uoc2xvdCwgc2xvdF9kZWZpbml0aW9uLCBjdHgsICQkc2NvcGUsIHNsb3RfY2hhbmdlcywgZ2V0X3Nsb3RfY29udGV4dF9mbikge1xuICAgIGlmIChzbG90X2NoYW5nZXMpIHtcbiAgICAgICAgY29uc3Qgc2xvdF9jb250ZXh0ID0gZ2V0X3Nsb3RfY29udGV4dChzbG90X2RlZmluaXRpb24sIGN0eCwgJCRzY29wZSwgZ2V0X3Nsb3RfY29udGV4dF9mbik7XG4gICAgICAgIHNsb3QucChzbG90X2NvbnRleHQsIHNsb3RfY2hhbmdlcyk7XG4gICAgfVxufVxuZnVuY3Rpb24gdXBkYXRlX3Nsb3Qoc2xvdCwgc2xvdF9kZWZpbml0aW9uLCBjdHgsICQkc2NvcGUsIGRpcnR5LCBnZXRfc2xvdF9jaGFuZ2VzX2ZuLCBnZXRfc2xvdF9jb250ZXh0X2ZuKSB7XG4gICAgY29uc3Qgc2xvdF9jaGFuZ2VzID0gZ2V0X3Nsb3RfY2hhbmdlcyhzbG90X2RlZmluaXRpb24sICQkc2NvcGUsIGRpcnR5LCBnZXRfc2xvdF9jaGFuZ2VzX2ZuKTtcbiAgICB1cGRhdGVfc2xvdF9iYXNlKHNsb3QsIHNsb3RfZGVmaW5pdGlvbiwgY3R4LCAkJHNjb3BlLCBzbG90X2NoYW5nZXMsIGdldF9zbG90X2NvbnRleHRfZm4pO1xufVxuZnVuY3Rpb24gZ2V0X2FsbF9kaXJ0eV9mcm9tX3Njb3BlKCQkc2NvcGUpIHtcbiAgICBpZiAoJCRzY29wZS5jdHgubGVuZ3RoID4gMzIpIHtcbiAgICAgICAgY29uc3QgZGlydHkgPSBbXTtcbiAgICAgICAgY29uc3QgbGVuZ3RoID0gJCRzY29wZS5jdHgubGVuZ3RoIC8gMzI7XG4gICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgbGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgIGRpcnR5W2ldID0gLTE7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGRpcnR5O1xuICAgIH1cbiAgICByZXR1cm4gLTE7XG59XG5mdW5jdGlvbiBleGNsdWRlX2ludGVybmFsX3Byb3BzKHByb3BzKSB7XG4gICAgY29uc3QgcmVzdWx0ID0ge307XG4gICAgZm9yIChjb25zdCBrIGluIHByb3BzKVxuICAgICAgICBpZiAoa1swXSAhPT0gJyQnKVxuICAgICAgICAgICAgcmVzdWx0W2tdID0gcHJvcHNba107XG4gICAgcmV0dXJuIHJlc3VsdDtcbn1cbmZ1bmN0aW9uIGNvbXB1dGVfcmVzdF9wcm9wcyhwcm9wcywga2V5cykge1xuICAgIGNvbnN0IHJlc3QgPSB7fTtcbiAgICBrZXlzID0gbmV3IFNldChrZXlzKTtcbiAgICBmb3IgKGNvbnN0IGsgaW4gcHJvcHMpXG4gICAgICAgIGlmICgha2V5cy5oYXMoaykgJiYga1swXSAhPT0gJyQnKVxuICAgICAgICAgICAgcmVzdFtrXSA9IHByb3BzW2tdO1xuICAgIHJldHVybiByZXN0O1xufVxuZnVuY3Rpb24gY29tcHV0ZV9zbG90cyhzbG90cykge1xuICAgIGNvbnN0IHJlc3VsdCA9IHt9O1xuICAgIGZvciAoY29uc3Qga2V5IGluIHNsb3RzKSB7XG4gICAgICAgIHJlc3VsdFtrZXldID0gdHJ1ZTtcbiAgICB9XG4gICAgcmV0dXJuIHJlc3VsdDtcbn1cbmZ1bmN0aW9uIG9uY2UoZm4pIHtcbiAgICBsZXQgcmFuID0gZmFsc2U7XG4gICAgcmV0dXJuIGZ1bmN0aW9uICguLi5hcmdzKSB7XG4gICAgICAgIGlmIChyYW4pXG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIHJhbiA9IHRydWU7XG4gICAgICAgIGZuLmNhbGwodGhpcywgLi4uYXJncyk7XG4gICAgfTtcbn1cbmZ1bmN0aW9uIG51bGxfdG9fZW1wdHkodmFsdWUpIHtcbiAgICByZXR1cm4gdmFsdWUgPT0gbnVsbCA/ICcnIDogdmFsdWU7XG59XG5mdW5jdGlvbiBzZXRfc3RvcmVfdmFsdWUoc3RvcmUsIHJldCwgdmFsdWUpIHtcbiAgICBzdG9yZS5zZXQodmFsdWUpO1xuICAgIHJldHVybiByZXQ7XG59XG5jb25zdCBoYXNfcHJvcCA9IChvYmosIHByb3ApID0+IE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmosIHByb3ApO1xuZnVuY3Rpb24gYWN0aW9uX2Rlc3Ryb3llcihhY3Rpb25fcmVzdWx0KSB7XG4gICAgcmV0dXJuIGFjdGlvbl9yZXN1bHQgJiYgaXNfZnVuY3Rpb24oYWN0aW9uX3Jlc3VsdC5kZXN0cm95KSA/IGFjdGlvbl9yZXN1bHQuZGVzdHJveSA6IG5vb3A7XG59XG5cbmNvbnN0IGlzX2NsaWVudCA9IHR5cGVvZiB3aW5kb3cgIT09ICd1bmRlZmluZWQnO1xubGV0IG5vdyA9IGlzX2NsaWVudFxuICAgID8gKCkgPT4gd2luZG93LnBlcmZvcm1hbmNlLm5vdygpXG4gICAgOiAoKSA9PiBEYXRlLm5vdygpO1xubGV0IHJhZiA9IGlzX2NsaWVudCA/IGNiID0+IHJlcXVlc3RBbmltYXRpb25GcmFtZShjYikgOiBub29wO1xuLy8gdXNlZCBpbnRlcm5hbGx5IGZvciB0ZXN0aW5nXG5mdW5jdGlvbiBzZXRfbm93KGZuKSB7XG4gICAgbm93ID0gZm47XG59XG5mdW5jdGlvbiBzZXRfcmFmKGZuKSB7XG4gICAgcmFmID0gZm47XG59XG5cbmNvbnN0IHRhc2tzID0gbmV3IFNldCgpO1xuZnVuY3Rpb24gcnVuX3Rhc2tzKG5vdykge1xuICAgIHRhc2tzLmZvckVhY2godGFzayA9PiB7XG4gICAgICAgIGlmICghdGFzay5jKG5vdykpIHtcbiAgICAgICAgICAgIHRhc2tzLmRlbGV0ZSh0YXNrKTtcbiAgICAgICAgICAgIHRhc2suZigpO1xuICAgICAgICB9XG4gICAgfSk7XG4gICAgaWYgKHRhc2tzLnNpemUgIT09IDApXG4gICAgICAgIHJhZihydW5fdGFza3MpO1xufVxuLyoqXG4gKiBGb3IgdGVzdGluZyBwdXJwb3NlcyBvbmx5IVxuICovXG5mdW5jdGlvbiBjbGVhcl9sb29wcygpIHtcbiAgICB0YXNrcy5jbGVhcigpO1xufVxuLyoqXG4gKiBDcmVhdGVzIGEgbmV3IHRhc2sgdGhhdCBydW5zIG9uIGVhY2ggcmFmIGZyYW1lXG4gKiB1bnRpbCBpdCByZXR1cm5zIGEgZmFsc3kgdmFsdWUgb3IgaXMgYWJvcnRlZFxuICovXG5mdW5jdGlvbiBsb29wKGNhbGxiYWNrKSB7XG4gICAgbGV0IHRhc2s7XG4gICAgaWYgKHRhc2tzLnNpemUgPT09IDApXG4gICAgICAgIHJhZihydW5fdGFza3MpO1xuICAgIHJldHVybiB7XG4gICAgICAgIHByb21pc2U6IG5ldyBQcm9taXNlKGZ1bGZpbGwgPT4ge1xuICAgICAgICAgICAgdGFza3MuYWRkKHRhc2sgPSB7IGM6IGNhbGxiYWNrLCBmOiBmdWxmaWxsIH0pO1xuICAgICAgICB9KSxcbiAgICAgICAgYWJvcnQoKSB7XG4gICAgICAgICAgICB0YXNrcy5kZWxldGUodGFzayk7XG4gICAgICAgIH1cbiAgICB9O1xufVxuXG4vLyBUcmFjayB3aGljaCBub2RlcyBhcmUgY2xhaW1lZCBkdXJpbmcgaHlkcmF0aW9uLiBVbmNsYWltZWQgbm9kZXMgY2FuIHRoZW4gYmUgcmVtb3ZlZCBmcm9tIHRoZSBET01cbi8vIGF0IHRoZSBlbmQgb2YgaHlkcmF0aW9uIHdpdGhvdXQgdG91Y2hpbmcgdGhlIHJlbWFpbmluZyBub2Rlcy5cbmxldCBpc19oeWRyYXRpbmcgPSBmYWxzZTtcbmZ1bmN0aW9uIHN0YXJ0X2h5ZHJhdGluZygpIHtcbiAgICBpc19oeWRyYXRpbmcgPSB0cnVlO1xufVxuZnVuY3Rpb24gZW5kX2h5ZHJhdGluZygpIHtcbiAgICBpc19oeWRyYXRpbmcgPSBmYWxzZTtcbn1cbmZ1bmN0aW9uIHVwcGVyX2JvdW5kKGxvdywgaGlnaCwga2V5LCB2YWx1ZSkge1xuICAgIC8vIFJldHVybiBmaXJzdCBpbmRleCBvZiB2YWx1ZSBsYXJnZXIgdGhhbiBpbnB1dCB2YWx1ZSBpbiB0aGUgcmFuZ2UgW2xvdywgaGlnaClcbiAgICB3aGlsZSAobG93IDwgaGlnaCkge1xuICAgICAgICBjb25zdCBtaWQgPSBsb3cgKyAoKGhpZ2ggLSBsb3cpID4+IDEpO1xuICAgICAgICBpZiAoa2V5KG1pZCkgPD0gdmFsdWUpIHtcbiAgICAgICAgICAgIGxvdyA9IG1pZCArIDE7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICBoaWdoID0gbWlkO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiBsb3c7XG59XG5mdW5jdGlvbiBpbml0X2h5ZHJhdGUodGFyZ2V0KSB7XG4gICAgaWYgKHRhcmdldC5oeWRyYXRlX2luaXQpXG4gICAgICAgIHJldHVybjtcbiAgICB0YXJnZXQuaHlkcmF0ZV9pbml0ID0gdHJ1ZTtcbiAgICAvLyBXZSBrbm93IHRoYXQgYWxsIGNoaWxkcmVuIGhhdmUgY2xhaW1fb3JkZXIgdmFsdWVzIHNpbmNlIHRoZSB1bmNsYWltZWQgaGF2ZSBiZWVuIGRldGFjaGVkIGlmIHRhcmdldCBpcyBub3QgPGhlYWQ+XG4gICAgbGV0IGNoaWxkcmVuID0gdGFyZ2V0LmNoaWxkTm9kZXM7XG4gICAgLy8gSWYgdGFyZ2V0IGlzIDxoZWFkPiwgdGhlcmUgbWF5IGJlIGNoaWxkcmVuIHdpdGhvdXQgY2xhaW1fb3JkZXJcbiAgICBpZiAodGFyZ2V0Lm5vZGVOYW1lID09PSAnSEVBRCcpIHtcbiAgICAgICAgY29uc3QgbXlDaGlsZHJlbiA9IFtdO1xuICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IGNoaWxkcmVuLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBjb25zdCBub2RlID0gY2hpbGRyZW5baV07XG4gICAgICAgICAgICBpZiAobm9kZS5jbGFpbV9vcmRlciAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAgICAgbXlDaGlsZHJlbi5wdXNoKG5vZGUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGNoaWxkcmVuID0gbXlDaGlsZHJlbjtcbiAgICB9XG4gICAgLypcbiAgICAqIFJlb3JkZXIgY2xhaW1lZCBjaGlsZHJlbiBvcHRpbWFsbHkuXG4gICAgKiBXZSBjYW4gcmVvcmRlciBjbGFpbWVkIGNoaWxkcmVuIG9wdGltYWxseSBieSBmaW5kaW5nIHRoZSBsb25nZXN0IHN1YnNlcXVlbmNlIG9mXG4gICAgKiBub2RlcyB0aGF0IGFyZSBhbHJlYWR5IGNsYWltZWQgaW4gb3JkZXIgYW5kIG9ubHkgbW92aW5nIHRoZSByZXN0LiBUaGUgbG9uZ2VzdFxuICAgICogc3Vic2VxdWVuY2Ugc3Vic2VxdWVuY2Ugb2Ygbm9kZXMgdGhhdCBhcmUgY2xhaW1lZCBpbiBvcmRlciBjYW4gYmUgZm91bmQgYnlcbiAgICAqIGNvbXB1dGluZyB0aGUgbG9uZ2VzdCBpbmNyZWFzaW5nIHN1YnNlcXVlbmNlIG9mIC5jbGFpbV9vcmRlciB2YWx1ZXMuXG4gICAgKlxuICAgICogVGhpcyBhbGdvcml0aG0gaXMgb3B0aW1hbCBpbiBnZW5lcmF0aW5nIHRoZSBsZWFzdCBhbW91bnQgb2YgcmVvcmRlciBvcGVyYXRpb25zXG4gICAgKiBwb3NzaWJsZS5cbiAgICAqXG4gICAgKiBQcm9vZjpcbiAgICAqIFdlIGtub3cgdGhhdCwgZ2l2ZW4gYSBzZXQgb2YgcmVvcmRlcmluZyBvcGVyYXRpb25zLCB0aGUgbm9kZXMgdGhhdCBkbyBub3QgbW92ZVxuICAgICogYWx3YXlzIGZvcm0gYW4gaW5jcmVhc2luZyBzdWJzZXF1ZW5jZSwgc2luY2UgdGhleSBkbyBub3QgbW92ZSBhbW9uZyBlYWNoIG90aGVyXG4gICAgKiBtZWFuaW5nIHRoYXQgdGhleSBtdXN0IGJlIGFscmVhZHkgb3JkZXJlZCBhbW9uZyBlYWNoIG90aGVyLiBUaHVzLCB0aGUgbWF4aW1hbFxuICAgICogc2V0IG9mIG5vZGVzIHRoYXQgZG8gbm90IG1vdmUgZm9ybSBhIGxvbmdlc3QgaW5jcmVhc2luZyBzdWJzZXF1ZW5jZS5cbiAgICAqL1xuICAgIC8vIENvbXB1dGUgbG9uZ2VzdCBpbmNyZWFzaW5nIHN1YnNlcXVlbmNlXG4gICAgLy8gbTogc3Vic2VxdWVuY2UgbGVuZ3RoIGogPT4gaW5kZXggayBvZiBzbWFsbGVzdCB2YWx1ZSB0aGF0IGVuZHMgYW4gaW5jcmVhc2luZyBzdWJzZXF1ZW5jZSBvZiBsZW5ndGggalxuICAgIGNvbnN0IG0gPSBuZXcgSW50MzJBcnJheShjaGlsZHJlbi5sZW5ndGggKyAxKTtcbiAgICAvLyBQcmVkZWNlc3NvciBpbmRpY2VzICsgMVxuICAgIGNvbnN0IHAgPSBuZXcgSW50MzJBcnJheShjaGlsZHJlbi5sZW5ndGgpO1xuICAgIG1bMF0gPSAtMTtcbiAgICBsZXQgbG9uZ2VzdCA9IDA7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBjaGlsZHJlbi5sZW5ndGg7IGkrKykge1xuICAgICAgICBjb25zdCBjdXJyZW50ID0gY2hpbGRyZW5baV0uY2xhaW1fb3JkZXI7XG4gICAgICAgIC8vIEZpbmQgdGhlIGxhcmdlc3Qgc3Vic2VxdWVuY2UgbGVuZ3RoIHN1Y2ggdGhhdCBpdCBlbmRzIGluIGEgdmFsdWUgbGVzcyB0aGFuIG91ciBjdXJyZW50IHZhbHVlXG4gICAgICAgIC8vIHVwcGVyX2JvdW5kIHJldHVybnMgZmlyc3QgZ3JlYXRlciB2YWx1ZSwgc28gd2Ugc3VidHJhY3Qgb25lXG4gICAgICAgIC8vIHdpdGggZmFzdCBwYXRoIGZvciB3aGVuIHdlIGFyZSBvbiB0aGUgY3VycmVudCBsb25nZXN0IHN1YnNlcXVlbmNlXG4gICAgICAgIGNvbnN0IHNlcUxlbiA9ICgobG9uZ2VzdCA+IDAgJiYgY2hpbGRyZW5bbVtsb25nZXN0XV0uY2xhaW1fb3JkZXIgPD0gY3VycmVudCkgPyBsb25nZXN0ICsgMSA6IHVwcGVyX2JvdW5kKDEsIGxvbmdlc3QsIGlkeCA9PiBjaGlsZHJlblttW2lkeF1dLmNsYWltX29yZGVyLCBjdXJyZW50KSkgLSAxO1xuICAgICAgICBwW2ldID0gbVtzZXFMZW5dICsgMTtcbiAgICAgICAgY29uc3QgbmV3TGVuID0gc2VxTGVuICsgMTtcbiAgICAgICAgLy8gV2UgY2FuIGd1YXJhbnRlZSB0aGF0IGN1cnJlbnQgaXMgdGhlIHNtYWxsZXN0IHZhbHVlLiBPdGhlcndpc2UsIHdlIHdvdWxkIGhhdmUgZ2VuZXJhdGVkIGEgbG9uZ2VyIHNlcXVlbmNlLlxuICAgICAgICBtW25ld0xlbl0gPSBpO1xuICAgICAgICBsb25nZXN0ID0gTWF0aC5tYXgobmV3TGVuLCBsb25nZXN0KTtcbiAgICB9XG4gICAgLy8gVGhlIGxvbmdlc3QgaW5jcmVhc2luZyBzdWJzZXF1ZW5jZSBvZiBub2RlcyAoaW5pdGlhbGx5IHJldmVyc2VkKVxuICAgIGNvbnN0IGxpcyA9IFtdO1xuICAgIC8vIFRoZSByZXN0IG9mIHRoZSBub2Rlcywgbm9kZXMgdGhhdCB3aWxsIGJlIG1vdmVkXG4gICAgY29uc3QgdG9Nb3ZlID0gW107XG4gICAgbGV0IGxhc3QgPSBjaGlsZHJlbi5sZW5ndGggLSAxO1xuICAgIGZvciAobGV0IGN1ciA9IG1bbG9uZ2VzdF0gKyAxOyBjdXIgIT0gMDsgY3VyID0gcFtjdXIgLSAxXSkge1xuICAgICAgICBsaXMucHVzaChjaGlsZHJlbltjdXIgLSAxXSk7XG4gICAgICAgIGZvciAoOyBsYXN0ID49IGN1cjsgbGFzdC0tKSB7XG4gICAgICAgICAgICB0b01vdmUucHVzaChjaGlsZHJlbltsYXN0XSk7XG4gICAgICAgIH1cbiAgICAgICAgbGFzdC0tO1xuICAgIH1cbiAgICBmb3IgKDsgbGFzdCA+PSAwOyBsYXN0LS0pIHtcbiAgICAgICAgdG9Nb3ZlLnB1c2goY2hpbGRyZW5bbGFzdF0pO1xuICAgIH1cbiAgICBsaXMucmV2ZXJzZSgpO1xuICAgIC8vIFdlIHNvcnQgdGhlIG5vZGVzIGJlaW5nIG1vdmVkIHRvIGd1YXJhbnRlZSB0aGF0IHRoZWlyIGluc2VydGlvbiBvcmRlciBtYXRjaGVzIHRoZSBjbGFpbSBvcmRlclxuICAgIHRvTW92ZS5zb3J0KChhLCBiKSA9PiBhLmNsYWltX29yZGVyIC0gYi5jbGFpbV9vcmRlcik7XG4gICAgLy8gRmluYWxseSwgd2UgbW92ZSB0aGUgbm9kZXNcbiAgICBmb3IgKGxldCBpID0gMCwgaiA9IDA7IGkgPCB0b01vdmUubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgd2hpbGUgKGogPCBsaXMubGVuZ3RoICYmIHRvTW92ZVtpXS5jbGFpbV9vcmRlciA+PSBsaXNbal0uY2xhaW1fb3JkZXIpIHtcbiAgICAgICAgICAgIGorKztcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBhbmNob3IgPSBqIDwgbGlzLmxlbmd0aCA/IGxpc1tqXSA6IG51bGw7XG4gICAgICAgIHRhcmdldC5pbnNlcnRCZWZvcmUodG9Nb3ZlW2ldLCBhbmNob3IpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGFwcGVuZCh0YXJnZXQsIG5vZGUpIHtcbiAgICB0YXJnZXQuYXBwZW5kQ2hpbGQobm9kZSk7XG59XG5mdW5jdGlvbiBhcHBlbmRfc3R5bGVzKHRhcmdldCwgc3R5bGVfc2hlZXRfaWQsIHN0eWxlcykge1xuICAgIGNvbnN0IGFwcGVuZF9zdHlsZXNfdG8gPSBnZXRfcm9vdF9mb3Jfc3R5bGUodGFyZ2V0KTtcbiAgICBpZiAoIWFwcGVuZF9zdHlsZXNfdG8uZ2V0RWxlbWVudEJ5SWQoc3R5bGVfc2hlZXRfaWQpKSB7XG4gICAgICAgIGNvbnN0IHN0eWxlID0gZWxlbWVudCgnc3R5bGUnKTtcbiAgICAgICAgc3R5bGUuaWQgPSBzdHlsZV9zaGVldF9pZDtcbiAgICAgICAgc3R5bGUudGV4dENvbnRlbnQgPSBzdHlsZXM7XG4gICAgICAgIGFwcGVuZF9zdHlsZXNoZWV0KGFwcGVuZF9zdHlsZXNfdG8sIHN0eWxlKTtcbiAgICB9XG59XG5mdW5jdGlvbiBnZXRfcm9vdF9mb3Jfc3R5bGUobm9kZSkge1xuICAgIGlmICghbm9kZSlcbiAgICAgICAgcmV0dXJuIGRvY3VtZW50O1xuICAgIGNvbnN0IHJvb3QgPSBub2RlLmdldFJvb3ROb2RlID8gbm9kZS5nZXRSb290Tm9kZSgpIDogbm9kZS5vd25lckRvY3VtZW50O1xuICAgIGlmIChyb290ICYmIHJvb3QuaG9zdCkge1xuICAgICAgICByZXR1cm4gcm9vdDtcbiAgICB9XG4gICAgcmV0dXJuIG5vZGUub3duZXJEb2N1bWVudDtcbn1cbmZ1bmN0aW9uIGFwcGVuZF9lbXB0eV9zdHlsZXNoZWV0KG5vZGUpIHtcbiAgICBjb25zdCBzdHlsZV9lbGVtZW50ID0gZWxlbWVudCgnc3R5bGUnKTtcbiAgICBhcHBlbmRfc3R5bGVzaGVldChnZXRfcm9vdF9mb3Jfc3R5bGUobm9kZSksIHN0eWxlX2VsZW1lbnQpO1xuICAgIHJldHVybiBzdHlsZV9lbGVtZW50LnNoZWV0O1xufVxuZnVuY3Rpb24gYXBwZW5kX3N0eWxlc2hlZXQobm9kZSwgc3R5bGUpIHtcbiAgICBhcHBlbmQobm9kZS5oZWFkIHx8IG5vZGUsIHN0eWxlKTtcbiAgICByZXR1cm4gc3R5bGUuc2hlZXQ7XG59XG5mdW5jdGlvbiBhcHBlbmRfaHlkcmF0aW9uKHRhcmdldCwgbm9kZSkge1xuICAgIGlmIChpc19oeWRyYXRpbmcpIHtcbiAgICAgICAgaW5pdF9oeWRyYXRlKHRhcmdldCk7XG4gICAgICAgIGlmICgodGFyZ2V0LmFjdHVhbF9lbmRfY2hpbGQgPT09IHVuZGVmaW5lZCkgfHwgKCh0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZCAhPT0gbnVsbCkgJiYgKHRhcmdldC5hY3R1YWxfZW5kX2NoaWxkLnBhcmVudE5vZGUgIT09IHRhcmdldCkpKSB7XG4gICAgICAgICAgICB0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZCA9IHRhcmdldC5maXJzdENoaWxkO1xuICAgICAgICB9XG4gICAgICAgIC8vIFNraXAgbm9kZXMgb2YgdW5kZWZpbmVkIG9yZGVyaW5nXG4gICAgICAgIHdoaWxlICgodGFyZ2V0LmFjdHVhbF9lbmRfY2hpbGQgIT09IG51bGwpICYmICh0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZC5jbGFpbV9vcmRlciA9PT0gdW5kZWZpbmVkKSkge1xuICAgICAgICAgICAgdGFyZ2V0LmFjdHVhbF9lbmRfY2hpbGQgPSB0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZC5uZXh0U2libGluZztcbiAgICAgICAgfVxuICAgICAgICBpZiAobm9kZSAhPT0gdGFyZ2V0LmFjdHVhbF9lbmRfY2hpbGQpIHtcbiAgICAgICAgICAgIC8vIFdlIG9ubHkgaW5zZXJ0IGlmIHRoZSBvcmRlcmluZyBvZiB0aGlzIG5vZGUgc2hvdWxkIGJlIG1vZGlmaWVkIG9yIHRoZSBwYXJlbnQgbm9kZSBpcyBub3QgdGFyZ2V0XG4gICAgICAgICAgICBpZiAobm9kZS5jbGFpbV9vcmRlciAhPT0gdW5kZWZpbmVkIHx8IG5vZGUucGFyZW50Tm9kZSAhPT0gdGFyZ2V0KSB7XG4gICAgICAgICAgICAgICAgdGFyZ2V0Lmluc2VydEJlZm9yZShub2RlLCB0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICB0YXJnZXQuYWN0dWFsX2VuZF9jaGlsZCA9IG5vZGUubmV4dFNpYmxpbmc7XG4gICAgICAgIH1cbiAgICB9XG4gICAgZWxzZSBpZiAobm9kZS5wYXJlbnROb2RlICE9PSB0YXJnZXQgfHwgbm9kZS5uZXh0U2libGluZyAhPT0gbnVsbCkge1xuICAgICAgICB0YXJnZXQuYXBwZW5kQ2hpbGQobm9kZSk7XG4gICAgfVxufVxuZnVuY3Rpb24gaW5zZXJ0KHRhcmdldCwgbm9kZSwgYW5jaG9yKSB7XG4gICAgdGFyZ2V0Lmluc2VydEJlZm9yZShub2RlLCBhbmNob3IgfHwgbnVsbCk7XG59XG5mdW5jdGlvbiBpbnNlcnRfaHlkcmF0aW9uKHRhcmdldCwgbm9kZSwgYW5jaG9yKSB7XG4gICAgaWYgKGlzX2h5ZHJhdGluZyAmJiAhYW5jaG9yKSB7XG4gICAgICAgIGFwcGVuZF9oeWRyYXRpb24odGFyZ2V0LCBub2RlKTtcbiAgICB9XG4gICAgZWxzZSBpZiAobm9kZS5wYXJlbnROb2RlICE9PSB0YXJnZXQgfHwgbm9kZS5uZXh0U2libGluZyAhPSBhbmNob3IpIHtcbiAgICAgICAgdGFyZ2V0Lmluc2VydEJlZm9yZShub2RlLCBhbmNob3IgfHwgbnVsbCk7XG4gICAgfVxufVxuZnVuY3Rpb24gZGV0YWNoKG5vZGUpIHtcbiAgICBub2RlLnBhcmVudE5vZGUucmVtb3ZlQ2hpbGQobm9kZSk7XG59XG5mdW5jdGlvbiBkZXN0cm95X2VhY2goaXRlcmF0aW9ucywgZGV0YWNoaW5nKSB7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBpdGVyYXRpb25zLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgIGlmIChpdGVyYXRpb25zW2ldKVxuICAgICAgICAgICAgaXRlcmF0aW9uc1tpXS5kKGRldGFjaGluZyk7XG4gICAgfVxufVxuZnVuY3Rpb24gZWxlbWVudChuYW1lKSB7XG4gICAgcmV0dXJuIGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQobmFtZSk7XG59XG5mdW5jdGlvbiBlbGVtZW50X2lzKG5hbWUsIGlzKSB7XG4gICAgcmV0dXJuIGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQobmFtZSwgeyBpcyB9KTtcbn1cbmZ1bmN0aW9uIG9iamVjdF93aXRob3V0X3Byb3BlcnRpZXMob2JqLCBleGNsdWRlKSB7XG4gICAgY29uc3QgdGFyZ2V0ID0ge307XG4gICAgZm9yIChjb25zdCBrIGluIG9iaikge1xuICAgICAgICBpZiAoaGFzX3Byb3Aob2JqLCBrKVxuICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgJiYgZXhjbHVkZS5pbmRleE9mKGspID09PSAtMSkge1xuICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgdGFyZ2V0W2tdID0gb2JqW2tdO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiB0YXJnZXQ7XG59XG5mdW5jdGlvbiBzdmdfZWxlbWVudChuYW1lKSB7XG4gICAgcmV0dXJuIGRvY3VtZW50LmNyZWF0ZUVsZW1lbnROUygnaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnLCBuYW1lKTtcbn1cbmZ1bmN0aW9uIHRleHQoZGF0YSkge1xuICAgIHJldHVybiBkb2N1bWVudC5jcmVhdGVUZXh0Tm9kZShkYXRhKTtcbn1cbmZ1bmN0aW9uIHNwYWNlKCkge1xuICAgIHJldHVybiB0ZXh0KCcgJyk7XG59XG5mdW5jdGlvbiBlbXB0eSgpIHtcbiAgICByZXR1cm4gdGV4dCgnJyk7XG59XG5mdW5jdGlvbiBsaXN0ZW4obm9kZSwgZXZlbnQsIGhhbmRsZXIsIG9wdGlvbnMpIHtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoZXZlbnQsIGhhbmRsZXIsIG9wdGlvbnMpO1xuICAgIHJldHVybiAoKSA9PiBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoZXZlbnQsIGhhbmRsZXIsIG9wdGlvbnMpO1xufVxuZnVuY3Rpb24gcHJldmVudF9kZWZhdWx0KGZuKSB7XG4gICAgcmV0dXJuIGZ1bmN0aW9uIChldmVudCkge1xuICAgICAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIHJldHVybiBmbi5jYWxsKHRoaXMsIGV2ZW50KTtcbiAgICB9O1xufVxuZnVuY3Rpb24gc3RvcF9wcm9wYWdhdGlvbihmbikge1xuICAgIHJldHVybiBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgICAgZXZlbnQuc3RvcFByb3BhZ2F0aW9uKCk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgcmV0dXJuIGZuLmNhbGwodGhpcywgZXZlbnQpO1xuICAgIH07XG59XG5mdW5jdGlvbiBzZWxmKGZuKSB7XG4gICAgcmV0dXJuIGZ1bmN0aW9uIChldmVudCkge1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGlmIChldmVudC50YXJnZXQgPT09IHRoaXMpXG4gICAgICAgICAgICBmbi5jYWxsKHRoaXMsIGV2ZW50KTtcbiAgICB9O1xufVxuZnVuY3Rpb24gdHJ1c3RlZChmbikge1xuICAgIHJldHVybiBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICBpZiAoZXZlbnQuaXNUcnVzdGVkKVxuICAgICAgICAgICAgZm4uY2FsbCh0aGlzLCBldmVudCk7XG4gICAgfTtcbn1cbmZ1bmN0aW9uIGF0dHIobm9kZSwgYXR0cmlidXRlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBudWxsKVxuICAgICAgICBub2RlLnJlbW92ZUF0dHJpYnV0ZShhdHRyaWJ1dGUpO1xuICAgIGVsc2UgaWYgKG5vZGUuZ2V0QXR0cmlidXRlKGF0dHJpYnV0ZSkgIT09IHZhbHVlKVxuICAgICAgICBub2RlLnNldEF0dHJpYnV0ZShhdHRyaWJ1dGUsIHZhbHVlKTtcbn1cbmZ1bmN0aW9uIHNldF9hdHRyaWJ1dGVzKG5vZGUsIGF0dHJpYnV0ZXMpIHtcbiAgICAvLyBAdHMtaWdub3JlXG4gICAgY29uc3QgZGVzY3JpcHRvcnMgPSBPYmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9ycyhub2RlLl9fcHJvdG9fXyk7XG4gICAgZm9yIChjb25zdCBrZXkgaW4gYXR0cmlidXRlcykge1xuICAgICAgICBpZiAoYXR0cmlidXRlc1trZXldID09IG51bGwpIHtcbiAgICAgICAgICAgIG5vZGUucmVtb3ZlQXR0cmlidXRlKGtleSk7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoa2V5ID09PSAnc3R5bGUnKSB7XG4gICAgICAgICAgICBub2RlLnN0eWxlLmNzc1RleHQgPSBhdHRyaWJ1dGVzW2tleV07XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoa2V5ID09PSAnX192YWx1ZScpIHtcbiAgICAgICAgICAgIG5vZGUudmFsdWUgPSBub2RlW2tleV0gPSBhdHRyaWJ1dGVzW2tleV07XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoZGVzY3JpcHRvcnNba2V5XSAmJiBkZXNjcmlwdG9yc1trZXldLnNldCkge1xuICAgICAgICAgICAgbm9kZVtrZXldID0gYXR0cmlidXRlc1trZXldO1xuICAgICAgICB9XG4gICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgYXR0cihub2RlLCBrZXksIGF0dHJpYnV0ZXNba2V5XSk7XG4gICAgICAgIH1cbiAgICB9XG59XG5mdW5jdGlvbiBzZXRfc3ZnX2F0dHJpYnV0ZXMobm9kZSwgYXR0cmlidXRlcykge1xuICAgIGZvciAoY29uc3Qga2V5IGluIGF0dHJpYnV0ZXMpIHtcbiAgICAgICAgYXR0cihub2RlLCBrZXksIGF0dHJpYnV0ZXNba2V5XSk7XG4gICAgfVxufVxuZnVuY3Rpb24gc2V0X2N1c3RvbV9lbGVtZW50X2RhdGEobm9kZSwgcHJvcCwgdmFsdWUpIHtcbiAgICBpZiAocHJvcCBpbiBub2RlKSB7XG4gICAgICAgIG5vZGVbcHJvcF0gPSB0eXBlb2Ygbm9kZVtwcm9wXSA9PT0gJ2Jvb2xlYW4nICYmIHZhbHVlID09PSAnJyA/IHRydWUgOiB2YWx1ZTtcbiAgICB9XG4gICAgZWxzZSB7XG4gICAgICAgIGF0dHIobm9kZSwgcHJvcCwgdmFsdWUpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHhsaW5rX2F0dHIobm9kZSwgYXR0cmlidXRlLCB2YWx1ZSkge1xuICAgIG5vZGUuc2V0QXR0cmlidXRlTlMoJ2h0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsnLCBhdHRyaWJ1dGUsIHZhbHVlKTtcbn1cbmZ1bmN0aW9uIGdldF9iaW5kaW5nX2dyb3VwX3ZhbHVlKGdyb3VwLCBfX3ZhbHVlLCBjaGVja2VkKSB7XG4gICAgY29uc3QgdmFsdWUgPSBuZXcgU2V0KCk7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBncm91cC5sZW5ndGg7IGkgKz0gMSkge1xuICAgICAgICBpZiAoZ3JvdXBbaV0uY2hlY2tlZClcbiAgICAgICAgICAgIHZhbHVlLmFkZChncm91cFtpXS5fX3ZhbHVlKTtcbiAgICB9XG4gICAgaWYgKCFjaGVja2VkKSB7XG4gICAgICAgIHZhbHVlLmRlbGV0ZShfX3ZhbHVlKTtcbiAgICB9XG4gICAgcmV0dXJuIEFycmF5LmZyb20odmFsdWUpO1xufVxuZnVuY3Rpb24gdG9fbnVtYmVyKHZhbHVlKSB7XG4gICAgcmV0dXJuIHZhbHVlID09PSAnJyA/IG51bGwgOiArdmFsdWU7XG59XG5mdW5jdGlvbiB0aW1lX3Jhbmdlc190b19hcnJheShyYW5nZXMpIHtcbiAgICBjb25zdCBhcnJheSA9IFtdO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgcmFuZ2VzLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgIGFycmF5LnB1c2goeyBzdGFydDogcmFuZ2VzLnN0YXJ0KGkpLCBlbmQ6IHJhbmdlcy5lbmQoaSkgfSk7XG4gICAgfVxuICAgIHJldHVybiBhcnJheTtcbn1cbmZ1bmN0aW9uIGNoaWxkcmVuKGVsZW1lbnQpIHtcbiAgICByZXR1cm4gQXJyYXkuZnJvbShlbGVtZW50LmNoaWxkTm9kZXMpO1xufVxuZnVuY3Rpb24gaW5pdF9jbGFpbV9pbmZvKG5vZGVzKSB7XG4gICAgaWYgKG5vZGVzLmNsYWltX2luZm8gPT09IHVuZGVmaW5lZCkge1xuICAgICAgICBub2Rlcy5jbGFpbV9pbmZvID0geyBsYXN0X2luZGV4OiAwLCB0b3RhbF9jbGFpbWVkOiAwIH07XG4gICAgfVxufVxuZnVuY3Rpb24gY2xhaW1fbm9kZShub2RlcywgcHJlZGljYXRlLCBwcm9jZXNzTm9kZSwgY3JlYXRlTm9kZSwgZG9udFVwZGF0ZUxhc3RJbmRleCA9IGZhbHNlKSB7XG4gICAgLy8gVHJ5IHRvIGZpbmQgbm9kZXMgaW4gYW4gb3JkZXIgc3VjaCB0aGF0IHdlIGxlbmd0aGVuIHRoZSBsb25nZXN0IGluY3JlYXNpbmcgc3Vic2VxdWVuY2VcbiAgICBpbml0X2NsYWltX2luZm8obm9kZXMpO1xuICAgIGNvbnN0IHJlc3VsdE5vZGUgPSAoKCkgPT4ge1xuICAgICAgICAvLyBXZSBmaXJzdCB0cnkgdG8gZmluZCBhbiBlbGVtZW50IGFmdGVyIHRoZSBwcmV2aW91cyBvbmVcbiAgICAgICAgZm9yIChsZXQgaSA9IG5vZGVzLmNsYWltX2luZm8ubGFzdF9pbmRleDsgaSA8IG5vZGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICBjb25zdCBub2RlID0gbm9kZXNbaV07XG4gICAgICAgICAgICBpZiAocHJlZGljYXRlKG5vZGUpKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgcmVwbGFjZW1lbnQgPSBwcm9jZXNzTm9kZShub2RlKTtcbiAgICAgICAgICAgICAgICBpZiAocmVwbGFjZW1lbnQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgICAgICAgICBub2Rlcy5zcGxpY2UoaSwgMSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICBub2Rlc1tpXSA9IHJlcGxhY2VtZW50O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAoIWRvbnRVcGRhdGVMYXN0SW5kZXgpIHtcbiAgICAgICAgICAgICAgICAgICAgbm9kZXMuY2xhaW1faW5mby5sYXN0X2luZGV4ID0gaTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIG5vZGU7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgLy8gT3RoZXJ3aXNlLCB3ZSB0cnkgdG8gZmluZCBvbmUgYmVmb3JlXG4gICAgICAgIC8vIFdlIGl0ZXJhdGUgaW4gcmV2ZXJzZSBzbyB0aGF0IHdlIGRvbid0IGdvIHRvbyBmYXIgYmFja1xuICAgICAgICBmb3IgKGxldCBpID0gbm9kZXMuY2xhaW1faW5mby5sYXN0X2luZGV4IC0gMTsgaSA+PSAwOyBpLS0pIHtcbiAgICAgICAgICAgIGNvbnN0IG5vZGUgPSBub2Rlc1tpXTtcbiAgICAgICAgICAgIGlmIChwcmVkaWNhdGUobm9kZSkpIHtcbiAgICAgICAgICAgICAgICBjb25zdCByZXBsYWNlbWVudCA9IHByb2Nlc3NOb2RlKG5vZGUpO1xuICAgICAgICAgICAgICAgIGlmIChyZXBsYWNlbWVudCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAgICAgICAgIG5vZGVzLnNwbGljZShpLCAxKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIG5vZGVzW2ldID0gcmVwbGFjZW1lbnQ7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGlmICghZG9udFVwZGF0ZUxhc3RJbmRleCkge1xuICAgICAgICAgICAgICAgICAgICBub2Rlcy5jbGFpbV9pbmZvLmxhc3RfaW5kZXggPSBpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBlbHNlIGlmIChyZXBsYWNlbWVudCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIFNpbmNlIHdlIHNwbGljZWQgYmVmb3JlIHRoZSBsYXN0X2luZGV4LCB3ZSBkZWNyZWFzZSBpdFxuICAgICAgICAgICAgICAgICAgICBub2Rlcy5jbGFpbV9pbmZvLmxhc3RfaW5kZXgtLTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIG5vZGU7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgLy8gSWYgd2UgY2FuJ3QgZmluZCBhbnkgbWF0Y2hpbmcgbm9kZSwgd2UgY3JlYXRlIGEgbmV3IG9uZVxuICAgICAgICByZXR1cm4gY3JlYXRlTm9kZSgpO1xuICAgIH0pKCk7XG4gICAgcmVzdWx0Tm9kZS5jbGFpbV9vcmRlciA9IG5vZGVzLmNsYWltX2luZm8udG90YWxfY2xhaW1lZDtcbiAgICBub2Rlcy5jbGFpbV9pbmZvLnRvdGFsX2NsYWltZWQgKz0gMTtcbiAgICByZXR1cm4gcmVzdWx0Tm9kZTtcbn1cbmZ1bmN0aW9uIGNsYWltX2VsZW1lbnRfYmFzZShub2RlcywgbmFtZSwgYXR0cmlidXRlcywgY3JlYXRlX2VsZW1lbnQpIHtcbiAgICByZXR1cm4gY2xhaW1fbm9kZShub2RlcywgKG5vZGUpID0+IG5vZGUubm9kZU5hbWUgPT09IG5hbWUsIChub2RlKSA9PiB7XG4gICAgICAgIGNvbnN0IHJlbW92ZSA9IFtdO1xuICAgICAgICBmb3IgKGxldCBqID0gMDsgaiA8IG5vZGUuYXR0cmlidXRlcy5sZW5ndGg7IGorKykge1xuICAgICAgICAgICAgY29uc3QgYXR0cmlidXRlID0gbm9kZS5hdHRyaWJ1dGVzW2pdO1xuICAgICAgICAgICAgaWYgKCFhdHRyaWJ1dGVzW2F0dHJpYnV0ZS5uYW1lXSkge1xuICAgICAgICAgICAgICAgIHJlbW92ZS5wdXNoKGF0dHJpYnV0ZS5uYW1lKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICByZW1vdmUuZm9yRWFjaCh2ID0+IG5vZGUucmVtb3ZlQXR0cmlidXRlKHYpKTtcbiAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9LCAoKSA9PiBjcmVhdGVfZWxlbWVudChuYW1lKSk7XG59XG5mdW5jdGlvbiBjbGFpbV9lbGVtZW50KG5vZGVzLCBuYW1lLCBhdHRyaWJ1dGVzKSB7XG4gICAgcmV0dXJuIGNsYWltX2VsZW1lbnRfYmFzZShub2RlcywgbmFtZSwgYXR0cmlidXRlcywgZWxlbWVudCk7XG59XG5mdW5jdGlvbiBjbGFpbV9zdmdfZWxlbWVudChub2RlcywgbmFtZSwgYXR0cmlidXRlcykge1xuICAgIHJldHVybiBjbGFpbV9lbGVtZW50X2Jhc2Uobm9kZXMsIG5hbWUsIGF0dHJpYnV0ZXMsIHN2Z19lbGVtZW50KTtcbn1cbmZ1bmN0aW9uIGNsYWltX3RleHQobm9kZXMsIGRhdGEpIHtcbiAgICByZXR1cm4gY2xhaW1fbm9kZShub2RlcywgKG5vZGUpID0+IG5vZGUubm9kZVR5cGUgPT09IDMsIChub2RlKSA9PiB7XG4gICAgICAgIGNvbnN0IGRhdGFTdHIgPSAnJyArIGRhdGE7XG4gICAgICAgIGlmIChub2RlLmRhdGEuc3RhcnRzV2l0aChkYXRhU3RyKSkge1xuICAgICAgICAgICAgaWYgKG5vZGUuZGF0YS5sZW5ndGggIT09IGRhdGFTdHIubGVuZ3RoKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIG5vZGUuc3BsaXRUZXh0KGRhdGFTdHIubGVuZ3RoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgIG5vZGUuZGF0YSA9IGRhdGFTdHI7XG4gICAgICAgIH1cbiAgICB9LCAoKSA9PiB0ZXh0KGRhdGEpLCB0cnVlIC8vIFRleHQgbm9kZXMgc2hvdWxkIG5vdCB1cGRhdGUgbGFzdCBpbmRleCBzaW5jZSBpdCBpcyBsaWtlbHkgbm90IHdvcnRoIGl0IHRvIGVsaW1pbmF0ZSBhbiBpbmNyZWFzaW5nIHN1YnNlcXVlbmNlIG9mIGFjdHVhbCBlbGVtZW50c1xuICAgICk7XG59XG5mdW5jdGlvbiBjbGFpbV9zcGFjZShub2Rlcykge1xuICAgIHJldHVybiBjbGFpbV90ZXh0KG5vZGVzLCAnICcpO1xufVxuZnVuY3Rpb24gZmluZF9jb21tZW50KG5vZGVzLCB0ZXh0LCBzdGFydCkge1xuICAgIGZvciAobGV0IGkgPSBzdGFydDsgaSA8IG5vZGVzLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgIGNvbnN0IG5vZGUgPSBub2Rlc1tpXTtcbiAgICAgICAgaWYgKG5vZGUubm9kZVR5cGUgPT09IDggLyogY29tbWVudCBub2RlICovICYmIG5vZGUudGV4dENvbnRlbnQudHJpbSgpID09PSB0ZXh0KSB7XG4gICAgICAgICAgICByZXR1cm4gaTtcbiAgICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gbm9kZXMubGVuZ3RoO1xufVxuZnVuY3Rpb24gY2xhaW1faHRtbF90YWcobm9kZXMsIGlzX3N2Zykge1xuICAgIC8vIGZpbmQgaHRtbCBvcGVuaW5nIHRhZ1xuICAgIGNvbnN0IHN0YXJ0X2luZGV4ID0gZmluZF9jb21tZW50KG5vZGVzLCAnSFRNTF9UQUdfU1RBUlQnLCAwKTtcbiAgICBjb25zdCBlbmRfaW5kZXggPSBmaW5kX2NvbW1lbnQobm9kZXMsICdIVE1MX1RBR19FTkQnLCBzdGFydF9pbmRleCk7XG4gICAgaWYgKHN0YXJ0X2luZGV4ID09PSBlbmRfaW5kZXgpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBIdG1sVGFnSHlkcmF0aW9uKHVuZGVmaW5lZCwgaXNfc3ZnKTtcbiAgICB9XG4gICAgaW5pdF9jbGFpbV9pbmZvKG5vZGVzKTtcbiAgICBjb25zdCBodG1sX3RhZ19ub2RlcyA9IG5vZGVzLnNwbGljZShzdGFydF9pbmRleCwgZW5kX2luZGV4IC0gc3RhcnRfaW5kZXggKyAxKTtcbiAgICBkZXRhY2goaHRtbF90YWdfbm9kZXNbMF0pO1xuICAgIGRldGFjaChodG1sX3RhZ19ub2Rlc1todG1sX3RhZ19ub2Rlcy5sZW5ndGggLSAxXSk7XG4gICAgY29uc3QgY2xhaW1lZF9ub2RlcyA9IGh0bWxfdGFnX25vZGVzLnNsaWNlKDEsIGh0bWxfdGFnX25vZGVzLmxlbmd0aCAtIDEpO1xuICAgIGZvciAoY29uc3QgbiBvZiBjbGFpbWVkX25vZGVzKSB7XG4gICAgICAgIG4uY2xhaW1fb3JkZXIgPSBub2Rlcy5jbGFpbV9pbmZvLnRvdGFsX2NsYWltZWQ7XG4gICAgICAgIG5vZGVzLmNsYWltX2luZm8udG90YWxfY2xhaW1lZCArPSAxO1xuICAgIH1cbiAgICByZXR1cm4gbmV3IEh0bWxUYWdIeWRyYXRpb24oY2xhaW1lZF9ub2RlcywgaXNfc3ZnKTtcbn1cbmZ1bmN0aW9uIHNldF9kYXRhKHRleHQsIGRhdGEpIHtcbiAgICBkYXRhID0gJycgKyBkYXRhO1xuICAgIGlmICh0ZXh0Lndob2xlVGV4dCAhPT0gZGF0YSlcbiAgICAgICAgdGV4dC5kYXRhID0gZGF0YTtcbn1cbmZ1bmN0aW9uIHNldF9pbnB1dF92YWx1ZShpbnB1dCwgdmFsdWUpIHtcbiAgICBpbnB1dC52YWx1ZSA9IHZhbHVlID09IG51bGwgPyAnJyA6IHZhbHVlO1xufVxuZnVuY3Rpb24gc2V0X2lucHV0X3R5cGUoaW5wdXQsIHR5cGUpIHtcbiAgICB0cnkge1xuICAgICAgICBpbnB1dC50eXBlID0gdHlwZTtcbiAgICB9XG4gICAgY2F0Y2ggKGUpIHtcbiAgICAgICAgLy8gZG8gbm90aGluZ1xuICAgIH1cbn1cbmZ1bmN0aW9uIHNldF9zdHlsZShub2RlLCBrZXksIHZhbHVlLCBpbXBvcnRhbnQpIHtcbiAgICBpZiAodmFsdWUgPT09IG51bGwpIHtcbiAgICAgICAgbm9kZS5zdHlsZS5yZW1vdmVQcm9wZXJ0eShrZXkpO1xuICAgIH1cbiAgICBlbHNlIHtcbiAgICAgICAgbm9kZS5zdHlsZS5zZXRQcm9wZXJ0eShrZXksIHZhbHVlLCBpbXBvcnRhbnQgPyAnaW1wb3J0YW50JyA6ICcnKTtcbiAgICB9XG59XG5mdW5jdGlvbiBzZWxlY3Rfb3B0aW9uKHNlbGVjdCwgdmFsdWUpIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHNlbGVjdC5vcHRpb25zLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgIGNvbnN0IG9wdGlvbiA9IHNlbGVjdC5vcHRpb25zW2ldO1xuICAgICAgICBpZiAob3B0aW9uLl9fdmFsdWUgPT09IHZhbHVlKSB7XG4gICAgICAgICAgICBvcHRpb24uc2VsZWN0ZWQgPSB0cnVlO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgfVxuICAgIHNlbGVjdC5zZWxlY3RlZEluZGV4ID0gLTE7IC8vIG5vIG9wdGlvbiBzaG91bGQgYmUgc2VsZWN0ZWRcbn1cbmZ1bmN0aW9uIHNlbGVjdF9vcHRpb25zKHNlbGVjdCwgdmFsdWUpIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHNlbGVjdC5vcHRpb25zLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgIGNvbnN0IG9wdGlvbiA9IHNlbGVjdC5vcHRpb25zW2ldO1xuICAgICAgICBvcHRpb24uc2VsZWN0ZWQgPSB+dmFsdWUuaW5kZXhPZihvcHRpb24uX192YWx1ZSk7XG4gICAgfVxufVxuZnVuY3Rpb24gc2VsZWN0X3ZhbHVlKHNlbGVjdCkge1xuICAgIGNvbnN0IHNlbGVjdGVkX29wdGlvbiA9IHNlbGVjdC5xdWVyeVNlbGVjdG9yKCc6Y2hlY2tlZCcpIHx8IHNlbGVjdC5vcHRpb25zWzBdO1xuICAgIHJldHVybiBzZWxlY3RlZF9vcHRpb24gJiYgc2VsZWN0ZWRfb3B0aW9uLl9fdmFsdWU7XG59XG5mdW5jdGlvbiBzZWxlY3RfbXVsdGlwbGVfdmFsdWUoc2VsZWN0KSB7XG4gICAgcmV0dXJuIFtdLm1hcC5jYWxsKHNlbGVjdC5xdWVyeVNlbGVjdG9yQWxsKCc6Y2hlY2tlZCcpLCBvcHRpb24gPT4gb3B0aW9uLl9fdmFsdWUpO1xufVxuLy8gdW5mb3J0dW5hdGVseSB0aGlzIGNhbid0IGJlIGEgY29uc3RhbnQgYXMgdGhhdCB3b3VsZG4ndCBiZSB0cmVlLXNoYWtlYWJsZVxuLy8gc28gd2UgY2FjaGUgdGhlIHJlc3VsdCBpbnN0ZWFkXG5sZXQgY3Jvc3NvcmlnaW47XG5mdW5jdGlvbiBpc19jcm9zc29yaWdpbigpIHtcbiAgICBpZiAoY3Jvc3NvcmlnaW4gPT09IHVuZGVmaW5lZCkge1xuICAgICAgICBjcm9zc29yaWdpbiA9IGZhbHNlO1xuICAgICAgICB0cnkge1xuICAgICAgICAgICAgaWYgKHR5cGVvZiB3aW5kb3cgIT09ICd1bmRlZmluZWQnICYmIHdpbmRvdy5wYXJlbnQpIHtcbiAgICAgICAgICAgICAgICB2b2lkIHdpbmRvdy5wYXJlbnQuZG9jdW1lbnQ7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgICAgICBjcm9zc29yaWdpbiA9IHRydWU7XG4gICAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGNyb3Nzb3JpZ2luO1xufVxuZnVuY3Rpb24gYWRkX3Jlc2l6ZV9saXN0ZW5lcihub2RlLCBmbikge1xuICAgIGNvbnN0IGNvbXB1dGVkX3N0eWxlID0gZ2V0Q29tcHV0ZWRTdHlsZShub2RlKTtcbiAgICBpZiAoY29tcHV0ZWRfc3R5bGUucG9zaXRpb24gPT09ICdzdGF0aWMnKSB7XG4gICAgICAgIG5vZGUuc3R5bGUucG9zaXRpb24gPSAncmVsYXRpdmUnO1xuICAgIH1cbiAgICBjb25zdCBpZnJhbWUgPSBlbGVtZW50KCdpZnJhbWUnKTtcbiAgICBpZnJhbWUuc2V0QXR0cmlidXRlKCdzdHlsZScsICdkaXNwbGF5OiBibG9jazsgcG9zaXRpb246IGFic29sdXRlOyB0b3A6IDA7IGxlZnQ6IDA7IHdpZHRoOiAxMDAlOyBoZWlnaHQ6IDEwMCU7ICcgK1xuICAgICAgICAnb3ZlcmZsb3c6IGhpZGRlbjsgYm9yZGVyOiAwOyBvcGFjaXR5OiAwOyBwb2ludGVyLWV2ZW50czogbm9uZTsgei1pbmRleDogLTE7Jyk7XG4gICAgaWZyYW1lLnNldEF0dHJpYnV0ZSgnYXJpYS1oaWRkZW4nLCAndHJ1ZScpO1xuICAgIGlmcmFtZS50YWJJbmRleCA9IC0xO1xuICAgIGNvbnN0IGNyb3Nzb3JpZ2luID0gaXNfY3Jvc3NvcmlnaW4oKTtcbiAgICBsZXQgdW5zdWJzY3JpYmU7XG4gICAgaWYgKGNyb3Nzb3JpZ2luKSB7XG4gICAgICAgIGlmcmFtZS5zcmMgPSBcImRhdGE6dGV4dC9odG1sLDxzY3JpcHQ+b25yZXNpemU9ZnVuY3Rpb24oKXtwYXJlbnQucG9zdE1lc3NhZ2UoMCwnKicpfTwvc2NyaXB0PlwiO1xuICAgICAgICB1bnN1YnNjcmliZSA9IGxpc3Rlbih3aW5kb3csICdtZXNzYWdlJywgKGV2ZW50KSA9PiB7XG4gICAgICAgICAgICBpZiAoZXZlbnQuc291cmNlID09PSBpZnJhbWUuY29udGVudFdpbmRvdylcbiAgICAgICAgICAgICAgICBmbigpO1xuICAgICAgICB9KTtcbiAgICB9XG4gICAgZWxzZSB7XG4gICAgICAgIGlmcmFtZS5zcmMgPSAnYWJvdXQ6YmxhbmsnO1xuICAgICAgICBpZnJhbWUub25sb2FkID0gKCkgPT4ge1xuICAgICAgICAgICAgdW5zdWJzY3JpYmUgPSBsaXN0ZW4oaWZyYW1lLmNvbnRlbnRXaW5kb3csICdyZXNpemUnLCBmbik7XG4gICAgICAgIH07XG4gICAgfVxuICAgIGFwcGVuZChub2RlLCBpZnJhbWUpO1xuICAgIHJldHVybiAoKSA9PiB7XG4gICAgICAgIGlmIChjcm9zc29yaWdpbikge1xuICAgICAgICAgICAgdW5zdWJzY3JpYmUoKTtcbiAgICAgICAgfVxuICAgICAgICBlbHNlIGlmICh1bnN1YnNjcmliZSAmJiBpZnJhbWUuY29udGVudFdpbmRvdykge1xuICAgICAgICAgICAgdW5zdWJzY3JpYmUoKTtcbiAgICAgICAgfVxuICAgICAgICBkZXRhY2goaWZyYW1lKTtcbiAgICB9O1xufVxuZnVuY3Rpb24gdG9nZ2xlX2NsYXNzKGVsZW1lbnQsIG5hbWUsIHRvZ2dsZSkge1xuICAgIGVsZW1lbnQuY2xhc3NMaXN0W3RvZ2dsZSA/ICdhZGQnIDogJ3JlbW92ZSddKG5hbWUpO1xufVxuZnVuY3Rpb24gY3VzdG9tX2V2ZW50KHR5cGUsIGRldGFpbCwgeyBidWJibGVzID0gZmFsc2UsIGNhbmNlbGFibGUgPSBmYWxzZSB9ID0ge30pIHtcbiAgICBjb25zdCBlID0gZG9jdW1lbnQuY3JlYXRlRXZlbnQoJ0N1c3RvbUV2ZW50Jyk7XG4gICAgZS5pbml0Q3VzdG9tRXZlbnQodHlwZSwgYnViYmxlcywgY2FuY2VsYWJsZSwgZGV0YWlsKTtcbiAgICByZXR1cm4gZTtcbn1cbmZ1bmN0aW9uIHF1ZXJ5X3NlbGVjdG9yX2FsbChzZWxlY3RvciwgcGFyZW50ID0gZG9jdW1lbnQuYm9keSkge1xuICAgIHJldHVybiBBcnJheS5mcm9tKHBhcmVudC5xdWVyeVNlbGVjdG9yQWxsKHNlbGVjdG9yKSk7XG59XG5jbGFzcyBIdG1sVGFnIHtcbiAgICBjb25zdHJ1Y3Rvcihpc19zdmcgPSBmYWxzZSkge1xuICAgICAgICB0aGlzLmlzX3N2ZyA9IGZhbHNlO1xuICAgICAgICB0aGlzLmlzX3N2ZyA9IGlzX3N2ZztcbiAgICAgICAgdGhpcy5lID0gdGhpcy5uID0gbnVsbDtcbiAgICB9XG4gICAgYyhodG1sKSB7XG4gICAgICAgIHRoaXMuaChodG1sKTtcbiAgICB9XG4gICAgbShodG1sLCB0YXJnZXQsIGFuY2hvciA9IG51bGwpIHtcbiAgICAgICAgaWYgKCF0aGlzLmUpIHtcbiAgICAgICAgICAgIGlmICh0aGlzLmlzX3N2ZylcbiAgICAgICAgICAgICAgICB0aGlzLmUgPSBzdmdfZWxlbWVudCh0YXJnZXQubm9kZU5hbWUpO1xuICAgICAgICAgICAgZWxzZVxuICAgICAgICAgICAgICAgIHRoaXMuZSA9IGVsZW1lbnQodGFyZ2V0Lm5vZGVOYW1lKTtcbiAgICAgICAgICAgIHRoaXMudCA9IHRhcmdldDtcbiAgICAgICAgICAgIHRoaXMuYyhodG1sKTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmkoYW5jaG9yKTtcbiAgICB9XG4gICAgaChodG1sKSB7XG4gICAgICAgIHRoaXMuZS5pbm5lckhUTUwgPSBodG1sO1xuICAgICAgICB0aGlzLm4gPSBBcnJheS5mcm9tKHRoaXMuZS5jaGlsZE5vZGVzKTtcbiAgICB9XG4gICAgaShhbmNob3IpIHtcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB0aGlzLm4ubGVuZ3RoOyBpICs9IDEpIHtcbiAgICAgICAgICAgIGluc2VydCh0aGlzLnQsIHRoaXMubltpXSwgYW5jaG9yKTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBwKGh0bWwpIHtcbiAgICAgICAgdGhpcy5kKCk7XG4gICAgICAgIHRoaXMuaChodG1sKTtcbiAgICAgICAgdGhpcy5pKHRoaXMuYSk7XG4gICAgfVxuICAgIGQoKSB7XG4gICAgICAgIHRoaXMubi5mb3JFYWNoKGRldGFjaCk7XG4gICAgfVxufVxuY2xhc3MgSHRtbFRhZ0h5ZHJhdGlvbiBleHRlbmRzIEh0bWxUYWcge1xuICAgIGNvbnN0cnVjdG9yKGNsYWltZWRfbm9kZXMsIGlzX3N2ZyA9IGZhbHNlKSB7XG4gICAgICAgIHN1cGVyKGlzX3N2Zyk7XG4gICAgICAgIHRoaXMuZSA9IHRoaXMubiA9IG51bGw7XG4gICAgICAgIHRoaXMubCA9IGNsYWltZWRfbm9kZXM7XG4gICAgfVxuICAgIGMoaHRtbCkge1xuICAgICAgICBpZiAodGhpcy5sKSB7XG4gICAgICAgICAgICB0aGlzLm4gPSB0aGlzLmw7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICBzdXBlci5jKGh0bWwpO1xuICAgICAgICB9XG4gICAgfVxuICAgIGkoYW5jaG9yKSB7XG4gICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy5uLmxlbmd0aDsgaSArPSAxKSB7XG4gICAgICAgICAgICBpbnNlcnRfaHlkcmF0aW9uKHRoaXMudCwgdGhpcy5uW2ldLCBhbmNob3IpO1xuICAgICAgICB9XG4gICAgfVxufVxuZnVuY3Rpb24gYXR0cmlidXRlX3RvX29iamVjdChhdHRyaWJ1dGVzKSB7XG4gICAgY29uc3QgcmVzdWx0ID0ge307XG4gICAgZm9yIChjb25zdCBhdHRyaWJ1dGUgb2YgYXR0cmlidXRlcykge1xuICAgICAgICByZXN1bHRbYXR0cmlidXRlLm5hbWVdID0gYXR0cmlidXRlLnZhbHVlO1xuICAgIH1cbiAgICByZXR1cm4gcmVzdWx0O1xufVxuZnVuY3Rpb24gZ2V0X2N1c3RvbV9lbGVtZW50c19zbG90cyhlbGVtZW50KSB7XG4gICAgY29uc3QgcmVzdWx0ID0ge307XG4gICAgZWxlbWVudC5jaGlsZE5vZGVzLmZvckVhY2goKG5vZGUpID0+IHtcbiAgICAgICAgcmVzdWx0W25vZGUuc2xvdCB8fCAnZGVmYXVsdCddID0gdHJ1ZTtcbiAgICB9KTtcbiAgICByZXR1cm4gcmVzdWx0O1xufVxuXG4vLyB3ZSBuZWVkIHRvIHN0b3JlIHRoZSBpbmZvcm1hdGlvbiBmb3IgbXVsdGlwbGUgZG9jdW1lbnRzIGJlY2F1c2UgYSBTdmVsdGUgYXBwbGljYXRpb24gY291bGQgYWxzbyBjb250YWluIGlmcmFtZXNcbi8vIGh0dHBzOi8vZ2l0aHViLmNvbS9zdmVsdGVqcy9zdmVsdGUvaXNzdWVzLzM2MjRcbmNvbnN0IG1hbmFnZWRfc3R5bGVzID0gbmV3IE1hcCgpO1xubGV0IGFjdGl2ZSA9IDA7XG4vLyBodHRwczovL2dpdGh1Yi5jb20vZGFya3NreWFwcC9zdHJpbmctaGFzaC9ibG9iL21hc3Rlci9pbmRleC5qc1xuZnVuY3Rpb24gaGFzaChzdHIpIHtcbiAgICBsZXQgaGFzaCA9IDUzODE7XG4gICAgbGV0IGkgPSBzdHIubGVuZ3RoO1xuICAgIHdoaWxlIChpLS0pXG4gICAgICAgIGhhc2ggPSAoKGhhc2ggPDwgNSkgLSBoYXNoKSBeIHN0ci5jaGFyQ29kZUF0KGkpO1xuICAgIHJldHVybiBoYXNoID4+PiAwO1xufVxuZnVuY3Rpb24gY3JlYXRlX3N0eWxlX2luZm9ybWF0aW9uKGRvYywgbm9kZSkge1xuICAgIGNvbnN0IGluZm8gPSB7IHN0eWxlc2hlZXQ6IGFwcGVuZF9lbXB0eV9zdHlsZXNoZWV0KG5vZGUpLCBydWxlczoge30gfTtcbiAgICBtYW5hZ2VkX3N0eWxlcy5zZXQoZG9jLCBpbmZvKTtcbiAgICByZXR1cm4gaW5mbztcbn1cbmZ1bmN0aW9uIGNyZWF0ZV9ydWxlKG5vZGUsIGEsIGIsIGR1cmF0aW9uLCBkZWxheSwgZWFzZSwgZm4sIHVpZCA9IDApIHtcbiAgICBjb25zdCBzdGVwID0gMTYuNjY2IC8gZHVyYXRpb247XG4gICAgbGV0IGtleWZyYW1lcyA9ICd7XFxuJztcbiAgICBmb3IgKGxldCBwID0gMDsgcCA8PSAxOyBwICs9IHN0ZXApIHtcbiAgICAgICAgY29uc3QgdCA9IGEgKyAoYiAtIGEpICogZWFzZShwKTtcbiAgICAgICAga2V5ZnJhbWVzICs9IHAgKiAxMDAgKyBgJXske2ZuKHQsIDEgLSB0KX19XFxuYDtcbiAgICB9XG4gICAgY29uc3QgcnVsZSA9IGtleWZyYW1lcyArIGAxMDAlIHske2ZuKGIsIDEgLSBiKX19XFxufWA7XG4gICAgY29uc3QgbmFtZSA9IGBfX3N2ZWx0ZV8ke2hhc2gocnVsZSl9XyR7dWlkfWA7XG4gICAgY29uc3QgZG9jID0gZ2V0X3Jvb3RfZm9yX3N0eWxlKG5vZGUpO1xuICAgIGNvbnN0IHsgc3R5bGVzaGVldCwgcnVsZXMgfSA9IG1hbmFnZWRfc3R5bGVzLmdldChkb2MpIHx8IGNyZWF0ZV9zdHlsZV9pbmZvcm1hdGlvbihkb2MsIG5vZGUpO1xuICAgIGlmICghcnVsZXNbbmFtZV0pIHtcbiAgICAgICAgcnVsZXNbbmFtZV0gPSB0cnVlO1xuICAgICAgICBzdHlsZXNoZWV0Lmluc2VydFJ1bGUoYEBrZXlmcmFtZXMgJHtuYW1lfSAke3J1bGV9YCwgc3R5bGVzaGVldC5jc3NSdWxlcy5sZW5ndGgpO1xuICAgIH1cbiAgICBjb25zdCBhbmltYXRpb24gPSBub2RlLnN0eWxlLmFuaW1hdGlvbiB8fCAnJztcbiAgICBub2RlLnN0eWxlLmFuaW1hdGlvbiA9IGAke2FuaW1hdGlvbiA/IGAke2FuaW1hdGlvbn0sIGAgOiAnJ30ke25hbWV9ICR7ZHVyYXRpb259bXMgbGluZWFyICR7ZGVsYXl9bXMgMSBib3RoYDtcbiAgICBhY3RpdmUgKz0gMTtcbiAgICByZXR1cm4gbmFtZTtcbn1cbmZ1bmN0aW9uIGRlbGV0ZV9ydWxlKG5vZGUsIG5hbWUpIHtcbiAgICBjb25zdCBwcmV2aW91cyA9IChub2RlLnN0eWxlLmFuaW1hdGlvbiB8fCAnJykuc3BsaXQoJywgJyk7XG4gICAgY29uc3QgbmV4dCA9IHByZXZpb3VzLmZpbHRlcihuYW1lXG4gICAgICAgID8gYW5pbSA9PiBhbmltLmluZGV4T2YobmFtZSkgPCAwIC8vIHJlbW92ZSBzcGVjaWZpYyBhbmltYXRpb25cbiAgICAgICAgOiBhbmltID0+IGFuaW0uaW5kZXhPZignX19zdmVsdGUnKSA9PT0gLTEgLy8gcmVtb3ZlIGFsbCBTdmVsdGUgYW5pbWF0aW9uc1xuICAgICk7XG4gICAgY29uc3QgZGVsZXRlZCA9IHByZXZpb3VzLmxlbmd0aCAtIG5leHQubGVuZ3RoO1xuICAgIGlmIChkZWxldGVkKSB7XG4gICAgICAgIG5vZGUuc3R5bGUuYW5pbWF0aW9uID0gbmV4dC5qb2luKCcsICcpO1xuICAgICAgICBhY3RpdmUgLT0gZGVsZXRlZDtcbiAgICAgICAgaWYgKCFhY3RpdmUpXG4gICAgICAgICAgICBjbGVhcl9ydWxlcygpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGNsZWFyX3J1bGVzKCkge1xuICAgIHJhZigoKSA9PiB7XG4gICAgICAgIGlmIChhY3RpdmUpXG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIG1hbmFnZWRfc3R5bGVzLmZvckVhY2goaW5mbyA9PiB7XG4gICAgICAgICAgICBjb25zdCB7IG93bmVyTm9kZSB9ID0gaW5mby5zdHlsZXNoZWV0O1xuICAgICAgICAgICAgLy8gdGhlcmUgaXMgbm8gb3duZXJOb2RlIGlmIGl0IHJ1bnMgb24ganNkb20uXG4gICAgICAgICAgICBpZiAob3duZXJOb2RlKVxuICAgICAgICAgICAgICAgIGRldGFjaChvd25lck5vZGUpO1xuICAgICAgICB9KTtcbiAgICAgICAgbWFuYWdlZF9zdHlsZXMuY2xlYXIoKTtcbiAgICB9KTtcbn1cblxuZnVuY3Rpb24gY3JlYXRlX2FuaW1hdGlvbihub2RlLCBmcm9tLCBmbiwgcGFyYW1zKSB7XG4gICAgaWYgKCFmcm9tKVxuICAgICAgICByZXR1cm4gbm9vcDtcbiAgICBjb25zdCB0byA9IG5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG4gICAgaWYgKGZyb20ubGVmdCA9PT0gdG8ubGVmdCAmJiBmcm9tLnJpZ2h0ID09PSB0by5yaWdodCAmJiBmcm9tLnRvcCA9PT0gdG8udG9wICYmIGZyb20uYm90dG9tID09PSB0by5ib3R0b20pXG4gICAgICAgIHJldHVybiBub29wO1xuICAgIGNvbnN0IHsgZGVsYXkgPSAwLCBkdXJhdGlvbiA9IDMwMCwgZWFzaW5nID0gaWRlbnRpdHksIFxuICAgIC8vIEB0cy1pZ25vcmUgdG9kbzogc2hvdWxkIHRoaXMgYmUgc2VwYXJhdGVkIGZyb20gZGVzdHJ1Y3R1cmluZz8gT3Igc3RhcnQvZW5kIGFkZGVkIHRvIHB1YmxpYyBhcGkgYW5kIGRvY3VtZW50YXRpb24/XG4gICAgc3RhcnQ6IHN0YXJ0X3RpbWUgPSBub3coKSArIGRlbGF5LCBcbiAgICAvLyBAdHMtaWdub3JlIHRvZG86XG4gICAgZW5kID0gc3RhcnRfdGltZSArIGR1cmF0aW9uLCB0aWNrID0gbm9vcCwgY3NzIH0gPSBmbihub2RlLCB7IGZyb20sIHRvIH0sIHBhcmFtcyk7XG4gICAgbGV0IHJ1bm5pbmcgPSB0cnVlO1xuICAgIGxldCBzdGFydGVkID0gZmFsc2U7XG4gICAgbGV0IG5hbWU7XG4gICAgZnVuY3Rpb24gc3RhcnQoKSB7XG4gICAgICAgIGlmIChjc3MpIHtcbiAgICAgICAgICAgIG5hbWUgPSBjcmVhdGVfcnVsZShub2RlLCAwLCAxLCBkdXJhdGlvbiwgZGVsYXksIGVhc2luZywgY3NzKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoIWRlbGF5KSB7XG4gICAgICAgICAgICBzdGFydGVkID0gdHJ1ZTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBmdW5jdGlvbiBzdG9wKCkge1xuICAgICAgICBpZiAoY3NzKVxuICAgICAgICAgICAgZGVsZXRlX3J1bGUobm9kZSwgbmFtZSk7XG4gICAgICAgIHJ1bm5pbmcgPSBmYWxzZTtcbiAgICB9XG4gICAgbG9vcChub3cgPT4ge1xuICAgICAgICBpZiAoIXN0YXJ0ZWQgJiYgbm93ID49IHN0YXJ0X3RpbWUpIHtcbiAgICAgICAgICAgIHN0YXJ0ZWQgPSB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdGFydGVkICYmIG5vdyA+PSBlbmQpIHtcbiAgICAgICAgICAgIHRpY2soMSwgMCk7XG4gICAgICAgICAgICBzdG9wKCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKCFydW5uaW5nKSB7XG4gICAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHN0YXJ0ZWQpIHtcbiAgICAgICAgICAgIGNvbnN0IHAgPSBub3cgLSBzdGFydF90aW1lO1xuICAgICAgICAgICAgY29uc3QgdCA9IDAgKyAxICogZWFzaW5nKHAgLyBkdXJhdGlvbik7XG4gICAgICAgICAgICB0aWNrKHQsIDEgLSB0KTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9KTtcbiAgICBzdGFydCgpO1xuICAgIHRpY2soMCwgMSk7XG4gICAgcmV0dXJuIHN0b3A7XG59XG5mdW5jdGlvbiBmaXhfcG9zaXRpb24obm9kZSkge1xuICAgIGNvbnN0IHN0eWxlID0gZ2V0Q29tcHV0ZWRTdHlsZShub2RlKTtcbiAgICBpZiAoc3R5bGUucG9zaXRpb24gIT09ICdhYnNvbHV0ZScgJiYgc3R5bGUucG9zaXRpb24gIT09ICdmaXhlZCcpIHtcbiAgICAgICAgY29uc3QgeyB3aWR0aCwgaGVpZ2h0IH0gPSBzdHlsZTtcbiAgICAgICAgY29uc3QgYSA9IG5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG4gICAgICAgIG5vZGUuc3R5bGUucG9zaXRpb24gPSAnYWJzb2x1dGUnO1xuICAgICAgICBub2RlLnN0eWxlLndpZHRoID0gd2lkdGg7XG4gICAgICAgIG5vZGUuc3R5bGUuaGVpZ2h0ID0gaGVpZ2h0O1xuICAgICAgICBhZGRfdHJhbnNmb3JtKG5vZGUsIGEpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGFkZF90cmFuc2Zvcm0obm9kZSwgYSkge1xuICAgIGNvbnN0IGIgPSBub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuICAgIGlmIChhLmxlZnQgIT09IGIubGVmdCB8fCBhLnRvcCAhPT0gYi50b3ApIHtcbiAgICAgICAgY29uc3Qgc3R5bGUgPSBnZXRDb21wdXRlZFN0eWxlKG5vZGUpO1xuICAgICAgICBjb25zdCB0cmFuc2Zvcm0gPSBzdHlsZS50cmFuc2Zvcm0gPT09ICdub25lJyA/ICcnIDogc3R5bGUudHJhbnNmb3JtO1xuICAgICAgICBub2RlLnN0eWxlLnRyYW5zZm9ybSA9IGAke3RyYW5zZm9ybX0gdHJhbnNsYXRlKCR7YS5sZWZ0IC0gYi5sZWZ0fXB4LCAke2EudG9wIC0gYi50b3B9cHgpYDtcbiAgICB9XG59XG5cbmxldCBjdXJyZW50X2NvbXBvbmVudDtcbmZ1bmN0aW9uIHNldF9jdXJyZW50X2NvbXBvbmVudChjb21wb25lbnQpIHtcbiAgICBjdXJyZW50X2NvbXBvbmVudCA9IGNvbXBvbmVudDtcbn1cbmZ1bmN0aW9uIGdldF9jdXJyZW50X2NvbXBvbmVudCgpIHtcbiAgICBpZiAoIWN1cnJlbnRfY29tcG9uZW50KVxuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ0Z1bmN0aW9uIGNhbGxlZCBvdXRzaWRlIGNvbXBvbmVudCBpbml0aWFsaXphdGlvbicpO1xuICAgIHJldHVybiBjdXJyZW50X2NvbXBvbmVudDtcbn1cbmZ1bmN0aW9uIGJlZm9yZVVwZGF0ZShmbikge1xuICAgIGdldF9jdXJyZW50X2NvbXBvbmVudCgpLiQkLmJlZm9yZV91cGRhdGUucHVzaChmbik7XG59XG5mdW5jdGlvbiBvbk1vdW50KGZuKSB7XG4gICAgZ2V0X2N1cnJlbnRfY29tcG9uZW50KCkuJCQub25fbW91bnQucHVzaChmbik7XG59XG5mdW5jdGlvbiBhZnRlclVwZGF0ZShmbikge1xuICAgIGdldF9jdXJyZW50X2NvbXBvbmVudCgpLiQkLmFmdGVyX3VwZGF0ZS5wdXNoKGZuKTtcbn1cbmZ1bmN0aW9uIG9uRGVzdHJveShmbikge1xuICAgIGdldF9jdXJyZW50X2NvbXBvbmVudCgpLiQkLm9uX2Rlc3Ryb3kucHVzaChmbik7XG59XG5mdW5jdGlvbiBjcmVhdGVFdmVudERpc3BhdGNoZXIoKSB7XG4gICAgY29uc3QgY29tcG9uZW50ID0gZ2V0X2N1cnJlbnRfY29tcG9uZW50KCk7XG4gICAgcmV0dXJuICh0eXBlLCBkZXRhaWwsIHsgY2FuY2VsYWJsZSA9IGZhbHNlIH0gPSB7fSkgPT4ge1xuICAgICAgICBjb25zdCBjYWxsYmFja3MgPSBjb21wb25lbnQuJCQuY2FsbGJhY2tzW3R5cGVdO1xuICAgICAgICBpZiAoY2FsbGJhY2tzKSB7XG4gICAgICAgICAgICAvLyBUT0RPIGFyZSB0aGVyZSBzaXR1YXRpb25zIHdoZXJlIGV2ZW50cyBjb3VsZCBiZSBkaXNwYXRjaGVkXG4gICAgICAgICAgICAvLyBpbiBhIHNlcnZlciAobm9uLURPTSkgZW52aXJvbm1lbnQ/XG4gICAgICAgICAgICBjb25zdCBldmVudCA9IGN1c3RvbV9ldmVudCh0eXBlLCBkZXRhaWwsIHsgY2FuY2VsYWJsZSB9KTtcbiAgICAgICAgICAgIGNhbGxiYWNrcy5zbGljZSgpLmZvckVhY2goZm4gPT4ge1xuICAgICAgICAgICAgICAgIGZuLmNhbGwoY29tcG9uZW50LCBldmVudCk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIHJldHVybiAhZXZlbnQuZGVmYXVsdFByZXZlbnRlZDtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9O1xufVxuZnVuY3Rpb24gc2V0Q29udGV4dChrZXksIGNvbnRleHQpIHtcbiAgICBnZXRfY3VycmVudF9jb21wb25lbnQoKS4kJC5jb250ZXh0LnNldChrZXksIGNvbnRleHQpO1xuICAgIHJldHVybiBjb250ZXh0O1xufVxuZnVuY3Rpb24gZ2V0Q29udGV4dChrZXkpIHtcbiAgICByZXR1cm4gZ2V0X2N1cnJlbnRfY29tcG9uZW50KCkuJCQuY29udGV4dC5nZXQoa2V5KTtcbn1cbmZ1bmN0aW9uIGdldEFsbENvbnRleHRzKCkge1xuICAgIHJldHVybiBnZXRfY3VycmVudF9jb21wb25lbnQoKS4kJC5jb250ZXh0O1xufVxuZnVuY3Rpb24gaGFzQ29udGV4dChrZXkpIHtcbiAgICByZXR1cm4gZ2V0X2N1cnJlbnRfY29tcG9uZW50KCkuJCQuY29udGV4dC5oYXMoa2V5KTtcbn1cbi8vIFRPRE8gZmlndXJlIG91dCBpZiB3ZSBzdGlsbCB3YW50IHRvIHN1cHBvcnRcbi8vIHNob3J0aGFuZCBldmVudHMsIG9yIGlmIHdlIHdhbnQgdG8gaW1wbGVtZW50XG4vLyBhIHJlYWwgYnViYmxpbmcgbWVjaGFuaXNtXG5mdW5jdGlvbiBidWJibGUoY29tcG9uZW50LCBldmVudCkge1xuICAgIGNvbnN0IGNhbGxiYWNrcyA9IGNvbXBvbmVudC4kJC5jYWxsYmFja3NbZXZlbnQudHlwZV07XG4gICAgaWYgKGNhbGxiYWNrcykge1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGNhbGxiYWNrcy5zbGljZSgpLmZvckVhY2goZm4gPT4gZm4uY2FsbCh0aGlzLCBldmVudCkpO1xuICAgIH1cbn1cblxuY29uc3QgZGlydHlfY29tcG9uZW50cyA9IFtdO1xuY29uc3QgaW50cm9zID0geyBlbmFibGVkOiBmYWxzZSB9O1xuY29uc3QgYmluZGluZ19jYWxsYmFja3MgPSBbXTtcbmNvbnN0IHJlbmRlcl9jYWxsYmFja3MgPSBbXTtcbmNvbnN0IGZsdXNoX2NhbGxiYWNrcyA9IFtdO1xuY29uc3QgcmVzb2x2ZWRfcHJvbWlzZSA9IFByb21pc2UucmVzb2x2ZSgpO1xubGV0IHVwZGF0ZV9zY2hlZHVsZWQgPSBmYWxzZTtcbmZ1bmN0aW9uIHNjaGVkdWxlX3VwZGF0ZSgpIHtcbiAgICBpZiAoIXVwZGF0ZV9zY2hlZHVsZWQpIHtcbiAgICAgICAgdXBkYXRlX3NjaGVkdWxlZCA9IHRydWU7XG4gICAgICAgIHJlc29sdmVkX3Byb21pc2UudGhlbihmbHVzaCk7XG4gICAgfVxufVxuZnVuY3Rpb24gdGljaygpIHtcbiAgICBzY2hlZHVsZV91cGRhdGUoKTtcbiAgICByZXR1cm4gcmVzb2x2ZWRfcHJvbWlzZTtcbn1cbmZ1bmN0aW9uIGFkZF9yZW5kZXJfY2FsbGJhY2soZm4pIHtcbiAgICByZW5kZXJfY2FsbGJhY2tzLnB1c2goZm4pO1xufVxuZnVuY3Rpb24gYWRkX2ZsdXNoX2NhbGxiYWNrKGZuKSB7XG4gICAgZmx1c2hfY2FsbGJhY2tzLnB1c2goZm4pO1xufVxuLy8gZmx1c2goKSBjYWxscyBjYWxsYmFja3MgaW4gdGhpcyBvcmRlcjpcbi8vIDEuIEFsbCBiZWZvcmVVcGRhdGUgY2FsbGJhY2tzLCBpbiBvcmRlcjogcGFyZW50cyBiZWZvcmUgY2hpbGRyZW5cbi8vIDIuIEFsbCBiaW5kOnRoaXMgY2FsbGJhY2tzLCBpbiByZXZlcnNlIG9yZGVyOiBjaGlsZHJlbiBiZWZvcmUgcGFyZW50cy5cbi8vIDMuIEFsbCBhZnRlclVwZGF0ZSBjYWxsYmFja3MsIGluIG9yZGVyOiBwYXJlbnRzIGJlZm9yZSBjaGlsZHJlbi4gRVhDRVBUXG4vLyAgICBmb3IgYWZ0ZXJVcGRhdGVzIGNhbGxlZCBkdXJpbmcgdGhlIGluaXRpYWwgb25Nb3VudCwgd2hpY2ggYXJlIGNhbGxlZCBpblxuLy8gICAgcmV2ZXJzZSBvcmRlcjogY2hpbGRyZW4gYmVmb3JlIHBhcmVudHMuXG4vLyBTaW5jZSBjYWxsYmFja3MgbWlnaHQgdXBkYXRlIGNvbXBvbmVudCB2YWx1ZXMsIHdoaWNoIGNvdWxkIHRyaWdnZXIgYW5vdGhlclxuLy8gY2FsbCB0byBmbHVzaCgpLCB0aGUgZm9sbG93aW5nIHN0ZXBzIGd1YXJkIGFnYWluc3QgdGhpczpcbi8vIDEuIER1cmluZyBiZWZvcmVVcGRhdGUsIGFueSB1cGRhdGVkIGNvbXBvbmVudHMgd2lsbCBiZSBhZGRlZCB0byB0aGVcbi8vICAgIGRpcnR5X2NvbXBvbmVudHMgYXJyYXkgYW5kIHdpbGwgY2F1c2UgYSByZWVudHJhbnQgY2FsbCB0byBmbHVzaCgpLiBCZWNhdXNlXG4vLyAgICB0aGUgZmx1c2ggaW5kZXggaXMga2VwdCBvdXRzaWRlIHRoZSBmdW5jdGlvbiwgdGhlIHJlZW50cmFudCBjYWxsIHdpbGwgcGlja1xuLy8gICAgdXAgd2hlcmUgdGhlIGVhcmxpZXIgY2FsbCBsZWZ0IG9mZiBhbmQgZ28gdGhyb3VnaCBhbGwgZGlydHkgY29tcG9uZW50cy4gVGhlXG4vLyAgICBjdXJyZW50X2NvbXBvbmVudCB2YWx1ZSBpcyBzYXZlZCBhbmQgcmVzdG9yZWQgc28gdGhhdCB0aGUgcmVlbnRyYW50IGNhbGwgd2lsbFxuLy8gICAgbm90IGludGVyZmVyZSB3aXRoIHRoZSBcInBhcmVudFwiIGZsdXNoKCkgY2FsbC5cbi8vIDIuIGJpbmQ6dGhpcyBjYWxsYmFja3MgY2Fubm90IHRyaWdnZXIgbmV3IGZsdXNoKCkgY2FsbHMuXG4vLyAzLiBEdXJpbmcgYWZ0ZXJVcGRhdGUsIGFueSB1cGRhdGVkIGNvbXBvbmVudHMgd2lsbCBOT1QgaGF2ZSB0aGVpciBhZnRlclVwZGF0ZVxuLy8gICAgY2FsbGJhY2sgY2FsbGVkIGEgc2Vjb25kIHRpbWU7IHRoZSBzZWVuX2NhbGxiYWNrcyBzZXQsIG91dHNpZGUgdGhlIGZsdXNoKClcbi8vICAgIGZ1bmN0aW9uLCBndWFyYW50ZWVzIHRoaXMgYmVoYXZpb3IuXG5jb25zdCBzZWVuX2NhbGxiYWNrcyA9IG5ldyBTZXQoKTtcbmxldCBmbHVzaGlkeCA9IDA7IC8vIERvICpub3QqIG1vdmUgdGhpcyBpbnNpZGUgdGhlIGZsdXNoKCkgZnVuY3Rpb25cbmZ1bmN0aW9uIGZsdXNoKCkge1xuICAgIGNvbnN0IHNhdmVkX2NvbXBvbmVudCA9IGN1cnJlbnRfY29tcG9uZW50O1xuICAgIGRvIHtcbiAgICAgICAgLy8gZmlyc3QsIGNhbGwgYmVmb3JlVXBkYXRlIGZ1bmN0aW9uc1xuICAgICAgICAvLyBhbmQgdXBkYXRlIGNvbXBvbmVudHNcbiAgICAgICAgd2hpbGUgKGZsdXNoaWR4IDwgZGlydHlfY29tcG9uZW50cy5sZW5ndGgpIHtcbiAgICAgICAgICAgIGNvbnN0IGNvbXBvbmVudCA9IGRpcnR5X2NvbXBvbmVudHNbZmx1c2hpZHhdO1xuICAgICAgICAgICAgZmx1c2hpZHgrKztcbiAgICAgICAgICAgIHNldF9jdXJyZW50X2NvbXBvbmVudChjb21wb25lbnQpO1xuICAgICAgICAgICAgdXBkYXRlKGNvbXBvbmVudC4kJCk7XG4gICAgICAgIH1cbiAgICAgICAgc2V0X2N1cnJlbnRfY29tcG9uZW50KG51bGwpO1xuICAgICAgICBkaXJ0eV9jb21wb25lbnRzLmxlbmd0aCA9IDA7XG4gICAgICAgIGZsdXNoaWR4ID0gMDtcbiAgICAgICAgd2hpbGUgKGJpbmRpbmdfY2FsbGJhY2tzLmxlbmd0aClcbiAgICAgICAgICAgIGJpbmRpbmdfY2FsbGJhY2tzLnBvcCgpKCk7XG4gICAgICAgIC8vIHRoZW4sIG9uY2UgY29tcG9uZW50cyBhcmUgdXBkYXRlZCwgY2FsbFxuICAgICAgICAvLyBhZnRlclVwZGF0ZSBmdW5jdGlvbnMuIFRoaXMgbWF5IGNhdXNlXG4gICAgICAgIC8vIHN1YnNlcXVlbnQgdXBkYXRlcy4uLlxuICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHJlbmRlcl9jYWxsYmFja3MubGVuZ3RoOyBpICs9IDEpIHtcbiAgICAgICAgICAgIGNvbnN0IGNhbGxiYWNrID0gcmVuZGVyX2NhbGxiYWNrc1tpXTtcbiAgICAgICAgICAgIGlmICghc2Vlbl9jYWxsYmFja3MuaGFzKGNhbGxiYWNrKSkge1xuICAgICAgICAgICAgICAgIC8vIC4uLnNvIGd1YXJkIGFnYWluc3QgaW5maW5pdGUgbG9vcHNcbiAgICAgICAgICAgICAgICBzZWVuX2NhbGxiYWNrcy5hZGQoY2FsbGJhY2spO1xuICAgICAgICAgICAgICAgIGNhbGxiYWNrKCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgcmVuZGVyX2NhbGxiYWNrcy5sZW5ndGggPSAwO1xuICAgIH0gd2hpbGUgKGRpcnR5X2NvbXBvbmVudHMubGVuZ3RoKTtcbiAgICB3aGlsZSAoZmx1c2hfY2FsbGJhY2tzLmxlbmd0aCkge1xuICAgICAgICBmbHVzaF9jYWxsYmFja3MucG9wKCkoKTtcbiAgICB9XG4gICAgdXBkYXRlX3NjaGVkdWxlZCA9IGZhbHNlO1xuICAgIHNlZW5fY2FsbGJhY2tzLmNsZWFyKCk7XG4gICAgc2V0X2N1cnJlbnRfY29tcG9uZW50KHNhdmVkX2NvbXBvbmVudCk7XG59XG5mdW5jdGlvbiB1cGRhdGUoJCQpIHtcbiAgICBpZiAoJCQuZnJhZ21lbnQgIT09IG51bGwpIHtcbiAgICAgICAgJCQudXBkYXRlKCk7XG4gICAgICAgIHJ1bl9hbGwoJCQuYmVmb3JlX3VwZGF0ZSk7XG4gICAgICAgIGNvbnN0IGRpcnR5ID0gJCQuZGlydHk7XG4gICAgICAgICQkLmRpcnR5ID0gWy0xXTtcbiAgICAgICAgJCQuZnJhZ21lbnQgJiYgJCQuZnJhZ21lbnQucCgkJC5jdHgsIGRpcnR5KTtcbiAgICAgICAgJCQuYWZ0ZXJfdXBkYXRlLmZvckVhY2goYWRkX3JlbmRlcl9jYWxsYmFjayk7XG4gICAgfVxufVxuXG5sZXQgcHJvbWlzZTtcbmZ1bmN0aW9uIHdhaXQoKSB7XG4gICAgaWYgKCFwcm9taXNlKSB7XG4gICAgICAgIHByb21pc2UgPSBQcm9taXNlLnJlc29sdmUoKTtcbiAgICAgICAgcHJvbWlzZS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgIHByb21pc2UgPSBudWxsO1xuICAgICAgICB9KTtcbiAgICB9XG4gICAgcmV0dXJuIHByb21pc2U7XG59XG5mdW5jdGlvbiBkaXNwYXRjaChub2RlLCBkaXJlY3Rpb24sIGtpbmQpIHtcbiAgICBub2RlLmRpc3BhdGNoRXZlbnQoY3VzdG9tX2V2ZW50KGAke2RpcmVjdGlvbiA/ICdpbnRybycgOiAnb3V0cm8nfSR7a2luZH1gKSk7XG59XG5jb25zdCBvdXRyb2luZyA9IG5ldyBTZXQoKTtcbmxldCBvdXRyb3M7XG5mdW5jdGlvbiBncm91cF9vdXRyb3MoKSB7XG4gICAgb3V0cm9zID0ge1xuICAgICAgICByOiAwLFxuICAgICAgICBjOiBbXSxcbiAgICAgICAgcDogb3V0cm9zIC8vIHBhcmVudCBncm91cFxuICAgIH07XG59XG5mdW5jdGlvbiBjaGVja19vdXRyb3MoKSB7XG4gICAgaWYgKCFvdXRyb3Mucikge1xuICAgICAgICBydW5fYWxsKG91dHJvcy5jKTtcbiAgICB9XG4gICAgb3V0cm9zID0gb3V0cm9zLnA7XG59XG5mdW5jdGlvbiB0cmFuc2l0aW9uX2luKGJsb2NrLCBsb2NhbCkge1xuICAgIGlmIChibG9jayAmJiBibG9jay5pKSB7XG4gICAgICAgIG91dHJvaW5nLmRlbGV0ZShibG9jayk7XG4gICAgICAgIGJsb2NrLmkobG9jYWwpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHRyYW5zaXRpb25fb3V0KGJsb2NrLCBsb2NhbCwgZGV0YWNoLCBjYWxsYmFjaykge1xuICAgIGlmIChibG9jayAmJiBibG9jay5vKSB7XG4gICAgICAgIGlmIChvdXRyb2luZy5oYXMoYmxvY2spKVxuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICBvdXRyb2luZy5hZGQoYmxvY2spO1xuICAgICAgICBvdXRyb3MuYy5wdXNoKCgpID0+IHtcbiAgICAgICAgICAgIG91dHJvaW5nLmRlbGV0ZShibG9jayk7XG4gICAgICAgICAgICBpZiAoY2FsbGJhY2spIHtcbiAgICAgICAgICAgICAgICBpZiAoZGV0YWNoKVxuICAgICAgICAgICAgICAgICAgICBibG9jay5kKDEpO1xuICAgICAgICAgICAgICAgIGNhbGxiYWNrKCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgICBibG9jay5vKGxvY2FsKTtcbiAgICB9XG4gICAgZWxzZSBpZiAoY2FsbGJhY2spIHtcbiAgICAgICAgY2FsbGJhY2soKTtcbiAgICB9XG59XG5jb25zdCBudWxsX3RyYW5zaXRpb24gPSB7IGR1cmF0aW9uOiAwIH07XG5mdW5jdGlvbiBjcmVhdGVfaW5fdHJhbnNpdGlvbihub2RlLCBmbiwgcGFyYW1zKSB7XG4gICAgbGV0IGNvbmZpZyA9IGZuKG5vZGUsIHBhcmFtcyk7XG4gICAgbGV0IHJ1bm5pbmcgPSBmYWxzZTtcbiAgICBsZXQgYW5pbWF0aW9uX25hbWU7XG4gICAgbGV0IHRhc2s7XG4gICAgbGV0IHVpZCA9IDA7XG4gICAgZnVuY3Rpb24gY2xlYW51cCgpIHtcbiAgICAgICAgaWYgKGFuaW1hdGlvbl9uYW1lKVxuICAgICAgICAgICAgZGVsZXRlX3J1bGUobm9kZSwgYW5pbWF0aW9uX25hbWUpO1xuICAgIH1cbiAgICBmdW5jdGlvbiBnbygpIHtcbiAgICAgICAgY29uc3QgeyBkZWxheSA9IDAsIGR1cmF0aW9uID0gMzAwLCBlYXNpbmcgPSBpZGVudGl0eSwgdGljayA9IG5vb3AsIGNzcyB9ID0gY29uZmlnIHx8IG51bGxfdHJhbnNpdGlvbjtcbiAgICAgICAgaWYgKGNzcylcbiAgICAgICAgICAgIGFuaW1hdGlvbl9uYW1lID0gY3JlYXRlX3J1bGUobm9kZSwgMCwgMSwgZHVyYXRpb24sIGRlbGF5LCBlYXNpbmcsIGNzcywgdWlkKyspO1xuICAgICAgICB0aWNrKDAsIDEpO1xuICAgICAgICBjb25zdCBzdGFydF90aW1lID0gbm93KCkgKyBkZWxheTtcbiAgICAgICAgY29uc3QgZW5kX3RpbWUgPSBzdGFydF90aW1lICsgZHVyYXRpb247XG4gICAgICAgIGlmICh0YXNrKVxuICAgICAgICAgICAgdGFzay5hYm9ydCgpO1xuICAgICAgICBydW5uaW5nID0gdHJ1ZTtcbiAgICAgICAgYWRkX3JlbmRlcl9jYWxsYmFjaygoKSA9PiBkaXNwYXRjaChub2RlLCB0cnVlLCAnc3RhcnQnKSk7XG4gICAgICAgIHRhc2sgPSBsb29wKG5vdyA9PiB7XG4gICAgICAgICAgICBpZiAocnVubmluZykge1xuICAgICAgICAgICAgICAgIGlmIChub3cgPj0gZW5kX3RpbWUpIHtcbiAgICAgICAgICAgICAgICAgICAgdGljaygxLCAwKTtcbiAgICAgICAgICAgICAgICAgICAgZGlzcGF0Y2gobm9kZSwgdHJ1ZSwgJ2VuZCcpO1xuICAgICAgICAgICAgICAgICAgICBjbGVhbnVwKCk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBydW5uaW5nID0gZmFsc2U7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGlmIChub3cgPj0gc3RhcnRfdGltZSkge1xuICAgICAgICAgICAgICAgICAgICBjb25zdCB0ID0gZWFzaW5nKChub3cgLSBzdGFydF90aW1lKSAvIGR1cmF0aW9uKTtcbiAgICAgICAgICAgICAgICAgICAgdGljayh0LCAxIC0gdCk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcmV0dXJuIHJ1bm5pbmc7XG4gICAgICAgIH0pO1xuICAgIH1cbiAgICBsZXQgc3RhcnRlZCA9IGZhbHNlO1xuICAgIHJldHVybiB7XG4gICAgICAgIHN0YXJ0KCkge1xuICAgICAgICAgICAgaWYgKHN0YXJ0ZWQpXG4gICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgc3RhcnRlZCA9IHRydWU7XG4gICAgICAgICAgICBkZWxldGVfcnVsZShub2RlKTtcbiAgICAgICAgICAgIGlmIChpc19mdW5jdGlvbihjb25maWcpKSB7XG4gICAgICAgICAgICAgICAgY29uZmlnID0gY29uZmlnKCk7XG4gICAgICAgICAgICAgICAgd2FpdCgpLnRoZW4oZ28pO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgZ28oKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgaW52YWxpZGF0ZSgpIHtcbiAgICAgICAgICAgIHN0YXJ0ZWQgPSBmYWxzZTtcbiAgICAgICAgfSxcbiAgICAgICAgZW5kKCkge1xuICAgICAgICAgICAgaWYgKHJ1bm5pbmcpIHtcbiAgICAgICAgICAgICAgICBjbGVhbnVwKCk7XG4gICAgICAgICAgICAgICAgcnVubmluZyA9IGZhbHNlO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfTtcbn1cbmZ1bmN0aW9uIGNyZWF0ZV9vdXRfdHJhbnNpdGlvbihub2RlLCBmbiwgcGFyYW1zKSB7XG4gICAgbGV0IGNvbmZpZyA9IGZuKG5vZGUsIHBhcmFtcyk7XG4gICAgbGV0IHJ1bm5pbmcgPSB0cnVlO1xuICAgIGxldCBhbmltYXRpb25fbmFtZTtcbiAgICBjb25zdCBncm91cCA9IG91dHJvcztcbiAgICBncm91cC5yICs9IDE7XG4gICAgZnVuY3Rpb24gZ28oKSB7XG4gICAgICAgIGNvbnN0IHsgZGVsYXkgPSAwLCBkdXJhdGlvbiA9IDMwMCwgZWFzaW5nID0gaWRlbnRpdHksIHRpY2sgPSBub29wLCBjc3MgfSA9IGNvbmZpZyB8fCBudWxsX3RyYW5zaXRpb247XG4gICAgICAgIGlmIChjc3MpXG4gICAgICAgICAgICBhbmltYXRpb25fbmFtZSA9IGNyZWF0ZV9ydWxlKG5vZGUsIDEsIDAsIGR1cmF0aW9uLCBkZWxheSwgZWFzaW5nLCBjc3MpO1xuICAgICAgICBjb25zdCBzdGFydF90aW1lID0gbm93KCkgKyBkZWxheTtcbiAgICAgICAgY29uc3QgZW5kX3RpbWUgPSBzdGFydF90aW1lICsgZHVyYXRpb247XG4gICAgICAgIGFkZF9yZW5kZXJfY2FsbGJhY2soKCkgPT4gZGlzcGF0Y2gobm9kZSwgZmFsc2UsICdzdGFydCcpKTtcbiAgICAgICAgbG9vcChub3cgPT4ge1xuICAgICAgICAgICAgaWYgKHJ1bm5pbmcpIHtcbiAgICAgICAgICAgICAgICBpZiAobm93ID49IGVuZF90aW1lKSB7XG4gICAgICAgICAgICAgICAgICAgIHRpY2soMCwgMSk7XG4gICAgICAgICAgICAgICAgICAgIGRpc3BhdGNoKG5vZGUsIGZhbHNlLCAnZW5kJyk7XG4gICAgICAgICAgICAgICAgICAgIGlmICghLS1ncm91cC5yKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAvLyB0aGlzIHdpbGwgcmVzdWx0IGluIGBlbmQoKWAgYmVpbmcgY2FsbGVkLFxuICAgICAgICAgICAgICAgICAgICAgICAgLy8gc28gd2UgZG9uJ3QgbmVlZCB0byBjbGVhbiB1cCBoZXJlXG4gICAgICAgICAgICAgICAgICAgICAgICBydW5fYWxsKGdyb3VwLmMpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgaWYgKG5vdyA+PSBzdGFydF90aW1lKSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHQgPSBlYXNpbmcoKG5vdyAtIHN0YXJ0X3RpbWUpIC8gZHVyYXRpb24pO1xuICAgICAgICAgICAgICAgICAgICB0aWNrKDEgLSB0LCB0KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gcnVubmluZztcbiAgICAgICAgfSk7XG4gICAgfVxuICAgIGlmIChpc19mdW5jdGlvbihjb25maWcpKSB7XG4gICAgICAgIHdhaXQoKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgICAgIGNvbmZpZyA9IGNvbmZpZygpO1xuICAgICAgICAgICAgZ28oKTtcbiAgICAgICAgfSk7XG4gICAgfVxuICAgIGVsc2Uge1xuICAgICAgICBnbygpO1xuICAgIH1cbiAgICByZXR1cm4ge1xuICAgICAgICBlbmQocmVzZXQpIHtcbiAgICAgICAgICAgIGlmIChyZXNldCAmJiBjb25maWcudGljaykge1xuICAgICAgICAgICAgICAgIGNvbmZpZy50aWNrKDEsIDApO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKHJ1bm5pbmcpIHtcbiAgICAgICAgICAgICAgICBpZiAoYW5pbWF0aW9uX25hbWUpXG4gICAgICAgICAgICAgICAgICAgIGRlbGV0ZV9ydWxlKG5vZGUsIGFuaW1hdGlvbl9uYW1lKTtcbiAgICAgICAgICAgICAgICBydW5uaW5nID0gZmFsc2U7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9O1xufVxuZnVuY3Rpb24gY3JlYXRlX2JpZGlyZWN0aW9uYWxfdHJhbnNpdGlvbihub2RlLCBmbiwgcGFyYW1zLCBpbnRybykge1xuICAgIGxldCBjb25maWcgPSBmbihub2RlLCBwYXJhbXMpO1xuICAgIGxldCB0ID0gaW50cm8gPyAwIDogMTtcbiAgICBsZXQgcnVubmluZ19wcm9ncmFtID0gbnVsbDtcbiAgICBsZXQgcGVuZGluZ19wcm9ncmFtID0gbnVsbDtcbiAgICBsZXQgYW5pbWF0aW9uX25hbWUgPSBudWxsO1xuICAgIGZ1bmN0aW9uIGNsZWFyX2FuaW1hdGlvbigpIHtcbiAgICAgICAgaWYgKGFuaW1hdGlvbl9uYW1lKVxuICAgICAgICAgICAgZGVsZXRlX3J1bGUobm9kZSwgYW5pbWF0aW9uX25hbWUpO1xuICAgIH1cbiAgICBmdW5jdGlvbiBpbml0KHByb2dyYW0sIGR1cmF0aW9uKSB7XG4gICAgICAgIGNvbnN0IGQgPSAocHJvZ3JhbS5iIC0gdCk7XG4gICAgICAgIGR1cmF0aW9uICo9IE1hdGguYWJzKGQpO1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgYTogdCxcbiAgICAgICAgICAgIGI6IHByb2dyYW0uYixcbiAgICAgICAgICAgIGQsXG4gICAgICAgICAgICBkdXJhdGlvbixcbiAgICAgICAgICAgIHN0YXJ0OiBwcm9ncmFtLnN0YXJ0LFxuICAgICAgICAgICAgZW5kOiBwcm9ncmFtLnN0YXJ0ICsgZHVyYXRpb24sXG4gICAgICAgICAgICBncm91cDogcHJvZ3JhbS5ncm91cFxuICAgICAgICB9O1xuICAgIH1cbiAgICBmdW5jdGlvbiBnbyhiKSB7XG4gICAgICAgIGNvbnN0IHsgZGVsYXkgPSAwLCBkdXJhdGlvbiA9IDMwMCwgZWFzaW5nID0gaWRlbnRpdHksIHRpY2sgPSBub29wLCBjc3MgfSA9IGNvbmZpZyB8fCBudWxsX3RyYW5zaXRpb247XG4gICAgICAgIGNvbnN0IHByb2dyYW0gPSB7XG4gICAgICAgICAgICBzdGFydDogbm93KCkgKyBkZWxheSxcbiAgICAgICAgICAgIGJcbiAgICAgICAgfTtcbiAgICAgICAgaWYgKCFiKSB7XG4gICAgICAgICAgICAvLyBAdHMtaWdub3JlIHRvZG86IGltcHJvdmUgdHlwaW5nc1xuICAgICAgICAgICAgcHJvZ3JhbS5ncm91cCA9IG91dHJvcztcbiAgICAgICAgICAgIG91dHJvcy5yICs9IDE7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHJ1bm5pbmdfcHJvZ3JhbSB8fCBwZW5kaW5nX3Byb2dyYW0pIHtcbiAgICAgICAgICAgIHBlbmRpbmdfcHJvZ3JhbSA9IHByb2dyYW07XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAvLyBpZiB0aGlzIGlzIGFuIGludHJvLCBhbmQgdGhlcmUncyBhIGRlbGF5LCB3ZSBuZWVkIHRvIGRvXG4gICAgICAgICAgICAvLyBhbiBpbml0aWFsIHRpY2sgYW5kL29yIGFwcGx5IENTUyBhbmltYXRpb24gaW1tZWRpYXRlbHlcbiAgICAgICAgICAgIGlmIChjc3MpIHtcbiAgICAgICAgICAgICAgICBjbGVhcl9hbmltYXRpb24oKTtcbiAgICAgICAgICAgICAgICBhbmltYXRpb25fbmFtZSA9IGNyZWF0ZV9ydWxlKG5vZGUsIHQsIGIsIGR1cmF0aW9uLCBkZWxheSwgZWFzaW5nLCBjc3MpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKGIpXG4gICAgICAgICAgICAgICAgdGljaygwLCAxKTtcbiAgICAgICAgICAgIHJ1bm5pbmdfcHJvZ3JhbSA9IGluaXQocHJvZ3JhbSwgZHVyYXRpb24pO1xuICAgICAgICAgICAgYWRkX3JlbmRlcl9jYWxsYmFjaygoKSA9PiBkaXNwYXRjaChub2RlLCBiLCAnc3RhcnQnKSk7XG4gICAgICAgICAgICBsb29wKG5vdyA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHBlbmRpbmdfcHJvZ3JhbSAmJiBub3cgPiBwZW5kaW5nX3Byb2dyYW0uc3RhcnQpIHtcbiAgICAgICAgICAgICAgICAgICAgcnVubmluZ19wcm9ncmFtID0gaW5pdChwZW5kaW5nX3Byb2dyYW0sIGR1cmF0aW9uKTtcbiAgICAgICAgICAgICAgICAgICAgcGVuZGluZ19wcm9ncmFtID0gbnVsbDtcbiAgICAgICAgICAgICAgICAgICAgZGlzcGF0Y2gobm9kZSwgcnVubmluZ19wcm9ncmFtLmIsICdzdGFydCcpO1xuICAgICAgICAgICAgICAgICAgICBpZiAoY3NzKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjbGVhcl9hbmltYXRpb24oKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIGFuaW1hdGlvbl9uYW1lID0gY3JlYXRlX3J1bGUobm9kZSwgdCwgcnVubmluZ19wcm9ncmFtLmIsIHJ1bm5pbmdfcHJvZ3JhbS5kdXJhdGlvbiwgMCwgZWFzaW5nLCBjb25maWcuY3NzKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAocnVubmluZ19wcm9ncmFtKSB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChub3cgPj0gcnVubmluZ19wcm9ncmFtLmVuZCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGljayh0ID0gcnVubmluZ19wcm9ncmFtLmIsIDEgLSB0KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIGRpc3BhdGNoKG5vZGUsIHJ1bm5pbmdfcHJvZ3JhbS5iLCAnZW5kJyk7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoIXBlbmRpbmdfcHJvZ3JhbSkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIHdlJ3JlIGRvbmVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAocnVubmluZ19wcm9ncmFtLmIpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gaW50cm8g4oCUIHdlIGNhbiB0aWR5IHVwIGltbWVkaWF0ZWx5XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNsZWFyX2FuaW1hdGlvbigpO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gb3V0cm8g4oCUIG5lZWRzIHRvIGJlIGNvb3JkaW5hdGVkXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmICghLS1ydW5uaW5nX3Byb2dyYW0uZ3JvdXAucilcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJ1bl9hbGwocnVubmluZ19wcm9ncmFtLmdyb3VwLmMpO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIHJ1bm5pbmdfcHJvZ3JhbSA9IG51bGw7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgZWxzZSBpZiAobm93ID49IHJ1bm5pbmdfcHJvZ3JhbS5zdGFydCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc3QgcCA9IG5vdyAtIHJ1bm5pbmdfcHJvZ3JhbS5zdGFydDtcbiAgICAgICAgICAgICAgICAgICAgICAgIHQgPSBydW5uaW5nX3Byb2dyYW0uYSArIHJ1bm5pbmdfcHJvZ3JhbS5kICogZWFzaW5nKHAgLyBydW5uaW5nX3Byb2dyYW0uZHVyYXRpb24pO1xuICAgICAgICAgICAgICAgICAgICAgICAgdGljayh0LCAxIC0gdCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuICEhKHJ1bm5pbmdfcHJvZ3JhbSB8fCBwZW5kaW5nX3Byb2dyYW0pO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHtcbiAgICAgICAgcnVuKGIpIHtcbiAgICAgICAgICAgIGlmIChpc19mdW5jdGlvbihjb25maWcpKSB7XG4gICAgICAgICAgICAgICAgd2FpdCgpLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgICAgICAgICAgICAgIGNvbmZpZyA9IGNvbmZpZygpO1xuICAgICAgICAgICAgICAgICAgICBnbyhiKTtcbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgIGdvKGIpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBlbmQoKSB7XG4gICAgICAgICAgICBjbGVhcl9hbmltYXRpb24oKTtcbiAgICAgICAgICAgIHJ1bm5pbmdfcHJvZ3JhbSA9IHBlbmRpbmdfcHJvZ3JhbSA9IG51bGw7XG4gICAgICAgIH1cbiAgICB9O1xufVxuXG5mdW5jdGlvbiBoYW5kbGVfcHJvbWlzZShwcm9taXNlLCBpbmZvKSB7XG4gICAgY29uc3QgdG9rZW4gPSBpbmZvLnRva2VuID0ge307XG4gICAgZnVuY3Rpb24gdXBkYXRlKHR5cGUsIGluZGV4LCBrZXksIHZhbHVlKSB7XG4gICAgICAgIGlmIChpbmZvLnRva2VuICE9PSB0b2tlbilcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgaW5mby5yZXNvbHZlZCA9IHZhbHVlO1xuICAgICAgICBsZXQgY2hpbGRfY3R4ID0gaW5mby5jdHg7XG4gICAgICAgIGlmIChrZXkgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgY2hpbGRfY3R4ID0gY2hpbGRfY3R4LnNsaWNlKCk7XG4gICAgICAgICAgICBjaGlsZF9jdHhba2V5XSA9IHZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGJsb2NrID0gdHlwZSAmJiAoaW5mby5jdXJyZW50ID0gdHlwZSkoY2hpbGRfY3R4KTtcbiAgICAgICAgbGV0IG5lZWRzX2ZsdXNoID0gZmFsc2U7XG4gICAgICAgIGlmIChpbmZvLmJsb2NrKSB7XG4gICAgICAgICAgICBpZiAoaW5mby5ibG9ja3MpIHtcbiAgICAgICAgICAgICAgICBpbmZvLmJsb2Nrcy5mb3JFYWNoKChibG9jaywgaSkgPT4ge1xuICAgICAgICAgICAgICAgICAgICBpZiAoaSAhPT0gaW5kZXggJiYgYmxvY2spIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGdyb3VwX291dHJvcygpO1xuICAgICAgICAgICAgICAgICAgICAgICAgdHJhbnNpdGlvbl9vdXQoYmxvY2ssIDEsIDEsICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoaW5mby5ibG9ja3NbaV0gPT09IGJsb2NrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGluZm8uYmxvY2tzW2ldID0gbnVsbDtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNoZWNrX291dHJvcygpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgICAgICBpbmZvLmJsb2NrLmQoMSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBibG9jay5jKCk7XG4gICAgICAgICAgICB0cmFuc2l0aW9uX2luKGJsb2NrLCAxKTtcbiAgICAgICAgICAgIGJsb2NrLm0oaW5mby5tb3VudCgpLCBpbmZvLmFuY2hvcik7XG4gICAgICAgICAgICBuZWVkc19mbHVzaCA9IHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgaW5mby5ibG9jayA9IGJsb2NrO1xuICAgICAgICBpZiAoaW5mby5ibG9ja3MpXG4gICAgICAgICAgICBpbmZvLmJsb2Nrc1tpbmRleF0gPSBibG9jaztcbiAgICAgICAgaWYgKG5lZWRzX2ZsdXNoKSB7XG4gICAgICAgICAgICBmbHVzaCgpO1xuICAgICAgICB9XG4gICAgfVxuICAgIGlmIChpc19wcm9taXNlKHByb21pc2UpKSB7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRfY29tcG9uZW50ID0gZ2V0X2N1cnJlbnRfY29tcG9uZW50KCk7XG4gICAgICAgIHByb21pc2UudGhlbih2YWx1ZSA9PiB7XG4gICAgICAgICAgICBzZXRfY3VycmVudF9jb21wb25lbnQoY3VycmVudF9jb21wb25lbnQpO1xuICAgICAgICAgICAgdXBkYXRlKGluZm8udGhlbiwgMSwgaW5mby52YWx1ZSwgdmFsdWUpO1xuICAgICAgICAgICAgc2V0X2N1cnJlbnRfY29tcG9uZW50KG51bGwpO1xuICAgICAgICB9LCBlcnJvciA9PiB7XG4gICAgICAgICAgICBzZXRfY3VycmVudF9jb21wb25lbnQoY3VycmVudF9jb21wb25lbnQpO1xuICAgICAgICAgICAgdXBkYXRlKGluZm8uY2F0Y2gsIDIsIGluZm8uZXJyb3IsIGVycm9yKTtcbiAgICAgICAgICAgIHNldF9jdXJyZW50X2NvbXBvbmVudChudWxsKTtcbiAgICAgICAgICAgIGlmICghaW5mby5oYXNDYXRjaCkge1xuICAgICAgICAgICAgICAgIHRocm93IGVycm9yO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgICAgLy8gaWYgd2UgcHJldmlvdXNseSBoYWQgYSB0aGVuL2NhdGNoIGJsb2NrLCBkZXN0cm95IGl0XG4gICAgICAgIGlmIChpbmZvLmN1cnJlbnQgIT09IGluZm8ucGVuZGluZykge1xuICAgICAgICAgICAgdXBkYXRlKGluZm8ucGVuZGluZywgMCk7XG4gICAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgIH1cbiAgICBlbHNlIHtcbiAgICAgICAgaWYgKGluZm8uY3VycmVudCAhPT0gaW5mby50aGVuKSB7XG4gICAgICAgICAgICB1cGRhdGUoaW5mby50aGVuLCAxLCBpbmZvLnZhbHVlLCBwcm9taXNlKTtcbiAgICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIGluZm8ucmVzb2x2ZWQgPSBwcm9taXNlO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHVwZGF0ZV9hd2FpdF9ibG9ja19icmFuY2goaW5mbywgY3R4LCBkaXJ0eSkge1xuICAgIGNvbnN0IGNoaWxkX2N0eCA9IGN0eC5zbGljZSgpO1xuICAgIGNvbnN0IHsgcmVzb2x2ZWQgfSA9IGluZm87XG4gICAgaWYgKGluZm8uY3VycmVudCA9PT0gaW5mby50aGVuKSB7XG4gICAgICAgIGNoaWxkX2N0eFtpbmZvLnZhbHVlXSA9IHJlc29sdmVkO1xuICAgIH1cbiAgICBpZiAoaW5mby5jdXJyZW50ID09PSBpbmZvLmNhdGNoKSB7XG4gICAgICAgIGNoaWxkX2N0eFtpbmZvLmVycm9yXSA9IHJlc29sdmVkO1xuICAgIH1cbiAgICBpbmZvLmJsb2NrLnAoY2hpbGRfY3R4LCBkaXJ0eSk7XG59XG5cbmNvbnN0IGdsb2JhbHMgPSAodHlwZW9mIHdpbmRvdyAhPT0gJ3VuZGVmaW5lZCdcbiAgICA/IHdpbmRvd1xuICAgIDogdHlwZW9mIGdsb2JhbFRoaXMgIT09ICd1bmRlZmluZWQnXG4gICAgICAgID8gZ2xvYmFsVGhpc1xuICAgICAgICA6IGdsb2JhbCk7XG5cbmZ1bmN0aW9uIGRlc3Ryb3lfYmxvY2soYmxvY2ssIGxvb2t1cCkge1xuICAgIGJsb2NrLmQoMSk7XG4gICAgbG9va3VwLmRlbGV0ZShibG9jay5rZXkpO1xufVxuZnVuY3Rpb24gb3V0cm9fYW5kX2Rlc3Ryb3lfYmxvY2soYmxvY2ssIGxvb2t1cCkge1xuICAgIHRyYW5zaXRpb25fb3V0KGJsb2NrLCAxLCAxLCAoKSA9PiB7XG4gICAgICAgIGxvb2t1cC5kZWxldGUoYmxvY2sua2V5KTtcbiAgICB9KTtcbn1cbmZ1bmN0aW9uIGZpeF9hbmRfZGVzdHJveV9ibG9jayhibG9jaywgbG9va3VwKSB7XG4gICAgYmxvY2suZigpO1xuICAgIGRlc3Ryb3lfYmxvY2soYmxvY2ssIGxvb2t1cCk7XG59XG5mdW5jdGlvbiBmaXhfYW5kX291dHJvX2FuZF9kZXN0cm95X2Jsb2NrKGJsb2NrLCBsb29rdXApIHtcbiAgICBibG9jay5mKCk7XG4gICAgb3V0cm9fYW5kX2Rlc3Ryb3lfYmxvY2soYmxvY2ssIGxvb2t1cCk7XG59XG5mdW5jdGlvbiB1cGRhdGVfa2V5ZWRfZWFjaChvbGRfYmxvY2tzLCBkaXJ0eSwgZ2V0X2tleSwgZHluYW1pYywgY3R4LCBsaXN0LCBsb29rdXAsIG5vZGUsIGRlc3Ryb3ksIGNyZWF0ZV9lYWNoX2Jsb2NrLCBuZXh0LCBnZXRfY29udGV4dCkge1xuICAgIGxldCBvID0gb2xkX2Jsb2Nrcy5sZW5ndGg7XG4gICAgbGV0IG4gPSBsaXN0Lmxlbmd0aDtcbiAgICBsZXQgaSA9IG87XG4gICAgY29uc3Qgb2xkX2luZGV4ZXMgPSB7fTtcbiAgICB3aGlsZSAoaS0tKVxuICAgICAgICBvbGRfaW5kZXhlc1tvbGRfYmxvY2tzW2ldLmtleV0gPSBpO1xuICAgIGNvbnN0IG5ld19ibG9ja3MgPSBbXTtcbiAgICBjb25zdCBuZXdfbG9va3VwID0gbmV3IE1hcCgpO1xuICAgIGNvbnN0IGRlbHRhcyA9IG5ldyBNYXAoKTtcbiAgICBpID0gbjtcbiAgICB3aGlsZSAoaS0tKSB7XG4gICAgICAgIGNvbnN0IGNoaWxkX2N0eCA9IGdldF9jb250ZXh0KGN0eCwgbGlzdCwgaSk7XG4gICAgICAgIGNvbnN0IGtleSA9IGdldF9rZXkoY2hpbGRfY3R4KTtcbiAgICAgICAgbGV0IGJsb2NrID0gbG9va3VwLmdldChrZXkpO1xuICAgICAgICBpZiAoIWJsb2NrKSB7XG4gICAgICAgICAgICBibG9jayA9IGNyZWF0ZV9lYWNoX2Jsb2NrKGtleSwgY2hpbGRfY3R4KTtcbiAgICAgICAgICAgIGJsb2NrLmMoKTtcbiAgICAgICAgfVxuICAgICAgICBlbHNlIGlmIChkeW5hbWljKSB7XG4gICAgICAgICAgICBibG9jay5wKGNoaWxkX2N0eCwgZGlydHkpO1xuICAgICAgICB9XG4gICAgICAgIG5ld19sb29rdXAuc2V0KGtleSwgbmV3X2Jsb2Nrc1tpXSA9IGJsb2NrKTtcbiAgICAgICAgaWYgKGtleSBpbiBvbGRfaW5kZXhlcylcbiAgICAgICAgICAgIGRlbHRhcy5zZXQoa2V5LCBNYXRoLmFicyhpIC0gb2xkX2luZGV4ZXNba2V5XSkpO1xuICAgIH1cbiAgICBjb25zdCB3aWxsX21vdmUgPSBuZXcgU2V0KCk7XG4gICAgY29uc3QgZGlkX21vdmUgPSBuZXcgU2V0KCk7XG4gICAgZnVuY3Rpb24gaW5zZXJ0KGJsb2NrKSB7XG4gICAgICAgIHRyYW5zaXRpb25faW4oYmxvY2ssIDEpO1xuICAgICAgICBibG9jay5tKG5vZGUsIG5leHQpO1xuICAgICAgICBsb29rdXAuc2V0KGJsb2NrLmtleSwgYmxvY2spO1xuICAgICAgICBuZXh0ID0gYmxvY2suZmlyc3Q7XG4gICAgICAgIG4tLTtcbiAgICB9XG4gICAgd2hpbGUgKG8gJiYgbikge1xuICAgICAgICBjb25zdCBuZXdfYmxvY2sgPSBuZXdfYmxvY2tzW24gLSAxXTtcbiAgICAgICAgY29uc3Qgb2xkX2Jsb2NrID0gb2xkX2Jsb2Nrc1tvIC0gMV07XG4gICAgICAgIGNvbnN0IG5ld19rZXkgPSBuZXdfYmxvY2sua2V5O1xuICAgICAgICBjb25zdCBvbGRfa2V5ID0gb2xkX2Jsb2NrLmtleTtcbiAgICAgICAgaWYgKG5ld19ibG9jayA9PT0gb2xkX2Jsb2NrKSB7XG4gICAgICAgICAgICAvLyBkbyBub3RoaW5nXG4gICAgICAgICAgICBuZXh0ID0gbmV3X2Jsb2NrLmZpcnN0O1xuICAgICAgICAgICAgby0tO1xuICAgICAgICAgICAgbi0tO1xuICAgICAgICB9XG4gICAgICAgIGVsc2UgaWYgKCFuZXdfbG9va3VwLmhhcyhvbGRfa2V5KSkge1xuICAgICAgICAgICAgLy8gcmVtb3ZlIG9sZCBibG9ja1xuICAgICAgICAgICAgZGVzdHJveShvbGRfYmxvY2ssIGxvb2t1cCk7XG4gICAgICAgICAgICBvLS07XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoIWxvb2t1cC5oYXMobmV3X2tleSkgfHwgd2lsbF9tb3ZlLmhhcyhuZXdfa2V5KSkge1xuICAgICAgICAgICAgaW5zZXJ0KG5ld19ibG9jayk7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoZGlkX21vdmUuaGFzKG9sZF9rZXkpKSB7XG4gICAgICAgICAgICBvLS07XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAoZGVsdGFzLmdldChuZXdfa2V5KSA+IGRlbHRhcy5nZXQob2xkX2tleSkpIHtcbiAgICAgICAgICAgIGRpZF9tb3ZlLmFkZChuZXdfa2V5KTtcbiAgICAgICAgICAgIGluc2VydChuZXdfYmxvY2spO1xuICAgICAgICB9XG4gICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgd2lsbF9tb3ZlLmFkZChvbGRfa2V5KTtcbiAgICAgICAgICAgIG8tLTtcbiAgICAgICAgfVxuICAgIH1cbiAgICB3aGlsZSAoby0tKSB7XG4gICAgICAgIGNvbnN0IG9sZF9ibG9jayA9IG9sZF9ibG9ja3Nbb107XG4gICAgICAgIGlmICghbmV3X2xvb2t1cC5oYXMob2xkX2Jsb2NrLmtleSkpXG4gICAgICAgICAgICBkZXN0cm95KG9sZF9ibG9jaywgbG9va3VwKTtcbiAgICB9XG4gICAgd2hpbGUgKG4pXG4gICAgICAgIGluc2VydChuZXdfYmxvY2tzW24gLSAxXSk7XG4gICAgcmV0dXJuIG5ld19ibG9ja3M7XG59XG5mdW5jdGlvbiB2YWxpZGF0ZV9lYWNoX2tleXMoY3R4LCBsaXN0LCBnZXRfY29udGV4dCwgZ2V0X2tleSkge1xuICAgIGNvbnN0IGtleXMgPSBuZXcgU2V0KCk7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBsaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIGNvbnN0IGtleSA9IGdldF9rZXkoZ2V0X2NvbnRleHQoY3R4LCBsaXN0LCBpKSk7XG4gICAgICAgIGlmIChrZXlzLmhhcyhrZXkpKSB7XG4gICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ0Nhbm5vdCBoYXZlIGR1cGxpY2F0ZSBrZXlzIGluIGEga2V5ZWQgZWFjaCcpO1xuICAgICAgICB9XG4gICAgICAgIGtleXMuYWRkKGtleSk7XG4gICAgfVxufVxuXG5mdW5jdGlvbiBnZXRfc3ByZWFkX3VwZGF0ZShsZXZlbHMsIHVwZGF0ZXMpIHtcbiAgICBjb25zdCB1cGRhdGUgPSB7fTtcbiAgICBjb25zdCB0b19udWxsX291dCA9IHt9O1xuICAgIGNvbnN0IGFjY291bnRlZF9mb3IgPSB7ICQkc2NvcGU6IDEgfTtcbiAgICBsZXQgaSA9IGxldmVscy5sZW5ndGg7XG4gICAgd2hpbGUgKGktLSkge1xuICAgICAgICBjb25zdCBvID0gbGV2ZWxzW2ldO1xuICAgICAgICBjb25zdCBuID0gdXBkYXRlc1tpXTtcbiAgICAgICAgaWYgKG4pIHtcbiAgICAgICAgICAgIGZvciAoY29uc3Qga2V5IGluIG8pIHtcbiAgICAgICAgICAgICAgICBpZiAoIShrZXkgaW4gbikpXG4gICAgICAgICAgICAgICAgICAgIHRvX251bGxfb3V0W2tleV0gPSAxO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgZm9yIChjb25zdCBrZXkgaW4gbikge1xuICAgICAgICAgICAgICAgIGlmICghYWNjb3VudGVkX2ZvcltrZXldKSB7XG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZVtrZXldID0gbltrZXldO1xuICAgICAgICAgICAgICAgICAgICBhY2NvdW50ZWRfZm9yW2tleV0gPSAxO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGxldmVsc1tpXSA9IG47XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICBmb3IgKGNvbnN0IGtleSBpbiBvKSB7XG4gICAgICAgICAgICAgICAgYWNjb3VudGVkX2ZvcltrZXldID0gMTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbiAgICBmb3IgKGNvbnN0IGtleSBpbiB0b19udWxsX291dCkge1xuICAgICAgICBpZiAoIShrZXkgaW4gdXBkYXRlKSlcbiAgICAgICAgICAgIHVwZGF0ZVtrZXldID0gdW5kZWZpbmVkO1xuICAgIH1cbiAgICByZXR1cm4gdXBkYXRlO1xufVxuZnVuY3Rpb24gZ2V0X3NwcmVhZF9vYmplY3Qoc3ByZWFkX3Byb3BzKSB7XG4gICAgcmV0dXJuIHR5cGVvZiBzcHJlYWRfcHJvcHMgPT09ICdvYmplY3QnICYmIHNwcmVhZF9wcm9wcyAhPT0gbnVsbCA/IHNwcmVhZF9wcm9wcyA6IHt9O1xufVxuXG4vLyBzb3VyY2U6IGh0dHBzOi8vaHRtbC5zcGVjLndoYXR3Zy5vcmcvbXVsdGlwYWdlL2luZGljZXMuaHRtbFxuY29uc3QgYm9vbGVhbl9hdHRyaWJ1dGVzID0gbmV3IFNldChbXG4gICAgJ2FsbG93ZnVsbHNjcmVlbicsXG4gICAgJ2FsbG93cGF5bWVudHJlcXVlc3QnLFxuICAgICdhc3luYycsXG4gICAgJ2F1dG9mb2N1cycsXG4gICAgJ2F1dG9wbGF5JyxcbiAgICAnY2hlY2tlZCcsXG4gICAgJ2NvbnRyb2xzJyxcbiAgICAnZGVmYXVsdCcsXG4gICAgJ2RlZmVyJyxcbiAgICAnZGlzYWJsZWQnLFxuICAgICdmb3Jtbm92YWxpZGF0ZScsXG4gICAgJ2hpZGRlbicsXG4gICAgJ2lzbWFwJyxcbiAgICAnbG9vcCcsXG4gICAgJ211bHRpcGxlJyxcbiAgICAnbXV0ZWQnLFxuICAgICdub21vZHVsZScsXG4gICAgJ25vdmFsaWRhdGUnLFxuICAgICdvcGVuJyxcbiAgICAncGxheXNpbmxpbmUnLFxuICAgICdyZWFkb25seScsXG4gICAgJ3JlcXVpcmVkJyxcbiAgICAncmV2ZXJzZWQnLFxuICAgICdzZWxlY3RlZCdcbl0pO1xuXG4vKiogcmVnZXggb2YgYWxsIGh0bWwgdm9pZCBlbGVtZW50IG5hbWVzICovXG5jb25zdCB2b2lkX2VsZW1lbnRfbmFtZXMgPSAvXig/OmFyZWF8YmFzZXxicnxjb2x8Y29tbWFuZHxlbWJlZHxocnxpbWd8aW5wdXR8a2V5Z2VufGxpbmt8bWV0YXxwYXJhbXxzb3VyY2V8dHJhY2t8d2JyKSQvO1xuZnVuY3Rpb24gaXNfdm9pZChuYW1lKSB7XG4gICAgcmV0dXJuIHZvaWRfZWxlbWVudF9uYW1lcy50ZXN0KG5hbWUpIHx8IG5hbWUudG9Mb3dlckNhc2UoKSA9PT0gJyFkb2N0eXBlJztcbn1cblxuY29uc3QgaW52YWxpZF9hdHRyaWJ1dGVfbmFtZV9jaGFyYWN0ZXIgPSAvW1xccydcIj4vPVxcdXtGREQwfS1cXHV7RkRFRn1cXHV7RkZGRX1cXHV7RkZGRn1cXHV7MUZGRkV9XFx1ezFGRkZGfVxcdXsyRkZGRX1cXHV7MkZGRkZ9XFx1ezNGRkZFfVxcdXszRkZGRn1cXHV7NEZGRkV9XFx1ezRGRkZGfVxcdXs1RkZGRX1cXHV7NUZGRkZ9XFx1ezZGRkZFfVxcdXs2RkZGRn1cXHV7N0ZGRkV9XFx1ezdGRkZGfVxcdXs4RkZGRX1cXHV7OEZGRkZ9XFx1ezlGRkZFfVxcdXs5RkZGRn1cXHV7QUZGRkV9XFx1e0FGRkZGfVxcdXtCRkZGRX1cXHV7QkZGRkZ9XFx1e0NGRkZFfVxcdXtDRkZGRn1cXHV7REZGRkV9XFx1e0RGRkZGfVxcdXtFRkZGRX1cXHV7RUZGRkZ9XFx1e0ZGRkZFfVxcdXtGRkZGRn1cXHV7MTBGRkZFfVxcdXsxMEZGRkZ9XS91O1xuLy8gaHR0cHM6Ly9odG1sLnNwZWMud2hhdHdnLm9yZy9tdWx0aXBhZ2Uvc3ludGF4Lmh0bWwjYXR0cmlidXRlcy0yXG4vLyBodHRwczovL2luZnJhLnNwZWMud2hhdHdnLm9yZy8jbm9uY2hhcmFjdGVyXG5mdW5jdGlvbiBzcHJlYWQoYXJncywgYXR0cnNfdG9fYWRkKSB7XG4gICAgY29uc3QgYXR0cmlidXRlcyA9IE9iamVjdC5hc3NpZ24oe30sIC4uLmFyZ3MpO1xuICAgIGlmIChhdHRyc190b19hZGQpIHtcbiAgICAgICAgY29uc3QgY2xhc3Nlc190b19hZGQgPSBhdHRyc190b19hZGQuY2xhc3NlcztcbiAgICAgICAgY29uc3Qgc3R5bGVzX3RvX2FkZCA9IGF0dHJzX3RvX2FkZC5zdHlsZXM7XG4gICAgICAgIGlmIChjbGFzc2VzX3RvX2FkZCkge1xuICAgICAgICAgICAgaWYgKGF0dHJpYnV0ZXMuY2xhc3MgPT0gbnVsbCkge1xuICAgICAgICAgICAgICAgIGF0dHJpYnV0ZXMuY2xhc3MgPSBjbGFzc2VzX3RvX2FkZDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgIGF0dHJpYnV0ZXMuY2xhc3MgKz0gJyAnICsgY2xhc3Nlc190b19hZGQ7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHN0eWxlc190b19hZGQpIHtcbiAgICAgICAgICAgIGlmIChhdHRyaWJ1dGVzLnN0eWxlID09IG51bGwpIHtcbiAgICAgICAgICAgICAgICBhdHRyaWJ1dGVzLnN0eWxlID0gc3R5bGVfb2JqZWN0X3RvX3N0cmluZyhzdHlsZXNfdG9fYWRkKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgIGF0dHJpYnV0ZXMuc3R5bGUgPSBzdHlsZV9vYmplY3RfdG9fc3RyaW5nKG1lcmdlX3Nzcl9zdHlsZXMoYXR0cmlidXRlcy5zdHlsZSwgc3R5bGVzX3RvX2FkZCkpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuICAgIGxldCBzdHIgPSAnJztcbiAgICBPYmplY3Qua2V5cyhhdHRyaWJ1dGVzKS5mb3JFYWNoKG5hbWUgPT4ge1xuICAgICAgICBpZiAoaW52YWxpZF9hdHRyaWJ1dGVfbmFtZV9jaGFyYWN0ZXIudGVzdChuYW1lKSlcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBhdHRyaWJ1dGVzW25hbWVdO1xuICAgICAgICBpZiAodmFsdWUgPT09IHRydWUpXG4gICAgICAgICAgICBzdHIgKz0gJyAnICsgbmFtZTtcbiAgICAgICAgZWxzZSBpZiAoYm9vbGVhbl9hdHRyaWJ1dGVzLmhhcyhuYW1lLnRvTG93ZXJDYXNlKCkpKSB7XG4gICAgICAgICAgICBpZiAodmFsdWUpXG4gICAgICAgICAgICAgICAgc3RyICs9ICcgJyArIG5hbWU7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSBpZiAodmFsdWUgIT0gbnVsbCkge1xuICAgICAgICAgICAgc3RyICs9IGAgJHtuYW1lfT1cIiR7dmFsdWV9XCJgO1xuICAgICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuIHN0cjtcbn1cbmZ1bmN0aW9uIG1lcmdlX3Nzcl9zdHlsZXMoc3R5bGVfYXR0cmlidXRlLCBzdHlsZV9kaXJlY3RpdmUpIHtcbiAgICBjb25zdCBzdHlsZV9vYmplY3QgPSB7fTtcbiAgICBmb3IgKGNvbnN0IGluZGl2aWR1YWxfc3R5bGUgb2Ygc3R5bGVfYXR0cmlidXRlLnNwbGl0KCc7JykpIHtcbiAgICAgICAgY29uc3QgY29sb25faW5kZXggPSBpbmRpdmlkdWFsX3N0eWxlLmluZGV4T2YoJzonKTtcbiAgICAgICAgY29uc3QgbmFtZSA9IGluZGl2aWR1YWxfc3R5bGUuc2xpY2UoMCwgY29sb25faW5kZXgpLnRyaW0oKTtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBpbmRpdmlkdWFsX3N0eWxlLnNsaWNlKGNvbG9uX2luZGV4ICsgMSkudHJpbSgpO1xuICAgICAgICBpZiAoIW5hbWUpXG4gICAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgc3R5bGVfb2JqZWN0W25hbWVdID0gdmFsdWU7XG4gICAgfVxuICAgIGZvciAoY29uc3QgbmFtZSBpbiBzdHlsZV9kaXJlY3RpdmUpIHtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBzdHlsZV9kaXJlY3RpdmVbbmFtZV07XG4gICAgICAgIGlmICh2YWx1ZSkge1xuICAgICAgICAgICAgc3R5bGVfb2JqZWN0W25hbWVdID0gdmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICBkZWxldGUgc3R5bGVfb2JqZWN0W25hbWVdO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiBzdHlsZV9vYmplY3Q7XG59XG5jb25zdCBBVFRSX1JFR0VYID0gL1smXCJdL2c7XG5jb25zdCBDT05URU5UX1JFR0VYID0gL1smPF0vZztcbi8qKlxuICogTm90ZTogdGhpcyBtZXRob2QgaXMgcGVyZm9ybWFuY2Ugc2Vuc2l0aXZlIGFuZCBoYXMgYmVlbiBvcHRpbWl6ZWRcbiAqIGh0dHBzOi8vZ2l0aHViLmNvbS9zdmVsdGVqcy9zdmVsdGUvcHVsbC81NzAxXG4gKi9cbmZ1bmN0aW9uIGVzY2FwZSh2YWx1ZSwgaXNfYXR0ciA9IGZhbHNlKSB7XG4gICAgY29uc3Qgc3RyID0gU3RyaW5nKHZhbHVlKTtcbiAgICBjb25zdCBwYXR0ZXJuID0gaXNfYXR0ciA/IEFUVFJfUkVHRVggOiBDT05URU5UX1JFR0VYO1xuICAgIHBhdHRlcm4ubGFzdEluZGV4ID0gMDtcbiAgICBsZXQgZXNjYXBlZCA9ICcnO1xuICAgIGxldCBsYXN0ID0gMDtcbiAgICB3aGlsZSAocGF0dGVybi50ZXN0KHN0cikpIHtcbiAgICAgICAgY29uc3QgaSA9IHBhdHRlcm4ubGFzdEluZGV4IC0gMTtcbiAgICAgICAgY29uc3QgY2ggPSBzdHJbaV07XG4gICAgICAgIGVzY2FwZWQgKz0gc3RyLnN1YnN0cmluZyhsYXN0LCBpKSArIChjaCA9PT0gJyYnID8gJyZhbXA7JyA6IChjaCA9PT0gJ1wiJyA/ICcmcXVvdDsnIDogJyZsdDsnKSk7XG4gICAgICAgIGxhc3QgPSBpICsgMTtcbiAgICB9XG4gICAgcmV0dXJuIGVzY2FwZWQgKyBzdHIuc3Vic3RyaW5nKGxhc3QpO1xufVxuZnVuY3Rpb24gZXNjYXBlX2F0dHJpYnV0ZV92YWx1ZSh2YWx1ZSkge1xuICAgIC8vIGtlZXAgYm9vbGVhbnMsIG51bGwsIGFuZCB1bmRlZmluZWQgZm9yIHRoZSBzYWtlIG9mIGBzcHJlYWRgXG4gICAgY29uc3Qgc2hvdWxkX2VzY2FwZSA9IHR5cGVvZiB2YWx1ZSA9PT0gJ3N0cmluZycgfHwgKHZhbHVlICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcpO1xuICAgIHJldHVybiBzaG91bGRfZXNjYXBlID8gZXNjYXBlKHZhbHVlLCB0cnVlKSA6IHZhbHVlO1xufVxuZnVuY3Rpb24gZXNjYXBlX29iamVjdChvYmopIHtcbiAgICBjb25zdCByZXN1bHQgPSB7fTtcbiAgICBmb3IgKGNvbnN0IGtleSBpbiBvYmopIHtcbiAgICAgICAgcmVzdWx0W2tleV0gPSBlc2NhcGVfYXR0cmlidXRlX3ZhbHVlKG9ialtrZXldKTtcbiAgICB9XG4gICAgcmV0dXJuIHJlc3VsdDtcbn1cbmZ1bmN0aW9uIGVhY2goaXRlbXMsIGZuKSB7XG4gICAgbGV0IHN0ciA9ICcnO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgaXRlbXMubGVuZ3RoOyBpICs9IDEpIHtcbiAgICAgICAgc3RyICs9IGZuKGl0ZW1zW2ldLCBpKTtcbiAgICB9XG4gICAgcmV0dXJuIHN0cjtcbn1cbmNvbnN0IG1pc3NpbmdfY29tcG9uZW50ID0ge1xuICAgICQkcmVuZGVyOiAoKSA9PiAnJ1xufTtcbmZ1bmN0aW9uIHZhbGlkYXRlX2NvbXBvbmVudChjb21wb25lbnQsIG5hbWUpIHtcbiAgICBpZiAoIWNvbXBvbmVudCB8fCAhY29tcG9uZW50LiQkcmVuZGVyKSB7XG4gICAgICAgIGlmIChuYW1lID09PSAnc3ZlbHRlOmNvbXBvbmVudCcpXG4gICAgICAgICAgICBuYW1lICs9ICcgdGhpcz17Li4ufSc7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihgPCR7bmFtZX0+IGlzIG5vdCBhIHZhbGlkIFNTUiBjb21wb25lbnQuIFlvdSBtYXkgbmVlZCB0byByZXZpZXcgeW91ciBidWlsZCBjb25maWcgdG8gZW5zdXJlIHRoYXQgZGVwZW5kZW5jaWVzIGFyZSBjb21waWxlZCwgcmF0aGVyIHRoYW4gaW1wb3J0ZWQgYXMgcHJlLWNvbXBpbGVkIG1vZHVsZXNgKTtcbiAgICB9XG4gICAgcmV0dXJuIGNvbXBvbmVudDtcbn1cbmZ1bmN0aW9uIGRlYnVnKGZpbGUsIGxpbmUsIGNvbHVtbiwgdmFsdWVzKSB7XG4gICAgY29uc29sZS5sb2coYHtAZGVidWd9ICR7ZmlsZSA/IGZpbGUgKyAnICcgOiAnJ30oJHtsaW5lfToke2NvbHVtbn0pYCk7IC8vIGVzbGludC1kaXNhYmxlLWxpbmUgbm8tY29uc29sZVxuICAgIGNvbnNvbGUubG9nKHZhbHVlcyk7IC8vIGVzbGludC1kaXNhYmxlLWxpbmUgbm8tY29uc29sZVxuICAgIHJldHVybiAnJztcbn1cbmxldCBvbl9kZXN0cm95O1xuZnVuY3Rpb24gY3JlYXRlX3Nzcl9jb21wb25lbnQoZm4pIHtcbiAgICBmdW5jdGlvbiAkJHJlbmRlcihyZXN1bHQsIHByb3BzLCBiaW5kaW5ncywgc2xvdHMsIGNvbnRleHQpIHtcbiAgICAgICAgY29uc3QgcGFyZW50X2NvbXBvbmVudCA9IGN1cnJlbnRfY29tcG9uZW50O1xuICAgICAgICBjb25zdCAkJCA9IHtcbiAgICAgICAgICAgIG9uX2Rlc3Ryb3ksXG4gICAgICAgICAgICBjb250ZXh0OiBuZXcgTWFwKGNvbnRleHQgfHwgKHBhcmVudF9jb21wb25lbnQgPyBwYXJlbnRfY29tcG9uZW50LiQkLmNvbnRleHQgOiBbXSkpLFxuICAgICAgICAgICAgLy8gdGhlc2Ugd2lsbCBiZSBpbW1lZGlhdGVseSBkaXNjYXJkZWRcbiAgICAgICAgICAgIG9uX21vdW50OiBbXSxcbiAgICAgICAgICAgIGJlZm9yZV91cGRhdGU6IFtdLFxuICAgICAgICAgICAgYWZ0ZXJfdXBkYXRlOiBbXSxcbiAgICAgICAgICAgIGNhbGxiYWNrczogYmxhbmtfb2JqZWN0KClcbiAgICAgICAgfTtcbiAgICAgICAgc2V0X2N1cnJlbnRfY29tcG9uZW50KHsgJCQgfSk7XG4gICAgICAgIGNvbnN0IGh0bWwgPSBmbihyZXN1bHQsIHByb3BzLCBiaW5kaW5ncywgc2xvdHMpO1xuICAgICAgICBzZXRfY3VycmVudF9jb21wb25lbnQocGFyZW50X2NvbXBvbmVudCk7XG4gICAgICAgIHJldHVybiBodG1sO1xuICAgIH1cbiAgICByZXR1cm4ge1xuICAgICAgICByZW5kZXI6IChwcm9wcyA9IHt9LCB7ICQkc2xvdHMgPSB7fSwgY29udGV4dCA9IG5ldyBNYXAoKSB9ID0ge30pID0+IHtcbiAgICAgICAgICAgIG9uX2Rlc3Ryb3kgPSBbXTtcbiAgICAgICAgICAgIGNvbnN0IHJlc3VsdCA9IHsgdGl0bGU6ICcnLCBoZWFkOiAnJywgY3NzOiBuZXcgU2V0KCkgfTtcbiAgICAgICAgICAgIGNvbnN0IGh0bWwgPSAkJHJlbmRlcihyZXN1bHQsIHByb3BzLCB7fSwgJCRzbG90cywgY29udGV4dCk7XG4gICAgICAgICAgICBydW5fYWxsKG9uX2Rlc3Ryb3kpO1xuICAgICAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgICAgICBodG1sLFxuICAgICAgICAgICAgICAgIGNzczoge1xuICAgICAgICAgICAgICAgICAgICBjb2RlOiBBcnJheS5mcm9tKHJlc3VsdC5jc3MpLm1hcChjc3MgPT4gY3NzLmNvZGUpLmpvaW4oJ1xcbicpLFxuICAgICAgICAgICAgICAgICAgICBtYXA6IG51bGwgLy8gVE9ET1xuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgaGVhZDogcmVzdWx0LnRpdGxlICsgcmVzdWx0LmhlYWRcbiAgICAgICAgICAgIH07XG4gICAgICAgIH0sXG4gICAgICAgICQkcmVuZGVyXG4gICAgfTtcbn1cbmZ1bmN0aW9uIGFkZF9hdHRyaWJ1dGUobmFtZSwgdmFsdWUsIGJvb2xlYW4pIHtcbiAgICBpZiAodmFsdWUgPT0gbnVsbCB8fCAoYm9vbGVhbiAmJiAhdmFsdWUpKVxuICAgICAgICByZXR1cm4gJyc7XG4gICAgY29uc3QgYXNzaWdubWVudCA9IChib29sZWFuICYmIHZhbHVlID09PSB0cnVlKSA/ICcnIDogYD1cIiR7ZXNjYXBlKHZhbHVlLCB0cnVlKX1cImA7XG4gICAgcmV0dXJuIGAgJHtuYW1lfSR7YXNzaWdubWVudH1gO1xufVxuZnVuY3Rpb24gYWRkX2NsYXNzZXMoY2xhc3Nlcykge1xuICAgIHJldHVybiBjbGFzc2VzID8gYCBjbGFzcz1cIiR7Y2xhc3Nlc31cImAgOiAnJztcbn1cbmZ1bmN0aW9uIHN0eWxlX29iamVjdF90b19zdHJpbmcoc3R5bGVfb2JqZWN0KSB7XG4gICAgcmV0dXJuIE9iamVjdC5rZXlzKHN0eWxlX29iamVjdClcbiAgICAgICAgLmZpbHRlcihrZXkgPT4gc3R5bGVfb2JqZWN0W2tleV0pXG4gICAgICAgIC5tYXAoa2V5ID0+IGAke2tleX06ICR7c3R5bGVfb2JqZWN0W2tleV19O2ApXG4gICAgICAgIC5qb2luKCcgJyk7XG59XG5mdW5jdGlvbiBhZGRfc3R5bGVzKHN0eWxlX29iamVjdCkge1xuICAgIGNvbnN0IHN0eWxlcyA9IHN0eWxlX29iamVjdF90b19zdHJpbmcoc3R5bGVfb2JqZWN0KTtcbiAgICByZXR1cm4gc3R5bGVzID8gYCBzdHlsZT1cIiR7c3R5bGVzfVwiYCA6ICcnO1xufVxuXG5mdW5jdGlvbiBiaW5kKGNvbXBvbmVudCwgbmFtZSwgY2FsbGJhY2spIHtcbiAgICBjb25zdCBpbmRleCA9IGNvbXBvbmVudC4kJC5wcm9wc1tuYW1lXTtcbiAgICBpZiAoaW5kZXggIT09IHVuZGVmaW5lZCkge1xuICAgICAgICBjb21wb25lbnQuJCQuYm91bmRbaW5kZXhdID0gY2FsbGJhY2s7XG4gICAgICAgIGNhbGxiYWNrKGNvbXBvbmVudC4kJC5jdHhbaW5kZXhdKTtcbiAgICB9XG59XG5mdW5jdGlvbiBjcmVhdGVfY29tcG9uZW50KGJsb2NrKSB7XG4gICAgYmxvY2sgJiYgYmxvY2suYygpO1xufVxuZnVuY3Rpb24gY2xhaW1fY29tcG9uZW50KGJsb2NrLCBwYXJlbnRfbm9kZXMpIHtcbiAgICBibG9jayAmJiBibG9jay5sKHBhcmVudF9ub2Rlcyk7XG59XG5mdW5jdGlvbiBtb3VudF9jb21wb25lbnQoY29tcG9uZW50LCB0YXJnZXQsIGFuY2hvciwgY3VzdG9tRWxlbWVudCkge1xuICAgIGNvbnN0IHsgZnJhZ21lbnQsIG9uX21vdW50LCBvbl9kZXN0cm95LCBhZnRlcl91cGRhdGUgfSA9IGNvbXBvbmVudC4kJDtcbiAgICBmcmFnbWVudCAmJiBmcmFnbWVudC5tKHRhcmdldCwgYW5jaG9yKTtcbiAgICBpZiAoIWN1c3RvbUVsZW1lbnQpIHtcbiAgICAgICAgLy8gb25Nb3VudCBoYXBwZW5zIGJlZm9yZSB0aGUgaW5pdGlhbCBhZnRlclVwZGF0ZVxuICAgICAgICBhZGRfcmVuZGVyX2NhbGxiYWNrKCgpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IG5ld19vbl9kZXN0cm95ID0gb25fbW91bnQubWFwKHJ1bikuZmlsdGVyKGlzX2Z1bmN0aW9uKTtcbiAgICAgICAgICAgIGlmIChvbl9kZXN0cm95KSB7XG4gICAgICAgICAgICAgICAgb25fZGVzdHJveS5wdXNoKC4uLm5ld19vbl9kZXN0cm95KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgICAgIC8vIEVkZ2UgY2FzZSAtIGNvbXBvbmVudCB3YXMgZGVzdHJveWVkIGltbWVkaWF0ZWx5LFxuICAgICAgICAgICAgICAgIC8vIG1vc3QgbGlrZWx5IGFzIGEgcmVzdWx0IG9mIGEgYmluZGluZyBpbml0aWFsaXNpbmdcbiAgICAgICAgICAgICAgICBydW5fYWxsKG5ld19vbl9kZXN0cm95KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGNvbXBvbmVudC4kJC5vbl9tb3VudCA9IFtdO1xuICAgICAgICB9KTtcbiAgICB9XG4gICAgYWZ0ZXJfdXBkYXRlLmZvckVhY2goYWRkX3JlbmRlcl9jYWxsYmFjayk7XG59XG5mdW5jdGlvbiBkZXN0cm95X2NvbXBvbmVudChjb21wb25lbnQsIGRldGFjaGluZykge1xuICAgIGNvbnN0ICQkID0gY29tcG9uZW50LiQkO1xuICAgIGlmICgkJC5mcmFnbWVudCAhPT0gbnVsbCkge1xuICAgICAgICBydW5fYWxsKCQkLm9uX2Rlc3Ryb3kpO1xuICAgICAgICAkJC5mcmFnbWVudCAmJiAkJC5mcmFnbWVudC5kKGRldGFjaGluZyk7XG4gICAgICAgIC8vIFRPRE8gbnVsbCBvdXQgb3RoZXIgcmVmcywgaW5jbHVkaW5nIGNvbXBvbmVudC4kJCAoYnV0IG5lZWQgdG9cbiAgICAgICAgLy8gcHJlc2VydmUgZmluYWwgc3RhdGU/KVxuICAgICAgICAkJC5vbl9kZXN0cm95ID0gJCQuZnJhZ21lbnQgPSBudWxsO1xuICAgICAgICAkJC5jdHggPSBbXTtcbiAgICB9XG59XG5mdW5jdGlvbiBtYWtlX2RpcnR5KGNvbXBvbmVudCwgaSkge1xuICAgIGlmIChjb21wb25lbnQuJCQuZGlydHlbMF0gPT09IC0xKSB7XG4gICAgICAgIGRpcnR5X2NvbXBvbmVudHMucHVzaChjb21wb25lbnQpO1xuICAgICAgICBzY2hlZHVsZV91cGRhdGUoKTtcbiAgICAgICAgY29tcG9uZW50LiQkLmRpcnR5LmZpbGwoMCk7XG4gICAgfVxuICAgIGNvbXBvbmVudC4kJC5kaXJ0eVsoaSAvIDMxKSB8IDBdIHw9ICgxIDw8IChpICUgMzEpKTtcbn1cbmZ1bmN0aW9uIGluaXQoY29tcG9uZW50LCBvcHRpb25zLCBpbnN0YW5jZSwgY3JlYXRlX2ZyYWdtZW50LCBub3RfZXF1YWwsIHByb3BzLCBhcHBlbmRfc3R5bGVzLCBkaXJ0eSA9IFstMV0pIHtcbiAgICBjb25zdCBwYXJlbnRfY29tcG9uZW50ID0gY3VycmVudF9jb21wb25lbnQ7XG4gICAgc2V0X2N1cnJlbnRfY29tcG9uZW50KGNvbXBvbmVudCk7XG4gICAgY29uc3QgJCQgPSBjb21wb25lbnQuJCQgPSB7XG4gICAgICAgIGZyYWdtZW50OiBudWxsLFxuICAgICAgICBjdHg6IG51bGwsXG4gICAgICAgIC8vIHN0YXRlXG4gICAgICAgIHByb3BzLFxuICAgICAgICB1cGRhdGU6IG5vb3AsXG4gICAgICAgIG5vdF9lcXVhbCxcbiAgICAgICAgYm91bmQ6IGJsYW5rX29iamVjdCgpLFxuICAgICAgICAvLyBsaWZlY3ljbGVcbiAgICAgICAgb25fbW91bnQ6IFtdLFxuICAgICAgICBvbl9kZXN0cm95OiBbXSxcbiAgICAgICAgb25fZGlzY29ubmVjdDogW10sXG4gICAgICAgIGJlZm9yZV91cGRhdGU6IFtdLFxuICAgICAgICBhZnRlcl91cGRhdGU6IFtdLFxuICAgICAgICBjb250ZXh0OiBuZXcgTWFwKG9wdGlvbnMuY29udGV4dCB8fCAocGFyZW50X2NvbXBvbmVudCA/IHBhcmVudF9jb21wb25lbnQuJCQuY29udGV4dCA6IFtdKSksXG4gICAgICAgIC8vIGV2ZXJ5dGhpbmcgZWxzZVxuICAgICAgICBjYWxsYmFja3M6IGJsYW5rX29iamVjdCgpLFxuICAgICAgICBkaXJ0eSxcbiAgICAgICAgc2tpcF9ib3VuZDogZmFsc2UsXG4gICAgICAgIHJvb3Q6IG9wdGlvbnMudGFyZ2V0IHx8IHBhcmVudF9jb21wb25lbnQuJCQucm9vdFxuICAgIH07XG4gICAgYXBwZW5kX3N0eWxlcyAmJiBhcHBlbmRfc3R5bGVzKCQkLnJvb3QpO1xuICAgIGxldCByZWFkeSA9IGZhbHNlO1xuICAgICQkLmN0eCA9IGluc3RhbmNlXG4gICAgICAgID8gaW5zdGFuY2UoY29tcG9uZW50LCBvcHRpb25zLnByb3BzIHx8IHt9LCAoaSwgcmV0LCAuLi5yZXN0KSA9PiB7XG4gICAgICAgICAgICBjb25zdCB2YWx1ZSA9IHJlc3QubGVuZ3RoID8gcmVzdFswXSA6IHJldDtcbiAgICAgICAgICAgIGlmICgkJC5jdHggJiYgbm90X2VxdWFsKCQkLmN0eFtpXSwgJCQuY3R4W2ldID0gdmFsdWUpKSB7XG4gICAgICAgICAgICAgICAgaWYgKCEkJC5za2lwX2JvdW5kICYmICQkLmJvdW5kW2ldKVxuICAgICAgICAgICAgICAgICAgICAkJC5ib3VuZFtpXSh2YWx1ZSk7XG4gICAgICAgICAgICAgICAgaWYgKHJlYWR5KVxuICAgICAgICAgICAgICAgICAgICBtYWtlX2RpcnR5KGNvbXBvbmVudCwgaSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gcmV0O1xuICAgICAgICB9KVxuICAgICAgICA6IFtdO1xuICAgICQkLnVwZGF0ZSgpO1xuICAgIHJlYWR5ID0gdHJ1ZTtcbiAgICBydW5fYWxsKCQkLmJlZm9yZV91cGRhdGUpO1xuICAgIC8vIGBmYWxzZWAgYXMgYSBzcGVjaWFsIGNhc2Ugb2Ygbm8gRE9NIGNvbXBvbmVudFxuICAgICQkLmZyYWdtZW50ID0gY3JlYXRlX2ZyYWdtZW50ID8gY3JlYXRlX2ZyYWdtZW50KCQkLmN0eCkgOiBmYWxzZTtcbiAgICBpZiAob3B0aW9ucy50YXJnZXQpIHtcbiAgICAgICAgaWYgKG9wdGlvbnMuaHlkcmF0ZSkge1xuICAgICAgICAgICAgc3RhcnRfaHlkcmF0aW5nKCk7XG4gICAgICAgICAgICBjb25zdCBub2RlcyA9IGNoaWxkcmVuKG9wdGlvbnMudGFyZ2V0KTtcbiAgICAgICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBAdHlwZXNjcmlwdC1lc2xpbnQvbm8tbm9uLW51bGwtYXNzZXJ0aW9uXG4gICAgICAgICAgICAkJC5mcmFnbWVudCAmJiAkJC5mcmFnbWVudC5sKG5vZGVzKTtcbiAgICAgICAgICAgIG5vZGVzLmZvckVhY2goZGV0YWNoKTtcbiAgICAgICAgfVxuICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBAdHlwZXNjcmlwdC1lc2xpbnQvbm8tbm9uLW51bGwtYXNzZXJ0aW9uXG4gICAgICAgICAgICAkJC5mcmFnbWVudCAmJiAkJC5mcmFnbWVudC5jKCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKG9wdGlvbnMuaW50cm8pXG4gICAgICAgICAgICB0cmFuc2l0aW9uX2luKGNvbXBvbmVudC4kJC5mcmFnbWVudCk7XG4gICAgICAgIG1vdW50X2NvbXBvbmVudChjb21wb25lbnQsIG9wdGlvbnMudGFyZ2V0LCBvcHRpb25zLmFuY2hvciwgb3B0aW9ucy5jdXN0b21FbGVtZW50KTtcbiAgICAgICAgZW5kX2h5ZHJhdGluZygpO1xuICAgICAgICBmbHVzaCgpO1xuICAgIH1cbiAgICBzZXRfY3VycmVudF9jb21wb25lbnQocGFyZW50X2NvbXBvbmVudCk7XG59XG5sZXQgU3ZlbHRlRWxlbWVudDtcbmlmICh0eXBlb2YgSFRNTEVsZW1lbnQgPT09ICdmdW5jdGlvbicpIHtcbiAgICBTdmVsdGVFbGVtZW50ID0gY2xhc3MgZXh0ZW5kcyBIVE1MRWxlbWVudCB7XG4gICAgICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICAgICAgc3VwZXIoKTtcbiAgICAgICAgICAgIHRoaXMuYXR0YWNoU2hhZG93KHsgbW9kZTogJ29wZW4nIH0pO1xuICAgICAgICB9XG4gICAgICAgIGNvbm5lY3RlZENhbGxiYWNrKCkge1xuICAgICAgICAgICAgY29uc3QgeyBvbl9tb3VudCB9ID0gdGhpcy4kJDtcbiAgICAgICAgICAgIHRoaXMuJCQub25fZGlzY29ubmVjdCA9IG9uX21vdW50Lm1hcChydW4pLmZpbHRlcihpc19mdW5jdGlvbik7XG4gICAgICAgICAgICAvLyBAdHMtaWdub3JlIHRvZG86IGltcHJvdmUgdHlwaW5nc1xuICAgICAgICAgICAgZm9yIChjb25zdCBrZXkgaW4gdGhpcy4kJC5zbG90dGVkKSB7XG4gICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZSB0b2RvOiBpbXByb3ZlIHR5cGluZ3NcbiAgICAgICAgICAgICAgICB0aGlzLmFwcGVuZENoaWxkKHRoaXMuJCQuc2xvdHRlZFtrZXldKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBhdHRyaWJ1dGVDaGFuZ2VkQ2FsbGJhY2soYXR0ciwgX29sZFZhbHVlLCBuZXdWYWx1ZSkge1xuICAgICAgICAgICAgdGhpc1thdHRyXSA9IG5ld1ZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIGRpc2Nvbm5lY3RlZENhbGxiYWNrKCkge1xuICAgICAgICAgICAgcnVuX2FsbCh0aGlzLiQkLm9uX2Rpc2Nvbm5lY3QpO1xuICAgICAgICB9XG4gICAgICAgICRkZXN0cm95KCkge1xuICAgICAgICAgICAgZGVzdHJveV9jb21wb25lbnQodGhpcywgMSk7XG4gICAgICAgICAgICB0aGlzLiRkZXN0cm95ID0gbm9vcDtcbiAgICAgICAgfVxuICAgICAgICAkb24odHlwZSwgY2FsbGJhY2spIHtcbiAgICAgICAgICAgIC8vIFRPRE8gc2hvdWxkIHRoaXMgZGVsZWdhdGUgdG8gYWRkRXZlbnRMaXN0ZW5lcj9cbiAgICAgICAgICAgIGNvbnN0IGNhbGxiYWNrcyA9ICh0aGlzLiQkLmNhbGxiYWNrc1t0eXBlXSB8fCAodGhpcy4kJC5jYWxsYmFja3NbdHlwZV0gPSBbXSkpO1xuICAgICAgICAgICAgY2FsbGJhY2tzLnB1c2goY2FsbGJhY2spO1xuICAgICAgICAgICAgcmV0dXJuICgpID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCBpbmRleCA9IGNhbGxiYWNrcy5pbmRleE9mKGNhbGxiYWNrKTtcbiAgICAgICAgICAgICAgICBpZiAoaW5kZXggIT09IC0xKVxuICAgICAgICAgICAgICAgICAgICBjYWxsYmFja3Muc3BsaWNlKGluZGV4LCAxKTtcbiAgICAgICAgICAgIH07XG4gICAgICAgIH1cbiAgICAgICAgJHNldCgkJHByb3BzKSB7XG4gICAgICAgICAgICBpZiAodGhpcy4kJHNldCAmJiAhaXNfZW1wdHkoJCRwcm9wcykpIHtcbiAgICAgICAgICAgICAgICB0aGlzLiQkLnNraXBfYm91bmQgPSB0cnVlO1xuICAgICAgICAgICAgICAgIHRoaXMuJCRzZXQoJCRwcm9wcyk7XG4gICAgICAgICAgICAgICAgdGhpcy4kJC5za2lwX2JvdW5kID0gZmFsc2U7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICB9O1xufVxuLyoqXG4gKiBCYXNlIGNsYXNzIGZvciBTdmVsdGUgY29tcG9uZW50cy4gVXNlZCB3aGVuIGRldj1mYWxzZS5cbiAqL1xuY2xhc3MgU3ZlbHRlQ29tcG9uZW50IHtcbiAgICAkZGVzdHJveSgpIHtcbiAgICAgICAgZGVzdHJveV9jb21wb25lbnQodGhpcywgMSk7XG4gICAgICAgIHRoaXMuJGRlc3Ryb3kgPSBub29wO1xuICAgIH1cbiAgICAkb24odHlwZSwgY2FsbGJhY2spIHtcbiAgICAgICAgY29uc3QgY2FsbGJhY2tzID0gKHRoaXMuJCQuY2FsbGJhY2tzW3R5cGVdIHx8ICh0aGlzLiQkLmNhbGxiYWNrc1t0eXBlXSA9IFtdKSk7XG4gICAgICAgIGNhbGxiYWNrcy5wdXNoKGNhbGxiYWNrKTtcbiAgICAgICAgcmV0dXJuICgpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IGluZGV4ID0gY2FsbGJhY2tzLmluZGV4T2YoY2FsbGJhY2spO1xuICAgICAgICAgICAgaWYgKGluZGV4ICE9PSAtMSlcbiAgICAgICAgICAgICAgICBjYWxsYmFja3Muc3BsaWNlKGluZGV4LCAxKTtcbiAgICAgICAgfTtcbiAgICB9XG4gICAgJHNldCgkJHByb3BzKSB7XG4gICAgICAgIGlmICh0aGlzLiQkc2V0ICYmICFpc19lbXB0eSgkJHByb3BzKSkge1xuICAgICAgICAgICAgdGhpcy4kJC5za2lwX2JvdW5kID0gdHJ1ZTtcbiAgICAgICAgICAgIHRoaXMuJCRzZXQoJCRwcm9wcyk7XG4gICAgICAgICAgICB0aGlzLiQkLnNraXBfYm91bmQgPSBmYWxzZTtcbiAgICAgICAgfVxuICAgIH1cbn1cblxuZnVuY3Rpb24gZGlzcGF0Y2hfZGV2KHR5cGUsIGRldGFpbCkge1xuICAgIGRvY3VtZW50LmRpc3BhdGNoRXZlbnQoY3VzdG9tX2V2ZW50KHR5cGUsIE9iamVjdC5hc3NpZ24oeyB2ZXJzaW9uOiAnMy41MC4xJyB9LCBkZXRhaWwpLCB7IGJ1YmJsZXM6IHRydWUgfSkpO1xufVxuZnVuY3Rpb24gYXBwZW5kX2Rldih0YXJnZXQsIG5vZGUpIHtcbiAgICBkaXNwYXRjaF9kZXYoJ1N2ZWx0ZURPTUluc2VydCcsIHsgdGFyZ2V0LCBub2RlIH0pO1xuICAgIGFwcGVuZCh0YXJnZXQsIG5vZGUpO1xufVxuZnVuY3Rpb24gYXBwZW5kX2h5ZHJhdGlvbl9kZXYodGFyZ2V0LCBub2RlKSB7XG4gICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01JbnNlcnQnLCB7IHRhcmdldCwgbm9kZSB9KTtcbiAgICBhcHBlbmRfaHlkcmF0aW9uKHRhcmdldCwgbm9kZSk7XG59XG5mdW5jdGlvbiBpbnNlcnRfZGV2KHRhcmdldCwgbm9kZSwgYW5jaG9yKSB7XG4gICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01JbnNlcnQnLCB7IHRhcmdldCwgbm9kZSwgYW5jaG9yIH0pO1xuICAgIGluc2VydCh0YXJnZXQsIG5vZGUsIGFuY2hvcik7XG59XG5mdW5jdGlvbiBpbnNlcnRfaHlkcmF0aW9uX2Rldih0YXJnZXQsIG5vZGUsIGFuY2hvcikge1xuICAgIGRpc3BhdGNoX2RldignU3ZlbHRlRE9NSW5zZXJ0JywgeyB0YXJnZXQsIG5vZGUsIGFuY2hvciB9KTtcbiAgICBpbnNlcnRfaHlkcmF0aW9uKHRhcmdldCwgbm9kZSwgYW5jaG9yKTtcbn1cbmZ1bmN0aW9uIGRldGFjaF9kZXYobm9kZSkge1xuICAgIGRpc3BhdGNoX2RldignU3ZlbHRlRE9NUmVtb3ZlJywgeyBub2RlIH0pO1xuICAgIGRldGFjaChub2RlKTtcbn1cbmZ1bmN0aW9uIGRldGFjaF9iZXR3ZWVuX2RldihiZWZvcmUsIGFmdGVyKSB7XG4gICAgd2hpbGUgKGJlZm9yZS5uZXh0U2libGluZyAmJiBiZWZvcmUubmV4dFNpYmxpbmcgIT09IGFmdGVyKSB7XG4gICAgICAgIGRldGFjaF9kZXYoYmVmb3JlLm5leHRTaWJsaW5nKTtcbiAgICB9XG59XG5mdW5jdGlvbiBkZXRhY2hfYmVmb3JlX2RldihhZnRlcikge1xuICAgIHdoaWxlIChhZnRlci5wcmV2aW91c1NpYmxpbmcpIHtcbiAgICAgICAgZGV0YWNoX2RldihhZnRlci5wcmV2aW91c1NpYmxpbmcpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGRldGFjaF9hZnRlcl9kZXYoYmVmb3JlKSB7XG4gICAgd2hpbGUgKGJlZm9yZS5uZXh0U2libGluZykge1xuICAgICAgICBkZXRhY2hfZGV2KGJlZm9yZS5uZXh0U2libGluZyk7XG4gICAgfVxufVxuZnVuY3Rpb24gbGlzdGVuX2Rldihub2RlLCBldmVudCwgaGFuZGxlciwgb3B0aW9ucywgaGFzX3ByZXZlbnRfZGVmYXVsdCwgaGFzX3N0b3BfcHJvcGFnYXRpb24pIHtcbiAgICBjb25zdCBtb2RpZmllcnMgPSBvcHRpb25zID09PSB0cnVlID8gWydjYXB0dXJlJ10gOiBvcHRpb25zID8gQXJyYXkuZnJvbShPYmplY3Qua2V5cyhvcHRpb25zKSkgOiBbXTtcbiAgICBpZiAoaGFzX3ByZXZlbnRfZGVmYXVsdClcbiAgICAgICAgbW9kaWZpZXJzLnB1c2goJ3ByZXZlbnREZWZhdWx0Jyk7XG4gICAgaWYgKGhhc19zdG9wX3Byb3BhZ2F0aW9uKVxuICAgICAgICBtb2RpZmllcnMucHVzaCgnc3RvcFByb3BhZ2F0aW9uJyk7XG4gICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01BZGRFdmVudExpc3RlbmVyJywgeyBub2RlLCBldmVudCwgaGFuZGxlciwgbW9kaWZpZXJzIH0pO1xuICAgIGNvbnN0IGRpc3Bvc2UgPSBsaXN0ZW4obm9kZSwgZXZlbnQsIGhhbmRsZXIsIG9wdGlvbnMpO1xuICAgIHJldHVybiAoKSA9PiB7XG4gICAgICAgIGRpc3BhdGNoX2RldignU3ZlbHRlRE9NUmVtb3ZlRXZlbnRMaXN0ZW5lcicsIHsgbm9kZSwgZXZlbnQsIGhhbmRsZXIsIG1vZGlmaWVycyB9KTtcbiAgICAgICAgZGlzcG9zZSgpO1xuICAgIH07XG59XG5mdW5jdGlvbiBhdHRyX2Rldihub2RlLCBhdHRyaWJ1dGUsIHZhbHVlKSB7XG4gICAgYXR0cihub2RlLCBhdHRyaWJ1dGUsIHZhbHVlKTtcbiAgICBpZiAodmFsdWUgPT0gbnVsbClcbiAgICAgICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01SZW1vdmVBdHRyaWJ1dGUnLCB7IG5vZGUsIGF0dHJpYnV0ZSB9KTtcbiAgICBlbHNlXG4gICAgICAgIGRpc3BhdGNoX2RldignU3ZlbHRlRE9NU2V0QXR0cmlidXRlJywgeyBub2RlLCBhdHRyaWJ1dGUsIHZhbHVlIH0pO1xufVxuZnVuY3Rpb24gcHJvcF9kZXYobm9kZSwgcHJvcGVydHksIHZhbHVlKSB7XG4gICAgbm9kZVtwcm9wZXJ0eV0gPSB2YWx1ZTtcbiAgICBkaXNwYXRjaF9kZXYoJ1N2ZWx0ZURPTVNldFByb3BlcnR5JywgeyBub2RlLCBwcm9wZXJ0eSwgdmFsdWUgfSk7XG59XG5mdW5jdGlvbiBkYXRhc2V0X2Rldihub2RlLCBwcm9wZXJ0eSwgdmFsdWUpIHtcbiAgICBub2RlLmRhdGFzZXRbcHJvcGVydHldID0gdmFsdWU7XG4gICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01TZXREYXRhc2V0JywgeyBub2RlLCBwcm9wZXJ0eSwgdmFsdWUgfSk7XG59XG5mdW5jdGlvbiBzZXRfZGF0YV9kZXYodGV4dCwgZGF0YSkge1xuICAgIGRhdGEgPSAnJyArIGRhdGE7XG4gICAgaWYgKHRleHQud2hvbGVUZXh0ID09PSBkYXRhKVxuICAgICAgICByZXR1cm47XG4gICAgZGlzcGF0Y2hfZGV2KCdTdmVsdGVET01TZXREYXRhJywgeyBub2RlOiB0ZXh0LCBkYXRhIH0pO1xuICAgIHRleHQuZGF0YSA9IGRhdGE7XG59XG5mdW5jdGlvbiB2YWxpZGF0ZV9lYWNoX2FyZ3VtZW50KGFyZykge1xuICAgIGlmICh0eXBlb2YgYXJnICE9PSAnc3RyaW5nJyAmJiAhKGFyZyAmJiB0eXBlb2YgYXJnID09PSAnb2JqZWN0JyAmJiAnbGVuZ3RoJyBpbiBhcmcpKSB7XG4gICAgICAgIGxldCBtc2cgPSAneyNlYWNofSBvbmx5IGl0ZXJhdGVzIG92ZXIgYXJyYXktbGlrZSBvYmplY3RzLic7XG4gICAgICAgIGlmICh0eXBlb2YgU3ltYm9sID09PSAnZnVuY3Rpb24nICYmIGFyZyAmJiBTeW1ib2wuaXRlcmF0b3IgaW4gYXJnKSB7XG4gICAgICAgICAgICBtc2cgKz0gJyBZb3UgY2FuIHVzZSBhIHNwcmVhZCB0byBjb252ZXJ0IHRoaXMgaXRlcmFibGUgaW50byBhbiBhcnJheS4nO1xuICAgICAgICB9XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihtc2cpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHZhbGlkYXRlX3Nsb3RzKG5hbWUsIHNsb3QsIGtleXMpIHtcbiAgICBmb3IgKGNvbnN0IHNsb3Rfa2V5IG9mIE9iamVjdC5rZXlzKHNsb3QpKSB7XG4gICAgICAgIGlmICghfmtleXMuaW5kZXhPZihzbG90X2tleSkpIHtcbiAgICAgICAgICAgIGNvbnNvbGUud2FybihgPCR7bmFtZX0+IHJlY2VpdmVkIGFuIHVuZXhwZWN0ZWQgc2xvdCBcIiR7c2xvdF9rZXl9XCIuYCk7XG4gICAgICAgIH1cbiAgICB9XG59XG5mdW5jdGlvbiB2YWxpZGF0ZV9keW5hbWljX2VsZW1lbnQodGFnKSB7XG4gICAgY29uc3QgaXNfc3RyaW5nID0gdHlwZW9mIHRhZyA9PT0gJ3N0cmluZyc7XG4gICAgaWYgKHRhZyAmJiAhaXNfc3RyaW5nKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcignPHN2ZWx0ZTplbGVtZW50PiBleHBlY3RzIFwidGhpc1wiIGF0dHJpYnV0ZSB0byBiZSBhIHN0cmluZy4nKTtcbiAgICB9XG59XG5mdW5jdGlvbiB2YWxpZGF0ZV92b2lkX2R5bmFtaWNfZWxlbWVudCh0YWcpIHtcbiAgICBpZiAodGFnICYmIGlzX3ZvaWQodGFnKSkge1xuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYDxzdmVsdGU6ZWxlbWVudCB0aGlzPVwiJHt0YWd9XCI+IGlzIHNlbGYtY2xvc2luZyBhbmQgY2Fubm90IGhhdmUgY29udGVudC5gKTtcbiAgICB9XG59XG4vKipcbiAqIEJhc2UgY2xhc3MgZm9yIFN2ZWx0ZSBjb21wb25lbnRzIHdpdGggc29tZSBtaW5vciBkZXYtZW5oYW5jZW1lbnRzLiBVc2VkIHdoZW4gZGV2PXRydWUuXG4gKi9cbmNsYXNzIFN2ZWx0ZUNvbXBvbmVudERldiBleHRlbmRzIFN2ZWx0ZUNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3Iob3B0aW9ucykge1xuICAgICAgICBpZiAoIW9wdGlvbnMgfHwgKCFvcHRpb25zLnRhcmdldCAmJiAhb3B0aW9ucy4kJGlubGluZSkpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihcIid0YXJnZXQnIGlzIGEgcmVxdWlyZWQgb3B0aW9uXCIpO1xuICAgICAgICB9XG4gICAgICAgIHN1cGVyKCk7XG4gICAgfVxuICAgICRkZXN0cm95KCkge1xuICAgICAgICBzdXBlci4kZGVzdHJveSgpO1xuICAgICAgICB0aGlzLiRkZXN0cm95ID0gKCkgPT4ge1xuICAgICAgICAgICAgY29uc29sZS53YXJuKCdDb21wb25lbnQgd2FzIGFscmVhZHkgZGVzdHJveWVkJyk7IC8vIGVzbGludC1kaXNhYmxlLWxpbmUgbm8tY29uc29sZVxuICAgICAgICB9O1xuICAgIH1cbiAgICAkY2FwdHVyZV9zdGF0ZSgpIHsgfVxuICAgICRpbmplY3Rfc3RhdGUoKSB7IH1cbn1cbi8qKlxuICogQmFzZSBjbGFzcyB0byBjcmVhdGUgc3Ryb25nbHkgdHlwZWQgU3ZlbHRlIGNvbXBvbmVudHMuXG4gKiBUaGlzIG9ubHkgZXhpc3RzIGZvciB0eXBpbmcgcHVycG9zZXMgYW5kIHNob3VsZCBiZSB1c2VkIGluIGAuZC50c2AgZmlsZXMuXG4gKlxuICogIyMjIEV4YW1wbGU6XG4gKlxuICogWW91IGhhdmUgY29tcG9uZW50IGxpYnJhcnkgb24gbnBtIGNhbGxlZCBgY29tcG9uZW50LWxpYnJhcnlgLCBmcm9tIHdoaWNoXG4gKiB5b3UgZXhwb3J0IGEgY29tcG9uZW50IGNhbGxlZCBgTXlDb21wb25lbnRgLiBGb3IgU3ZlbHRlK1R5cGVTY3JpcHQgdXNlcnMsXG4gKiB5b3Ugd2FudCB0byBwcm92aWRlIHR5cGluZ3MuIFRoZXJlZm9yZSB5b3UgY3JlYXRlIGEgYGluZGV4LmQudHNgOlxuICogYGBgdHNcbiAqIGltcG9ydCB7IFN2ZWx0ZUNvbXBvbmVudFR5cGVkIH0gZnJvbSBcInN2ZWx0ZVwiO1xuICogZXhwb3J0IGNsYXNzIE15Q29tcG9uZW50IGV4dGVuZHMgU3ZlbHRlQ29tcG9uZW50VHlwZWQ8e2Zvbzogc3RyaW5nfT4ge31cbiAqIGBgYFxuICogVHlwaW5nIHRoaXMgbWFrZXMgaXQgcG9zc2libGUgZm9yIElERXMgbGlrZSBWUyBDb2RlIHdpdGggdGhlIFN2ZWx0ZSBleHRlbnNpb25cbiAqIHRvIHByb3ZpZGUgaW50ZWxsaXNlbnNlIGFuZCB0byB1c2UgdGhlIGNvbXBvbmVudCBsaWtlIHRoaXMgaW4gYSBTdmVsdGUgZmlsZVxuICogd2l0aCBUeXBlU2NyaXB0OlxuICogYGBgc3ZlbHRlXG4gKiA8c2NyaXB0IGxhbmc9XCJ0c1wiPlxuICogXHRpbXBvcnQgeyBNeUNvbXBvbmVudCB9IGZyb20gXCJjb21wb25lbnQtbGlicmFyeVwiO1xuICogPC9zY3JpcHQ+XG4gKiA8TXlDb21wb25lbnQgZm9vPXsnYmFyJ30gLz5cbiAqIGBgYFxuICpcbiAqICMjIyMgV2h5IG5vdCBtYWtlIHRoaXMgcGFydCBvZiBgU3ZlbHRlQ29tcG9uZW50KERldilgP1xuICogQmVjYXVzZVxuICogYGBgdHNcbiAqIGNsYXNzIEFTdWJjbGFzc09mU3ZlbHRlQ29tcG9uZW50IGV4dGVuZHMgU3ZlbHRlQ29tcG9uZW50PHtmb286IHN0cmluZ30+IHt9XG4gKiBjb25zdCBjb21wb25lbnQ6IHR5cGVvZiBTdmVsdGVDb21wb25lbnQgPSBBU3ViY2xhc3NPZlN2ZWx0ZUNvbXBvbmVudDtcbiAqIGBgYFxuICogd2lsbCB0aHJvdyBhIHR5cGUgZXJyb3IsIHNvIHdlIG5lZWQgdG8gc2VwYXJhdGUgdGhlIG1vcmUgc3RyaWN0bHkgdHlwZWQgY2xhc3MuXG4gKi9cbmNsYXNzIFN2ZWx0ZUNvbXBvbmVudFR5cGVkIGV4dGVuZHMgU3ZlbHRlQ29tcG9uZW50RGV2IHtcbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zKSB7XG4gICAgICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGxvb3BfZ3VhcmQodGltZW91dCkge1xuICAgIGNvbnN0IHN0YXJ0ID0gRGF0ZS5ub3coKTtcbiAgICByZXR1cm4gKCkgPT4ge1xuICAgICAgICBpZiAoRGF0ZS5ub3coKSAtIHN0YXJ0ID4gdGltZW91dCkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdJbmZpbml0ZSBsb29wIGRldGVjdGVkJyk7XG4gICAgICAgIH1cbiAgICB9O1xufVxuXG5leHBvcnQgeyBIdG1sVGFnLCBIdG1sVGFnSHlkcmF0aW9uLCBTdmVsdGVDb21wb25lbnQsIFN2ZWx0ZUNvbXBvbmVudERldiwgU3ZlbHRlQ29tcG9uZW50VHlwZWQsIFN2ZWx0ZUVsZW1lbnQsIGFjdGlvbl9kZXN0cm95ZXIsIGFkZF9hdHRyaWJ1dGUsIGFkZF9jbGFzc2VzLCBhZGRfZmx1c2hfY2FsbGJhY2ssIGFkZF9sb2NhdGlvbiwgYWRkX3JlbmRlcl9jYWxsYmFjaywgYWRkX3Jlc2l6ZV9saXN0ZW5lciwgYWRkX3N0eWxlcywgYWRkX3RyYW5zZm9ybSwgYWZ0ZXJVcGRhdGUsIGFwcGVuZCwgYXBwZW5kX2RldiwgYXBwZW5kX2VtcHR5X3N0eWxlc2hlZXQsIGFwcGVuZF9oeWRyYXRpb24sIGFwcGVuZF9oeWRyYXRpb25fZGV2LCBhcHBlbmRfc3R5bGVzLCBhc3NpZ24sIGF0dHIsIGF0dHJfZGV2LCBhdHRyaWJ1dGVfdG9fb2JqZWN0LCBiZWZvcmVVcGRhdGUsIGJpbmQsIGJpbmRpbmdfY2FsbGJhY2tzLCBibGFua19vYmplY3QsIGJ1YmJsZSwgY2hlY2tfb3V0cm9zLCBjaGlsZHJlbiwgY2xhaW1fY29tcG9uZW50LCBjbGFpbV9lbGVtZW50LCBjbGFpbV9odG1sX3RhZywgY2xhaW1fc3BhY2UsIGNsYWltX3N2Z19lbGVtZW50LCBjbGFpbV90ZXh0LCBjbGVhcl9sb29wcywgY29tcG9uZW50X3N1YnNjcmliZSwgY29tcHV0ZV9yZXN0X3Byb3BzLCBjb21wdXRlX3Nsb3RzLCBjcmVhdGVFdmVudERpc3BhdGNoZXIsIGNyZWF0ZV9hbmltYXRpb24sIGNyZWF0ZV9iaWRpcmVjdGlvbmFsX3RyYW5zaXRpb24sIGNyZWF0ZV9jb21wb25lbnQsIGNyZWF0ZV9pbl90cmFuc2l0aW9uLCBjcmVhdGVfb3V0X3RyYW5zaXRpb24sIGNyZWF0ZV9zbG90LCBjcmVhdGVfc3NyX2NvbXBvbmVudCwgY3VycmVudF9jb21wb25lbnQsIGN1c3RvbV9ldmVudCwgZGF0YXNldF9kZXYsIGRlYnVnLCBkZXN0cm95X2Jsb2NrLCBkZXN0cm95X2NvbXBvbmVudCwgZGVzdHJveV9lYWNoLCBkZXRhY2gsIGRldGFjaF9hZnRlcl9kZXYsIGRldGFjaF9iZWZvcmVfZGV2LCBkZXRhY2hfYmV0d2Vlbl9kZXYsIGRldGFjaF9kZXYsIGRpcnR5X2NvbXBvbmVudHMsIGRpc3BhdGNoX2RldiwgZWFjaCwgZWxlbWVudCwgZWxlbWVudF9pcywgZW1wdHksIGVuZF9oeWRyYXRpbmcsIGVzY2FwZSwgZXNjYXBlX2F0dHJpYnV0ZV92YWx1ZSwgZXNjYXBlX29iamVjdCwgZXhjbHVkZV9pbnRlcm5hbF9wcm9wcywgZml4X2FuZF9kZXN0cm95X2Jsb2NrLCBmaXhfYW5kX291dHJvX2FuZF9kZXN0cm95X2Jsb2NrLCBmaXhfcG9zaXRpb24sIGZsdXNoLCBnZXRBbGxDb250ZXh0cywgZ2V0Q29udGV4dCwgZ2V0X2FsbF9kaXJ0eV9mcm9tX3Njb3BlLCBnZXRfYmluZGluZ19ncm91cF92YWx1ZSwgZ2V0X2N1cnJlbnRfY29tcG9uZW50LCBnZXRfY3VzdG9tX2VsZW1lbnRzX3Nsb3RzLCBnZXRfcm9vdF9mb3Jfc3R5bGUsIGdldF9zbG90X2NoYW5nZXMsIGdldF9zcHJlYWRfb2JqZWN0LCBnZXRfc3ByZWFkX3VwZGF0ZSwgZ2V0X3N0b3JlX3ZhbHVlLCBnbG9iYWxzLCBncm91cF9vdXRyb3MsIGhhbmRsZV9wcm9taXNlLCBoYXNDb250ZXh0LCBoYXNfcHJvcCwgaWRlbnRpdHksIGluaXQsIGluc2VydCwgaW5zZXJ0X2RldiwgaW5zZXJ0X2h5ZHJhdGlvbiwgaW5zZXJ0X2h5ZHJhdGlvbl9kZXYsIGludHJvcywgaW52YWxpZF9hdHRyaWJ1dGVfbmFtZV9jaGFyYWN0ZXIsIGlzX2NsaWVudCwgaXNfY3Jvc3NvcmlnaW4sIGlzX2VtcHR5LCBpc19mdW5jdGlvbiwgaXNfcHJvbWlzZSwgaXNfdm9pZCwgbGlzdGVuLCBsaXN0ZW5fZGV2LCBsb29wLCBsb29wX2d1YXJkLCBtZXJnZV9zc3Jfc3R5bGVzLCBtaXNzaW5nX2NvbXBvbmVudCwgbW91bnRfY29tcG9uZW50LCBub29wLCBub3RfZXF1YWwsIG5vdywgbnVsbF90b19lbXB0eSwgb2JqZWN0X3dpdGhvdXRfcHJvcGVydGllcywgb25EZXN0cm95LCBvbk1vdW50LCBvbmNlLCBvdXRyb19hbmRfZGVzdHJveV9ibG9jaywgcHJldmVudF9kZWZhdWx0LCBwcm9wX2RldiwgcXVlcnlfc2VsZWN0b3JfYWxsLCByYWYsIHJ1biwgcnVuX2FsbCwgc2FmZV9ub3RfZXF1YWwsIHNjaGVkdWxlX3VwZGF0ZSwgc2VsZWN0X211bHRpcGxlX3ZhbHVlLCBzZWxlY3Rfb3B0aW9uLCBzZWxlY3Rfb3B0aW9ucywgc2VsZWN0X3ZhbHVlLCBzZWxmLCBzZXRDb250ZXh0LCBzZXRfYXR0cmlidXRlcywgc2V0X2N1cnJlbnRfY29tcG9uZW50LCBzZXRfY3VzdG9tX2VsZW1lbnRfZGF0YSwgc2V0X2RhdGEsIHNldF9kYXRhX2Rldiwgc2V0X2lucHV0X3R5cGUsIHNldF9pbnB1dF92YWx1ZSwgc2V0X25vdywgc2V0X3JhZiwgc2V0X3N0b3JlX3ZhbHVlLCBzZXRfc3R5bGUsIHNldF9zdmdfYXR0cmlidXRlcywgc3BhY2UsIHNwcmVhZCwgc3JjX3VybF9lcXVhbCwgc3RhcnRfaHlkcmF0aW5nLCBzdG9wX3Byb3BhZ2F0aW9uLCBzdWJzY3JpYmUsIHN2Z19lbGVtZW50LCB0ZXh0LCB0aWNrLCB0aW1lX3Jhbmdlc190b19hcnJheSwgdG9fbnVtYmVyLCB0b2dnbGVfY2xhc3MsIHRyYW5zaXRpb25faW4sIHRyYW5zaXRpb25fb3V0LCB0cnVzdGVkLCB1cGRhdGVfYXdhaXRfYmxvY2tfYnJhbmNoLCB1cGRhdGVfa2V5ZWRfZWFjaCwgdXBkYXRlX3Nsb3QsIHVwZGF0ZV9zbG90X2Jhc2UsIHZhbGlkYXRlX2NvbXBvbmVudCwgdmFsaWRhdGVfZHluYW1pY19lbGVtZW50LCB2YWxpZGF0ZV9lYWNoX2FyZ3VtZW50LCB2YWxpZGF0ZV9lYWNoX2tleXMsIHZhbGlkYXRlX3Nsb3RzLCB2YWxpZGF0ZV9zdG9yZSwgdmFsaWRhdGVfdm9pZF9keW5hbWljX2VsZW1lbnQsIHhsaW5rX2F0dHIgfTtcbiIsIi8qKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKipcclxuQ29weXJpZ2h0IChjKSBNaWNyb3NvZnQgQ29ycG9yYXRpb24uXHJcblxyXG5QZXJtaXNzaW9uIHRvIHVzZSwgY29weSwgbW9kaWZ5LCBhbmQvb3IgZGlzdHJpYnV0ZSB0aGlzIHNvZnR3YXJlIGZvciBhbnlcclxucHVycG9zZSB3aXRoIG9yIHdpdGhvdXQgZmVlIGlzIGhlcmVieSBncmFudGVkLlxyXG5cclxuVEhFIFNPRlRXQVJFIElTIFBST1ZJREVEIFwiQVMgSVNcIiBBTkQgVEhFIEFVVEhPUiBESVNDTEFJTVMgQUxMIFdBUlJBTlRJRVMgV0lUSFxyXG5SRUdBUkQgVE8gVEhJUyBTT0ZUV0FSRSBJTkNMVURJTkcgQUxMIElNUExJRUQgV0FSUkFOVElFUyBPRiBNRVJDSEFOVEFCSUxJVFlcclxuQU5EIEZJVE5FU1MuIElOIE5PIEVWRU5UIFNIQUxMIFRIRSBBVVRIT1IgQkUgTElBQkxFIEZPUiBBTlkgU1BFQ0lBTCwgRElSRUNULFxyXG5JTkRJUkVDVCwgT1IgQ09OU0VRVUVOVElBTCBEQU1BR0VTIE9SIEFOWSBEQU1BR0VTIFdIQVRTT0VWRVIgUkVTVUxUSU5HIEZST01cclxuTE9TUyBPRiBVU0UsIERBVEEgT1IgUFJPRklUUywgV0hFVEhFUiBJTiBBTiBBQ1RJT04gT0YgQ09OVFJBQ1QsIE5FR0xJR0VOQ0UgT1JcclxuT1RIRVIgVE9SVElPVVMgQUNUSU9OLCBBUklTSU5HIE9VVCBPRiBPUiBJTiBDT05ORUNUSU9OIFdJVEggVEhFIFVTRSBPUlxyXG5QRVJGT1JNQU5DRSBPRiBUSElTIFNPRlRXQVJFLlxyXG4qKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKiAqL1xyXG4vKiBnbG9iYWwgUmVmbGVjdCwgUHJvbWlzZSAqL1xyXG5cclxudmFyIGV4dGVuZFN0YXRpY3MgPSBmdW5jdGlvbihkLCBiKSB7XHJcbiAgICBleHRlbmRTdGF0aWNzID0gT2JqZWN0LnNldFByb3RvdHlwZU9mIHx8XHJcbiAgICAgICAgKHsgX19wcm90b19fOiBbXSB9IGluc3RhbmNlb2YgQXJyYXkgJiYgZnVuY3Rpb24gKGQsIGIpIHsgZC5fX3Byb3RvX18gPSBiOyB9KSB8fFxyXG4gICAgICAgIGZ1bmN0aW9uIChkLCBiKSB7IGZvciAodmFyIHAgaW4gYikgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChiLCBwKSkgZFtwXSA9IGJbcF07IH07XHJcbiAgICByZXR1cm4gZXh0ZW5kU3RhdGljcyhkLCBiKTtcclxufTtcclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX2V4dGVuZHMoZCwgYikge1xyXG4gICAgaWYgKHR5cGVvZiBiICE9PSBcImZ1bmN0aW9uXCIgJiYgYiAhPT0gbnVsbClcclxuICAgICAgICB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XHJcbiAgICBleHRlbmRTdGF0aWNzKGQsIGIpO1xyXG4gICAgZnVuY3Rpb24gX18oKSB7IHRoaXMuY29uc3RydWN0b3IgPSBkOyB9XHJcbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XHJcbn1cclxuXHJcbmV4cG9ydCB2YXIgX19hc3NpZ24gPSBmdW5jdGlvbigpIHtcclxuICAgIF9fYXNzaWduID0gT2JqZWN0LmFzc2lnbiB8fCBmdW5jdGlvbiBfX2Fzc2lnbih0KSB7XHJcbiAgICAgICAgZm9yICh2YXIgcywgaSA9IDEsIG4gPSBhcmd1bWVudHMubGVuZ3RoOyBpIDwgbjsgaSsrKSB7XHJcbiAgICAgICAgICAgIHMgPSBhcmd1bWVudHNbaV07XHJcbiAgICAgICAgICAgIGZvciAodmFyIHAgaW4gcykgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzLCBwKSkgdFtwXSA9IHNbcF07XHJcbiAgICAgICAgfVxyXG4gICAgICAgIHJldHVybiB0O1xyXG4gICAgfVxyXG4gICAgcmV0dXJuIF9fYXNzaWduLmFwcGx5KHRoaXMsIGFyZ3VtZW50cyk7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX3Jlc3QocywgZSkge1xyXG4gICAgdmFyIHQgPSB7fTtcclxuICAgIGZvciAodmFyIHAgaW4gcykgaWYgKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChzLCBwKSAmJiBlLmluZGV4T2YocCkgPCAwKVxyXG4gICAgICAgIHRbcF0gPSBzW3BdO1xyXG4gICAgaWYgKHMgIT0gbnVsbCAmJiB0eXBlb2YgT2JqZWN0LmdldE93blByb3BlcnR5U3ltYm9scyA9PT0gXCJmdW5jdGlvblwiKVxyXG4gICAgICAgIGZvciAodmFyIGkgPSAwLCBwID0gT2JqZWN0LmdldE93blByb3BlcnR5U3ltYm9scyhzKTsgaSA8IHAubGVuZ3RoOyBpKyspIHtcclxuICAgICAgICAgICAgaWYgKGUuaW5kZXhPZihwW2ldKSA8IDAgJiYgT2JqZWN0LnByb3RvdHlwZS5wcm9wZXJ0eUlzRW51bWVyYWJsZS5jYWxsKHMsIHBbaV0pKVxyXG4gICAgICAgICAgICAgICAgdFtwW2ldXSA9IHNbcFtpXV07XHJcbiAgICAgICAgfVxyXG4gICAgcmV0dXJuIHQ7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX2RlY29yYXRlKGRlY29yYXRvcnMsIHRhcmdldCwga2V5LCBkZXNjKSB7XHJcbiAgICB2YXIgYyA9IGFyZ3VtZW50cy5sZW5ndGgsIHIgPSBjIDwgMyA/IHRhcmdldCA6IGRlc2MgPT09IG51bGwgPyBkZXNjID0gT2JqZWN0LmdldE93blByb3BlcnR5RGVzY3JpcHRvcih0YXJnZXQsIGtleSkgOiBkZXNjLCBkO1xyXG4gICAgaWYgKHR5cGVvZiBSZWZsZWN0ID09PSBcIm9iamVjdFwiICYmIHR5cGVvZiBSZWZsZWN0LmRlY29yYXRlID09PSBcImZ1bmN0aW9uXCIpIHIgPSBSZWZsZWN0LmRlY29yYXRlKGRlY29yYXRvcnMsIHRhcmdldCwga2V5LCBkZXNjKTtcclxuICAgIGVsc2UgZm9yICh2YXIgaSA9IGRlY29yYXRvcnMubGVuZ3RoIC0gMTsgaSA+PSAwOyBpLS0pIGlmIChkID0gZGVjb3JhdG9yc1tpXSkgciA9IChjIDwgMyA/IGQocikgOiBjID4gMyA/IGQodGFyZ2V0LCBrZXksIHIpIDogZCh0YXJnZXQsIGtleSkpIHx8IHI7XHJcbiAgICByZXR1cm4gYyA+IDMgJiYgciAmJiBPYmplY3QuZGVmaW5lUHJvcGVydHkodGFyZ2V0LCBrZXksIHIpLCByO1xyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19wYXJhbShwYXJhbUluZGV4LCBkZWNvcmF0b3IpIHtcclxuICAgIHJldHVybiBmdW5jdGlvbiAodGFyZ2V0LCBrZXkpIHsgZGVjb3JhdG9yKHRhcmdldCwga2V5LCBwYXJhbUluZGV4KTsgfVxyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19tZXRhZGF0YShtZXRhZGF0YUtleSwgbWV0YWRhdGFWYWx1ZSkge1xyXG4gICAgaWYgKHR5cGVvZiBSZWZsZWN0ID09PSBcIm9iamVjdFwiICYmIHR5cGVvZiBSZWZsZWN0Lm1ldGFkYXRhID09PSBcImZ1bmN0aW9uXCIpIHJldHVybiBSZWZsZWN0Lm1ldGFkYXRhKG1ldGFkYXRhS2V5LCBtZXRhZGF0YVZhbHVlKTtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fYXdhaXRlcih0aGlzQXJnLCBfYXJndW1lbnRzLCBQLCBnZW5lcmF0b3IpIHtcclxuICAgIGZ1bmN0aW9uIGFkb3B0KHZhbHVlKSB7IHJldHVybiB2YWx1ZSBpbnN0YW5jZW9mIFAgPyB2YWx1ZSA6IG5ldyBQKGZ1bmN0aW9uIChyZXNvbHZlKSB7IHJlc29sdmUodmFsdWUpOyB9KTsgfVxyXG4gICAgcmV0dXJuIG5ldyAoUCB8fCAoUCA9IFByb21pc2UpKShmdW5jdGlvbiAocmVzb2x2ZSwgcmVqZWN0KSB7XHJcbiAgICAgICAgZnVuY3Rpb24gZnVsZmlsbGVkKHZhbHVlKSB7IHRyeSB7IHN0ZXAoZ2VuZXJhdG9yLm5leHQodmFsdWUpKTsgfSBjYXRjaCAoZSkgeyByZWplY3QoZSk7IH0gfVxyXG4gICAgICAgIGZ1bmN0aW9uIHJlamVjdGVkKHZhbHVlKSB7IHRyeSB7IHN0ZXAoZ2VuZXJhdG9yW1widGhyb3dcIl0odmFsdWUpKTsgfSBjYXRjaCAoZSkgeyByZWplY3QoZSk7IH0gfVxyXG4gICAgICAgIGZ1bmN0aW9uIHN0ZXAocmVzdWx0KSB7IHJlc3VsdC5kb25lID8gcmVzb2x2ZShyZXN1bHQudmFsdWUpIDogYWRvcHQocmVzdWx0LnZhbHVlKS50aGVuKGZ1bGZpbGxlZCwgcmVqZWN0ZWQpOyB9XHJcbiAgICAgICAgc3RlcCgoZ2VuZXJhdG9yID0gZ2VuZXJhdG9yLmFwcGx5KHRoaXNBcmcsIF9hcmd1bWVudHMgfHwgW10pKS5uZXh0KCkpO1xyXG4gICAgfSk7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX2dlbmVyYXRvcih0aGlzQXJnLCBib2R5KSB7XHJcbiAgICB2YXIgXyA9IHsgbGFiZWw6IDAsIHNlbnQ6IGZ1bmN0aW9uKCkgeyBpZiAodFswXSAmIDEpIHRocm93IHRbMV07IHJldHVybiB0WzFdOyB9LCB0cnlzOiBbXSwgb3BzOiBbXSB9LCBmLCB5LCB0LCBnO1xyXG4gICAgcmV0dXJuIGcgPSB7IG5leHQ6IHZlcmIoMCksIFwidGhyb3dcIjogdmVyYigxKSwgXCJyZXR1cm5cIjogdmVyYigyKSB9LCB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgKGdbU3ltYm9sLml0ZXJhdG9yXSA9IGZ1bmN0aW9uKCkgeyByZXR1cm4gdGhpczsgfSksIGc7XHJcbiAgICBmdW5jdGlvbiB2ZXJiKG4pIHsgcmV0dXJuIGZ1bmN0aW9uICh2KSB7IHJldHVybiBzdGVwKFtuLCB2XSk7IH07IH1cclxuICAgIGZ1bmN0aW9uIHN0ZXAob3ApIHtcclxuICAgICAgICBpZiAoZikgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkdlbmVyYXRvciBpcyBhbHJlYWR5IGV4ZWN1dGluZy5cIik7XHJcbiAgICAgICAgd2hpbGUgKF8pIHRyeSB7XHJcbiAgICAgICAgICAgIGlmIChmID0gMSwgeSAmJiAodCA9IG9wWzBdICYgMiA/IHlbXCJyZXR1cm5cIl0gOiBvcFswXSA/IHlbXCJ0aHJvd1wiXSB8fCAoKHQgPSB5W1wicmV0dXJuXCJdKSAmJiB0LmNhbGwoeSksIDApIDogeS5uZXh0KSAmJiAhKHQgPSB0LmNhbGwoeSwgb3BbMV0pKS5kb25lKSByZXR1cm4gdDtcclxuICAgICAgICAgICAgaWYgKHkgPSAwLCB0KSBvcCA9IFtvcFswXSAmIDIsIHQudmFsdWVdO1xyXG4gICAgICAgICAgICBzd2l0Y2ggKG9wWzBdKSB7XHJcbiAgICAgICAgICAgICAgICBjYXNlIDA6IGNhc2UgMTogdCA9IG9wOyBicmVhaztcclxuICAgICAgICAgICAgICAgIGNhc2UgNDogXy5sYWJlbCsrOyByZXR1cm4geyB2YWx1ZTogb3BbMV0sIGRvbmU6IGZhbHNlIH07XHJcbiAgICAgICAgICAgICAgICBjYXNlIDU6IF8ubGFiZWwrKzsgeSA9IG9wWzFdOyBvcCA9IFswXTsgY29udGludWU7XHJcbiAgICAgICAgICAgICAgICBjYXNlIDc6IG9wID0gXy5vcHMucG9wKCk7IF8udHJ5cy5wb3AoKTsgY29udGludWU7XHJcbiAgICAgICAgICAgICAgICBkZWZhdWx0OlxyXG4gICAgICAgICAgICAgICAgICAgIGlmICghKHQgPSBfLnRyeXMsIHQgPSB0Lmxlbmd0aCA+IDAgJiYgdFt0Lmxlbmd0aCAtIDFdKSAmJiAob3BbMF0gPT09IDYgfHwgb3BbMF0gPT09IDIpKSB7IF8gPSAwOyBjb250aW51ZTsgfVxyXG4gICAgICAgICAgICAgICAgICAgIGlmIChvcFswXSA9PT0gMyAmJiAoIXQgfHwgKG9wWzFdID4gdFswXSAmJiBvcFsxXSA8IHRbM10pKSkgeyBfLmxhYmVsID0gb3BbMV07IGJyZWFrOyB9XHJcbiAgICAgICAgICAgICAgICAgICAgaWYgKG9wWzBdID09PSA2ICYmIF8ubGFiZWwgPCB0WzFdKSB7IF8ubGFiZWwgPSB0WzFdOyB0ID0gb3A7IGJyZWFrOyB9XHJcbiAgICAgICAgICAgICAgICAgICAgaWYgKHQgJiYgXy5sYWJlbCA8IHRbMl0pIHsgXy5sYWJlbCA9IHRbMl07IF8ub3BzLnB1c2gob3ApOyBicmVhazsgfVxyXG4gICAgICAgICAgICAgICAgICAgIGlmICh0WzJdKSBfLm9wcy5wb3AoKTtcclxuICAgICAgICAgICAgICAgICAgICBfLnRyeXMucG9wKCk7IGNvbnRpbnVlO1xyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIG9wID0gYm9keS5jYWxsKHRoaXNBcmcsIF8pO1xyXG4gICAgICAgIH0gY2F0Y2ggKGUpIHsgb3AgPSBbNiwgZV07IHkgPSAwOyB9IGZpbmFsbHkgeyBmID0gdCA9IDA7IH1cclxuICAgICAgICBpZiAob3BbMF0gJiA1KSB0aHJvdyBvcFsxXTsgcmV0dXJuIHsgdmFsdWU6IG9wWzBdID8gb3BbMV0gOiB2b2lkIDAsIGRvbmU6IHRydWUgfTtcclxuICAgIH1cclxufVxyXG5cclxuZXhwb3J0IHZhciBfX2NyZWF0ZUJpbmRpbmcgPSBPYmplY3QuY3JlYXRlID8gKGZ1bmN0aW9uKG8sIG0sIGssIGsyKSB7XHJcbiAgICBpZiAoazIgPT09IHVuZGVmaW5lZCkgazIgPSBrO1xyXG4gICAgdmFyIGRlc2MgPSBPYmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9yKG0sIGspO1xyXG4gICAgaWYgKCFkZXNjIHx8IChcImdldFwiIGluIGRlc2MgPyAhbS5fX2VzTW9kdWxlIDogZGVzYy53cml0YWJsZSB8fCBkZXNjLmNvbmZpZ3VyYWJsZSkpIHtcclxuICAgICAgICBkZXNjID0geyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGZ1bmN0aW9uKCkgeyByZXR1cm4gbVtrXTsgfSB9O1xyXG4gICAgfVxyXG4gICAgT2JqZWN0LmRlZmluZVByb3BlcnR5KG8sIGsyLCBkZXNjKTtcclxufSkgOiAoZnVuY3Rpb24obywgbSwgaywgazIpIHtcclxuICAgIGlmIChrMiA9PT0gdW5kZWZpbmVkKSBrMiA9IGs7XHJcbiAgICBvW2syXSA9IG1ba107XHJcbn0pO1xyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fZXhwb3J0U3RhcihtLCBvKSB7XHJcbiAgICBmb3IgKHZhciBwIGluIG0pIGlmIChwICE9PSBcImRlZmF1bHRcIiAmJiAhT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG8sIHApKSBfX2NyZWF0ZUJpbmRpbmcobywgbSwgcCk7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX3ZhbHVlcyhvKSB7XHJcbiAgICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsIG0gPSBzICYmIG9bc10sIGkgPSAwO1xyXG4gICAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XHJcbiAgICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XHJcbiAgICAgICAgbmV4dDogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xyXG4gICAgICAgICAgICByZXR1cm4geyB2YWx1ZTogbyAmJiBvW2krK10sIGRvbmU6ICFvIH07XHJcbiAgICAgICAgfVxyXG4gICAgfTtcclxuICAgIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fcmVhZChvLCBuKSB7XHJcbiAgICB2YXIgbSA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvW1N5bWJvbC5pdGVyYXRvcl07XHJcbiAgICBpZiAoIW0pIHJldHVybiBvO1xyXG4gICAgdmFyIGkgPSBtLmNhbGwobyksIHIsIGFyID0gW10sIGU7XHJcbiAgICB0cnkge1xyXG4gICAgICAgIHdoaWxlICgobiA9PT0gdm9pZCAwIHx8IG4tLSA+IDApICYmICEociA9IGkubmV4dCgpKS5kb25lKSBhci5wdXNoKHIudmFsdWUpO1xyXG4gICAgfVxyXG4gICAgY2F0Y2ggKGVycm9yKSB7IGUgPSB7IGVycm9yOiBlcnJvciB9OyB9XHJcbiAgICBmaW5hbGx5IHtcclxuICAgICAgICB0cnkge1xyXG4gICAgICAgICAgICBpZiAociAmJiAhci5kb25lICYmIChtID0gaVtcInJldHVyblwiXSkpIG0uY2FsbChpKTtcclxuICAgICAgICB9XHJcbiAgICAgICAgZmluYWxseSB7IGlmIChlKSB0aHJvdyBlLmVycm9yOyB9XHJcbiAgICB9XHJcbiAgICByZXR1cm4gYXI7XHJcbn1cclxuXHJcbi8qKiBAZGVwcmVjYXRlZCAqL1xyXG5leHBvcnQgZnVuY3Rpb24gX19zcHJlYWQoKSB7XHJcbiAgICBmb3IgKHZhciBhciA9IFtdLCBpID0gMDsgaSA8IGFyZ3VtZW50cy5sZW5ndGg7IGkrKylcclxuICAgICAgICBhciA9IGFyLmNvbmNhdChfX3JlYWQoYXJndW1lbnRzW2ldKSk7XHJcbiAgICByZXR1cm4gYXI7XHJcbn1cclxuXHJcbi8qKiBAZGVwcmVjYXRlZCAqL1xyXG5leHBvcnQgZnVuY3Rpb24gX19zcHJlYWRBcnJheXMoKSB7XHJcbiAgICBmb3IgKHZhciBzID0gMCwgaSA9IDAsIGlsID0gYXJndW1lbnRzLmxlbmd0aDsgaSA8IGlsOyBpKyspIHMgKz0gYXJndW1lbnRzW2ldLmxlbmd0aDtcclxuICAgIGZvciAodmFyIHIgPSBBcnJheShzKSwgayA9IDAsIGkgPSAwOyBpIDwgaWw7IGkrKylcclxuICAgICAgICBmb3IgKHZhciBhID0gYXJndW1lbnRzW2ldLCBqID0gMCwgamwgPSBhLmxlbmd0aDsgaiA8IGpsOyBqKyssIGsrKylcclxuICAgICAgICAgICAgcltrXSA9IGFbal07XHJcbiAgICByZXR1cm4gcjtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fc3ByZWFkQXJyYXkodG8sIGZyb20sIHBhY2spIHtcclxuICAgIGlmIChwYWNrIHx8IGFyZ3VtZW50cy5sZW5ndGggPT09IDIpIGZvciAodmFyIGkgPSAwLCBsID0gZnJvbS5sZW5ndGgsIGFyOyBpIDwgbDsgaSsrKSB7XHJcbiAgICAgICAgaWYgKGFyIHx8ICEoaSBpbiBmcm9tKSkge1xyXG4gICAgICAgICAgICBpZiAoIWFyKSBhciA9IEFycmF5LnByb3RvdHlwZS5zbGljZS5jYWxsKGZyb20sIDAsIGkpO1xyXG4gICAgICAgICAgICBhcltpXSA9IGZyb21baV07XHJcbiAgICAgICAgfVxyXG4gICAgfVxyXG4gICAgcmV0dXJuIHRvLmNvbmNhdChhciB8fCBBcnJheS5wcm90b3R5cGUuc2xpY2UuY2FsbChmcm9tKSk7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX2F3YWl0KHYpIHtcclxuICAgIHJldHVybiB0aGlzIGluc3RhbmNlb2YgX19hd2FpdCA/ICh0aGlzLnYgPSB2LCB0aGlzKSA6IG5ldyBfX2F3YWl0KHYpO1xyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19hc3luY0dlbmVyYXRvcih0aGlzQXJnLCBfYXJndW1lbnRzLCBnZW5lcmF0b3IpIHtcclxuICAgIGlmICghU3ltYm9sLmFzeW5jSXRlcmF0b3IpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJTeW1ib2wuYXN5bmNJdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XHJcbiAgICB2YXIgZyA9IGdlbmVyYXRvci5hcHBseSh0aGlzQXJnLCBfYXJndW1lbnRzIHx8IFtdKSwgaSwgcSA9IFtdO1xyXG4gICAgcmV0dXJuIGkgPSB7fSwgdmVyYihcIm5leHRcIiksIHZlcmIoXCJ0aHJvd1wiKSwgdmVyYihcInJldHVyblwiKSwgaVtTeW1ib2wuYXN5bmNJdGVyYXRvcl0gPSBmdW5jdGlvbiAoKSB7IHJldHVybiB0aGlzOyB9LCBpO1xyXG4gICAgZnVuY3Rpb24gdmVyYihuKSB7IGlmIChnW25dKSBpW25dID0gZnVuY3Rpb24gKHYpIHsgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uIChhLCBiKSB7IHEucHVzaChbbiwgdiwgYSwgYl0pID4gMSB8fCByZXN1bWUobiwgdik7IH0pOyB9OyB9XHJcbiAgICBmdW5jdGlvbiByZXN1bWUobiwgdikgeyB0cnkgeyBzdGVwKGdbbl0odikpOyB9IGNhdGNoIChlKSB7IHNldHRsZShxWzBdWzNdLCBlKTsgfSB9XHJcbiAgICBmdW5jdGlvbiBzdGVwKHIpIHsgci52YWx1ZSBpbnN0YW5jZW9mIF9fYXdhaXQgPyBQcm9taXNlLnJlc29sdmUoci52YWx1ZS52KS50aGVuKGZ1bGZpbGwsIHJlamVjdCkgOiBzZXR0bGUocVswXVsyXSwgcik7IH1cclxuICAgIGZ1bmN0aW9uIGZ1bGZpbGwodmFsdWUpIHsgcmVzdW1lKFwibmV4dFwiLCB2YWx1ZSk7IH1cclxuICAgIGZ1bmN0aW9uIHJlamVjdCh2YWx1ZSkgeyByZXN1bWUoXCJ0aHJvd1wiLCB2YWx1ZSk7IH1cclxuICAgIGZ1bmN0aW9uIHNldHRsZShmLCB2KSB7IGlmIChmKHYpLCBxLnNoaWZ0KCksIHEubGVuZ3RoKSByZXN1bWUocVswXVswXSwgcVswXVsxXSk7IH1cclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fYXN5bmNEZWxlZ2F0b3Iobykge1xyXG4gICAgdmFyIGksIHA7XHJcbiAgICByZXR1cm4gaSA9IHt9LCB2ZXJiKFwibmV4dFwiKSwgdmVyYihcInRocm93XCIsIGZ1bmN0aW9uIChlKSB7IHRocm93IGU7IH0pLCB2ZXJiKFwicmV0dXJuXCIpLCBpW1N5bWJvbC5pdGVyYXRvcl0gPSBmdW5jdGlvbiAoKSB7IHJldHVybiB0aGlzOyB9LCBpO1xyXG4gICAgZnVuY3Rpb24gdmVyYihuLCBmKSB7IGlbbl0gPSBvW25dID8gZnVuY3Rpb24gKHYpIHsgcmV0dXJuIChwID0gIXApID8geyB2YWx1ZTogX19hd2FpdChvW25dKHYpKSwgZG9uZTogbiA9PT0gXCJyZXR1cm5cIiB9IDogZiA/IGYodikgOiB2OyB9IDogZjsgfVxyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19hc3luY1ZhbHVlcyhvKSB7XHJcbiAgICBpZiAoIVN5bWJvbC5hc3luY0l0ZXJhdG9yKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiU3ltYm9sLmFzeW5jSXRlcmF0b3IgaXMgbm90IGRlZmluZWQuXCIpO1xyXG4gICAgdmFyIG0gPSBvW1N5bWJvbC5hc3luY0l0ZXJhdG9yXSwgaTtcclxuICAgIHJldHVybiBtID8gbS5jYWxsKG8pIDogKG8gPSB0eXBlb2YgX192YWx1ZXMgPT09IFwiZnVuY3Rpb25cIiA/IF9fdmFsdWVzKG8pIDogb1tTeW1ib2wuaXRlcmF0b3JdKCksIGkgPSB7fSwgdmVyYihcIm5leHRcIiksIHZlcmIoXCJ0aHJvd1wiKSwgdmVyYihcInJldHVyblwiKSwgaVtTeW1ib2wuYXN5bmNJdGVyYXRvcl0gPSBmdW5jdGlvbiAoKSB7IHJldHVybiB0aGlzOyB9LCBpKTtcclxuICAgIGZ1bmN0aW9uIHZlcmIobikgeyBpW25dID0gb1tuXSAmJiBmdW5jdGlvbiAodikgeyByZXR1cm4gbmV3IFByb21pc2UoZnVuY3Rpb24gKHJlc29sdmUsIHJlamVjdCkgeyB2ID0gb1tuXSh2KSwgc2V0dGxlKHJlc29sdmUsIHJlamVjdCwgdi5kb25lLCB2LnZhbHVlKTsgfSk7IH07IH1cclxuICAgIGZ1bmN0aW9uIHNldHRsZShyZXNvbHZlLCByZWplY3QsIGQsIHYpIHsgUHJvbWlzZS5yZXNvbHZlKHYpLnRoZW4oZnVuY3Rpb24odikgeyByZXNvbHZlKHsgdmFsdWU6IHYsIGRvbmU6IGQgfSk7IH0sIHJlamVjdCk7IH1cclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fbWFrZVRlbXBsYXRlT2JqZWN0KGNvb2tlZCwgcmF3KSB7XHJcbiAgICBpZiAoT2JqZWN0LmRlZmluZVByb3BlcnR5KSB7IE9iamVjdC5kZWZpbmVQcm9wZXJ0eShjb29rZWQsIFwicmF3XCIsIHsgdmFsdWU6IHJhdyB9KTsgfSBlbHNlIHsgY29va2VkLnJhdyA9IHJhdzsgfVxyXG4gICAgcmV0dXJuIGNvb2tlZDtcclxufTtcclxuXHJcbnZhciBfX3NldE1vZHVsZURlZmF1bHQgPSBPYmplY3QuY3JlYXRlID8gKGZ1bmN0aW9uKG8sIHYpIHtcclxuICAgIE9iamVjdC5kZWZpbmVQcm9wZXJ0eShvLCBcImRlZmF1bHRcIiwgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdiB9KTtcclxufSkgOiBmdW5jdGlvbihvLCB2KSB7XHJcbiAgICBvW1wiZGVmYXVsdFwiXSA9IHY7XHJcbn07XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19pbXBvcnRTdGFyKG1vZCkge1xyXG4gICAgaWYgKG1vZCAmJiBtb2QuX19lc01vZHVsZSkgcmV0dXJuIG1vZDtcclxuICAgIHZhciByZXN1bHQgPSB7fTtcclxuICAgIGlmIChtb2QgIT0gbnVsbCkgZm9yICh2YXIgayBpbiBtb2QpIGlmIChrICE9PSBcImRlZmF1bHRcIiAmJiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwobW9kLCBrKSkgX19jcmVhdGVCaW5kaW5nKHJlc3VsdCwgbW9kLCBrKTtcclxuICAgIF9fc2V0TW9kdWxlRGVmYXVsdChyZXN1bHQsIG1vZCk7XHJcbiAgICByZXR1cm4gcmVzdWx0O1xyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gX19pbXBvcnREZWZhdWx0KG1vZCkge1xyXG4gICAgcmV0dXJuIChtb2QgJiYgbW9kLl9fZXNNb2R1bGUpID8gbW9kIDogeyBkZWZhdWx0OiBtb2QgfTtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fY2xhc3NQcml2YXRlRmllbGRHZXQocmVjZWl2ZXIsIHN0YXRlLCBraW5kLCBmKSB7XHJcbiAgICBpZiAoa2luZCA9PT0gXCJhXCIgJiYgIWYpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJQcml2YXRlIGFjY2Vzc29yIHdhcyBkZWZpbmVkIHdpdGhvdXQgYSBnZXR0ZXJcIik7XHJcbiAgICBpZiAodHlwZW9mIHN0YXRlID09PSBcImZ1bmN0aW9uXCIgPyByZWNlaXZlciAhPT0gc3RhdGUgfHwgIWYgOiAhc3RhdGUuaGFzKHJlY2VpdmVyKSkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNhbm5vdCByZWFkIHByaXZhdGUgbWVtYmVyIGZyb20gYW4gb2JqZWN0IHdob3NlIGNsYXNzIGRpZCBub3QgZGVjbGFyZSBpdFwiKTtcclxuICAgIHJldHVybiBraW5kID09PSBcIm1cIiA/IGYgOiBraW5kID09PSBcImFcIiA/IGYuY2FsbChyZWNlaXZlcikgOiBmID8gZi52YWx1ZSA6IHN0YXRlLmdldChyZWNlaXZlcik7XHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBfX2NsYXNzUHJpdmF0ZUZpZWxkU2V0KHJlY2VpdmVyLCBzdGF0ZSwgdmFsdWUsIGtpbmQsIGYpIHtcclxuICAgIGlmIChraW5kID09PSBcIm1cIikgdGhyb3cgbmV3IFR5cGVFcnJvcihcIlByaXZhdGUgbWV0aG9kIGlzIG5vdCB3cml0YWJsZVwiKTtcclxuICAgIGlmIChraW5kID09PSBcImFcIiAmJiAhZikgdGhyb3cgbmV3IFR5cGVFcnJvcihcIlByaXZhdGUgYWNjZXNzb3Igd2FzIGRlZmluZWQgd2l0aG91dCBhIHNldHRlclwiKTtcclxuICAgIGlmICh0eXBlb2Ygc3RhdGUgPT09IFwiZnVuY3Rpb25cIiA/IHJlY2VpdmVyICE9PSBzdGF0ZSB8fCAhZiA6ICFzdGF0ZS5oYXMocmVjZWl2ZXIpKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2Fubm90IHdyaXRlIHByaXZhdGUgbWVtYmVyIHRvIGFuIG9iamVjdCB3aG9zZSBjbGFzcyBkaWQgbm90IGRlY2xhcmUgaXRcIik7XHJcbiAgICByZXR1cm4gKGtpbmQgPT09IFwiYVwiID8gZi5jYWxsKHJlY2VpdmVyLCB2YWx1ZSkgOiBmID8gZi52YWx1ZSA9IHZhbHVlIDogc3RhdGUuc2V0KHJlY2VpdmVyLCB2YWx1ZSkpLCB2YWx1ZTtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIF9fY2xhc3NQcml2YXRlRmllbGRJbihzdGF0ZSwgcmVjZWl2ZXIpIHtcclxuICAgIGlmIChyZWNlaXZlciA9PT0gbnVsbCB8fCAodHlwZW9mIHJlY2VpdmVyICE9PSBcIm9iamVjdFwiICYmIHR5cGVvZiByZWNlaXZlciAhPT0gXCJmdW5jdGlvblwiKSkgdGhyb3cgbmV3IFR5cGVFcnJvcihcIkNhbm5vdCB1c2UgJ2luJyBvcGVyYXRvciBvbiBub24tb2JqZWN0XCIpO1xyXG4gICAgcmV0dXJuIHR5cGVvZiBzdGF0ZSA9PT0gXCJmdW5jdGlvblwiID8gcmVjZWl2ZXIgPT09IHN0YXRlIDogc3RhdGUuaGFzKHJlY2VpdmVyKTtcclxufVxyXG4iLCI8c2NyaXB0IGxhbmc9XCJ0c1wiPlxyXG4gICAgaW1wb3J0IHR5cGUgVGFibGVHZW5lcmF0b3JQbHVnaW4gZnJvbSBcIi4uLy4uL3RhYmxlR2VuZXJhdG9ySW5kZXhcIjtcclxuXHJcbiAgICBleHBvcnQgbGV0IHBsdWdpbjogVGFibGVHZW5lcmF0b3JQbHVnaW47XHJcbiAgICBleHBvcnQgbGV0IHJvd051bTogbnVtYmVyID0gODtcclxuICAgIGV4cG9ydCBsZXQgY29sTnVtOiBudW1iZXIgPSA4O1xyXG4gICAgZXhwb3J0IGxldCBob3ZlclRhYmxlRW5kOiBudW1iZXJbXTtcclxuICAgIGV4cG9ydCBsZXQgaW5zZXJ0VGFibGU6IChzZWxlY3RlZFRhYmxlRW5kOiBudW1iZXJbXSkgPT4gdm9pZDtcclxuXHJcbiAgICBsZXQgZ3JpZCA9IFtyb3dOdW0sIGNvbE51bV07XHJcblxyXG4gICAgJDogY29sID0gYHJlcGVhdCgkeyBncmlkWzFdIH0sIDFmcilgO1xyXG4gICAgJDogcm93ID0gYHJlcGVhdCgkeyBncmlkWzBdIH0sIDFmcilgO1xyXG4gICAgJDogaXNfYWN0aXZlID0gQXJyYXkoZ3JpZFswXSkuZmlsbCgwKS5tYXAoXyA9PiBBcnJheShncmlkWzFdKS5maWxsKGZhbHNlKSk7XHJcblxyXG4gICAgbGV0IHN0YXJ0OiBudW1iZXJbXSA9IFtdO1xyXG4gICAgbGV0IGVuZDogbnVtYmVyW10gPSBbXTtcclxuXHJcbiAgICBmdW5jdGlvbiBob3ZlcihpOiBudW1iZXIsIGo6IG51bWJlcikge1xyXG4gICAgICAgIHN0YXJ0ID0gWzAsIDBdO1xyXG4gICAgICAgIGVuZCA9IFtpLCBqXTtcclxuICAgICAgICBob3ZlclRhYmxlRW5kID0gW2kgKyAxLCBqICsgMV07XHJcbiAgICAgICAgY2hlY2tBY3RpdmUoZW5kKTtcclxuICAgIH1cclxuXHJcbiAgICBmdW5jdGlvbiB1bkhvdmVyKCkge1xyXG4gICAgICAgIHN0YXJ0ID0gZW5kID0gWy0xLCAtMV07XHJcbiAgICAgICAgc2V0VGltZW91dCgoKSA9PiB7XHJcbiAgICAgICAgICAgIGhvdmVyVGFibGVFbmQgPSBbMCwgMF07XHJcbiAgICAgICAgICAgIGNoZWNrQWN0aXZlKGVuZCk7XHJcbiAgICAgICAgfSwgMTAwMCk7XHJcbiAgICB9XHJcblxyXG4gICAgZnVuY3Rpb24gY2xpY2soaTogbnVtYmVyLCBqOiBudW1iZXIpIHtcclxuICAgICAgICBpZiAoaiA9PT0gMCkgcmV0dXJuO1xyXG4gICAgICAgIGluc2VydFRhYmxlKFtpICsgMSwgaiArIDFdKTtcclxuICAgICAgICBwbHVnaW4uaGlkZVRhYmxlKCk7XHJcbiAgICB9XHJcblxyXG4gICAgZnVuY3Rpb24gaXNJblJhbmdlKFtpLCBqXTogbnVtYmVyW10sIFtpMiwgajJdOiBudW1iZXJbXSkge1xyXG4gICAgICAgIHJldHVybiAoKGkgLSBzdGFydFswXSkgKiAoaSAtIGkyKSA8PSAwKSAmJlxyXG4gICAgICAgICAgICAoKGogLSBzdGFydFsxXSkgKiAoaiAtIGoyKSA8PSAwKVxyXG4gICAgfVxyXG5cclxuICAgIGZ1bmN0aW9uIGNoZWNrQWN0aXZlKGVuZDogbnVtYmVyW10pIHtcclxuICAgICAgICBpc19hY3RpdmUgPSBpc19hY3RpdmUubWFwKFxyXG4gICAgICAgICAgICAoYSwgaSkgPT4gYS5tYXAoKF8sIGopID0+IGlzSW5SYW5nZShbaSwgal0sIGVuZCkpKTtcclxuICAgIH1cclxuPC9zY3JpcHQ+XHJcblxyXG48ZGl2IGNsYXNzPVwidGFibGUtY29udGFpbmVyXCIgc3R5bGU6Z3JpZC10ZW1wbGF0ZS1yb3dzPXtyb3d9IHN0eWxlOmdyaWQtdGVtcGxhdGUtY29sdW1ucz17Y29sfVxyXG4gICAgIG9uOm1vdXNlbGVhdmU9eygpID0+IHVuSG92ZXIoKX0gb246Ymx1cj17KCkgPT4gdW5Ib3ZlcigpfT5cclxuICAgIHsjZWFjaCB7bGVuZ3RoOiBncmlkWzBdfSBhcyBfLCBpIChpKX1cclxuICAgICAgICB7I2VhY2gge2xlbmd0aDogZ3JpZFsxXX0gYXMgXywgaiAoail9XHJcbiAgICAgICAgICAgIDxkaXZcclxuICAgICAgICAgICAgICAgIGNsYXNzPVwidGFibGUtZ2VuZXJhdG9yLWNlbGxcIlxyXG4gICAgICAgICAgICAgICAgY2xhc3M6YWN0aXZlPXtpc19hY3RpdmVbaV1bal19XHJcbiAgICAgICAgICAgICAgICBvbjptb3VzZWVudGVyPXsoKSA9PiBob3ZlcihpLCBqKX1cclxuICAgICAgICAgICAgICAgIG9uOmNsaWNrPXsoKSA9PiBjbGljayhpLCBqKX1cclxuICAgICAgICAgICAgPjwvZGl2PlxyXG4gICAgICAgIHsvZWFjaH1cclxuICAgIHsvZWFjaH1cclxuPC9kaXY+XHJcblxyXG48c3R5bGU+XHJcblxyXG4gICAgLnRhYmxlLWNvbnRhaW5lciB7XHJcbiAgICAgICAgZGlzcGxheTogZ3JpZDtcclxuICAgICAgICBib3JkZXItYm90dG9tOiAycHggZG90dGVkIHZhcigtLWNvbG9yLWJhc2UtNDApO1xyXG4gICAgICAgIGJvcmRlci10b3A6IDJweCBkb3R0ZWQgdmFyKC0tY29sb3ItYmFzZS00MCk7XHJcbiAgICAgICAgcGFkZGluZy10b3A6IHZhcigtLXNpemUtMi0xKTtcclxuICAgICAgICBwYWRkaW5nLWJvdHRvbTogdmFyKC0tc2l6ZS0yLTEpO1xyXG4gICAgICAgIHdpZHRoOiAxMDAlO1xyXG4gICAgICAgIGhlaWdodDogMTUwcHg7XHJcbiAgICAgICAgZ3JpZC1nYXA6IDFweDtcclxuICAgIH1cclxuXHJcbiAgICAudGFibGUtY29udGFpbmVyIGRpdiB7XHJcbiAgICAgICAgYmFja2dyb3VuZDogdmFyKC0tY29sb3ItYmFzZS0wMCk7XHJcbiAgICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0tcmFkaXVzLXMpO1xyXG4gICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWNvbG9yLWJhc2UtNDApO1xyXG4gICAgfVxyXG5cclxuICAgIC50YWJsZS1jb250YWluZXIgLnRhYmxlLWdlbmVyYXRvci1jZWxsIHtcclxuICAgICAgICBoZWlnaHQ6IHZhcigtLXNpemUtNC00KTtcclxuICAgICAgICB3aWR0aDogdmFyKC0tc2l6ZS00LTQpO1xyXG4gICAgfVxyXG5cclxuICAgIGRpdi5hY3RpdmUge1xyXG4gICAgICAgIGJhY2tncm91bmQtY29sb3I6IHZhcigtLWFjdGl2ZS1jb2xvcik7XHJcbiAgICB9XHJcblxyXG48L3N0eWxlPlxyXG4iLCI8c2NyaXB0IGxhbmc9XCJ0c1wiPlxyXG4gICAgaW1wb3J0IFRhYmxlIGZyb20gXCIuL1RhYmxlLnN2ZWx0ZVwiO1xyXG4gICAgaW1wb3J0IHsgTm90aWNlIH0gZnJvbSBcIm9ic2lkaWFuXCI7XHJcbiAgICBpbXBvcnQgdHlwZSBUYWJsZUdlbmVyYXRvclBsdWdpbiBmcm9tIFwiLi4vLi4vdGFibGVHZW5lcmF0b3JJbmRleFwiO1xyXG5cclxuICAgIGV4cG9ydCBsZXQgdGl0bGU6IHN0cmluZztcclxuICAgIGV4cG9ydCBsZXQgcGx1Z2luOiBUYWJsZUdlbmVyYXRvclBsdWdpbjtcclxuICAgIGV4cG9ydCBsZXQgb25JbnNlcnQ6IChzZWxlY3RlZEdyaWQ6IG51bWJlcltdKSA9PiB2b2lkO1xyXG5cclxuICAgIGxldCBob3ZlclRhYmxlRW5kOiBudW1iZXJbXTtcclxuICAgIGxldCBncmlkUm93OiBudW1iZXI7XHJcbiAgICBsZXQgZ3JpZENvbDogbnVtYmVyO1xyXG5cclxuICAgICQ6IGlmIChob3ZlclRhYmxlRW5kKSB7XHJcbiAgICAgICAgc2V0Um93QW5kQ29sKGhvdmVyVGFibGVFbmQpO1xyXG4gICAgfVxyXG5cclxuICAgIGxldCBzZXR0aW5ncyA9IHtcclxuICAgICAgICByb3dOdW06IHBsdWdpbj8uc2V0dGluZ3Mucm93Q291bnQgPz8gOCxcclxuICAgICAgICBjb2xOdW06IHBsdWdpbj8uc2V0dGluZ3MuY29sdW1uQ291bnQgPz8gOCxcclxuICAgIH1cclxuXHJcbiAgICBmdW5jdGlvbiBzZXRSb3dBbmRDb2woZW5kOiBudW1iZXJbXSkge1xyXG4gICAgICAgIGlmIChlbmQubGVuZ3RoID09PSAwKSB7XHJcbiAgICAgICAgICAgIGdyaWRSb3cgPSAwO1xyXG4gICAgICAgICAgICBncmlkQ29sID0gMDtcclxuICAgICAgICAgICAgcmV0dXJuO1xyXG4gICAgICAgIH1cclxuICAgICAgICBpZiAoIShob3ZlclRhYmxlRW5kWzBdID09PSAwICYmIGhvdmVyVGFibGVFbmRbMV0gPT09IDApKSB7XHJcbiAgICAgICAgICAgIGdyaWRSb3cgPSBob3ZlclRhYmxlRW5kWzBdO1xyXG4gICAgICAgICAgICBncmlkQ29sID0gaG92ZXJUYWJsZUVuZFsxXTtcclxuICAgICAgICB9XHJcbiAgICB9XHJcbjwvc2NyaXB0PlxyXG5cclxuPGRpdiBjbGFzcz1cInRhYmxlLWdlbmVyYXRvclwiPlxyXG4gICAgPGRpdiBjbGFzcz1cInRhYmxlLWdlbmVyYXRvci1oZWFkZXJcIj5cclxuICAgICAgICA8ZGl2IGNsYXNzPVwiSDFcIj5cclxuICAgICAgICAgICAge3RpdGxlfVxyXG4gICAgICAgIDwvZGl2PlxyXG4gICAgICAgIDxzbG90IG5hbWU9XCJoZWFkZXJDb250cm9sc1wiPjwvc2xvdD5cclxuICAgIDwvZGl2PlxyXG4gICAgPFRhYmxlIHJvd051bT17c2V0dGluZ3Mucm93TnVtfSBjb2xOdW09e3NldHRpbmdzLmNvbE51bX0gaW5zZXJ0VGFibGU9e29uSW5zZXJ0fSB7cGx1Z2lufVxyXG4gICAgICAgICAgIGJpbmQ6aG92ZXJUYWJsZUVuZD17aG92ZXJUYWJsZUVuZH0vPlxyXG4gICAgPGRpdiBjbGFzcz1cImlucHV0LXRhYmxlLWdlbmVyYXRvclwiPlxyXG4gICAgICAgIDxkaXYgY2xhc3M9XCJpbnB1dC10YWJsZS1nZW5lcmF0b3Itcm93XCI+XHJcbiAgICAgICAgICAgIFJPVzpcclxuICAgICAgICAgICAgPGlucHV0IGNsYXNzPVwicm93LWlucHV0XCIgYmluZDp2YWx1ZT17Z3JpZFJvd30+XHJcbiAgICAgICAgPC9kaXY+XHJcbiAgICAgICAgPGRpdiBjbGFzcz1cImlucHV0LXRhYmxlLWdlbmVyYXRvci1jb2xcIj5cclxuICAgICAgICAgICAgQ09MOlxyXG4gICAgICAgICAgICA8aW5wdXQgY2xhc3M9XCJjb2wtaW5wdXRcIiBiaW5kOnZhbHVlPXtncmlkQ29sfT5cclxuICAgICAgICA8L2Rpdj5cclxuICAgIDwvZGl2PlxyXG4gICAgPHNsb3QgbmFtZT1cInNpemVDb250cm9sc1wiPjwvc2xvdD5cclxuICAgIDxidXR0b24gb246Y2xpY2s9eygpID0+IHtcclxuICAgICAgICAgICAgaWYoL15cXGQrJC8udGVzdChncmlkUm93LnRvU3RyaW5nKCkpICYmIC9eXFxkKyQvLnRlc3QoZ3JpZENvbC50b1N0cmluZygpKSkge1xyXG4gICAgICAgICAgICAgICAgb25JbnNlcnQoW2dyaWRSb3csIGdyaWRDb2xdKTtcclxuICAgICAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgICAgICAgIG5ldyBOb3RpY2UoXCJQbGVhc2UgZW50ZXIgYSB2YWxpZCBudW1iZXJcIik7XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9fT5JbnNlcnRcclxuICAgIDwvYnV0dG9uPlxyXG48L2Rpdj5cclxuXHJcbjxzdHlsZT5cclxuICAgIC50YWJsZS1nZW5lcmF0b3Ige1xyXG4gICAgICAgIHBhZGRpbmctbGVmdDogNXB4O1xyXG4gICAgICAgIHBhZGRpbmctcmlnaHQ6IDVweDtcclxuICAgICAgICB3aWR0aDogMjIwcHg7XHJcbiAgICB9XHJcblxyXG4gICAgLnRhYmxlLWdlbmVyYXRvci1oZWFkZXIge1xyXG4gICAgICAgIGRpc3BsYXk6IGZsZXg7XHJcbiAgICAgICAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuO1xyXG4gICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XHJcbiAgICAgICAgbWFyZ2luLXRvcDogdmFyKC0tc2l6ZS00LTEpO1xyXG4gICAgICAgIG1hcmdpbi1ib3R0b206IHZhcigtLXNpemUtNC0xKTtcclxuICAgIH1cclxuXHJcbiAgICAuaW5wdXQtdGFibGUtZ2VuZXJhdG9yIHtcclxuICAgICAgICBtYXJnaW4tbGVmdDogdmFyKC0tc2l6ZS0yLTIpO1xyXG4gICAgICAgIG1hcmdpbi1yaWdodDogdmFyKC0tc2l6ZS0yLTIpO1xyXG4gICAgICAgIG1hcmdpbi10b3A6IHZhcigtLXNpemUtNC0yKTtcclxuICAgICAgICBtYXJnaW4tYm90dG9tOiB2YXIoLS1zaXplLTQtMik7XHJcbiAgICAgICAgZGlzcGxheTogZmxleDtcclxuICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWFyb3VuZDtcclxuICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG4gICAgfVxyXG5cclxuICAgIC5pbnB1dC10YWJsZS1nZW5lcmF0b3Itcm93LCAuaW5wdXQtdGFibGUtZ2VuZXJhdG9yLWNvbCB7XHJcbiAgICAgICAgZGlzcGxheTogZmxleDtcclxuICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWFyb3VuZDtcclxuICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG4gICAgfVxyXG5cclxuICAgIGJ1dHRvbiB7XHJcbiAgICAgICAgd2lkdGg6IDgwcHg7XHJcbiAgICAgICAgaGVpZ2h0OiAyMHB4O1xyXG4gICAgICAgIG1hcmdpbjogdmFyKC0tc2l6ZS00LTEpIGF1dG8gdmFyKC0tc2l6ZS00LTIpO1xyXG4gICAgICAgIHBhZGRpbmc6IDBweCAxMHB4O1xyXG4gICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjtcclxuICAgICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7XHJcbiAgICAgICAgZGlzcGxheTogZmxleDtcclxuICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG4gICAgfVxyXG5cclxuICAgIGlucHV0IHtcclxuICAgICAgICB3aWR0aDogNDBweDtcclxuICAgICAgICBoZWlnaHQ6IDE4cHg7XHJcbiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tY29sb3ItYmFzZS01MCk7XHJcbiAgICAgICAgbWFyZ2luLWxlZnQ6IHZhcigtLXNpemUtMi0yKTtcclxuICAgICAgICBib3JkZXItcmFkaXVzOiB2YXIoLS1yYWRpdXMtbSk7XHJcbiAgICAgICAgdGV4dC1hbGlnbjogY2VudGVyO1xyXG4gICAgfVxyXG5cclxuICAgIC5IMSB7XHJcbiAgICAgICAgbWFyZ2luLWxlZnQ6IGF1dG87XHJcbiAgICAgICAgbWFyZ2luLXJpZ2h0OiBhdXRvO1xyXG4gICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjtcclxuICAgIH1cclxuPC9zdHlsZT5cclxuIiwiaW1wb3J0IHR5cGUgeyBFZGl0b3IgfSBmcm9tIFwib2JzaWRpYW5cIjtcclxuXHJcbmNvbnN0IGFsaWduTGluZVRleHQgPSAoYWxpZ246IEFsaWduTW9kZSkgPT4ge1xyXG4gICAgc3dpdGNoIChhbGlnbikge1xyXG4gICAgICAgIGNhc2UgXCJsZWZ0XCI6XHJcbiAgICAgICAgICAgIHJldHVybiBcInw6LS0tLS1cIjtcclxuICAgICAgICBjYXNlIFwiY2VudGVyXCI6XHJcbiAgICAgICAgICAgIHJldHVybiBcInw6LS0tLTpcIjtcclxuICAgICAgICBjYXNlIFwicmlnaHRcIjpcclxuICAgICAgICAgICAgcmV0dXJuIFwifC0tLS0tOlwiO1xyXG4gICAgICAgIGRlZmF1bHQ6XHJcbiAgICAgICAgICAgIHJldHVybiBcIlwiO1xyXG4gICAgfVxyXG59XHJcblxyXG5leHBvcnQgY29uc3QgZ2VuZXJhdGVNYXJrZG93blRhYmxlID0gKHNlbGVjdGVkR3JpZDogbnVtYmVyW10sIGFsaWduOiBBbGlnbk1vZGUpID0+IHtcclxuICAgIGxldCB0YWJsZSA9IFwiXCI7XHJcbiAgICBsZXQgc2Vjb25kTGluZSA9IFwiXCI7XHJcbiAgICBsZXQgbm9ybWFsTGluZSA9IFwiXCI7XHJcbiAgICBjb25zdCBhbGlnblRleHQgPSBhbGlnbkxpbmVUZXh0KGFsaWduKTtcclxuICAgIGlmIChzZWxlY3RlZEdyaWQubGVuZ3RoID09PSAwKSByZXR1cm4gdGFibGU7XHJcblxyXG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBOdW1iZXIoc2VsZWN0ZWRHcmlkWzFdKTsgaSsrKSB7XHJcbiAgICAgICAgc2Vjb25kTGluZSArPSBhbGlnblRleHQ7XHJcbiAgICB9XHJcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IE51bWJlcihzZWxlY3RlZEdyaWRbMV0pOyBpKyspIHtcclxuICAgICAgICBub3JtYWxMaW5lICs9IFwifCAgICAgIFwiO1xyXG4gICAgfVxyXG5cclxuICAgIGlmICghc2VsZWN0ZWRHcmlkWzBdKSB7XHJcbiAgICAgICAgdGFibGUgPSBub3JtYWxMaW5lICsgXCJ8XFxuXCIgKyBzZWNvbmRMaW5lICsgXCJ8XFxuXCI7XHJcbiAgICAgICAgcmV0dXJuIHRhYmxlO1xyXG4gICAgfVxyXG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBOdW1iZXIoc2VsZWN0ZWRHcmlkWzBdKSArIDE7IGkrKykge1xyXG4gICAgICAgIGlmICghaSkgdGFibGUgPSB0YWJsZSArIG5vcm1hbExpbmUgKyBcInxcXG5cIjtcclxuICAgICAgICBpZiAoaSA9PT0gMSkgdGFibGUgPSB0YWJsZSArIHNlY29uZExpbmUgKyBcInxcXG5cIjtcclxuICAgICAgICBpZiAoaSA+IDEpIHRhYmxlID0gdGFibGUgKyBub3JtYWxMaW5lICsgXCJ8XFxuXCI7XHJcbiAgICB9XHJcbiAgICByZXR1cm4gdGFibGUudHJpbSgpO1xyXG59XHJcblxyXG5leHBvcnQgZnVuY3Rpb24gY2hlY2tCbGFua0xpbmUoZWRpdG9yOiBFZGl0b3IsIGxpbmU6IG51bWJlcikge1xyXG4gICAgY29uc3QgZ2V0TGluZSA9IGVkaXRvci5nZXRMaW5lKGxpbmUpO1xyXG4gICAgaWYgKGdldExpbmUudHJpbSgpLmxlbmd0aCA+IDApIHJldHVybiBmYWxzZTtcclxuICAgIHJldHVybiB0cnVlO1xyXG59XHJcbiIsIjxzY3JpcHQgbGFuZz1cInRzXCI+XHJcbiAgICBpbXBvcnQgeyBvbk1vdW50LCBjcmVhdGVFdmVudERpc3BhdGNoZXIgfSBmcm9tIFwic3ZlbHRlXCI7XHJcbiAgICBpbXBvcnQgeyBzZXRJY29uIH0gZnJvbSBcIm9ic2lkaWFuXCI7XHJcblxyXG4gICAgZXhwb3J0IGxldCBhbGlnbjogQWxpZ25Nb2RlID0gJ2xlZnQnO1xyXG5cclxuICAgIGNvbnN0IGRpc3BhdGNoID0gY3JlYXRlRXZlbnREaXNwYXRjaGVyKCk7XHJcbiAgICBjb25zdCBhbGlnbm1lbnRzOiBBbGlnbk1vZGVbXSA9IFsnbGVmdCcsICdjZW50ZXInLCAncmlnaHQnXTtcclxuXHJcbiAgICBsZXQgcmVmczogUmVmc09iamVjdCA9IHt9O1xyXG5cclxuICAgIG9uTW91bnQoKCkgPT4ge1xyXG4gICAgICAgIHNldEljb24ocmVmc1snbGVmdCddISwgJ2FsaWduLWxlZnQnKTtcclxuICAgICAgICBzZXRJY29uKHJlZnNbJ2NlbnRlciddISwgJ2FsaWduLWNlbnRlcicpO1xyXG4gICAgICAgIHNldEljb24ocmVmc1sncmlnaHQnXSEsICdhbGlnbi1yaWdodCcpO1xyXG4gICAgfSk7XHJcblxyXG4gICAgZnVuY3Rpb24gY2xpY2sodXBkYXRlOiBBbGlnbk1vZGUpIHtcclxuICAgICAgICBhbGlnbiA9IHVwZGF0ZTtcclxuICAgICAgICBkaXNwYXRjaCgndXBkYXRlJywgYWxpZ24pO1xyXG4gICAgfVxyXG48L3NjcmlwdD5cclxuXHJcbjxkaXYgY2xhc3M9XCJ0YWJsZS1nZW5lcmF0b3ItYWxpZ24tZ3JvdXBcIj5cclxuICAgIHsjZWFjaCBhbGlnbm1lbnRzIGFzIGFsaWdubWVudCAoYWxpZ25tZW50KX1cclxuICAgICAgICA8ZGl2XHJcbiAgICAgICAgICAgIGJpbmQ6dGhpcz17cmVmc1thbGlnbm1lbnRdfVxyXG4gICAgICAgICAgICBjbGFzcz1cInRhYmxlLWdlbmVyYXRvci1hbGlnbi1pY29uXCJcclxuICAgICAgICAgICAgY2xhc3M6YWN0aXZlPXthbGlnbiA9PT0gYWxpZ25tZW50fVxyXG4gICAgICAgICAgICBvbjpjbGljaz17KCkgPT4gY2xpY2soYWxpZ25tZW50KX1cclxuICAgICAgICA+PC9kaXY+XHJcbiAgICB7L2VhY2h9XHJcbjwvZGl2PlxyXG5cclxuPHN0eWxlPlxyXG4gICAgLnRhYmxlLWdlbmVyYXRvci1hbGlnbi1ncm91cCB7XHJcbiAgICAgICAgZGlzcGxheTogZmxleDtcclxuICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG4gICAgICAgIGZsZXgtZGlyZWN0aW9uOiByb3c7XHJcbiAgICAgICAgZ2FwOiB2YXIoLS1zaXplLTItMik7XHJcbiAgICB9XHJcblxyXG4gICAgLnRhYmxlLWdlbmVyYXRvci1hbGlnbi1pY29uIHtcclxuICAgICAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XHJcbiAgICAgICAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7XHJcbiAgICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0tcmFkaXVzLXMpO1xyXG4gICAgICAgIHBhZGRpbmc6IHZhcigtLXNpemUtMi0xKTtcclxuICAgIH1cclxuXHJcbiAgICAudGFibGUtZ2VuZXJhdG9yLWFsaWduLWljb246bm90KC5hY3RpdmUpOmhvdmVyIHtcclxuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1iYWNrZ3JvdW5kLW1vZGlmaWVyLWhvdmVyKTtcclxuICAgIH1cclxuXHJcbiAgICAudGFibGUtZ2VuZXJhdG9yLWFsaWduLWljb24uYWN0aXZlIHtcclxuICAgICAgICBiYWNrZ3JvdW5kLWNvbG9yOiB2YXIoLS1iYWNrZ3JvdW5kLW1vZGlmaWVyLWJvcmRlci1ob3Zlcik7XHJcbiAgICB9XHJcbjwvc3R5bGU+XHJcbiIsIjxzY3JpcHQgbGFuZz1cInRzXCI+XHJcbiAgICBpbXBvcnQgdHlwZSB7IEVkaXRvciB9IGZyb20gXCJvYnNpZGlhblwiO1xyXG4gICAgaW1wb3J0IFRhYmxlR2VuZXJhdG9yQ29tcG9uZW50IGZyb20gXCIuL2Jhc2ljL1RhYmxlR2VuZXJhdG9yQ29tcG9uZW50LnN2ZWx0ZVwiO1xyXG4gICAgaW1wb3J0IHsgY2hlY2tCbGFua0xpbmUsIGdlbmVyYXRlTWFya2Rvd25UYWJsZSB9IGZyb20gXCIuLi91dGlscy9tYXJrZG93blRhYmxlXCI7XHJcbiAgICBpbXBvcnQgdHlwZSBUYWJsZUdlbmVyYXRvclBsdWdpbiBmcm9tIFwiLi4vdGFibGVHZW5lcmF0b3JJbmRleFwiO1xyXG4gICAgaW1wb3J0IEFsaWduSXRlbXMgZnJvbSBcIi4vYmFzaWMvQWxpZ25JdGVtcy5zdmVsdGVcIjtcclxuXHJcbiAgICBleHBvcnQgbGV0IGVkaXRvcjogRWRpdG9yO1xyXG4gICAgZXhwb3J0IGxldCBwbHVnaW46IFRhYmxlR2VuZXJhdG9yUGx1Z2luO1xyXG4gICAgbGV0IGN1cnJlbnRBbGlnbjogQWxpZ25Nb2RlID0gcGx1Z2luPy5zZXR0aW5ncy5kZWZhdWx0QWxpZ25tZW50ID8/ICdsZWZ0JztcclxuXHJcbiAgICBhc3luYyBmdW5jdGlvbiBoYW5kbGVBbGlnbk1vZGVVcGRhdGUoZXZlbnQ6IGFueSkge1xyXG4gICAgICAgIGN1cnJlbnRBbGlnbiA9IGV2ZW50LmRldGFpbDtcclxuICAgICAgICAvLyBAdHMtaWdub3JlXHJcbiAgICAgICAgcGx1Z2luPy5zZXR0aW5ncz8uZGVmYXVsdEFsaWdubWVudCA9IGN1cnJlbnRBbGlnbjtcclxuICAgICAgICBhd2FpdCBwbHVnaW4/LnNhdmVTZXR0aW5ncygpO1xyXG4gICAgfVxyXG5cclxuICAgIGZ1bmN0aW9uIGluc2VydFRhYmxlKHNlbGVjdGVkR3JpZDogbnVtYmVyW10pIHtcclxuICAgICAgICBpZiAoc2VsZWN0ZWRHcmlkLmxlbmd0aCA9PT0gMCB8fCBzZWxlY3RlZEdyaWRbMV0gPCAyKSByZXR1cm47XHJcbiAgICAgICAgY29uc3QgYmFzaWNUYWJsZSA9IGdlbmVyYXRlTWFya2Rvd25UYWJsZShzZWxlY3RlZEdyaWQsIGN1cnJlbnRBbGlnbik7XHJcbiAgICAgICAgbGV0IG1hcmtkb3duVGFibGUgPSBiYXNpY1RhYmxlO1xyXG4gICAgICAgIGNvbnN0IGN1cnNvciA9IGVkaXRvci5nZXRDdXJzb3IoJ2Zyb20nKTtcclxuICAgICAgICBjb25zdCBsaW5lID0gZWRpdG9yLmdldExpbmUoY3Vyc29yLmxpbmUpO1xyXG5cclxuICAgICAgICBpZihjdXJzb3IubGluZSAhPT0gMCAmJiAobGluZS50cmltKCkubGVuZ3RoICE9PSAwKSkge1xyXG4gICAgICAgICAgICBtYXJrZG93blRhYmxlID0gJ1xcbicgKyBtYXJrZG93blRhYmxlO1xyXG4gICAgICAgIH1cclxuXHJcbiAgICAgICAgaWYgKGN1cnNvci5saW5lICE9PSBlZGl0b3IubGFzdExpbmUoKSAmJiAhY2hlY2tCbGFua0xpbmUoZWRpdG9yLCBjdXJzb3IubGluZSArIDEpKSB7XHJcbiAgICAgICAgICAgIG1hcmtkb3duVGFibGUgPSBtYXJrZG93blRhYmxlICsgJ1xcbic7XHJcbiAgICAgICAgfSBlbHNlIGlmIChjdXJzb3IubGluZSA9PT0gZWRpdG9yLmxhc3RMaW5lKCkpIHtcclxuICAgICAgICAgICAgbWFya2Rvd25UYWJsZSA9ICdcXG4nICsgbWFya2Rvd25UYWJsZTtcclxuICAgICAgICB9XHJcblxyXG4gICAgICAgIGlmIChsaW5lLnRyaW0oKS5sZW5ndGggPiAwKSB7XHJcbiAgICAgICAgICAgIGVkaXRvci5yZXBsYWNlUmFuZ2UobWFya2Rvd25UYWJsZSwgeyBsaW5lOiBjdXJzb3IubGluZSArIDEsIGNoOiAwIH0sIHtcclxuICAgICAgICAgICAgICAgIGxpbmU6IGN1cnNvci5saW5lICsgMSxcclxuICAgICAgICAgICAgICAgIGNoOiAwXHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgICAgIGVkaXRvci5yZXBsYWNlUmFuZ2UobWFya2Rvd25UYWJsZSwgeyBsaW5lOiBjdXJzb3IubGluZSwgY2g6IDAgfSwgeyBsaW5lOiBjdXJzb3IubGluZSwgY2g6IDAgfSk7XHJcbiAgICAgICAgfVxyXG4gICAgfVxyXG5cclxuPC9zY3JpcHQ+XHJcblxyXG48VGFibGVHZW5lcmF0b3JDb21wb25lbnQgdGl0bGU9XCJUYWJsZSBHZW5lcmF0b3JcIiB7cGx1Z2lufSBvbkluc2VydD17aW5zZXJ0VGFibGV9PlxyXG4gICAgPEFsaWduSXRlbXMgYWxpZ249e2N1cnJlbnRBbGlnbn0gb246dXBkYXRlPXtoYW5kbGVBbGlnbk1vZGVVcGRhdGV9IHNsb3Q9XCJoZWFkZXJDb250cm9sc1wiIC8+XHJcbjwvVGFibGVHZW5lcmF0b3JDb21wb25lbnQ+XHJcblxyXG48c3R5bGU+PC9zdHlsZT5cclxuIiwiaW1wb3J0IHR5cGUgeyBFZGl0b3IgfSBmcm9tIFwib2JzaWRpYW5cIjtcclxuaW1wb3J0IHsgcmVxdWlyZUFwaVZlcnNpb24gfSBmcm9tIFwib2JzaWRpYW5cIjtcclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBnZXRMaW5lSGVpZ2h0KGVkaXRvcjogRWRpdG9yLCBwb3M6IG51bWJlcikge1xyXG4gICAgY29uc3QgbGluZUluZm8gPSAoZWRpdG9yIGFzIGFueSkuY20uc3RhdGUuZG9jLmxpbmVBdChwb3MpO1xyXG4gICAgY29uc3QgbGluZURPTSA9IChlZGl0b3IgYXMgYW55KS5jbS5kb21BdFBvcyhsaW5lSW5mby5mcm9tKTtcclxuICAgIHJldHVybiAobGluZURPTS5ub2RlIGFzIEhUTUxFbGVtZW50KS5vZmZzZXRIZWlnaHQ7IC8vIOi/meWwhui/lOWbnuihjOeahOmrmOW6plxyXG59XHJcblxyXG5leHBvcnQgY29uc3QgcmFuZG9tID0gKGU6IG51bWJlcikgPT4ge1xyXG4gICAgY29uc3QgdCA9IFtdO1xyXG4gICAgZm9yIChsZXQgbiA9IDA7IG4gPCBlOyBuKyspIHtcclxuICAgICAgICB0LnB1c2goKDE2ICogTWF0aC5yYW5kb20oKSB8IDApLnRvU3RyaW5nKDE2KSk7XHJcbiAgICB9XHJcbiAgICByZXR1cm4gdC5qb2luKFwiXCIpXHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiByZXZlcnNlQ2FsY3VsYXRpb24objoge1xyXG4gICAgeDogbnVtYmVyO1xyXG4gICAgeTogbnVtYmVyO1xyXG59LCB0OiBhbnkpIHtcclxuICAgIGNvbnN0IHIgPSB0LnNjYWxlO1xyXG4gICAgY29uc3QgY3ggPSB0LmNhbnZhc1JlY3QuY3g7XHJcbiAgICBjb25zdCBjeSA9IHQuY2FudmFzUmVjdC5jeTtcclxuICAgIGNvbnN0IHggPSB0Lng7XHJcbiAgICBjb25zdCB5ID0gdC55O1xyXG5cclxuICAgIGNvbnN0IGVDbGllbnRYID0gKG4ueCAtIHgpICogciArIGN4O1xyXG4gICAgY29uc3QgZUNsaWVudFkgPSAobi55IC0geSkgKiByICsgY3k7XHJcblxyXG4gICAgcmV0dXJuIHtcclxuICAgICAgICBjbGllbnRYOiBlQ2xpZW50WCxcclxuICAgICAgICBjbGllbnRZOiBlQ2xpZW50WVxyXG4gICAgfTtcclxufVxyXG5cclxuZXhwb3J0IGZ1bmN0aW9uIGNhbGN1bGF0ZUVkaXRvcihlZGl0b3I6IEVkaXRvciwgdGFibGVHZW5lcmF0b3JCb2FyZDogSFRNTEVsZW1lbnQgfCBudWxsKSB7XHJcbiAgICBpZiAoIXRhYmxlR2VuZXJhdG9yQm9hcmQpIHJldHVybjtcclxuXHJcbiAgICBjb25zdCBjdXJzb3IgPSBlZGl0b3IuZ2V0Q3Vyc29yKCdmcm9tJyk7XHJcbiAgICBsZXQgY29vcmRzOiBDb29yZHM7XHJcblxyXG4gICAgLy8gR2V0IHRoZSBjdXJzb3IgcG9zaXRpb24gdXNpbmcgdGhlIGFwcHJvcHJpYXRlIENNNSBvciBDTTYgaW50ZXJmYWNlXHJcbiAgICBpZiAoKGVkaXRvciBhcyBhbnkpLmN1cnNvckNvb3Jkcykge1xyXG4gICAgICAgIGNvb3JkcyA9IChlZGl0b3IgYXMgYW55KS5jdXJzb3JDb29yZHModHJ1ZSwgJ3dpbmRvdycpO1xyXG4gICAgfSBlbHNlIGlmICgoZWRpdG9yIGFzIGFueSkuY29vcmRzQXRQb3MpIHtcclxuICAgICAgICBjb25zdCBvZmZzZXQgPSBlZGl0b3IucG9zVG9PZmZzZXQoY3Vyc29yKTtcclxuICAgICAgICBjb29yZHMgPSAoZWRpdG9yIGFzIGFueSkuY20uY29vcmRzQXRQb3M/LihvZmZzZXQpID8/IChlZGl0b3IgYXMgYW55KS5jb29yZHNBdFBvcyhvZmZzZXQpO1xyXG4gICAgfSBlbHNlIHtcclxuICAgICAgICByZXR1cm47XHJcbiAgICB9XHJcblxyXG4gICAgY29uc3QgbGluZUhlaWdodCA9IGdldExpbmVIZWlnaHQoZWRpdG9yLCBlZGl0b3IucG9zVG9PZmZzZXQoY3Vyc29yKSk7XHJcblxyXG4gICAgY29uc3QgY2FsY3VsYXRlVG9wID0gKHJlcXVpcmVBcGlWZXJzaW9uKFwiMC4xNS4wXCIpID9cclxuICAgICAgICBhY3RpdmVEb2N1bWVudCA6IGRvY3VtZW50KT8uYm9keS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS5oZWlnaHQgLSAoY29vcmRzLnRvcCB8fCAwKSAtIChjb29yZHMuaGVpZ2h0IHx8IGxpbmVIZWlnaHQpO1xyXG4gICAgcmV0dXJuIHtcclxuICAgICAgICB0b3A6IGNhbGN1bGF0ZVRvcCB8fCAwLFxyXG4gICAgICAgIGxlZnQ6IGNvb3Jkcy5sZWZ0IHx8IDAsXHJcbiAgICAgICAgYm90dG9tOiBjb29yZHMuYm90dG9tIHx8IDAsXHJcbiAgICAgICAgaGVpZ2h0OiBjb29yZHMuaGVpZ2h0IHx8IGxpbmVIZWlnaHRcclxuICAgIH1cclxufVxyXG4iLCJleHBvcnQgZnVuY3Rpb24gYXJvdW5kKG9iaiwgZmFjdG9yaWVzKSB7XG4gICAgY29uc3QgcmVtb3ZlcnMgPSBPYmplY3Qua2V5cyhmYWN0b3JpZXMpLm1hcChrZXkgPT4gYXJvdW5kMShvYmosIGtleSwgZmFjdG9yaWVzW2tleV0pKTtcbiAgICByZXR1cm4gcmVtb3ZlcnMubGVuZ3RoID09PSAxID8gcmVtb3ZlcnNbMF0gOiBmdW5jdGlvbiAoKSB7IHJlbW92ZXJzLmZvckVhY2gociA9PiByKCkpOyB9O1xufVxuZnVuY3Rpb24gYXJvdW5kMShvYmosIG1ldGhvZCwgY3JlYXRlV3JhcHBlcikge1xuICAgIGNvbnN0IG9yaWdpbmFsID0gb2JqW21ldGhvZF0sIGhhZE93biA9IG9iai5oYXNPd25Qcm9wZXJ0eShtZXRob2QpO1xuICAgIGxldCBjdXJyZW50ID0gY3JlYXRlV3JhcHBlcihvcmlnaW5hbCk7XG4gICAgLy8gTGV0IG91ciB3cmFwcGVyIGluaGVyaXQgc3RhdGljIHByb3BzIGZyb20gdGhlIHdyYXBwaW5nIG1ldGhvZCxcbiAgICAvLyBhbmQgdGhlIHdyYXBwaW5nIG1ldGhvZCwgcHJvcHMgZnJvbSB0aGUgb3JpZ2luYWwgbWV0aG9kXG4gICAgaWYgKG9yaWdpbmFsKVxuICAgICAgICBPYmplY3Quc2V0UHJvdG90eXBlT2YoY3VycmVudCwgb3JpZ2luYWwpO1xuICAgIE9iamVjdC5zZXRQcm90b3R5cGVPZih3cmFwcGVyLCBjdXJyZW50KTtcbiAgICBvYmpbbWV0aG9kXSA9IHdyYXBwZXI7XG4gICAgLy8gUmV0dXJuIGEgY2FsbGJhY2sgdG8gYWxsb3cgc2FmZSByZW1vdmFsXG4gICAgcmV0dXJuIHJlbW92ZTtcbiAgICBmdW5jdGlvbiB3cmFwcGVyKC4uLmFyZ3MpIHtcbiAgICAgICAgLy8gSWYgd2UgaGF2ZSBiZWVuIGRlYWN0aXZhdGVkIGFuZCBhcmUgbm8gbG9uZ2VyIHdyYXBwZWQsIHJlbW92ZSBvdXJzZWx2ZXNcbiAgICAgICAgaWYgKGN1cnJlbnQgPT09IG9yaWdpbmFsICYmIG9ialttZXRob2RdID09PSB3cmFwcGVyKVxuICAgICAgICAgICAgcmVtb3ZlKCk7XG4gICAgICAgIHJldHVybiBjdXJyZW50LmFwcGx5KHRoaXMsIGFyZ3MpO1xuICAgIH1cbiAgICBmdW5jdGlvbiByZW1vdmUoKSB7XG4gICAgICAgIC8vIElmIG5vIG90aGVyIHBhdGNoZXMsIGp1c3QgZG8gYSBkaXJlY3QgcmVtb3ZhbFxuICAgICAgICBpZiAob2JqW21ldGhvZF0gPT09IHdyYXBwZXIpIHtcbiAgICAgICAgICAgIGlmIChoYWRPd24pXG4gICAgICAgICAgICAgICAgb2JqW21ldGhvZF0gPSBvcmlnaW5hbDtcbiAgICAgICAgICAgIGVsc2VcbiAgICAgICAgICAgICAgICBkZWxldGUgb2JqW21ldGhvZF07XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGN1cnJlbnQgPT09IG9yaWdpbmFsKVxuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAvLyBFbHNlIHBhc3MgZnV0dXJlIGNhbGxzIHRocm91Z2gsIGFuZCByZW1vdmUgd3JhcHBlciBmcm9tIHRoZSBwcm90b3R5cGUgY2hhaW5cbiAgICAgICAgY3VycmVudCA9IG9yaWdpbmFsO1xuICAgICAgICBPYmplY3Quc2V0UHJvdG90eXBlT2Yod3JhcHBlciwgb3JpZ2luYWwgfHwgRnVuY3Rpb24pO1xuICAgIH1cbn1cbmV4cG9ydCBmdW5jdGlvbiBkZWR1cGUoa2V5LCBvbGRGbiwgbmV3Rm4pIHtcbiAgICBjaGVja1trZXldID0ga2V5O1xuICAgIHJldHVybiBjaGVjaztcbiAgICBmdW5jdGlvbiBjaGVjayguLi5hcmdzKSB7XG4gICAgICAgIHJldHVybiAob2xkRm5ba2V5XSA9PT0ga2V5ID8gb2xkRm4gOiBuZXdGbikuYXBwbHkodGhpcywgYXJncyk7XG4gICAgfVxufVxuZXhwb3J0IGZ1bmN0aW9uIGFmdGVyKHByb21pc2UsIGNiKSB7XG4gICAgcmV0dXJuIHByb21pc2UudGhlbihjYiwgY2IpO1xufVxuZXhwb3J0IGZ1bmN0aW9uIHNlcmlhbGl6ZShhc3luY0Z1bmN0aW9uKSB7XG4gICAgbGV0IGxhc3RSdW4gPSBQcm9taXNlLnJlc29sdmUoKTtcbiAgICBmdW5jdGlvbiB3cmFwcGVyKC4uLmFyZ3MpIHtcbiAgICAgICAgcmV0dXJuIGxhc3RSdW4gPSBuZXcgUHJvbWlzZSgocmVzLCByZWopID0+IHtcbiAgICAgICAgICAgIGFmdGVyKGxhc3RSdW4sICgpID0+IHtcbiAgICAgICAgICAgICAgICBhc3luY0Z1bmN0aW9uLmFwcGx5KHRoaXMsIGFyZ3MpLnRoZW4ocmVzLCByZWopO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0pO1xuICAgIH1cbiAgICB3cmFwcGVyLmFmdGVyID0gZnVuY3Rpb24gKCkge1xuICAgICAgICByZXR1cm4gbGFzdFJ1biA9IG5ldyBQcm9taXNlKChyZXMsIHJlaikgPT4geyBhZnRlcihsYXN0UnVuLCByZXMpOyB9KTtcbiAgICB9O1xuICAgIHJldHVybiB3cmFwcGVyO1xufVxuIiwiPHNjcmlwdCBsYW5nPVwidHNcIj5cclxuICAgIGltcG9ydCB7IGNyZWF0ZUV2ZW50RGlzcGF0Y2hlciB9IGZyb20gJ3N2ZWx0ZSc7XHJcblxyXG4gICAgLy8g5Yib5bu65LiA5Liq5LqL5Lu25YiG5Y+R5ZmoXHJcbiAgICBjb25zdCBkaXNwYXRjaCA9IGNyZWF0ZUV2ZW50RGlzcGF0Y2hlcigpO1xyXG5cclxuICAgIGV4cG9ydCBsZXQgaGVpZ2h0ID0gMTYwO1xyXG4gICAgZXhwb3J0IGxldCB3aWR0aCA9IDE2MDtcclxuXHJcbiAgICAvLyDlvZMgd2lkdGgg5oiWIGhlaWdodCDlj5HnlJ/lj5jljJbml7bvvIzlj5HpgIHmm7TmlrDkuovku7ZcclxuICAgICQ6IGRpc3BhdGNoKCdzaXplVXBkYXRlJywgeyBoZWlnaHQsd2lkdGggIH0pO1xyXG5cclxuPC9zY3JpcHQ+XHJcblxyXG48ZGl2IGNsYXNzPVwiaW5wdXQtdGFibGUtZ2VuZXJhdG9yXCI+XHJcbiAgICA8ZGl2IGNsYXNzPVwiaW5wdXQtdGFibGUtZ2VuZXJhdG9yLWhlaWdodFwiPlxyXG4gICAgICAgIEg6XHJcbiAgICAgICAgPGlucHV0IGNsYXNzPVwiaGVpZ2h0LWlucHV0XCIgYmluZDp2YWx1ZT17aGVpZ2h0fT5cclxuICAgIDwvZGl2PlxyXG4gICAgPGRpdiBjbGFzcz1cImlucHV0LXRhYmxlLWdlbmVyYXRvci13aWR0aFwiPlxyXG4gICAgICAgIFc6XHJcbiAgICAgICAgPGlucHV0IGNsYXNzPVwid2lkdGgtaW5wdXRcIiBiaW5kOnZhbHVlPXt3aWR0aH0+XHJcbiAgICA8L2Rpdj5cclxuPC9kaXY+XHJcblxyXG48c3R5bGU+XHJcbiAgICAuaW5wdXQtdGFibGUtZ2VuZXJhdG9yIHtcclxuICAgICAgICBtYXJnaW4tbGVmdDogdmFyKC0tc2l6ZS0yLTIpO1xyXG4gICAgICAgIG1hcmdpbi1yaWdodDogdmFyKC0tc2l6ZS0yLTIpO1xyXG4gICAgICAgIG1hcmdpbi10b3A6IHZhcigtLXNpemUtNC0yKTtcclxuICAgICAgICBtYXJnaW4tYm90dG9tOiB2YXIoLS1zaXplLTQtMik7XHJcbiAgICAgICAgZGlzcGxheTogZmxleDtcclxuICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWFyb3VuZDtcclxuICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyO1xyXG4gICAgfVxyXG5cclxuICAgIC5pbnB1dC10YWJsZS1nZW5lcmF0b3Itd2lkdGgsIC5pbnB1dC10YWJsZS1nZW5lcmF0b3ItaGVpZ2h0IHtcclxuICAgICAgICBkaXNwbGF5OiBmbGV4O1xyXG4gICAgICAgIGp1c3RpZnktY29udGVudDogc3BhY2UtYXJvdW5kO1xyXG4gICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7XHJcbiAgICB9XHJcblxyXG4gICAgaW5wdXQge1xyXG4gICAgICAgIHdpZHRoOiA3MHB4O1xyXG4gICAgICAgIGhlaWdodDogMThweDtcclxuICAgICAgICBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS1jb2xvci1iYXNlLTUwKTtcclxuICAgICAgICBtYXJnaW4tbGVmdDogdmFyKC0tc2l6ZS0yLTIpO1xyXG4gICAgICAgIGJvcmRlci1yYWRpdXM6IHZhcigtLXJhZGl1cy1tKTtcclxuICAgICAgICB0ZXh0LWFsaWduOiBjZW50ZXI7XHJcbiAgICB9XHJcbjwvc3R5bGU+XHJcbiIsIjxzY3JpcHQgbGFuZz1cInRzXCI+XHJcbiAgICBpbXBvcnQgdHlwZSBUYWJsZUdlbmVyYXRvclBsdWdpbiBmcm9tIFwiLi4vdGFibGVHZW5lcmF0b3JJbmRleFwiO1xyXG4gICAgaW1wb3J0IHsgcmFuZG9tIH0gZnJvbSBcIi4uL3V0aWxzL3RhYmxlUE9TXCI7XHJcbiAgICBpbXBvcnQgVGFibGVHZW5lcmF0b3JDb21wb25lbnQgZnJvbSBcIi4vYmFzaWMvVGFibGVHZW5lcmF0b3JDb21wb25lbnQuc3ZlbHRlXCI7XHJcbiAgICBpbXBvcnQgU2l6ZUNvbnRyb2xzIGZyb20gXCIuL2Jhc2ljL1NpemVDb250cm9scy5zdmVsdGVcIjtcclxuXHJcbiAgICBleHBvcnQgbGV0IGNhbnZhczogYW55O1xyXG4gICAgZXhwb3J0IGxldCBjb29yZHM6IHtcclxuICAgICAgICB4OiBudW1iZXI7XHJcbiAgICAgICAgeTogbnVtYmVyO1xyXG4gICAgfTtcclxuICAgIGV4cG9ydCBsZXQgcGx1Z2luOiBUYWJsZUdlbmVyYXRvclBsdWdpbjtcclxuXHJcbiAgICBsZXQgd2lkdGggPSBwbHVnaW4uc2V0dGluZ3MuZGVmYXVsdENhcmRXaWR0aCB8fCAxNjA7XHJcbiAgICBsZXQgaGVpZ2h0ID0gcGx1Z2luLnNldHRpbmdzLmRlZmF1bHRDYXJkSGVpZ2h0IHx8IDE2MDtcclxuXHJcbiAgICBmdW5jdGlvbiBoYW5kbGVTaXplVXBkYXRlKGV2ZW50OiBhbnkpIHtcclxuICAgICAgICBoZWlnaHQgPSBwYXJzZUludChldmVudC5kZXRhaWwuaGVpZ2h0LDEwKTtcclxuICAgICAgICB3aWR0aCA9IHBhcnNlSW50KGV2ZW50LmRldGFpbC53aWR0aCwxMCk7XHJcblxyXG4gICAgICAgIHBsdWdpbi5zZXR0aW5ncy5kZWZhdWx0Q2FyZEhlaWdodCA9IGhlaWdodDtcclxuICAgICAgICBwbHVnaW4uc2V0dGluZ3MuZGVmYXVsdENhcmRXaWR0aCA9IHdpZHRoO1xyXG4gICAgICAgIHBsdWdpbi5zYXZlU2V0dGluZ3MoKTtcclxuICAgIH1cclxuXHJcbiAgICBhc3luYyBmdW5jdGlvbiBpbnNlcnRUYWJsZShzZWxlY3RlZEdyaWQ6IG51bWJlcltdKSB7XHJcbiAgICAgICAgaWYgKHNlbGVjdGVkR3JpZC5sZW5ndGggPT09IDAgfHwgc2VsZWN0ZWRHcmlkWzFdIDwgMikgcmV0dXJuO1xyXG4gICAgICAgIGNvbnN0IGNhbnZhc0ZpbGUgPSBhd2FpdCBwbHVnaW4uYXBwLnZhdWx0LmNhY2hlZFJlYWQoY2FudmFzLnZpZXcuZmlsZSk7XHJcbiAgICAgICAgY29uc3QgY2FudmFzRmlsZURhdGEgPSBKU09OLnBhcnNlKGNhbnZhc0ZpbGUpO1xyXG4gICAgICAgIGNvbnNvbGUubG9nKHNlbGVjdGVkR3JpZCk7XHJcbiAgICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBzZWxlY3RlZEdyaWRbMF07IGkrKykge1xyXG4gICAgICAgICAgICBmb3IgKGxldCBqID0gMDsgaiA8IHNlbGVjdGVkR3JpZFsxXTsgaisrKSB7XHJcbiAgICAgICAgICAgICAgICBjYW52YXNGaWxlRGF0YS5ub2Rlcy5wdXNoKHtcclxuICAgICAgICAgICAgICAgICAgICBpZDogcmFuZG9tKDE2KSxcclxuICAgICAgICAgICAgICAgICAgICB4OiBjb29yZHMueCArIGogKiAod2lkdGggKyAxMCkgKyA0MCxcclxuICAgICAgICAgICAgICAgICAgICB5OiBjb29yZHMueSArIGkgKiAoaGVpZ2h0ICsgMTApICsgNDAsXHJcbiAgICAgICAgICAgICAgICAgICAgd2lkdGg6IHdpZHRoLFxyXG4gICAgICAgICAgICAgICAgICAgIGhlaWdodDogaGVpZ2h0LFxyXG4gICAgICAgICAgICAgICAgICAgIHR5cGU6IFwidGV4dFwiLFxyXG4gICAgICAgICAgICAgICAgICAgIHRleHQ6IFwiXCIsXHJcbiAgICAgICAgICAgICAgICB9KVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfVxyXG4gICAgICAgIGNvbnNvbGUubG9nKGNhbnZhc0ZpbGVEYXRhKTtcclxuICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcclxuICAgICAgICAgICAgY2FudmFzLnNldERhdGEoY2FudmFzRmlsZURhdGEpO1xyXG4gICAgICAgICAgICBjYW52YXMucmVxdWVzdFNhdmUoKTtcclxuICAgICAgICB9LCAxMDApO1xyXG4gICAgfVxyXG5cclxuPC9zY3JpcHQ+XHJcblxyXG48VGFibGVHZW5lcmF0b3JDb21wb25lbnQgdGl0bGU9XCJDYXJkIEdlbmVyYXRvclwiIHtwbHVnaW59IG9uSW5zZXJ0PXtpbnNlcnRUYWJsZX0+XHJcbiAgICA8U2l6ZUNvbnRyb2xzIHNsb3Q9XCJzaXplQ29udHJvbHNcIiB3aWR0aD17d2lkdGh9IGhlaWdodD17aGVpZ2h0fSBvbjpzaXplVXBkYXRlPXtoYW5kbGVTaXplVXBkYXRlfT48L1NpemVDb250cm9scz5cclxuPC9UYWJsZUdlbmVyYXRvckNvbXBvbmVudD5cclxuXHJcbjxzdHlsZT48L3N0eWxlPlxyXG4iLCJleHBvcnQgZnVuY3Rpb24gc2V0VGFibGVHZW5lcmF0b3JNZW51UG9zaXRpb24odGFibGVHZW5lcmF0b3JCb2FyZDogSFRNTEVsZW1lbnQgfCBudWxsLCBjb29yZHM6IENvb3JkcywgZGlzcGxheU1vZGU6IFwiY2FudmFzXCIgfCBcImVkaXRvclwiKSB7XHJcbiAgICBpZighdGFibGVHZW5lcmF0b3JCb2FyZCkgcmV0dXJuO1xyXG5cclxuICAgIHNldFRpbWVvdXQoKCk9PntcclxuICAgICAgICB0YWJsZUdlbmVyYXRvckJvYXJkLnN0eWxlLmRpc3BsYXkgPSAnYmxvY2snO1xyXG4gICAgICAgIHN3aXRjaCAoZGlzcGxheU1vZGUpIHtcclxuICAgICAgICAgICAgY2FzZSBcImNhbnZhc1wiOlxyXG4gICAgICAgICAgICAgICAgdGFibGVHZW5lcmF0b3JCb2FyZC5zdHlsZS50b3AgPSBgJHtjb29yZHMudG9wfXB4YDtcclxuICAgICAgICAgICAgICAgIHRhYmxlR2VuZXJhdG9yQm9hcmQuc3R5bGUubGVmdCA9IGAke2Nvb3Jkcy5sZWZ0fXB4YDtcclxuICAgICAgICAgICAgICAgIGJyZWFrO1xyXG4gICAgICAgICAgICBjYXNlIFwiZWRpdG9yXCI6XHJcbiAgICAgICAgICAgICAgICB0YWJsZUdlbmVyYXRvckJvYXJkLnN0eWxlLnRyYW5zZm9ybSA9IGB0cmFuc2xhdGUoJHtjb29yZHMubGVmdH1weCwtJHtjb29yZHMudG9wfXB4YDtcclxuICAgICAgICAgICAgICAgIGJyZWFrO1xyXG4gICAgICAgIH1cclxuICAgIH0pXHJcbn1cclxuXHJcbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlVGFibGVHZW5lcmF0b3JNZW51KGV2dDogTW91c2VFdmVudCwgdGFibGVHZW5lcmF0b3JFbDogSFRNTEVsZW1lbnQgfCBudWxsKSB7XHJcbiAgICBjb25zdCB0YXJnZXQgPSBldnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xyXG5cclxuICAgIGlmICghdGFibGVHZW5lcmF0b3JFbCB8fCAhdGFyZ2V0KSByZXR1cm47XHJcbiAgICBpZiAodGFyZ2V0LmNsYXNzTGlzdC5jb250YWlucyhcInRhYmxlLWdlbmVyYXRvci1tZW51XCIpIHx8XHJcbiAgICAgICAgdGFyZ2V0LnBhcmVudEVsZW1lbnQ/LmNsYXNzTGlzdC5jb250YWlucyhcInRhYmxlLWdlbmVyYXRvci1tZW51XCIpIHx8XHJcbiAgICAgICAgdGFyZ2V0LnRhZ05hbWUgPT0gXCJCVVRUT05cIikgcmV0dXJuO1xyXG4gICAgaWYgKHRhYmxlR2VuZXJhdG9yRWw/LmNvbnRhaW5zKHRhcmdldCkpIHJldHVybjtcclxuICAgIGlmICghZG9jdW1lbnQuYm9keS5jb250YWlucyh0YWJsZUdlbmVyYXRvckVsKSkgcmV0dXJuO1xyXG5cclxuICAgIHRhYmxlR2VuZXJhdG9yRWwuZGV0YWNoKCk7XHJcbn1cclxuIiwiaW1wb3J0IHtcclxuICAgIEFwcCxcclxuICAgIEVkaXRvcixcclxuICAgIE1hcmtkb3duVmlldyxcclxuICAgIE1lbnUsXHJcbiAgICBNZW51SXRlbSxcclxuICAgIFBsdWdpbixcclxuICAgIFBsdWdpblNldHRpbmdUYWIsXHJcbiAgICByZXF1aXJlQXBpVmVyc2lvbixcclxuICAgIFNldHRpbmdcclxufSBmcm9tICdvYnNpZGlhbic7XHJcbmltcG9ydCBUYWJsZUdlbmVyYXRvciBmcm9tIFwiLi91aS9UYWJsZUdlbmVyYXRvci5zdmVsdGVcIjtcclxuaW1wb3J0IFwiLi9jc3MvdGFibGVHZW5lcmF0b3JEZWZhdWx0LmNzc1wiO1xyXG5pbXBvcnQgeyBjYWxjdWxhdGVFZGl0b3IsIHJldmVyc2VDYWxjdWxhdGlvbiB9IGZyb20gXCIuL3V0aWxzL3RhYmxlUE9TXCI7XHJcbmltcG9ydCB7IGFyb3VuZCB9IGZyb20gXCJtb25rZXktYXJvdW5kXCI7XHJcbmltcG9ydCBDYXJkR2VuZXJhdG9yIGZyb20gXCIuL3VpL0NhcmRHZW5lcmF0b3Iuc3ZlbHRlXCI7XHJcbmltcG9ydCB7IGhhbmRsZUhpZGVUYWJsZUdlbmVyYXRvck1lbnUsIHNldFRhYmxlR2VuZXJhdG9yTWVudVBvc2l0aW9uIH0gZnJvbSBcIi4vdXRpbHMvdGFibGVET01cIjtcclxuXHJcbmludGVyZmFjZSBUYWJsZUdlbmVyYXRvclBsdWdpblNldHRpbmdzIHtcclxuICAgIHJvd0NvdW50OiBudW1iZXI7XHJcbiAgICBjb2x1bW5Db3VudDogbnVtYmVyO1xyXG4gICAgZGVmYXVsdEFsaWdubWVudDogQWxpZ25Nb2RlO1xyXG4gICAgZGVmYXVsdENhcmRXaWR0aDogbnVtYmVyO1xyXG4gICAgZGVmYXVsdENhcmRIZWlnaHQ6IG51bWJlcjtcclxufVxyXG5cclxuXHJcblxyXG5jb25zdCBERUZBVUxUX1NFVFRJTkdTOiBUYWJsZUdlbmVyYXRvclBsdWdpblNldHRpbmdzID0ge1xyXG4gICAgcm93Q291bnQ6IDgsXHJcbiAgICBjb2x1bW5Db3VudDogOCxcclxuICAgIGRlZmF1bHRBbGlnbm1lbnQ6IFwibGVmdFwiLFxyXG4gICAgZGVmYXVsdENhcmRXaWR0aDogMTYwLFxyXG4gICAgZGVmYXVsdENhcmRIZWlnaHQ6IDE2MCxcclxufVxyXG5cclxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVGFibGVHZW5lcmF0b3JQbHVnaW4gZXh0ZW5kcyBQbHVnaW4ge1xyXG4gICAgdGFibGVHZW5lcmF0b3JFbDogSFRNTEVsZW1lbnQgfCBudWxsID0gbnVsbDtcclxuICAgIHRhYmxlR2VuZXJhdG9yQ29tcG9uZW50OiBUYWJsZUdlbmVyYXRvcjtcclxuICAgIHNldHRpbmdzOiBUYWJsZUdlbmVyYXRvclBsdWdpblNldHRpbmdzO1xyXG5cclxuICAgIGFzeW5jIG9ubG9hZCgpIHtcclxuICAgICAgICB0aGlzLnJlZ2lzdGVyRXZlbnQoXHJcbiAgICAgICAgICAgIHRoaXMuYXBwLndvcmtzcGFjZS5vbihcImVkaXRvci1tZW51XCIsIChtZW51OiBNZW51LCBlZGl0b3I6IEVkaXRvciwgdmlldzogTWFya2Rvd25WaWV3KSA9PiB0aGlzLmhhbmRsZUNyZWF0ZVRhYmxlR2VuZXJhdG9ySW5NZW51KG1lbnUsIGVkaXRvciwgdmlldykpXHJcbiAgICAgICAgKTtcclxuXHJcbiAgICAgICAgYXdhaXQgdGhpcy5yZWdpc3RlclNldHRpbmdzKCk7XHJcbiAgICAgICAgdGhpcy5yZWdpc3RlckRvbUV2ZW50KHdpbmRvdywgJ2NsaWNrJywgKGV2dDogTW91c2VFdmVudCkgPT4gaGFuZGxlSGlkZVRhYmxlR2VuZXJhdG9yTWVudShldnQsIHRoaXMudGFibGVHZW5lcmF0b3JFbCkpO1xyXG4gICAgICAgIC8vIEhhbmRsZSBzYW1lIG1vdXNlZXZlbnQgaW4gbXVsdGkgd2luZG93cyB3aGVuIHVzZWQgaW4gbmV3ZXIgdmVyc2lvbiBsaWtlIDAuMTUuMFxyXG4gICAgICAgIGlmIChyZXF1aXJlQXBpVmVyc2lvbihcIjAuMTUuMFwiKSkgdGhpcy5yZWdpc3RlclRhYmxlR2VuZXJhdG9yTWVudSgpO1xyXG5cclxuICAgICAgICB0aGlzLnJlZ2lzdGVyQ29tbWFuZHMoKTtcclxuICAgICAgICB0aGlzLnJlZ2lzdGVyQ2FudmFzTWVudSgpO1xyXG4gICAgfVxyXG5cclxuICAgIGhpZGVUYWJsZSgpIHtcclxuICAgICAgICB0aGlzLnRhYmxlR2VuZXJhdG9yRWw/LmRldGFjaCgpO1xyXG4gICAgfVxyXG5cclxuICAgIGhhbmRsZUNyZWF0ZVRhYmxlR2VuZXJhdG9ySW5NZW51KG1lbnU6IE1lbnUsIGVkaXRvcjogRWRpdG9yLCB2aWV3OiBNYXJrZG93blZpZXcpIHtcclxuICAgICAgICBtZW51LmFkZEl0ZW0oKGl0ZW0pID0+IHtcclxuICAgICAgICAgICAgY29uc3QgaXRlbURvbSA9IChpdGVtIGFzIGFueSkuZG9tIGFzIEhUTUxFbGVtZW50O1xyXG4gICAgICAgICAgICBpdGVtRG9tLmFkZENsYXNzKFwidGFibGUtZ2VuZXJhdG9yLW1lbnVcIik7XHJcbiAgICAgICAgICAgIGl0ZW1cclxuICAgICAgICAgICAgICAgIC5zZXRUaXRsZShcIkFkZCBNYXJrZG93biBUYWJsZVwiKVxyXG4gICAgICAgICAgICAgICAgLnNldEljb24oXCJ0YWJsZVwiKVxyXG4gICAgICAgICAgICAgICAgLnNldFNlY3Rpb24oXCJhY3Rpb25cIilcclxuICAgICAgICAgICAgICAgIC5vbkNsaWNrKGFzeW5jICgpID0+IHtcclxuICAgICAgICAgICAgICAgICAgICB0aGlzLmNyZWF0ZUdlbmVyYXRvck1lbnUoXCJ0YWJsZVwiLCB7IGVkaXRvcjogZWRpdG9yIH0sIHRoaXMpO1xyXG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IGNvb3JkcyA9IGNhbGN1bGF0ZUVkaXRvcihlZGl0b3IsIHRoaXMudGFibGVHZW5lcmF0b3JFbCk7XHJcbiAgICAgICAgICAgICAgICAgICAgaWYoIWNvb3JkcykgcmV0dXJuO1xyXG4gICAgICAgICAgICAgICAgICAgIHNldFRhYmxlR2VuZXJhdG9yTWVudVBvc2l0aW9uKHRoaXMudGFibGVHZW5lcmF0b3JFbCwgY29vcmRzLCBcImVkaXRvclwiKTtcclxuICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuICAgIGNyZWF0ZUdlbmVyYXRvck1lbnUoXHJcbiAgICAgICAgdHlwZTogXCJ0YWJsZVwiIHwgXCJjYXJkXCIsXHJcbiAgICAgICAgY29udGV4dDogeyBlZGl0b3I/OiBFZGl0b3IsIGNhbnZhcz86IGFueSwgY29vcmRzPzogeyB4OiBudW1iZXIsIHk6IG51bWJlciB9IH0sXHJcbiAgICAgICAgcGx1Z2luOiBUYWJsZUdlbmVyYXRvclBsdWdpblxyXG4gICAgKSB7XHJcbiAgICAgICAgLy8gQ2hlY2sgaWYgdGhpcyB0YWJsZUdlbmVyYXRvckVsIGlzIGFscmVhZHkgY3JlYXRlZCwgaWYgc28gZGVsZXRlIGl0O1xyXG4gICAgICAgIC8vIFVzZWQgZm9yIE11bHRpIHBvcG91dCB3aW5kb3dzLlxyXG4gICAgICAgIGlmICh0aGlzLnRhYmxlR2VuZXJhdG9yRWwpIHRoaXMudGFibGVHZW5lcmF0b3JFbC5kZXRhY2goKTtcclxuXHJcbiAgICAgICAgdGhpcy50YWJsZUdlbmVyYXRvckVsID0gKHJlcXVpcmVBcGlWZXJzaW9uKFwiMC4xNS4wXCIpID8gYWN0aXZlRG9jdW1lbnQgOiBkb2N1bWVudCk/LmJvZHkuY3JlYXRlRWwoXCJkaXZcIiwgeyBjbHM6IFwidGFibGUtZ2VuZXJhdG9yLXZpZXdcIiB9KTtcclxuICAgICAgICB0aGlzLnRhYmxlR2VuZXJhdG9yRWwuaGlkZSgpO1xyXG5cclxuICAgICAgICBpZiAodHlwZSA9PT0gXCJ0YWJsZVwiKSB7XHJcbiAgICAgICAgICAgIHRoaXMudGFibGVHZW5lcmF0b3JDb21wb25lbnQgPSBuZXcgVGFibGVHZW5lcmF0b3Ioe1xyXG4gICAgICAgICAgICAgICAgdGFyZ2V0OiB0aGlzLnRhYmxlR2VuZXJhdG9yRWwsXHJcbiAgICAgICAgICAgICAgICBwcm9wczogeyBlZGl0b3I6IGNvbnRleHQuZWRpdG9yLCBwbHVnaW46IHBsdWdpbiB9XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0gZWxzZSBpZiAodHlwZSA9PT0gXCJjYXJkXCIpIHtcclxuICAgICAgICAgICAgdGhpcy50YWJsZUdlbmVyYXRvckNvbXBvbmVudCA9IG5ldyBDYXJkR2VuZXJhdG9yKHtcclxuICAgICAgICAgICAgICAgIHRhcmdldDogdGhpcy50YWJsZUdlbmVyYXRvckVsLFxyXG4gICAgICAgICAgICAgICAgcHJvcHM6IHsgY2FudmFzOiBjb250ZXh0LmNhbnZhcywgY29vcmRzOiBjb250ZXh0LmNvb3JkcywgcGx1Z2luOiBwbHVnaW4gfVxyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICB9XHJcbiAgICB9XHJcblxyXG5cclxuXHJcbiAgICBhc3luYyByZWdpc3RlclNldHRpbmdzKCkge1xyXG4gICAgICAgIGF3YWl0IHRoaXMubG9hZFNldHRpbmdzKCk7XHJcbiAgICAgICAgdGhpcy5hZGRTZXR0aW5nVGFiKG5ldyBUYWJsZUdlbmVyYXRvclNldHRpbmdUYWIodGhpcy5hcHAsIHRoaXMpKTtcclxuICAgICAgICB0aGlzLnJlZ2lzdGVySW50ZXJ2YWwod2luZG93LnNldFRpbWVvdXQoKCkgPT4ge1xyXG4gICAgICAgICAgICAgICAgdGhpcy5zYXZlU2V0dGluZ3MoKTtcclxuICAgICAgICAgICAgfSwgMTAwKVxyXG4gICAgICAgICk7XHJcbiAgICB9XHJcblxyXG4gICAgcmVnaXN0ZXJDYW52YXNNZW51KCkge1xyXG4gICAgICAgIGNvbnN0IGNyZWF0ZUNhcmRUYWJsZSA9IChjYW52YXM6IGFueSwgZTogTWVudSwgdDoge1xyXG4gICAgICAgICAgICB4OiBudW1iZXI7XHJcbiAgICAgICAgICAgIHk6IG51bWJlcjtcclxuICAgICAgICB9LCBhOiBhbnkpID0+IHtcclxuICAgICAgICAgICAgY29uc3QgeyB0b3AsIGxlZnQgfSA9IGUuZG9tLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xyXG4gICAgICAgICAgICBjb25zdCBkYXRhID0gcmV2ZXJzZUNhbGN1bGF0aW9uKHQsIGNhbnZhcyk7XHJcbiAgICAgICAgICAgIGNvbnNvbGUubG9nKGRhdGEpO1xyXG4gICAgICAgICAgICBzZXRUaW1lb3V0KCgpPT57XHJcbiAgICAgICAgICAgICAgICB0aGlzLmNyZWF0ZUdlbmVyYXRvck1lbnUoXCJjYXJkXCIsIHsgY2FudmFzOiBjYW52YXMsIGNvb3JkczogdCB9LCB0aGlzKTtcclxuICAgICAgICAgICAgICAgIHNldFRhYmxlR2VuZXJhdG9yTWVudVBvc2l0aW9uKHRoaXMudGFibGVHZW5lcmF0b3JFbCwgeyB0b3A6IHRvcCAsIGxlZnQ6IGxlZnQsIGJvdHRvbTogMCwgaGVpZ2h0OiAwIH0sIFwiY2FudmFzXCIpO1xyXG4gICAgICAgICAgICB9LCAwKTtcclxuICAgICAgICB9XHJcblxyXG4gICAgICAgIGNvbnN0IHBhdGNoTm9kZSA9ICgpID0+IHtcclxuICAgICAgICAgICAgY29uc3QgY2FudmFzVmlldyA9IHRoaXMuYXBwLndvcmtzcGFjZS5nZXRMZWF2ZXNPZlR5cGUoXCJjYW52YXNcIikuZmlyc3QoKT8udmlldztcclxuICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxyXG4gICAgICAgICAgICBjb25zdCBjYW52YXMgPSBjYW52YXNWaWV3Py5jYW52YXM7XHJcbiAgICAgICAgICAgIGlmKCFjYW52YXMpIHJldHVybiBmYWxzZTtcclxuXHJcbiAgICAgICAgICAgIGNvbnN0IHVuaW5zdGFsbGVyID0gYXJvdW5kKGNhbnZhcy5jb25zdHJ1Y3Rvci5wcm90b3R5cGUsIHtcclxuICAgICAgICAgICAgICAgIHNob3dDcmVhdGlvbk1lbnU6IChuZXh0OiBhbnkpID0+XHJcbiAgICAgICAgICAgICAgICAgICAgZnVuY3Rpb24gKGU6IE1lbnUsIHQ6YW55LCBhOmFueSkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zdCByZXN1bHQgPSBuZXh0LmNhbGwodGhpcywgZSwgdCwgYSk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGUuYWRkU2VwYXJhdG9yKCkuYWRkSXRlbSgoaXRlbTogTWVudUl0ZW0pID0+IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGl0ZW0uc2V0U2VjdGlvbihcImNyZWF0ZVwiKVxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5zZXRUaXRsZShcIkFkZCBDYXJkIFRhYmxlXCIpXHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLnNldEljb24oXCJ0YWJsZVwiKVxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5vbkNsaWNrKGFzeW5jICgpID0+IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3JlYXRlQ2FyZFRhYmxlKHRoaXMsIGUsIHQsIGEpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHJlc3VsdDtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgICAgIHRoaXMucmVnaXN0ZXIodW5pbnN0YWxsZXIpO1xyXG5cclxuICAgICAgICAgICAgY29uc29sZS5sb2coXCJPYnNpZGlhbi1DYW52YXMtTWluZE1hcDogY2FudmFzIG5vZGUgcGF0Y2hlZFwiKTtcclxuICAgICAgICAgICAgcmV0dXJuIHRydWU7XHJcbiAgICAgICAgfVxyXG5cclxuICAgICAgICB0aGlzLmFwcC53b3Jrc3BhY2Uub25MYXlvdXRSZWFkeSgoKSA9PiB7XHJcbiAgICAgICAgICAgIGlmICghcGF0Y2hOb2RlKCkpIHtcclxuICAgICAgICAgICAgICAgIGNvbnN0IGV2dCA9IHRoaXMuYXBwLndvcmtzcGFjZS5vbihcImxheW91dC1jaGFuZ2VcIiwgKCkgPT4ge1xyXG4gICAgICAgICAgICAgICAgICAgIHBhdGNoTm9kZSgpICYmIHRoaXMuYXBwLndvcmtzcGFjZS5vZmZyZWYoZXZ0KTtcclxuICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICAgICAgdGhpcy5yZWdpc3RlckV2ZW50KGV2dCk7XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9KTtcclxuICAgIH1cclxuXHJcbiAgICByZWdpc3RlckNvbW1hbmRzKCkge1xyXG4gICAgICAgIHRoaXMuYWRkQ29tbWFuZCh7XHJcbiAgICAgICAgICAgIGlkOiAnY3JlYXRlLXRhYmxlLWdlbmVydGF0b3InLFxyXG4gICAgICAgICAgICBuYW1lOiAnQ3JlYXRlIFRhYmxlIEdlbmVyYXRvcicsXHJcbiAgICAgICAgICAgIGVkaXRvckNhbGxiYWNrOiAoZWRpdG9yOiBFZGl0b3IsIHZpZXc6IE1hcmtkb3duVmlldykgPT4ge1xyXG4gICAgICAgICAgICAgICAgaWYgKChyZXF1aXJlQXBpVmVyc2lvbihcIjAuMTUuMFwiKSA/IGFjdGl2ZURvY3VtZW50IDogZG9jdW1lbnQpPy5ib2R5LmNvbnRhaW5zKHRoaXMudGFibGVHZW5lcmF0b3JFbCkpIHJldHVybjtcclxuXHJcbiAgICAgICAgICAgICAgICB0aGlzLmNyZWF0ZUdlbmVyYXRvck1lbnUoXCJ0YWJsZVwiLCB7IGVkaXRvcjogZWRpdG9yIH0sIHRoaXMpO1xyXG4gICAgICAgICAgICAgICAgY29uc3QgY29vcmRzID0gY2FsY3VsYXRlRWRpdG9yKGVkaXRvciwgdGhpcy50YWJsZUdlbmVyYXRvckVsKTtcclxuICAgICAgICAgICAgICAgIGlmKCFjb29yZHMpIHJldHVybjtcclxuICAgICAgICAgICAgICAgIHNldFRhYmxlR2VuZXJhdG9yTWVudVBvc2l0aW9uKHRoaXMudGFibGVHZW5lcmF0b3JFbCwgY29vcmRzLCBcImVkaXRvclwiKTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuICAgIHJlZ2lzdGVyVGFibGVHZW5lcmF0b3JNZW51KCkge1xyXG4gICAgICAgIHRoaXMuYXBwLndvcmtzcGFjZS5vbignd2luZG93LW9wZW4nLCAobGVhZikgPT4ge1xyXG4gICAgICAgICAgICB0aGlzLnJlZ2lzdGVyRG9tRXZlbnQobGVhZi5kb2MsICdjbGljaycsIChldnQ6IE1vdXNlRXZlbnQpID0+IHtcclxuICAgICAgICAgICAgICAgIGNvbnN0IHRhcmdldCA9IGV2dC50YXJnZXQgYXMgSFRNTEVsZW1lbnQ7XHJcblxyXG4gICAgICAgICAgICAgICAgaWYgKCF0aGlzLnRhYmxlR2VuZXJhdG9yRWwgfHwgIXRhcmdldCkgcmV0dXJuO1xyXG4gICAgICAgICAgICAgICAgaWYgKHRhcmdldC5jbGFzc0xpc3QuY29udGFpbnMoXCJ0YWJsZS1nZW5lcmF0b3ItbWVudVwiKSB8fCB0YXJnZXQucGFyZW50RWxlbWVudD8uY2xhc3NMaXN0LmNvbnRhaW5zKFwidGFibGUtZ2VuZXJhdG9yLW1lbnVcIikgfHwgdGFyZ2V0LnRhZ05hbWUgPT0gXCJCVVRUT05cIikgcmV0dXJuO1xyXG4gICAgICAgICAgICAgICAgaWYgKHRoaXMudGFibGVHZW5lcmF0b3JFbD8uY29udGFpbnModGFyZ2V0KSkgcmV0dXJuO1xyXG4gICAgICAgICAgICAgICAgaWYgKCFhY3RpdmVEb2N1bWVudC5ib2R5LmNvbnRhaW5zKHRoaXMudGFibGVHZW5lcmF0b3JFbCkpIHJldHVybjtcclxuXHJcbiAgICAgICAgICAgICAgICB0aGlzLnRhYmxlR2VuZXJhdG9yRWwuZGV0YWNoKCk7XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0pO1xyXG4gICAgfVxyXG5cclxuICAgIG9udW5sb2FkKCkge1xyXG4gICAgICAgIGlmICh0aGlzLnRhYmxlR2VuZXJhdG9yRWwpIHtcclxuICAgICAgICAgICAgdGhpcy50YWJsZUdlbmVyYXRvckNvbXBvbmVudC4kZGVzdHJveSgpO1xyXG4gICAgICAgICAgICB0aGlzLnRhYmxlR2VuZXJhdG9yRWwuZGV0YWNoKCk7XHJcbiAgICAgICAgfVxyXG4gICAgfVxyXG5cclxuICAgIGFzeW5jIGxvYWRTZXR0aW5ncygpIHtcclxuICAgICAgICB0aGlzLnNldHRpbmdzID0gT2JqZWN0LmFzc2lnbih7fSwgREVGQVVMVF9TRVRUSU5HUywgYXdhaXQgdGhpcy5sb2FkRGF0YSgpKTtcclxuICAgIH1cclxuXHJcbiAgICBhc3luYyBzYXZlU2V0dGluZ3MoKSB7XHJcbiAgICAgICAgYXdhaXQgdGhpcy5zYXZlRGF0YSh0aGlzLnNldHRpbmdzKTtcclxuICAgIH1cclxufVxyXG5cclxuY2xhc3MgVGFibGVHZW5lcmF0b3JTZXR0aW5nVGFiIGV4dGVuZHMgUGx1Z2luU2V0dGluZ1RhYiB7XHJcbiAgICBwbHVnaW46IFRhYmxlR2VuZXJhdG9yUGx1Z2luO1xyXG5cclxuICAgIGNvbnN0cnVjdG9yKGFwcDogQXBwLCBwbHVnaW46IFRhYmxlR2VuZXJhdG9yUGx1Z2luKSB7XHJcbiAgICAgICAgc3VwZXIoYXBwLCBwbHVnaW4pO1xyXG4gICAgICAgIHRoaXMucGx1Z2luID0gcGx1Z2luO1xyXG4gICAgfVxyXG5cclxuICAgIGRpc3BsYXkoKTogdm9pZCB7XHJcbiAgICAgICAgY29uc3QgeyBjb250YWluZXJFbCB9ID0gdGhpcztcclxuXHJcbiAgICAgICAgY29udGFpbmVyRWwuZW1wdHkoKTtcclxuXHJcbiAgICAgICAgY29udGFpbmVyRWwuY3JlYXRlRWwoJ2gyJywgeyB0ZXh0OiAnVGFibGUgR2VuZXJhdG9yJyB9KTtcclxuXHJcbiAgICAgICAgbGV0IHJvd1RleHQ6IEhUTUxEaXZFbGVtZW50O1xyXG4gICAgICAgIG5ldyBTZXR0aW5nKGNvbnRhaW5lckVsKVxyXG4gICAgICAgICAgICAuc2V0TmFtZSgnUm93IENvdW50JylcclxuICAgICAgICAgICAgLnNldERlc2MoJ1RoZSBudW1iZXIgb2Ygcm93cyBpbiB0aGUgdGFibGUnKVxyXG4gICAgICAgICAgICAuYWRkU2xpZGVyKChzbGlkZXIpID0+XHJcbiAgICAgICAgICAgICAgICBzbGlkZXJcclxuICAgICAgICAgICAgICAgICAgICAuc2V0TGltaXRzKDIsIDEyLCAxKVxyXG4gICAgICAgICAgICAgICAgICAgIC5zZXRWYWx1ZSh0aGlzLnBsdWdpbi5zZXR0aW5ncy5yb3dDb3VudClcclxuICAgICAgICAgICAgICAgICAgICAub25DaGFuZ2UoYXN5bmMgKHZhbHVlKSA9PiB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHJvd1RleHQuaW5uZXJUZXh0ID0gYCAkeyB2YWx1ZS50b1N0cmluZygpIH1gO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnBsdWdpbi5zZXR0aW5ncy5yb3dDb3VudCA9IHZhbHVlO1xyXG4gICAgICAgICAgICAgICAgICAgIH0pLFxyXG4gICAgICAgICAgICApXHJcbiAgICAgICAgICAgIC5zZXR0aW5nRWwuY3JlYXRlRGl2KFwiXCIsIChlbCkgPT4ge1xyXG4gICAgICAgICAgICByb3dUZXh0ID0gZWw7XHJcbiAgICAgICAgICAgIGVsLmNsYXNzTmFtZSA9IFwidGFibGUtZ2VuZXJhdG9yLXNldHRpbmctdGV4dFwiO1xyXG4gICAgICAgICAgICBlbC5pbm5lclRleHQgPSBgICR7IHRoaXMucGx1Z2luLnNldHRpbmdzLnJvd0NvdW50LnRvU3RyaW5nKCkgfWA7XHJcbiAgICAgICAgfSk7XHJcblxyXG4gICAgICAgIGxldCBjb2x1bW5UZXh0OiBIVE1MRGl2RWxlbWVudDtcclxuICAgICAgICBuZXcgU2V0dGluZyhjb250YWluZXJFbClcclxuICAgICAgICAgICAgLnNldE5hbWUoJ0NvbHVtbnMgQ291bnQnKVxyXG4gICAgICAgICAgICAuc2V0RGVzYygnVGhlIG51bWJlciBvZiBjb2x1bW5zIGluIHRoZSB0YWJsZScpXHJcbiAgICAgICAgICAgIC5hZGRTbGlkZXIoKHNsaWRlcikgPT5cclxuICAgICAgICAgICAgICAgIHNsaWRlclxyXG4gICAgICAgICAgICAgICAgICAgIC5zZXRMaW1pdHMoMiwgMTIsIDEpXHJcbiAgICAgICAgICAgICAgICAgICAgLnNldFZhbHVlKHRoaXMucGx1Z2luLnNldHRpbmdzLmNvbHVtbkNvdW50KVxyXG4gICAgICAgICAgICAgICAgICAgIC5vbkNoYW5nZShhc3luYyAodmFsdWUpID0+IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgY29sdW1uVGV4dC5pbm5lclRleHQgPSBgICR7IHZhbHVlLnRvU3RyaW5nKCkgfWA7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMucGx1Z2luLnNldHRpbmdzLmNvbHVtbkNvdW50ID0gdmFsdWU7XHJcbiAgICAgICAgICAgICAgICAgICAgfSksXHJcbiAgICAgICAgICAgIClcclxuICAgICAgICAgICAgLnNldHRpbmdFbC5jcmVhdGVEaXYoXCJcIiwgKGVsKSA9PiB7XHJcbiAgICAgICAgICAgIGNvbHVtblRleHQgPSBlbDtcclxuICAgICAgICAgICAgZWwuY2xhc3NOYW1lID0gXCJ0YWJsZS1nZW5lcmF0b3Itc2V0dGluZy10ZXh0XCI7XHJcbiAgICAgICAgICAgIGVsLmlubmVyVGV4dCA9IGAgJHsgdGhpcy5wbHVnaW4uc2V0dGluZ3MuY29sdW1uQ291bnQudG9TdHJpbmcoKSB9YDtcclxuICAgICAgICB9KTtcclxuXHJcbiAgICAgICAgdGhpcy5jb250YWluZXJFbC5jcmVhdGVFbCgnaDInLCB7IHRleHQ6ICdTYXkgVGhhbmsgWW91JyB9KTtcclxuXHJcbiAgICAgICAgbmV3IFNldHRpbmcoY29udGFpbmVyRWwpXHJcbiAgICAgICAgICAgIC5zZXROYW1lKCdEb25hdGUnKVxyXG4gICAgICAgICAgICAuc2V0RGVzYygnSWYgeW91IGxpa2UgdGhpcyBwbHVnaW4sIGNvbnNpZGVyIGRvbmF0aW5nIHRvIHN1cHBvcnQgY29udGludWVkIGRldmVsb3BtZW50OicpXHJcbiAgICAgICAgICAgIC5hZGRCdXR0b24oKGJ0KSA9PiB7XHJcbiAgICAgICAgICAgICAgICBidC5idXR0b25FbC5vdXRlckhUTUwgPSBgPGEgaHJlZj1cImh0dHBzOi8vd3d3LmJ1eW1lYWNvZmZlZS5jb20vYm9uaW5hbGxcIj48aW1nIHNyYz1cImh0dHBzOi8vaW1nLmJ1eW1lYWNvZmZlZS5jb20vYnV0dG9uLWFwaS8/dGV4dD1CdXkgbWUgYSBjb2ZmZWUmZW1vamk9JnNsdWc9Ym9uaW5hbGwmYnV0dG9uX2NvbG91cj02NDk1RUQmZm9udF9jb2xvdXI9ZmZmZmZmJmZvbnRfZmFtaWx5PUludGVyJm91dGxpbmVfY29sb3VyPTAwMDAwMCZjb2ZmZWVfY29sb3VyPUZGREQwMFwiPjwvYT5gO1xyXG4gICAgICAgICAgICB9KTtcclxuICAgIH1cclxufVxyXG4iXSwibmFtZXMiOlsiZWxlbWVudCIsImZpbGUiLCJkZXRhY2giLCJjcmVhdGVfZWFjaF9ibG9jayIsImluc2VydCIsImluc3RhbmNlIiwiY3JlYXRlX2ZyYWdtZW50IiwidGV4dCIsImN0eCIsImVuZCIsIk5vdGljZSIsInNldEljb24iLCJ1cGRhdGUiLCJfYSIsInJlcXVpcmVBcGlWZXJzaW9uIiwiUGx1Z2luIiwiUGx1Z2luU2V0dGluZ1RhYiIsIlNldHRpbmciXSwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUEsU0FBUyxPQUFPO0FBQUc7QUFFbkIsU0FBUyxPQUFPLEtBQUssS0FBSztBQUV0QixhQUFXLEtBQUs7QUFDWixRQUFJLEtBQUssSUFBSTtBQUNqQixTQUFPO0FBQ1g7QUFJQSxTQUFTLGFBQWFBLFVBQVNDLE9BQU0sTUFBTSxRQUFRLE1BQU07QUFDckQsRUFBQUQsU0FBUSxnQkFBZ0I7QUFBQSxJQUNwQixLQUFLLEVBQUUsTUFBQUMsT0FBTSxNQUFNLFFBQVEsS0FBTTtBQUFBLEVBQ3pDO0FBQ0E7QUFDQSxTQUFTLElBQUksSUFBSTtBQUNiLFNBQU8sR0FBRTtBQUNiO0FBQ0EsU0FBUyxlQUFlO0FBQ3BCLFNBQU8sdUJBQU8sT0FBTyxJQUFJO0FBQzdCO0FBQ0EsU0FBUyxRQUFRLEtBQUs7QUFDbEIsTUFBSSxRQUFRLEdBQUc7QUFDbkI7QUFDQSxTQUFTLFlBQVksT0FBTztBQUN4QixTQUFPLE9BQU8sVUFBVTtBQUM1QjtBQUNBLFNBQVMsZUFBZSxHQUFHLEdBQUc7QUFDMUIsU0FBTyxLQUFLLElBQUksS0FBSyxJQUFJLE1BQU0sTUFBTyxLQUFLLE9BQU8sTUFBTSxZQUFhLE9BQU8sTUFBTTtBQUN0RjtBQVlBLFNBQVMsU0FBUyxLQUFLO0FBQ25CLFNBQU8sT0FBTyxLQUFLLEdBQUcsRUFBRSxXQUFXO0FBQ3ZDO0FBcUJBLFNBQVMsWUFBWSxZQUFZLEtBQUssU0FBUyxJQUFJO0FBQy9DLE1BQUksWUFBWTtBQUNaLFVBQU0sV0FBVyxpQkFBaUIsWUFBWSxLQUFLLFNBQVMsRUFBRTtBQUM5RCxXQUFPLFdBQVcsR0FBRyxRQUFRO0FBQUEsRUFDaEM7QUFDTDtB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
