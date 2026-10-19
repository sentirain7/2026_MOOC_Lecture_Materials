/* @ds-bundle: {"format":3,"namespace":"NACMIDDesignSystem_2c921a","components":[{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"IconButton","sourcePath":"components/core/IconButton.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"Select","sourcePath":"components/core/Select.jsx"},{"name":"Badge","sourcePath":"components/feedback/Badge.jsx"},{"name":"CategoryBadge","sourcePath":"components/feedback/CategoryBadge.jsx"},{"name":"ProgressBar","sourcePath":"components/feedback/ProgressBar.jsx"},{"name":"ScoreBar","sourcePath":"components/feedback/ScoreBar.jsx"},{"name":"StatusBadge","sourcePath":"components/feedback/StatusBadge.jsx"},{"name":"TierBadge","sourcePath":"components/feedback/TierBadge.jsx"},{"name":"StatCard","sourcePath":"components/navigation/StatCard.jsx"},{"name":"Tabs","sourcePath":"components/navigation/Tabs.jsx"}],"sourceHashes":{"components/core/Button.jsx":"3d14460b07be","components/core/Card.jsx":"ec6c33fc751f","components/core/IconButton.jsx":"9611478f2c02","components/core/Input.jsx":"99245f325226","components/core/Select.jsx":"8ea8214d2d1c","components/feedback/Badge.jsx":"ed63418da7ac","components/feedback/CategoryBadge.jsx":"d7f8b7d7c496","components/feedback/ProgressBar.jsx":"045c9584a2e8","components/feedback/ScoreBar.jsx":"312abbbe17c5","components/feedback/StatusBadge.jsx":"8fa4a4b80cf5","components/feedback/TierBadge.jsx":"3540782300fb","components/navigation/StatCard.jsx":"47439db123d7","components/navigation/Tabs.jsx":"ab6051321924","ui_kits/nacmid/DashboardScreen.jsx":"76c2ac45d048","ui_kits/nacmid/Header.jsx":"fff2276d8a14","ui_kits/nacmid/InverseDesignScreen.jsx":"7be87c6dcabf","ui_kits/nacmid/MoleculesScreen.jsx":"2ae76edbb499","ui_kits/nacmid/Sidebar.jsx":"d1314df41960","ui_kits/nacmid/icons.jsx":"d3fbe5b47316","ui_kits/nacmid/mockData.js":"310214f0064d"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.NACMIDDesignSystem_2c921a = window.NACMIDDesignSystem_2c921a || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Button — the platform's primary action control.
 * Variants mirror the app's .btn-* utility classes (gradient primary,
 * solid-slate secondary, blue-outline, danger). Sizes sm / md / lg.
 */
const SIZES = {
  sm: {
    padding: '0.375rem 0.75rem',
    fontSize: 'var(--text-sm)',
    radius: 'var(--radius-sm)'
  },
  md: {
    padding: '0.625rem 1rem',
    fontSize: 'var(--text-sm)',
    radius: 'var(--radius-md)'
  },
  lg: {
    padding: '0.75rem 1.5rem',
    fontSize: 'var(--text-base)',
    radius: 'var(--radius-xl)'
  }
};
const VARIANTS = {
  primary: {
    background: 'var(--gradient-button)',
    color: '#fff',
    border: '1px solid transparent'
  },
  secondary: {
    background: 'var(--bg-tertiary)',
    color: '#fff',
    border: '1px solid var(--border-light)'
  },
  outline: {
    background: 'transparent',
    color: 'var(--primary-400)',
    border: '1px solid var(--primary-500)'
  },
  danger: {
    background: 'linear-gradient(to right, #dc2626, #e11d48)',
    color: '#fff',
    border: '1px solid transparent'
  },
  ghost: {
    background: 'transparent',
    color: 'var(--text-secondary)',
    border: '1px solid transparent'
  }
};
function Button({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconRight: IconRight,
  disabled = false,
  type = 'button',
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const sz = SIZES[size] || SIZES.md;
  const v = VARIANTS[variant] || VARIANTS.primary;
  const lift = hover && !disabled && variant === 'primary';
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    onClick: onClick,
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '0.5rem',
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--weight-medium)',
      lineHeight: 1,
      whiteSpace: 'nowrap',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.4 : 1,
      boxShadow: lift ? 'var(--glow-btn-primary)' : 'var(--shadow-sm)',
      transform: lift ? 'translateY(-2px)' : 'none',
      transition: 'all var(--duration-base) var(--ease-standard)',
      padding: sz.padding,
      fontSize: sz.fontSize,
      borderRadius: sz.radius,
      filter: hover && !disabled && variant === 'secondary' ? 'brightness(1.25)' : 'none',
      ...v,
      ...style
    }
  }, rest), Icon ? /*#__PURE__*/React.createElement(Icon, {
    style: {
      width: '1.05em',
      height: '1.05em'
    }
  }) : null, children, IconRight ? /*#__PURE__*/React.createElement(IconRight, {
    style: {
      width: '1.05em',
      height: '1.05em'
    }
  }) : null);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Card — the floating dark-slate container used across the dashboard.
 * #111827 fill, 1px #1f2937 border, rounded-xl, deep shadow + backdrop blur.
 * Optional `title`/`actions` render the bordered header row; `elevated` swaps
 * to the stronger shadow + inner white ring.
 */
function Card({
  title,
  actions,
  children,
  elevated = false,
  padded = true,
  style,
  bodyStyle,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      background: 'var(--bg-secondary)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: elevated ? 'var(--shadow-card-elevated)' : 'var(--shadow-xl)',
      backdropFilter: 'var(--blur-card)',
      color: 'var(--text)',
      overflow: 'hidden',
      ...style
    }
  }, rest), (title || actions) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '0.75rem',
      padding: 'var(--space-4) var(--space-5)',
      borderBottom: '1px solid var(--border)',
      fontWeight: 'var(--weight-semibold)',
      color: '#fff'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)'
    }
  }, title), actions ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: '0.5rem',
      alignItems: 'center'
    }
  }, actions) : null), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: padded ? 'var(--space-5)' : 0,
      ...bodyStyle
    }
  }, children));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID IconButton — square, icon-only control used in the header
 * (bell, settings) and toolbars. Slate-700 hover fill, slate-400→white icon.
 */
function IconButton({
  icon: Icon,
  label,
  size = 'md',
  active = false,
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const dim = size === 'sm' ? '2rem' : size === 'lg' ? '2.75rem' : '2.25rem';
  const iconDim = size === 'sm' ? '1rem' : size === 'lg' ? '1.375rem' : '1.25rem';
  const lit = hover || active;
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    "aria-label": label,
    title: label,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      width: dim,
      height: dim,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 'var(--radius-md)',
      border: 'none',
      cursor: 'pointer',
      background: lit ? 'var(--surface-input)' : 'transparent',
      color: lit ? '#fff' : 'var(--text-secondary)',
      transition: 'all var(--duration-base) var(--ease-standard)',
      ...style
    }
  }, rest), Icon ? /*#__PURE__*/React.createElement(Icon, {
    style: {
      width: iconDim,
      height: iconDim
    }
  }) : null);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Input — labelled text/number field. Slate-700 fill, slate-600
 * border, blue focus ring. Supports an optional label, hint, and error.
 */
function Input({
  label,
  hint,
  error,
  type = 'text',
  value,
  onChange,
  placeholder,
  mono = false,
  disabled = false,
  id,
  style,
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const autoId = React.useId();
  const fieldId = id || autoId;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '0.25rem'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-medium)',
      color: '#cbd5e1'
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    type: type,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      width: '100%',
      padding: '0.5rem 0.75rem',
      background: 'var(--surface-input)',
      border: '1px solid',
      borderColor: error ? 'var(--error)' : focus ? 'transparent' : 'var(--border-light)',
      borderRadius: 'var(--radius-md)',
      color: '#fff',
      fontFamily: mono ? 'var(--font-mono)' : 'var(--font-sans)',
      fontSize: 'var(--text-sm)',
      outline: 'none',
      boxShadow: focus ? 'var(--ring-focus)' : 'none',
      opacity: disabled ? 0.5 : 1,
      transition: 'box-shadow var(--duration-base) var(--ease-standard)',
      ...style
    }
  }, rest)), error ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--status-failed-fg)'
    }
  }, error) : hint ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)'
    }
  }, hint) : null);
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Select — labelled native dropdown styled to match the dark form
 * fields (slate-800 fill in the app's inline form rows). Pass `options` as
 * an array of strings or { value, label } objects.
 */
function Select({
  label,
  value,
  onChange,
  options = [],
  disabled = false,
  id,
  style,
  ...rest
}) {
  const autoId = React.useId();
  const fieldId = id || autoId;
  const norm = options.map(o => typeof o === 'object' ? o : {
    value: o,
    label: String(o)
  });
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '0.25rem'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 'var(--weight-medium)',
      color: '#cbd5e1'
    }
  }, label), /*#__PURE__*/React.createElement("select", _extends({
    id: fieldId,
    value: value,
    onChange: onChange,
    disabled: disabled,
    style: {
      appearance: 'none',
      width: '100%',
      padding: '0.5rem 2rem 0.5rem 0.75rem',
      background: 'var(--bg-tertiary) url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E") no-repeat right 0.6rem center',
      border: '1px solid var(--border-light)',
      borderRadius: 'var(--radius-md)',
      color: '#e2e8f0',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-sm)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      ...style
    }
  }, rest), norm.map(o => /*#__PURE__*/React.createElement("option", {
    key: o.value,
    value: o.value
  }, o.label))));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Select.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Badge — the base pill. The whole semantic-color system is built on
 * this triad: translucent fill (color/20), colored text (color-400), and a
 * color/30 border. Pass a `tone` for a preset, or `color` for a custom hue.
 */
const TONES = {
  blue: '59,130,246',
  indigo: '99,102,241',
  violet: '139,92,246',
  green: '34,197,94',
  emerald: '16,185,129',
  amber: '245,158,11',
  yellow: '234,179,8',
  orange: '249,115,22',
  red: '239,68,68',
  rose: '244,63,94',
  cyan: '6,182,212',
  sky: '14,165,233',
  teal: '20,184,166',
  slate: '100,116,139',
  gray: '107,114,128'
};
const TEXT = {
  blue: '#60a5fa',
  indigo: '#a5b4fc',
  violet: '#a78bfa',
  green: '#4ade80',
  emerald: '#34d399',
  amber: '#fbbf24',
  yellow: '#facc15',
  orange: '#fb923c',
  red: '#f87171',
  rose: '#fb7185',
  cyan: '#22d3ee',
  sky: '#38bdf8',
  teal: '#2dd4bf',
  slate: '#cbd5e1',
  gray: '#9ca3af'
};
function Badge({
  children,
  tone = 'blue',
  size = 'md',
  icon: Icon,
  color,
  textColor,
  style,
  ...rest
}) {
  const rgb = color || TONES[tone] || TONES.blue;
  const fg = textColor || TEXT[tone] || '#60a5fa';
  const pad = size === 'sm' ? '0.0625rem 0.5rem' : '0.125rem 0.625rem';
  const fs = size === 'sm' ? 'var(--text-2xs)' : 'var(--text-xs)';
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.25rem',
      padding: pad,
      borderRadius: 'var(--radius-full)',
      fontSize: fs,
      fontWeight: 'var(--weight-medium)',
      lineHeight: 1.4,
      background: `rgba(${rgb}, 0.20)`,
      color: fg,
      border: `1px solid rgba(${rgb}, 0.30)`,
      whiteSpace: 'nowrap',
      ...style
    }
  }, rest), Icon ? /*#__PURE__*/React.createElement(Icon, {
    style: {
      width: '0.85em',
      height: '0.85em'
    }
  }) : null, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Badge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/CategoryBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID CategoryBadge — molecule family / additive category chip. Maps the
 * domain taxonomy to SSOT colors: SARA families (saturate/aromatic/resin/
 * asphaltene), additive classes (polymer, surfactant, nanoparticle…), and
 * single-mole categories (atmospheric, solvent, deicing…). Fixed width,
 * capitalized, underscores shown as spaces.
 */
const CATS = {
  saturate: '34,197,94',
  aromatic: '234,179,8',
  resin: '249,115,22',
  asphaltene: '239,68,68',
  additive: '139,92,246',
  atmospheric: '14,165,233',
  fuel: '245,158,11',
  solvent: '20,184,166',
  organic_acid: '132,204,22',
  deicing: '99,102,241',
  aging: '244,63,94',
  inorganic_acid: '220,38,38',
  inorganic: '6,182,212',
  polymer: '139,92,246',
  organic_polymer: '139,92,246',
  chemical: '236,72,153',
  organic_wax: '202,138,4',
  recycled_polymer: '5,150,105',
  surfactant: '217,70,239',
  nanoparticle: '37,99,235'
};
const TEXT = {
  saturate: '#4ade80',
  aromatic: '#facc15',
  resin: '#fb923c',
  asphaltene: '#f87171',
  additive: '#a78bfa',
  atmospheric: '#38bdf8',
  fuel: '#fbbf24',
  solvent: '#2dd4bf',
  organic_acid: '#a3e635',
  deicing: '#a5b4fc',
  aging: '#fb7185',
  inorganic_acid: '#ef4444',
  inorganic: '#22d3ee',
  polymer: '#a78bfa',
  organic_polymer: '#a78bfa',
  chemical: '#f472b6',
  organic_wax: '#eab308',
  recycled_polymer: '#10b981',
  surfactant: '#e879f9',
  nanoparticle: '#3b82f6'
};
function CategoryBadge({
  category,
  fixedWidth = true,
  style,
  ...rest
}) {
  const rgb = CATS[category] || '107,114,128';
  const fg = TEXT[category] || '#9ca3af';
  return /*#__PURE__*/React.createElement("span", _extends({
    title: category,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: fixedWidth ? '5rem' : undefined,
      padding: '0.0625rem 0.375rem',
      borderRadius: 'var(--radius-sm)',
      fontSize: 'var(--text-2xs)',
      fontWeight: 'var(--weight-medium)',
      textTransform: 'capitalize',
      background: `rgba(${rgb}, 0.20)`,
      color: fg,
      border: `1px solid rgba(${rgb}, 0.30)`,
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
      ...style
    }
  }, rest), String(category || '').replace(/_/g, ' '));
}
Object.assign(__ds_scope, { CategoryBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/CategoryBadge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ProgressBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID ProgressBar — track + fill with optional step text. Used for job
 * progress and pipeline completion. Colors: blue / green / yellow / red.
 */
const FILL = {
  blue: '#3b82f6',
  green: '#22c55e',
  yellow: '#eab308',
  red: '#ef4444',
  indigo: '#6366f1'
};
const TRACK_W = {
  sm: '4rem',
  md: '6rem',
  lg: '8rem'
};
const TRACK_H = {
  sm: '0.25rem',
  md: '0.5rem',
  lg: '0.75rem'
};
function ProgressBar({
  progress = 0,
  currentStep,
  totalSteps,
  showText = true,
  size = 'md',
  color = 'blue',
  fullWidth = false,
  style,
  ...rest
}) {
  const pct = Math.min(100, Math.max(0, progress));
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      width: fullWidth ? '100%' : TRACK_W[size],
      height: TRACK_H[size],
      background: 'var(--surface-input)',
      borderRadius: 'var(--radius-full)',
      overflow: 'hidden',
      flex: fullWidth ? 1 : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      width: `${pct}%`,
      background: FILL[color] || FILL.blue,
      borderRadius: 'var(--radius-full)',
      transition: 'width var(--duration-slow) var(--ease-standard)'
    }
  })), showText && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      color: 'var(--text-secondary)',
      fontFamily: 'var(--font-mono)',
      whiteSpace: 'nowrap'
    }
  }, totalSteps && totalSteps > 0 ? /*#__PURE__*/React.createElement(React.Fragment, null, (currentStep ?? 0).toLocaleString(), " / ", totalSteps.toLocaleString(), ' ', /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "(", pct.toFixed(1), "%)")) : `${pct.toFixed(1)}%`));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ScoreBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID ScoreBar — compact 0–1 score meter used on candidate/recommendation
 * cards. Fill color thresholds: ≥0.8 emerald, ≥0.5 amber, else red. Shows the
 * numeric score to 2 decimals.
 */
function ScoreBar({
  score = 0,
  maxScore = 1.0,
  label,
  style,
  ...rest
}) {
  const pct = Math.min(100, Math.max(0, score / maxScore * 100));
  const fill = pct >= 80 ? '#10b981' : pct >= 50 ? '#f59e0b' : '#ef4444';
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.375rem',
      ...style
    }
  }, rest), label && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-secondary)'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      width: '4rem',
      height: '0.375rem',
      background: 'var(--surface-input)',
      borderRadius: 'var(--radius-full)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      width: `${pct}%`,
      background: fill,
      borderRadius: 'var(--radius-full)'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: '#cbd5e1',
      fontFamily: 'var(--font-mono)'
    }
  }, score != null ? score.toFixed(2) : '-'));
}
Object.assign(__ds_scope, { ScoreBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ScoreBar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/StatusBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID StatusBadge — experiment/job lifecycle status. Single source of
 * truth for status styling (matches the app's statusConfig). Status text
 * renders lowercase, verbatim. Optionally leads with a lifecycle icon.
 */
const CONFIG = {
  pending: {
    rgb: '234,179,8',
    fg: '#facc15',
    glyph: '◷'
  },
  draft: {
    rgb: '100,116,139',
    fg: '#cbd5e1',
    glyph: '◷'
  },
  queued: {
    rgb: '59,130,246',
    fg: '#60a5fa',
    glyph: '◷'
  },
  submitted: {
    rgb: '6,182,212',
    fg: '#22d3ee',
    glyph: '◷'
  },
  building: {
    rgb: '99,102,241',
    fg: '#a5b4fc',
    glyph: '▦'
  },
  ready: {
    rgb: '6,182,212',
    fg: '#22d3ee',
    glyph: '◷'
  },
  running: {
    rgb: '34,197,94',
    fg: '#4ade80',
    glyph: '▶'
  },
  active: {
    rgb: '14,165,233',
    fg: '#38bdf8',
    glyph: '▶'
  },
  completed: {
    rgb: '107,114,128',
    fg: '#9ca3af',
    glyph: '✓'
  },
  approved: {
    rgb: '16,185,129',
    fg: '#34d399',
    glyph: '✓'
  },
  matched: {
    rgb: '20,184,166',
    fg: '#2dd4bf',
    glyph: '✓'
  },
  failed: {
    rgb: '239,68,68',
    fg: '#f87171',
    glyph: '✕'
  },
  error: {
    rgb: '239,68,68',
    fg: '#f87171',
    glyph: '✕'
  },
  rejected: {
    rgb: '244,63,94',
    fg: '#fb7185',
    glyph: '✕'
  },
  cancelled: {
    rgb: '107,114,128',
    fg: '#9ca3af',
    glyph: '✕'
  },
  timeout: {
    rgb: '249,115,22',
    fg: '#fb923c',
    glyph: '◷'
  },
  blocked: {
    rgb: '245,158,11',
    fg: '#fbbf24',
    glyph: '◷'
  },
  planned: {
    rgb: '14,165,233',
    fg: '#38bdf8',
    glyph: '◷'
  }
};
function StatusBadge({
  status,
  showIcon = false,
  size = 'md',
  style,
  ...rest
}) {
  const c = CONFIG[status] || CONFIG.pending;
  const pad = size === 'sm' ? '0.0625rem 0.375rem' : '0.125rem 0.5rem';
  const fs = size === 'sm' ? 'var(--text-2xs)' : 'var(--text-xs)';
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.25rem',
      padding: pad,
      borderRadius: 'var(--radius-sm)',
      fontSize: fs,
      fontWeight: 'var(--weight-medium)',
      lineHeight: 1.4,
      background: `rgba(${c.rgb}, 0.20)`,
      color: c.fg,
      border: `1px solid rgba(${c.rgb}, 0.30)`,
      ...style
    }
  }, rest), showIcon ? /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '0.85em',
      lineHeight: 1
    }
  }, c.glyph) : null, status);
}
Object.assign(__ds_scope, { StatusBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/StatusBadge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/TierBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID TierBadge — simulation run tier. Four fixed tiers with SSOT colors:
 * screening (blue), confirm (violet), viscosity (orange), validation (red).
 */
const TIERS = {
  screening: {
    rgb: '59,130,246',
    fg: '#60a5fa'
  },
  confirm: {
    rgb: '139,92,246',
    fg: '#a78bfa'
  },
  viscosity: {
    rgb: '249,115,22',
    fg: '#fb923c'
  },
  validation: {
    rgb: '239,68,68',
    fg: '#f87171'
  }
};
function TierBadge({
  tier,
  size = 'md',
  style,
  ...rest
}) {
  const c = TIERS[tier] || TIERS.screening;
  const pad = size === 'sm' ? '0.0625rem 0.375rem' : '0.125rem 0.5rem';
  const fs = size === 'sm' ? 'var(--text-2xs)' : 'var(--text-xs)';
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      padding: pad,
      borderRadius: 'var(--radius-sm)',
      fontSize: fs,
      fontWeight: 'var(--weight-medium)',
      lineHeight: 1.4,
      background: `rgba(${c.rgb}, 0.20)`,
      color: c.fg,
      border: `1px solid rgba(${c.rgb}, 0.30)`,
      ...style
    }
  }, rest), tier);
}
Object.assign(__ds_scope, { TierBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/TierBadge.jsx", error: String((e && e.message) || e) }); }

// components/navigation/StatCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID StatCard — the compact metric tile from the dashboard status panel.
 * Translucent toned background + 1px border, a small solid icon chip, an
 * uppercase label, and a bold value. Hovers up slightly (scale 1.05).
 */
const TONES = {
  slate: {
    rgb: '100,116,139',
    fg: '#cbd5e1',
    solid: '#64748b'
  },
  blue: {
    rgb: '59,130,246',
    fg: '#60a5fa',
    solid: '#3b82f6'
  },
  indigo: {
    rgb: '99,102,241',
    fg: '#a5b4fc',
    solid: '#6366f1'
  },
  green: {
    rgb: '34,197,94',
    fg: '#4ade80',
    solid: '#22c55e'
  },
  yellow: {
    rgb: '234,179,8',
    fg: '#facc15',
    solid: '#eab308'
  },
  orange: {
    rgb: '249,115,22',
    fg: '#fb923c',
    solid: '#f97316'
  },
  red: {
    rgb: '239,68,68',
    fg: '#f87171',
    solid: '#ef4444'
  },
  violet: {
    rgb: '139,92,246',
    fg: '#a78bfa',
    solid: '#8b5cf6'
  },
  gray: {
    rgb: '107,114,128',
    fg: '#9ca3af',
    solid: '#6b7280'
  }
};
function StatCard({
  label,
  value,
  icon: Icon,
  tone = 'blue',
  loading = false,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const t = TONES[tone] || TONES.blue;
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '0.5rem',
      padding: '0.5rem 0.75rem',
      borderRadius: 'var(--radius-lg)',
      background: `rgba(${t.rgb}, 0.20)`,
      border: `1px solid rgba(${t.rgb}, 0.30)`,
      color: t.fg,
      transform: hover ? 'scale(1.05)' : 'none',
      transition: 'transform var(--duration-base) var(--ease-standard)',
      minWidth: '60px',
      ...style
    }
  }, rest), Icon && /*#__PURE__*/React.createElement("span", {
    style: {
      width: '1rem',
      height: '1rem',
      borderRadius: 'var(--radius-sm)',
      background: t.solid,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    style: {
      width: '0.625rem',
      height: '0.625rem',
      color: '#fff'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-2xs)',
      fontWeight: 'var(--weight-medium)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-wide)',
      opacity: 0.8
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-lg)',
      fontWeight: 'var(--weight-bold)'
    }
  }, loading ? '·' : value));
}
Object.assign(__ds_scope, { StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/StatCard.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tabs.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * NACMID Tabs — underline tab strip. Active tab: slate-700 fill, white text,
 * 2px blue bottom border. Inactive: slate-400, hover slate-200. Arrow-key
 * navigable. `tabs` is an array of { key, label }.
 */
function Tabs({
  tabs = [],
  activeTab,
  onTabChange,
  style,
  ...rest
}) {
  const prefix = React.useId();
  const onKey = (e, index) => {
    let next;
    if (e.key === 'ArrowRight') next = (index + 1) % tabs.length;else if (e.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;else return;
    e.preventDefault();
    onTabChange?.(tabs[next].key);
    document.getElementById(`${prefix}-tab-${tabs[next].key}`)?.focus();
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "tablist",
    style: {
      display: 'flex',
      gap: '0.25rem',
      borderBottom: '1px solid var(--surface-input)',
      ...style
    }
  }, rest), tabs.map((tab, i) => {
    const on = activeTab === tab.key;
    return /*#__PURE__*/React.createElement("button", {
      key: tab.key,
      id: `${prefix}-tab-${tab.key}`,
      role: "tab",
      "aria-selected": on,
      tabIndex: on ? 0 : -1,
      onClick: () => onTabChange?.(tab.key),
      onKeyDown: e => onKey(e, i),
      style: {
        padding: '0.375rem 0.75rem',
        fontSize: 'var(--text-xs)',
        fontWeight: 'var(--weight-medium)',
        borderRadius: 'var(--radius-sm) var(--radius-sm) 0 0',
        border: 'none',
        borderBottom: on ? '2px solid var(--primary-500)' : '2px solid transparent',
        marginBottom: '-1px',
        background: on ? 'var(--surface-input)' : 'transparent',
        color: on ? '#fff' : 'var(--text-secondary)',
        cursor: 'pointer',
        transition: 'all var(--duration-base) var(--ease-standard)'
      }
    }, tab.label);
  }));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tabs.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/DashboardScreen.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
// NACMID UI kit — Dashboard screen (status panel + experiment queue + GPU/charts).
function DensityChart() {
  const {
    DENSITY_SERIES
  } = window.NData;
  const W = 300,
    H = 150,
    pad = 28;
  const all = [...DENSITY_SERIES.AAA1, ...DENSITY_SERIES.SBS];
  const xs = all.map(p => p.t),
    ds = all.map(p => p.d);
  const minX = Math.min(...xs),
    maxX = Math.max(...xs);
  const minY = Math.min(...ds) - 0.005,
    maxY = Math.max(...ds) + 0.005;
  const X = t => pad + (t - minX) / (maxX - minX) * (W - pad - 8);
  const Y = d => pad - 8 + (1 - (d - minY) / (maxY - minY)) * (H - pad - 8);
  const line = s => s.map((p, i) => `${i ? 'L' : 'M'}${X(p.t).toFixed(1)},${Y(p.d).toFixed(1)}`).join(' ');
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${W} ${H}`,
    style: {
      width: '100%',
      height: 'auto'
    }
  }, [0, 0.25, 0.5, 0.75, 1].map(f => {
    const y = pad - 8 + f * (H - pad - 8);
    return /*#__PURE__*/React.createElement("line", {
      key: f,
      x1: pad,
      y1: y,
      x2: W - 8,
      y2: y,
      stroke: "#334155",
      strokeWidth: "0.5"
    });
  }), /*#__PURE__*/React.createElement("path", {
    d: line(DENSITY_SERIES.AAA1),
    fill: "none",
    stroke: "var(--sara-aromatic)",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("path", {
    d: line(DENSITY_SERIES.SBS),
    fill: "none",
    stroke: "var(--sara-additive)",
    strokeWidth: "2"
  }), DENSITY_SERIES.AAA1.map(p => /*#__PURE__*/React.createElement("circle", {
    key: `a${p.t}`,
    cx: X(p.t),
    cy: Y(p.d),
    r: "2.4",
    fill: "var(--sara-aromatic)"
  })), DENSITY_SERIES.SBS.map(p => /*#__PURE__*/React.createElement("circle", {
    key: `s${p.t}`,
    cx: X(p.t),
    cy: Y(p.d),
    r: "2.4",
    fill: "var(--sara-additive)"
  })));
}
function CEDBars() {
  const {
    CED_BY_ADDITIVE
  } = window.NData;
  const max = Math.max(...CED_BY_ADDITIVE.map(d => d.ced));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 8
    }
  }, CED_BY_ADDITIVE.map(d => /*#__PURE__*/React.createElement("div", {
    key: d.additive,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 56,
      fontSize: 'var(--text-xs)',
      color: 'var(--text-secondary)',
      textAlign: 'right'
    }
  }, d.additive), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      height: 14,
      background: 'var(--bg-tertiary)',
      borderRadius: 'var(--radius-sm)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: `${d.ced / max * 100}%`,
      height: '100%',
      background: 'var(--gradient-button)',
      borderRadius: 'var(--radius-sm)'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 34,
      fontSize: 'var(--text-xs)',
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, d.ced))));
}
function DashboardScreen() {
  const {
    Card,
    StatCard,
    StatusBadge,
    TierBadge,
    ProgressBar
  } = window.NACMIDDesignSystem_2c921a;
  const I = window.NIcon;
  const {
    QUEUE_STATS,
    EXPERIMENTS,
    GPUS
  } = window.NData;
  const s = QUEUE_STATS;
  const tiles = [{
    label: 'Total',
    value: s.total.toLocaleString(),
    icon: I.Layers,
    tone: 'slate'
  }, {
    label: 'Pending',
    value: s.pending,
    icon: I.Clock,
    tone: 'yellow'
  }, {
    label: 'Queued',
    value: s.queued,
    icon: I.Clock,
    tone: 'blue'
  }, {
    label: 'Building',
    value: s.building,
    icon: I.Layers,
    tone: 'indigo'
  }, {
    label: 'Running',
    value: s.running,
    icon: I.Play,
    tone: 'green'
  }, {
    label: 'Completed',
    value: s.completed.toLocaleString(),
    icon: I.CheckCircle,
    tone: 'gray'
  }, {
    label: 'Failed',
    value: s.failed,
    icon: I.XCircle,
    tone: 'red'
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 700,
      color: '#fff'
    }
  }, "Dashboard"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-sm)',
      marginTop: 4
    }
  }, "Monitor simulation progress and review recent results.")), /*#__PURE__*/React.createElement(Card, {
    title: "Current Status"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8
    }
  }, tiles.map(t => /*#__PURE__*/React.createElement(StatCard, _extends({
    key: t.label
  }, t))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1.6fr 1fr',
      gap: 16,
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Experiment Queue",
    padded: false
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxHeight: 380,
      overflowY: 'auto'
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      fontSize: 'var(--text-sm)',
      borderCollapse: 'collapse'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      color: 'var(--text-secondary)',
      textAlign: 'left'
    }
  }, /*#__PURE__*/React.createElement("th", {
    style: {
      padding: '10px 16px',
      fontWeight: 500,
      position: 'sticky',
      top: 0,
      background: 'var(--bg-secondary)'
    }
  }, "Experiment"), /*#__PURE__*/React.createElement("th", {
    style: {
      padding: '10px 8px',
      fontWeight: 500,
      position: 'sticky',
      top: 0,
      background: 'var(--bg-secondary)'
    }
  }, "Tier"), /*#__PURE__*/React.createElement("th", {
    style: {
      padding: '10px 8px',
      fontWeight: 500,
      position: 'sticky',
      top: 0,
      background: 'var(--bg-secondary)'
    }
  }, "Status"), /*#__PURE__*/React.createElement("th", {
    style: {
      padding: '10px 16px',
      fontWeight: 500,
      position: 'sticky',
      top: 0,
      background: 'var(--bg-secondary)'
    }
  }, "Progress"))), /*#__PURE__*/React.createElement("tbody", null, EXPERIMENTS.map(e => /*#__PURE__*/React.createElement("tr", {
    key: e.id,
    style: {
      borderTop: '1px solid rgba(51,65,85,0.5)'
    }
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '9px 16px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      color: '#e2e8f0',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      maxWidth: 220
    },
    title: e.id
  }, e.id), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: 'var(--text-muted)'
    }
  }, e.binder, " \xB7 ", e.additive, " \xB7 ", e.temp, " K")), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '9px 8px'
    }
  }, /*#__PURE__*/React.createElement(TierBadge, {
    tier: e.tier,
    size: "sm"
  })), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '9px 8px'
    }
  }, /*#__PURE__*/React.createElement(StatusBadge, {
    status: e.status,
    size: "sm"
  })), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '9px 16px'
    }
  }, /*#__PURE__*/React.createElement(ProgressBar, {
    progress: e.progress,
    size: "sm",
    color: e.status === 'failed' ? 'red' : e.status === 'completed' ? 'green' : 'blue'
  })))))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "GPU Utilization"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 12
    }
  }, GPUS.map(g => /*#__PURE__*/React.createElement("div", {
    key: g.id
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      fontSize: 'var(--text-xs)',
      marginBottom: 4
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: '#cbd5e1',
      fontWeight: 500
    }
  }, g.id, " \xB7 ", g.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      color: g.util > 0 ? 'var(--sara-saturate)' : 'var(--text-muted)'
    }
  }, g.util, "%")), /*#__PURE__*/React.createElement(ProgressBar, {
    progress: g.util,
    showText: false,
    fullWidth: true,
    color: g.util > 0 ? 'green' : 'blue'
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10,
      color: 'var(--text-muted)',
      marginTop: 3,
      fontFamily: 'var(--font-mono)',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, g.job || 'idle'))))), /*#__PURE__*/React.createElement(Card, {
    title: "Density vs Temperature"
  }, /*#__PURE__*/React.createElement(DensityChart, null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 16,
      marginTop: 8,
      fontSize: 11,
      color: 'var(--text-secondary)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 5
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 3,
      background: 'var(--sara-aromatic)',
      borderRadius: 2
    }
  }), "AAA1"), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 5
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 10,
      height: 3,
      background: 'var(--sara-additive)',
      borderRadius: 2
    }
  }), "AAA1 + SBS"))), /*#__PURE__*/React.createElement(Card, {
    title: "CED by Additive"
  }, /*#__PURE__*/React.createElement(CEDBars, null)))));
}
window.DashboardScreen = DashboardScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/DashboardScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/Header.jsx
try { (() => {
// NACMID UI kit — fixed top header (CI lockup + system stats + health dots).
function KitHeader() {
  const {
    Bell,
    Settings,
    Cpu,
    HardDrive
  } = window.NIcon;
  const {
    IconButton
  } = window.NACMIDDesignSystem_2c921a;
  const health = [{
    label: 'DB',
    status: 'ready'
  }, {
    label: 'Redis',
    status: 'ready'
  }, {
    label: 'Worker',
    status: 'limited'
  }];
  const dot = s => s === 'ready' ? '#4ade80' : s === 'limited' ? '#facc15' : '#f87171';
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      height: 'var(--header-height)',
      zIndex: 50,
      background: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border)',
      boxShadow: 'var(--shadow-header)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '100%',
      padding: '0 24px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/nacmid-icon.svg",
    width: "44",
    height: "44",
    alt: "NACMID"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/nacmid-logotype.svg",
    alt: "NACMID",
    style: {
      height: 26
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '-2px 0 0',
      fontSize: 9,
      color: 'var(--text-secondary)',
      letterSpacing: '0.02em',
      fontWeight: 500
    }
  }, "AI-Driven Computational Platform for Nanoscale Construction Material Inverse Design"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 16,
      fontSize: 'var(--text-xs)',
      borderRight: '1px solid var(--border-light)',
      paddingRight: 16
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      color: 'var(--text-secondary)'
    }
  }, /*#__PURE__*/React.createElement(Cpu, {
    size: 14
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, "61%")), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      color: 'var(--text-secondary)'
    }
  }, /*#__PURE__*/React.createElement(HardDrive, {
    size: 14
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, "48%"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, health.map(h => /*#__PURE__*/React.createElement("span", {
    key: h.label,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 5,
      fontSize: 11,
      color: 'var(--text-secondary)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: dot(h.status)
    }
  }), h.label))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11,
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-mono)'
    }
  }, "v01.05.60"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 4
    }
  }, /*#__PURE__*/React.createElement(IconButton, {
    icon: Bell,
    label: "Notifications"
  }), /*#__PURE__*/React.createElement(IconButton, {
    icon: Settings,
    label: "Settings"
  })))));
}
window.KitHeader = KitHeader;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/Header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/InverseDesignScreen.jsx
try { (() => {
// NACMID UI kit — Inverse Design wizard (① targets → ② plan → ③ monitor → ④ results).
function StepIndicator({
  step
}) {
  const steps = ['Targets', 'Plan', 'Run', 'Results'];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      marginBottom: 8
    }
  }, steps.map((label, i) => {
    const n = i + 1,
      done = n < step,
      on = n === step;
    return /*#__PURE__*/React.createElement(React.Fragment, {
      key: label
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 8
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        width: 26,
        height: 26,
        borderRadius: '50%',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 'var(--text-xs)',
        fontWeight: 700,
        fontFamily: 'var(--font-mono)',
        background: on ? 'var(--gradient-button)' : done ? 'rgba(16,185,129,0.2)' : 'var(--bg-tertiary)',
        color: on ? '#fff' : done ? 'var(--sara-saturate)' : 'var(--text-muted)',
        border: on ? 'none' : `1px solid ${done ? 'rgba(16,185,129,0.4)' : 'var(--border-light)'}`
      }
    }, done ? '✓' : n), /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 'var(--text-sm)',
        fontWeight: on ? 600 : 400,
        color: on ? '#fff' : 'var(--text-secondary)'
      }
    }, label)), i < steps.length - 1 && /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        height: 1,
        background: 'var(--border-light)',
        maxWidth: 60
      }
    }));
  }));
}
function TargetsStep({
  onPreview
}) {
  const {
    Card,
    Button,
    Select,
    Badge
  } = window.NACMIDDesignSystem_2c921a;
  const I = window.NIcon;
  const METRICS = [{
    name: 'work_of_separation',
    label: 'Work of Separation',
    unit: 'mJ/m²'
  }, {
    name: 'viscosity',
    label: 'Viscosity',
    unit: 'mPa·s'
  }, {
    name: 'density',
    label: 'Density',
    unit: 'g/cm³'
  }, {
    name: 'glass_transition_temperature_k',
    label: 'Tg',
    unit: 'K'
  }];
  const [targets, setTargets] = React.useState([{
    metric: 'work_of_separation',
    dir: 'maximize',
    min: 55,
    max: ''
  }, {
    metric: 'viscosity',
    dir: 'target',
    min: 120,
    max: 180
  }]);
  const [aggs, setAggs] = React.useState(['SiO2', 'CaCO3']);
  const AGG = ['SiO2', 'CaCO3', 'Al2O3', 'MgO', 'Fe2O3'];
  const upd = (i, patch) => setTargets(targets.map((t, j) => j === i ? {
    ...t,
    ...patch
  } : t));
  const unitOf = n => METRICS.find(m => m.name === n)?.unit;
  return /*#__PURE__*/React.createElement(Card, {
    title: "\u2460 Target properties"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 10
    }
  }, targets.map((t, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      alignItems: 'center',
      gap: 8,
      background: 'rgba(51,65,85,0.3)',
      borderRadius: 'var(--radius-md)',
      padding: 8
    }
  }, /*#__PURE__*/React.createElement("select", {
    value: t.metric,
    onChange: e => upd(i, {
      metric: e.target.value
    }),
    style: {
      background: 'var(--bg-tertiary)',
      color: '#e2e8f0',
      fontSize: 'var(--text-sm)',
      borderRadius: 'var(--radius-sm)',
      padding: '5px 8px',
      border: '1px solid var(--border-light)'
    }
  }, METRICS.map(m => /*#__PURE__*/React.createElement("option", {
    key: m.name,
    value: m.name
  }, m.label, " (", m.unit, ")"))), /*#__PURE__*/React.createElement("select", {
    value: t.dir,
    onChange: e => upd(i, {
      dir: e.target.value
    }),
    style: {
      background: 'var(--bg-tertiary)',
      color: '#e2e8f0',
      fontSize: 'var(--text-sm)',
      borderRadius: 'var(--radius-sm)',
      padding: '5px 8px',
      border: '1px solid var(--border-light)'
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "maximize"
  }, "Maximize"), /*#__PURE__*/React.createElement("option", {
    value: "minimize"
  }, "Minimize"), /*#__PURE__*/React.createElement("option", {
    value: "target"
  }, "Target range")), /*#__PURE__*/React.createElement("input", {
    type: "number",
    placeholder: "min",
    value: t.min,
    onChange: e => upd(i, {
      min: e.target.value
    }),
    style: {
      width: 72,
      background: 'var(--bg-tertiary)',
      color: '#e2e8f0',
      fontSize: 'var(--text-sm)',
      borderRadius: 'var(--radius-sm)',
      padding: '5px 8px',
      border: '1px solid var(--border-light)',
      fontFamily: 'var(--font-mono)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "~"), /*#__PURE__*/React.createElement("input", {
    type: "number",
    placeholder: "max",
    value: t.max,
    onChange: e => upd(i, {
      max: e.target.value
    }),
    style: {
      width: 72,
      background: 'var(--bg-tertiary)',
      color: '#e2e8f0',
      fontSize: 'var(--text-sm)',
      borderRadius: 'var(--radius-sm)',
      padding: '5px 8px',
      border: '1px solid var(--border-light)',
      fontFamily: 'var(--font-mono)'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)'
    }
  }, unitOf(t.metric)), /*#__PURE__*/React.createElement("button", {
    onClick: () => setTargets(targets.filter((_, j) => j !== i)),
    style: {
      marginLeft: 'auto',
      background: 'none',
      border: 'none',
      color: 'var(--text-muted)',
      cursor: 'pointer',
      fontSize: 14
    }
  }, "\u2715"))), /*#__PURE__*/React.createElement("button", {
    onClick: () => setTargets([...targets, {
      metric: 'density',
      dir: 'maximize',
      min: '',
      max: ''
    }]),
    style: {
      alignSelf: 'flex-start',
      background: 'none',
      border: 'none',
      color: 'var(--info)',
      cursor: 'pointer',
      fontSize: 'var(--text-sm)'
    }
  }, "+ Add target")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 24,
      marginTop: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 150
    }
  }, /*#__PURE__*/React.createElement(Select, {
    label: "Binder type",
    options: ['AAA1', 'AAK1', 'AAM1']
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 120
    }
  }, /*#__PURE__*/React.createElement(Select, {
    label: "Structure size",
    options: ['X1', 'X2', 'X3']
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 18
    }
  }, /*#__PURE__*/React.createElement("h4", {
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 600,
      color: '#cbd5e1',
      marginBottom: 8
    }
  }, "Aggregate (crystal) \u2014 interface targets"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, AGG.map(m => {
    const on = aggs.includes(m);
    return /*#__PURE__*/React.createElement("button", {
      key: m,
      onClick: () => setAggs(on ? aggs.filter(x => x !== m) : [...aggs, m]),
      style: {
        padding: '6px 14px',
        borderRadius: 'var(--radius-md)',
        fontSize: 'var(--text-sm)',
        cursor: 'pointer',
        border: 'none',
        background: on ? 'var(--primary-600)' : 'var(--bg-tertiary)',
        color: on ? '#fff' : 'var(--text-secondary)'
      }
    }, m);
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 24,
      display: 'flex',
      justifyContent: 'flex-end'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    icon: I.Sparkles,
    onClick: onPreview
  }, "Preview plan")));
}
function PlanStep({
  onApprove,
  onBack
}) {
  const {
    Card,
    Button,
    Badge,
    ScoreBar,
    TierBadge
  } = window.NACMIDDesignSystem_2c921a;
  const I = window.NIcon;
  const {
    PLAN_CANDIDATES,
    PLAN_DOE
  } = window.NData;
  const SARA_C = {
    asphaltene: 'var(--sara-asphaltene)',
    resin: 'var(--sara-resin)',
    aromatic: 'var(--sara-aromatic)',
    saturate: 'var(--sara-saturate)'
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "\u2461 Design plan",
    actions: /*#__PURE__*/React.createElement(Badge, {
      tone: "emerald",
      icon: I.Sparkles
    }, "BO \xB7 Bayesian design")
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 'var(--text-sm)',
      color: 'var(--text-secondary)',
      marginBottom: 14
    }
  }, "Champion model available \xB7 47 training labels \xB7 feasibility ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--sara-saturate)'
    }
  }, "feasible"), ". Top candidates from EHVI acquisition:"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: 12
    }
  }, PLAN_CANDIDATES.map(c => /*#__PURE__*/React.createElement("div", {
    key: c.rank,
    style: {
      background: 'rgba(51,65,85,0.3)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 600,
      color: '#fff',
      fontSize: 'var(--text-sm)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)'
    }
  }, "#", c.rank + 1), " ", c.additive, " ", c.wt, " wt%"), /*#__PURE__*/React.createElement(ScoreBar, {
    score: c.score
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      height: 8,
      borderRadius: 'var(--radius-full)',
      overflow: 'hidden',
      marginBottom: 10
    }
  }, Object.entries(c.sara).map(([k, v]) => /*#__PURE__*/React.createElement("div", {
    key: k,
    style: {
      width: `${v}%`,
      background: SARA_C[k]
    },
    title: `${k} ${v}%`
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-secondary)'
    }
  }, /*#__PURE__*/React.createElement("span", null, "W_sep ", /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, c.pred.work_of_separation)), /*#__PURE__*/React.createElement("span", null, "\u03B7 ", /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, c.pred.viscosity))))))), /*#__PURE__*/React.createElement(Card, {
    title: "DOE experiment plan",
    padded: false
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      fontSize: 'var(--text-sm)',
      borderCollapse: 'collapse'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      color: 'var(--text-secondary)',
      textAlign: 'left'
    }
  }, ['Kind', 'Aggregate', 'Temp', 'Tier', 'Replica', 'Dependency', 'Action'].map(h => /*#__PURE__*/React.createElement("th", {
    key: h,
    style: {
      padding: '10px 16px',
      fontWeight: 500,
      borderBottom: '1px solid var(--border)'
    }
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, PLAN_DOE.map((r, i) => /*#__PURE__*/React.createElement("tr", {
    key: i,
    style: {
      borderTop: '1px solid rgba(51,65,85,0.4)'
    }
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px',
      color: '#e2e8f0'
    }
  }, r.kind), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px',
      color: 'var(--text-secondary)'
    }
  }, r.aggregate), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px',
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, r.temp, " K"), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px'
    }
  }, /*#__PURE__*/React.createElement(TierBadge, {
    tier: r.tier,
    size: "sm"
  })), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px',
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, r.replica, "\xD7"), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-mono)'
    }
  }, r.dep), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '10px 16px'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: r.action === 'reuse' ? 'cyan' : 'blue',
    size: "sm"
  }, r.action))))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    onClick: onBack
  }, "Back"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    icon: I.ArrowRight,
    iconRight: I.ArrowRight,
    onClick: onApprove
  }, "Approve & run")));
}
function RunStep({
  onBack
}) {
  const {
    Card,
    Button,
    ProgressBar,
    StatusBadge,
    Badge
  } = window.NACMIDDesignSystem_2c921a;
  const members = [{
    id: 'binder #1 · 293K',
    status: 'completed'
  }, {
    id: 'binder #2 · 313K',
    status: 'completed'
  }, {
    id: 'layered SiO2 · seed 1',
    status: 'running'
  }, {
    id: 'layered SiO2 · seed 2',
    status: 'running'
  }, {
    id: 'layered SiO2 · seed 3',
    status: 'queued'
  }, {
    id: 'layered CaCO3 · seed 1',
    status: 'building'
  }, {
    id: 'layered CaCO3 · seed 2',
    status: 'pending'
  }, {
    id: 'layered CaCO3 · seed 3',
    status: 'pending'
  }];
  const done = members.filter(m => m.status === 'completed').length;
  return /*#__PURE__*/React.createElement(Card, {
    title: "\u2462 Pipeline monitor",
    actions: /*#__PURE__*/React.createElement(Badge, {
      tone: "violet"
    }, "pipeline \xB7 9f3c2a")
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement(ProgressBar, {
    progress: done / members.length * 100,
    showText: false,
    fullWidth: true,
    color: "green"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-sm)',
      color: '#cbd5e1',
      whiteSpace: 'nowrap'
    }
  }, done, " / ", members.length)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(2, 1fr)',
      gap: 8
    }
  }, members.map(m => /*#__PURE__*/React.createElement("div", {
    key: m.id,
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      background: 'rgba(51,65,85,0.3)',
      borderRadius: 'var(--radius-md)',
      padding: '8px 12px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      color: '#e2e8f0',
      fontFamily: 'var(--font-mono)'
    }
  }, m.id), /*#__PURE__*/React.createElement(StatusBadge, {
    status: m.status,
    size: "sm",
    showIcon: true
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 20,
      display: 'flex',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    onClick: onBack
  }, "Back to plan"), /*#__PURE__*/React.createElement(Button, {
    variant: "outline"
  }, "View results")));
}
function InverseDesignScreen() {
  const [step, setStep] = React.useState(1);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 700,
      color: '#fff'
    }
  }, "Inverse Design"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-sm)',
      marginTop: 4
    }
  }, "Specify target properties; the platform recommends compositions and plans the verification experiments.")), /*#__PURE__*/React.createElement(StepIndicator, {
    step: step
  }), step === 1 && /*#__PURE__*/React.createElement(TargetsStep, {
    onPreview: () => setStep(2)
  }), step === 2 && /*#__PURE__*/React.createElement(PlanStep, {
    onBack: () => setStep(1),
    onApprove: () => setStep(3)
  }), step >= 3 && /*#__PURE__*/React.createElement(RunStep, {
    onBack: () => setStep(2)
  }));
}
window.InverseDesignScreen = InverseDesignScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/InverseDesignScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/MoleculesScreen.jsx
try { (() => {
// NACMID UI kit — Molecules database screen (SARA library table + search/filter).
function MoleculesScreen() {
  const {
    Card,
    CategoryBadge,
    StatusBadge,
    Badge,
    Input,
    Button
  } = window.NACMIDDesignSystem_2c921a;
  const I = window.NIcon;
  const {
    MOLECULES,
    AGING_LABELS,
    AGING_TONE
  } = window.NData;
  const [query, setQuery] = React.useState('');
  const [filter, setFilter] = React.useState('all');
  const cats = ['all', 'saturate', 'aromatic', 'resin', 'asphaltene', 'additive'];
  const rows = MOLECULES.filter(m => (filter === 'all' || m.sara === filter) && (m.name.toLowerCase().includes(query.toLowerCase()) || m.id.toLowerCase().includes(query.toLowerCase())));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'space-between',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 'var(--text-2xl)',
      fontWeight: 700,
      color: '#fff'
    }
  }, "Molecules"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-sm)',
      marginTop: 4
    }
  }, "SARA molecule library \u2014 30 molecules across aging states, GAFF2 / AM1-BCC parameterized.")), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    icon: I.Plus
  }, "New molecule")), /*#__PURE__*/React.createElement(Card, {
    padded: false
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '14px 16px',
      borderBottom: '1px solid var(--border)',
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      width: 280
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      left: 10,
      top: '50%',
      transform: 'translateY(-50%)',
      color: 'var(--text-muted)',
      display: 'flex'
    }
  }, /*#__PURE__*/React.createElement(I.Search, {
    size: 16
  })), /*#__PURE__*/React.createElement("input", {
    value: query,
    onChange: e => setQuery(e.target.value),
    placeholder: "Search molecules or IDs\u2026",
    style: {
      width: '100%',
      padding: '0.5rem 0.75rem 0.5rem 2rem',
      background: 'var(--surface-input)',
      border: '1px solid var(--border-light)',
      borderRadius: 'var(--radius-md)',
      color: '#fff',
      fontSize: 'var(--text-sm)',
      fontFamily: 'var(--font-sans)',
      outline: 'none'
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 6,
      flexWrap: 'wrap'
    }
  }, cats.map(c => /*#__PURE__*/React.createElement("button", {
    key: c,
    onClick: () => setFilter(c),
    style: {
      padding: '5px 12px',
      borderRadius: 'var(--radius-full)',
      fontSize: 'var(--text-xs)',
      fontWeight: 500,
      cursor: 'pointer',
      textTransform: 'capitalize',
      transition: 'all var(--duration-base)',
      border: '1px solid',
      borderColor: filter === c ? 'var(--primary-500)' : 'var(--border-light)',
      background: filter === c ? 'rgba(51,119,255,0.15)' : 'transparent',
      color: filter === c ? 'var(--primary-400)' : 'var(--text-secondary)'
    }
  }, c))), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 'auto',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-mono)'
    }
  }, rows.length, " / ", MOLECULES.length)), /*#__PURE__*/React.createElement("div", {
    style: {
      maxHeight: 420,
      overflowY: 'auto'
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      width: '100%',
      fontSize: 'var(--text-sm)',
      borderCollapse: 'collapse'
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      color: 'var(--text-secondary)',
      textAlign: 'left'
    }
  }, ['Molecule', 'mol_id', 'Family', 'MW', 'Aging', 'FF status'].map(h => /*#__PURE__*/React.createElement("th", {
    key: h,
    style: {
      padding: '10px 16px',
      fontWeight: 500,
      position: 'sticky',
      top: 0,
      background: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border)'
    }
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, rows.map(m => /*#__PURE__*/React.createElement("tr", {
    key: m.id,
    style: {
      borderTop: '1px solid rgba(51,65,85,0.4)'
    },
    onMouseEnter: e => e.currentTarget.style.background = 'rgba(30,41,59,0.5)',
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px',
      color: '#fff',
      fontWeight: 500
    }
  }, m.name), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-secondary)'
    }
  }, m.id), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px'
    }
  }, /*#__PURE__*/React.createElement(CategoryBadge, {
    category: m.sara
  })), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px',
      fontFamily: 'var(--font-mono)',
      color: '#cbd5e1'
    }
  }, m.mw.toFixed(1)), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: AGING_TONE[m.aging],
    size: "sm"
  }, AGING_LABELS[m.aging])), /*#__PURE__*/React.createElement("td", {
    style: {
      padding: '11px 16px'
    }
  }, /*#__PURE__*/React.createElement(StatusBadge, {
    status: m.ff === 'ready' ? 'ready' : 'building',
    size: "sm",
    showIcon: true
  })))))))));
}
window.MoleculesScreen = MoleculesScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/MoleculesScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/Sidebar.jsx
try { (() => {
// NACMID UI kit — fixed left sidebar with grouped nav + active state.
function KitSidebar({
  active,
  onNavigate
}) {
  const I = window.NIcon;
  const {
    ChevronRight
  } = I;
  const items = [{
    type: 'group',
    label: 'AI Agent'
  }, {
    key: 'mlops',
    icon: I.Cpu,
    label: 'MLOps',
    level: 1
  }, {
    key: 'inverse',
    icon: I.Target,
    label: 'Inverse Design',
    level: 1
  }, {
    key: 'binder',
    icon: I.FlaskConical,
    label: 'Binder Analysis',
    level: 1
  }, {
    type: 'group',
    label: 'Database'
  }, {
    key: 'molecules',
    icon: I.Atom,
    label: 'Molecules',
    level: 1
  }, {
    key: 'cells',
    icon: I.Droplets,
    label: 'Binder Cells',
    level: 1
  }, {
    key: 'interface',
    icon: I.TestTubes,
    label: 'Interface Molecules',
    level: 1
  }, {
    key: 'crystal',
    icon: I.Gem,
    label: 'Crystal Structures',
    level: 1
  }, {
    key: 'layered',
    icon: I.Layers,
    label: 'Layered Structures',
    level: 1
  }, {
    type: 'group',
    label: 'Analysis'
  }, {
    key: 'analysis',
    icon: I.BarChart3,
    label: 'Analysis',
    level: 1
  }, {
    type: 'group',
    label: 'Dynamics'
  }, {
    key: 'dashboard',
    icon: I.LayoutDashboard,
    label: 'Dashboard',
    level: 1
  }, {
    type: 'subgroup',
    label: 'Single Job'
  }, {
    key: 'sj-mol',
    icon: I.Atom,
    label: 'Single Molecule',
    level: 2
  }, {
    key: 'sj-cell',
    icon: I.Droplets,
    label: 'Binder Cell',
    level: 2
  }, {
    type: 'subgroup',
    label: 'Batch Job'
  }, {
    key: 'bj-mol',
    icon: I.Atom,
    label: 'Single Molecule',
    level: 2
  }, {
    key: 'bj-cell',
    icon: I.ListChecks,
    label: 'Binder Cell',
    level: 2
  }, {
    type: 'group',
    label: 'Settings'
  }, {
    key: 'settings',
    icon: I.Settings,
    label: 'Settings',
    level: 1
  }];
  let seenGroup = false;
  return /*#__PURE__*/React.createElement("aside", {
    style: {
      position: 'fixed',
      left: 0,
      top: 'var(--header-height)',
      bottom: 0,
      width: 'var(--sidebar-width)',
      background: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border)',
      overflowY: 'auto',
      padding: 16
    }
  }, /*#__PURE__*/React.createElement("nav", null, items.map((it, i) => {
    if (it.type === 'group') {
      const top = seenGroup;
      seenGroup = true;
      return /*#__PURE__*/React.createElement("div", {
        key: `g${i}`,
        style: {
          padding: '16px 16px 6px',
          fontSize: 'var(--text-xs)',
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-wide)',
          color: 'var(--primary-400)',
          marginTop: top ? 12 : 0,
          borderTop: top ? '1px solid var(--border)' : 'none'
        }
      }, it.label);
    }
    if (it.type === 'subgroup') {
      return /*#__PURE__*/React.createElement("div", {
        key: `s${i}`,
        style: {
          padding: '8px 32px 4px',
          fontSize: 11,
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: 'var(--tracking-wide)',
          color: 'var(--text-muted)'
        }
      }, it.label);
    }
    const Icon = it.icon;
    const on = active === it.key;
    const pad = it.level === 2 ? '10px 16px 10px 48px' : '10px 16px 10px 32px';
    return /*#__PURE__*/React.createElement("a", {
      key: it.key,
      onClick: () => onNavigate?.(it.key),
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        padding: pad,
        borderRadius: 'var(--radius-lg)',
        fontSize: 'var(--text-sm)',
        cursor: 'pointer',
        transition: 'all var(--duration-base) var(--ease-standard)',
        background: on ? 'var(--gradient-active)' : 'transparent',
        color: on ? '#fff' : 'var(--text-secondary)',
        borderLeft: on ? '2px solid var(--primary-500)' : '2px solid transparent'
      },
      onMouseEnter: e => {
        if (!on) {
          e.currentTarget.style.background = 'var(--bg-tertiary)';
          e.currentTarget.style.color = '#fff';
        }
      },
      onMouseLeave: e => {
        if (!on) {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--text-secondary)';
        }
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      size: 20,
      style: {
        color: on ? 'var(--primary-400)' : 'inherit',
        flexShrink: 0
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1
      }
    }, it.label), on && /*#__PURE__*/React.createElement(ChevronRight, {
      size: 16,
      style: {
        color: 'var(--primary-400)'
      }
    }));
  })));
}
window.KitSidebar = KitSidebar;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/Sidebar.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/icons.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
// NACMID UI kit — lucide-style inline icon components (stroke 2, round joins).
// Matches the product's lucide-react usage without an npm dependency.
const Svg = ({
  children,
  size = 20,
  style,
  strokeWidth = 2,
  ...rest
}) => /*#__PURE__*/React.createElement("svg", _extends({
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: strokeWidth,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  style: style
}, rest), children);
const LayoutDashboard = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "3",
  width: "7",
  height: "9",
  rx: "1"
}), /*#__PURE__*/React.createElement("rect", {
  x: "14",
  y: "3",
  width: "7",
  height: "5",
  rx: "1"
}), /*#__PURE__*/React.createElement("rect", {
  x: "14",
  y: "12",
  width: "7",
  height: "9",
  rx: "1"
}), /*#__PURE__*/React.createElement("rect", {
  x: "3",
  y: "16",
  width: "7",
  height: "5",
  rx: "1"
}));
const Atom = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "1"
}), /*#__PURE__*/React.createElement("path", {
  d: "M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"
}), /*#__PURE__*/React.createElement("path", {
  d: "M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z"
}));
const Layers = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("polygon", {
  points: "12 2 2 7 12 12 22 7 12 2"
}), /*#__PURE__*/React.createElement("polyline", {
  points: "2 17 12 22 22 17"
}), /*#__PURE__*/React.createElement("polyline", {
  points: "2 12 12 17 22 12"
}));
const Droplets = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 4.7 7 3c-.29 1.7-1.14 3.13-2.29 4.06S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05Z"
}), /*#__PURE__*/React.createElement("path", {
  d: "M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6 6 0 0 1-11.91 1"
}));
const Gem = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M6 3h12l4 6-10 13L2 9Z"
}), /*#__PURE__*/React.createElement("path", {
  d: "M11 3 8 9l4 13 4-13-3-6"
}), /*#__PURE__*/React.createElement("path", {
  d: "M2 9h20"
}));
const FlaskConical = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M10 2v7.31"
}), /*#__PURE__*/React.createElement("path", {
  d: "M14 9.3V1.99"
}), /*#__PURE__*/React.createElement("path", {
  d: "M8.5 2h7"
}), /*#__PURE__*/React.createElement("path", {
  d: "M14 9.3a6.5 6.5 0 1 1-4 0"
}), /*#__PURE__*/React.createElement("path", {
  d: "M5.58 16.5h12.85"
}));
const Target = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "10"
}), /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "6"
}), /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "2"
}));
const Cpu = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("rect", {
  x: "4",
  y: "4",
  width: "16",
  height: "16",
  rx: "2"
}), /*#__PURE__*/React.createElement("rect", {
  x: "9",
  y: "9",
  width: "6",
  height: "6"
}), /*#__PURE__*/React.createElement("path", {
  d: "M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"
}));
const BarChart3 = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M3 3v18h18"
}), /*#__PURE__*/React.createElement("path", {
  d: "M18 17V9"
}), /*#__PURE__*/React.createElement("path", {
  d: "M13 17V5"
}), /*#__PURE__*/React.createElement("path", {
  d: "M8 17v-3"
}));
const Settings = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2Z"
}), /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "3"
}));
const Bell = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"
}), /*#__PURE__*/React.createElement("path", {
  d: "M10.3 21a1.94 1.94 0 0 0 3.4 0"
}));
const ChevronRight = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("polyline", {
  points: "9 18 15 12 9 6"
}));
const Clock = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "10"
}), /*#__PURE__*/React.createElement("polyline", {
  points: "12 6 12 12 16 14"
}));
const Play = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("polygon", {
  points: "6 3 20 12 6 21 6 3",
  fill: "currentColor",
  stroke: "none"
}));
const CheckCircle = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M22 11.08V12a10 10 0 1 1-5.93-9.14"
}), /*#__PURE__*/React.createElement("polyline", {
  points: "22 4 12 14.01 9 11.01"
}));
const XCircle = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
  cx: "12",
  cy: "12",
  r: "10"
}), /*#__PURE__*/React.createElement("line", {
  x1: "15",
  y1: "9",
  x2: "9",
  y2: "15"
}), /*#__PURE__*/React.createElement("line", {
  x1: "9",
  y1: "9",
  x2: "15",
  y2: "15"
}));
const HardDrive = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("line", {
  x1: "22",
  y1: "12",
  x2: "2",
  y2: "12"
}), /*#__PURE__*/React.createElement("path", {
  d: "M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"
}), /*#__PURE__*/React.createElement("line", {
  x1: "6",
  y1: "16",
  x2: "6.01",
  y2: "16"
}), /*#__PURE__*/React.createElement("line", {
  x1: "10",
  y1: "16",
  x2: "10.01",
  y2: "16"
}));
const Plus = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("line", {
  x1: "12",
  y1: "5",
  x2: "12",
  y2: "19"
}), /*#__PURE__*/React.createElement("line", {
  x1: "5",
  y1: "12",
  x2: "19",
  y2: "12"
}));
const Search = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
  cx: "11",
  cy: "11",
  r: "8"
}), /*#__PURE__*/React.createElement("line", {
  x1: "21",
  y1: "21",
  x2: "16.65",
  y2: "16.65"
}));
const ListChecks = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "m3 17 2 2 4-4"
}), /*#__PURE__*/React.createElement("path", {
  d: "m3 7 2 2 4-4"
}), /*#__PURE__*/React.createElement("path", {
  d: "M13 6h8M13 12h8M13 18h8"
}));
const TestTubes = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M9 2v17.5A2.5 2.5 0 0 1 6.5 22A2.5 2.5 0 0 1 4 19.5V2"
}), /*#__PURE__*/React.createElement("path", {
  d: "M20 2v17.5a2.5 2.5 0 0 1-2.5 2.5a2.5 2.5 0 0 1-2.5-2.5V2"
}), /*#__PURE__*/React.createElement("path", {
  d: "M3 2h7M14 2h7M9 16H4M20 16h-5"
}));
const Sparkles = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"
}));
const ArrowRight = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("line", {
  x1: "5",
  y1: "12",
  x2: "19",
  y2: "12"
}), /*#__PURE__*/React.createElement("polyline", {
  points: "12 5 19 12 12 19"
}));
const Beaker = p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
  d: "M4.5 3h15M6 3v16a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V3M6 14h12"
}));
Object.assign(window, {
  NIcon: {
    LayoutDashboard,
    Atom,
    Layers,
    Droplets,
    Gem,
    FlaskConical,
    Target,
    Cpu,
    BarChart3,
    Settings,
    Bell,
    ChevronRight,
    Clock,
    Play,
    CheckCircle,
    XCircle,
    HardDrive,
    Plus,
    Search,
    ListChecks,
    TestTubes,
    Sparkles,
    ArrowRight,
    Beaker
  }
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/icons.jsx", error: String((e && e.message) || e) }); }

// ui_kits/nacmid/mockData.js
try { (() => {
// NACMID UI kit — mock data approximating the real platform's domain objects.
const EXPERIMENTS = [{
  id: 'A1_X1_NA_none_293K_f32f00',
  binder: 'AAA1',
  additive: 'none',
  tier: 'screening',
  temp: 293,
  status: 'completed',
  progress: 100,
  density: 1.0182
}, {
  id: 'A1_X1_LA_SBS_3_7_313K_e54514',
  binder: 'AAA1',
  additive: 'SBS',
  tier: 'confirm',
  temp: 313,
  status: 'running',
  progress: 64,
  density: null
}, {
  id: 'A1_X1_LA_Graphine_273K_208da9',
  binder: 'AAA1',
  additive: 'Graphene',
  tier: 'screening',
  temp: 273,
  status: 'running',
  progress: 38,
  density: null
}, {
  id: 'M1_X3_LA_SiO2_293K_3507be',
  binder: 'AAM1',
  additive: 'SiO2',
  tier: 'viscosity',
  temp: 293,
  status: 'queued',
  progress: 0,
  density: null
}, {
  id: 'A1_X1_LA_Lignin_333K_3c0ef6',
  binder: 'AAA1',
  additive: 'Lignin',
  tier: 'screening',
  temp: 333,
  status: 'building',
  progress: 12,
  density: null
}, {
  id: 'K1_X1_NA_none_253K_14c85e',
  binder: 'AAK1',
  additive: 'none',
  tier: 'validation',
  temp: 253,
  status: 'failed',
  progress: 47,
  density: null
}, {
  id: 'A1_X1_LA_CNT_233K_4d8fea',
  binder: 'AAA1',
  additive: 'CNT',
  tier: 'screening',
  temp: 233,
  status: 'completed',
  progress: 100,
  density: 1.0461
}, {
  id: 'M1_X1_LA_Sasobit_373K_aac3e3',
  binder: 'AAM1',
  additive: 'Sasobit',
  tier: 'confirm',
  temp: 373,
  status: 'pending',
  progress: 0,
  density: null
}];
const QUEUE_STATS = {
  total: 1284,
  pending: 42,
  queued: 18,
  building: 6,
  running: 8,
  completed: 1166,
  failed: 44
};

// Density vs temperature series (g/cm3) for a couple binders
const DENSITY_SERIES = {
  AAA1: [{
    t: 233,
    d: 1.046
  }, {
    t: 253,
    d: 1.038
  }, {
    t: 273,
    d: 1.029
  }, {
    t: 293,
    d: 1.018
  }, {
    t: 313,
    d: 1.006
  }, {
    t: 333,
    d: 0.994
  }, {
    t: 373,
    d: 0.969
  }],
  SBS: [{
    t: 233,
    d: 1.039
  }, {
    t: 253,
    d: 1.031
  }, {
    t: 273,
    d: 1.022
  }, {
    t: 293,
    d: 1.012
  }, {
    t: 313,
    d: 1.001
  }, {
    t: 333,
    d: 0.990
  }, {
    t: 373,
    d: 0.966
  }]
};
const CED_BY_ADDITIVE = [{
  additive: 'none',
  ced: 372
}, {
  additive: 'SBS',
  ced: 401
}, {
  additive: 'SiO2',
  ced: 388
}, {
  additive: 'CNT',
  ced: 412
}, {
  additive: 'Lignin',
  ced: 379
}, {
  additive: 'Sasobit',
  ced: 365
}];
const GPUS = [{
  id: 'GPU 0',
  name: 'H200',
  util: 96,
  mem: 71,
  job: 'A1_X1_LA_SBS_3_7_313K'
}, {
  id: 'GPU 1',
  name: 'H200',
  util: 88,
  mem: 64,
  job: 'A1_X1_LA_Graphine_273K'
}, {
  id: 'GPU 2',
  name: 'H200',
  util: 0,
  mem: 4,
  job: null
}];
const MOLECULES = [{
  id: 'U-SA-Squalane-0293',
  name: 'Squalane',
  sara: 'saturate',
  mw: 422.8,
  aging: 'non_aging',
  ff: 'ready'
}, {
  id: 'U-AR-PHENANTH-0293',
  name: 'Phenanthrene',
  sara: 'aromatic',
  mw: 178.2,
  aging: 'non_aging',
  ff: 'ready'
}, {
  id: 'S-AR-DOCHN-0293',
  name: 'Dioctyl-cyclohexane-naphthalene',
  sara: 'aromatic',
  mw: 406.7,
  aging: 'short_aging',
  ff: 'ready'
}, {
  id: 'U-RE-Thio-0293',
  name: 'Thiophene resin',
  sara: 'resin',
  mw: 354.6,
  aging: 'non_aging',
  ff: 'ready'
}, {
  id: 'L-AS-Asphaltene-0293',
  name: 'Asphaltene (PAV)',
  sara: 'asphaltene',
  mw: 575.0,
  aging: 'long_aging',
  ff: 'ready'
}, {
  id: 'U-AS-Violanthrone-0293',
  name: 'Violanthrone-78',
  sara: 'asphaltene',
  mw: 887.3,
  aging: 'non_aging',
  ff: 'building'
}, {
  id: 'U-AD-SBS-0293',
  name: 'SBS copolymer',
  sara: 'additive',
  mw: 642.1,
  aging: 'non_aging',
  ff: 'ready'
}, {
  id: 'U-AD-SiO2-0293',
  name: 'Silica nanoparticle',
  sara: 'additive',
  mw: 240.3,
  aging: 'non_aging',
  ff: 'ready'
}];
const AGING_LABELS = {
  non_aging: 'U · Virgin',
  short_aging: 'S · RTFOT',
  long_aging: 'L · PAV'
};
const AGING_TONE = {
  non_aging: 'blue',
  short_aging: 'amber',
  long_aging: 'rose'
};

// Inverse design plan preview
const PLAN_CANDIDATES = [{
  rank: 0,
  additive: 'SBS',
  wt: 4.5,
  score: 0.91,
  sara: {
    asphaltene: 18,
    resin: 32,
    aromatic: 38,
    saturate: 12
  },
  pred: {
    work_of_separation: 64.2,
    viscosity: 158
  }
}, {
  rank: 1,
  additive: 'CNT',
  wt: 1.8,
  score: 0.84,
  sara: {
    asphaltene: 20,
    resin: 30,
    aromatic: 36,
    saturate: 14
  },
  pred: {
    work_of_separation: 61.0,
    viscosity: 171
  }
}, {
  rank: 2,
  additive: 'SiO2',
  wt: 3.2,
  score: 0.77,
  sara: {
    asphaltene: 17,
    resin: 34,
    aromatic: 37,
    saturate: 12
  },
  pred: {
    work_of_separation: 58.4,
    viscosity: 149
  }
}];
const PLAN_DOE = [{
  kind: 'binder cell',
  aggregate: '—',
  temp: 293,
  tier: 'screening',
  replica: 1,
  dep: '—',
  action: 'build'
}, {
  kind: 'binder cell',
  aggregate: '—',
  temp: 313,
  tier: 'confirm',
  replica: 1,
  dep: '—',
  action: 'reuse'
}, {
  kind: 'layered tensile',
  aggregate: 'SiO2',
  temp: 293,
  tier: 'screening',
  replica: 3,
  dep: 'binder #1',
  action: 'build'
}, {
  kind: 'layered tensile',
  aggregate: 'CaCO3',
  temp: 293,
  tier: 'screening',
  replica: 3,
  dep: 'binder #1',
  action: 'build'
}];
Object.assign(window, {
  NData: {
    EXPERIMENTS,
    QUEUE_STATS,
    DENSITY_SERIES,
    CED_BY_ADDITIVE,
    GPUS,
    MOLECULES,
    AGING_LABELS,
    AGING_TONE,
    PLAN_CANDIDATES,
    PLAN_DOE
  }
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/nacmid/mockData.js", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.CategoryBadge = __ds_scope.CategoryBadge;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.ScoreBar = __ds_scope.ScoreBar;

__ds_ns.StatusBadge = __ds_scope.StatusBadge;

__ds_ns.TierBadge = __ds_scope.TierBadge;

__ds_ns.StatCard = __ds_scope.StatCard;

__ds_ns.Tabs = __ds_scope.Tabs;

})();
