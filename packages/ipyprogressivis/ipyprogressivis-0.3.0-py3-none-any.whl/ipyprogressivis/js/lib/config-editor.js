'use strict';

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.register_config_editor = register_config_editor;
var _react = _interopRequireDefault(require("react"));
var _propTypes = _interopRequireDefault(require("prop-types"));
var _reactDom = _interopRequireDefault(require("react-dom"));
var _es6ElementReady = require("./es6-element-ready");
var _jquery = _interopRequireDefault(require("jquery"));
function _interopRequireDefault(e) { return e && e.__esModule ? e : { "default": e }; }
function _classCallCheck(a, n) { if (!(a instanceof n)) throw new TypeError("Cannot call a class as a function"); }
function _defineProperties(e, r) { for (var t = 0; t < r.length; t++) { var o = r[t]; o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, _toPropertyKey(o.key), o); } }
function _createClass(e, r, t) { return r && _defineProperties(e.prototype, r), t && _defineProperties(e, t), Object.defineProperty(e, "prototype", { writable: !1 }), e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _callSuper(t, o, e) { return o = _getPrototypeOf(o), _possibleConstructorReturn(t, _isNativeReflectConstruct() ? Reflect.construct(o, e || [], _getPrototypeOf(t).constructor) : o.apply(t, e)); }
function _possibleConstructorReturn(t, e) { if (e && ("object" == _typeof(e) || "function" == typeof e)) return e; if (void 0 !== e) throw new TypeError("Derived constructors may only return object or undefined"); return _assertThisInitialized(t); }
function _assertThisInitialized(e) { if (void 0 === e) throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); return e; }
function _isNativeReflectConstruct() { try { var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); } catch (t) {} return (_isNativeReflectConstruct = function _isNativeReflectConstruct() { return !!t; })(); }
function _getPrototypeOf(t) { return _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function (t) { return t.__proto__ || Object.getPrototypeOf(t); }, _getPrototypeOf(t); }
function _inherits(t, e) { if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function"); t.prototype = Object.create(e && e.prototype, { constructor: { value: t, writable: !0, configurable: !0 } }), Object.defineProperty(t, "prototype", { writable: !1 }), e && _setPrototypeOf(t, e); }
function _setPrototypeOf(t, e) { return _setPrototypeOf = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function (t, e) { return t.__proto__ = e, t; }, _setPrototypeOf(t, e); }
function getOnly(dict, keys) {
  var res = {};
  keys.forEach(function (e) {
    res[e] = dict[e];
  });
  return res;
}
function renderSelect(val, opts, chg) {
  return /*#__PURE__*/_react["default"].createElement("select", {
    value: val,
    onChange: chg
  }, Object.keys(opts).map(function (k) {
    return /*#__PURE__*/_react["default"].createElement("option", {
      key: k,
      value: k
    }, opts[k]);
  }));
}
function renderHeader(title, label, dict, val, handler) {
  return /*#__PURE__*/_react["default"].createElement("tbody", {
    key: title
  }, /*#__PURE__*/_react["default"].createElement("tr", null, /*#__PURE__*/_react["default"].createElement("td", {
    colSpan: "2"
  }, /*#__PURE__*/_react["default"].createElement("h3", null, title))), /*#__PURE__*/_react["default"].createElement("tr", null, /*#__PURE__*/_react["default"].createElement("td", null, /*#__PURE__*/_react["default"].createElement("label", null, label, "\xA0")), /*#__PURE__*/_react["default"].createElement("td", null, renderSelect(val, dict, handler))));
}
function renderNamedSelect(label, dict, val, handler) {
  return /*#__PURE__*/_react["default"].createElement("tbody", {
    key: label
  }, /*#__PURE__*/_react["default"].createElement("tr", null, /*#__PURE__*/_react["default"].createElement("td", null, /*#__PURE__*/_react["default"].createElement("label", null, label, "\xA0")), /*#__PURE__*/_react["default"].createElement("td", null, renderSelect(val, dict, handler))));
}
function renderInput(label, type, name, val, handler) {
  return /*#__PURE__*/_react["default"].createElement("tbody", {
    key: name
  }, /*#__PURE__*/_react["default"].createElement("tr", null, /*#__PURE__*/_react["default"].createElement("td", null, /*#__PURE__*/_react["default"].createElement("label", null, label, "\xA0")), /*#__PURE__*/_react["default"].createElement("td", null, /*#__PURE__*/_react["default"].createElement("input", {
    value: val,
    name: name,
    type: type,
    onChange: handler
  }))));
}
var Rebin = /*#__PURE__*/function (_React$Component) {
  function Rebin(props) {
    var _this;
    _classCallCheck(this, Rebin);
    _this = _callSuper(this, Rebin, [props]);
    _this.handleChange = _this.handleChange.bind(_this);
    return _this;
  }
  _inherits(Rebin, _React$Component);
  return _createClass(Rebin, [{
    key: "handleChange",
    value: function handleChange(key) {
      var _this2 = this;
      return function (val) {
        _this2.props.handleChange(key, val);
      };
    }
  }, {
    key: "render",
    value: function render() {
      var typeDict = {
        none: 'None',
        square: 'Square',
        rect: 'Rect',
        voronoi: 'Voronoi'
      };
      var rebinType = this.props.value['type'];
      var res = [renderHeader('Rebin', 'Type', typeDict, rebinType, this.handleChange('type'))];
      if (rebinType == 'none') return /*#__PURE__*/_react["default"].createElement(_react["default"].Fragment, null, res);
      var aggrDict = {
        max: 'Max',
        mean: 'Mean',
        sum: 'Sum',
        min: 'Min'
      };
      res.push(renderNamedSelect('Aggregate', aggrDict, this.props.value['aggregation'], this.handleChange('aggregation')));
      if (rebinType == 'square') {
        res.push(renderInput('Size', 'number', 'rebinSize', this.props.value['size'], this.handleChange('size')));
      }
      if (rebinType == 'rect') {
        res.push(renderInput('Width', 'number', 'rebinWidth', this.props.value['width'], this.handleChange('width')));
        res.push(renderInput('Height', 'number', 'rebinHeight', this.props.value['height'], this.handleChange('height')));
      }
      if (rebinType == 'voronoi') {
        res.push(renderInput('Size', 'number', 'rebinSize', this.props.value['size'], this.handleChange('size')));
        res.push(renderInput('Stroke', 'text', 'rebinStroke', this.props.value['stroke'], this.handleChange('stroke')));
      }
      return /*#__PURE__*/_react["default"].createElement(_react["default"].Fragment, null, res);
    }
  }]);
}(_react["default"].Component);
Rebin.propTypes = {
  handleChange: _propTypes["default"].func,
  value: _propTypes["default"].any
};
var Rescale = /*#__PURE__*/function (_React$Component2) {
  function Rescale(props) {
    var _this3;
    _classCallCheck(this, Rescale);
    _this3 = _callSuper(this, Rescale, [props]);
    _this3.handleChange = _this3.handleChange.bind(_this3);
    return _this3;
  }
  _inherits(Rescale, _React$Component2);
  return _createClass(Rescale, [{
    key: "handleChange",
    value: function handleChange(key) {
      var _this4 = this;
      return function (val) {
        _this4.props.handleChange(key, val);
      };
    }
  }, {
    key: "render",
    value: function render() {
      var typeDict = {
        linear: 'Linear',
        log: 'Log',
        sqrt: 'Square Root',
        cbrt: 'Cubic Root',
        equidepth: 'Equi-depth'
      };
      var rescaleType = this.props.value['type'];
      var res = [renderHeader('Rescale', 'Type', typeDict, rescaleType, this.handleChange('type'))];
      if (rescaleType == 'equidepth') {
        res.push(renderInput('Size', 'number', 'rescaleLevels', this.props.value['levels'], this.handleChange('levels')));
      }
      return /*#__PURE__*/_react["default"].createElement(_react["default"].Fragment, null, res);
    }
  }]);
}(_react["default"].Component);
Rescale.propTypes = {
  handleChange: _propTypes["default"].func,
  value: _propTypes["default"].any
};
var Compose = /*#__PURE__*/function (_React$Component3) {
  function Compose(props) {
    var _this5;
    _classCallCheck(this, Compose);
    _this5 = _callSuper(this, Compose, [props]);
    _this5.handleChange = _this5.handleChange.bind(_this5);
    return _this5;
  }
  _inherits(Compose, _React$Component3);
  return _createClass(Compose, [{
    key: "handleChange",
    value: function handleChange(key) {
      var _this6 = this;
      return function (val) {
        _this6.props.handleChange(key, val);
      };
    }
  }, {
    key: "render",
    value: function render() {
      var compDict = {
        none: 'none',
        invmin: 'Invmin',
        mean: 'Mean',
        max: 'Max',
        blend: 'Blend',
        weaving: 'Weaving',
        /*propline: "Propline", hatching: "Hatching",*/
        separate: 'Separate',
        glyph: 'Glyph',
        dotdensity: 'Dotdensity',
        time: 'Time'
      };
      var compValue = this.props.value['mix'];
      var res = [renderHeader('Compose', 'Mix', compDict, compValue, this.handleChange('mix'))];
      if (compValue in ['none', 'mean', 'max', 'separate']) return /*#__PURE__*/_react["default"].createElement(_react["default"].Fragment, null, res);
      if (compValue == 'invmin') {
        res.push(renderInput('Threshold', 'number', 'compThreshold', this.props.value['threshold'], this.handleChange('threshold')));
      }
      if (compValue == 'blend') {
        var mixingDict = {
          additive: 'Additive',
          multiplicative: 'Multiplicative'
        };
        res.push(renderNamedSelect('Mixing', mixingDict, this.props.value['mixing'], this.handleChange('mixing')));
      }
      if (compValue == 'weaving') {
        var weavingDict = {
          square: 'Square',
          random: 'Random',
          hexagon: 'Hexagon',
          triangle: 'Triangle'
        };
        res.push(renderNamedSelect('Weaving', weavingDict, this.props.value['weaving'], this.handleChange('weaving')));
        res.push(renderInput('Size', 'number', 'compSize', this.props.value['size'], this.handleChange('size')));
      }
      if (compValue == 'glyph') {
        var templDict = {
          punchcard: 'punchcard',
          bars: 'bars'
        };
        res.push(renderNamedSelect('Template', templDict, this.props.value['template'], this.handleChange('glyph')));
        res.push(renderInput('Width', 'number', 'compWidth', this.props.value['width'], this.handleChange('width')));
        res.push(renderInput('Height', 'number', 'compHeight', this.props.value['height'], this.handleChange('height')));
      }
      if (compValue == 'dotdensity') {
        res.push(renderInput('Size', 'number', 'compSize', this.props.value['size'], this.handleChange('size')));
      }
      if (compValue == 'time') {
        res.push(renderInput('Interval(s)', 'number', 'compInterval', this.props.value['interval'], this.handleChange('interval')));
      }
      return /*#__PURE__*/_react["default"].createElement(_react["default"].Fragment, null, res);
    }
  }]);
}(_react["default"].Component);
Compose.propTypes = {
  handleChange: _propTypes["default"].func,
  value: _propTypes["default"].any
};
var ConfigForm = /*#__PURE__*/function (_React$Component4) {
  function ConfigForm(props) {
    var _this7;
    _classCallCheck(this, ConfigForm);
    _this7 = _callSuper(this, ConfigForm, [props]);
    _this7.handleRebin = _this7.handleRebin.bind(_this7);
    _this7.handleRescale = _this7.handleRescale.bind(_this7);
    _this7.handleCompose = _this7.handleCompose.bind(_this7);
    _this7.handleGrp = _this7.handleGrp.bind(_this7);
    _this7.tidy = _this7.tidy.bind(_this7);
    _this7.state = {
      rebin: {
        type: 'none',
        aggregation: 'max',
        size: 4,
        width: 4,
        height: 4,
        stroke: 'rgba(0, 0, 0, .1)'
      },
      rescale: {
        type: 'cbrt',
        levels: 4
      },
      compose: {
        mix: 'max',
        threshold: 1,
        size: 8,
        width: 32,
        height: 32,
        mixing: 'additive',
        shape: 'square',
        template: 'punchcard',
        interval: 0.6
      },
      data: {},
      legend: true
    };
    return _this7;
  }
  _inherits(ConfigForm, _React$Component4);
  return _createClass(ConfigForm, [{
    key: "handleGrp",
    value: function handleGrp(grp, key, evt) {
      var stateCopy = Object.assign({}, this.state);
      stateCopy[grp][key] = evt.target.value;
      this.setState(stateCopy);
      window.spec = this.tidy(Object.assign({}, stateCopy));
    }
  }, {
    key: "handleRebin",
    value: function handleRebin(key, val) {
      return this.handleGrp('rebin', key, val);
    }
  }, {
    key: "handleRescale",
    value: function handleRescale(key, val) {
      return this.handleGrp('rescale', key, val);
    }
  }, {
    key: "handleCompose",
    value: function handleCompose(key, val) {
      return this.handleGrp('compose', key, val);
    }
  }, {
    key: "renderRebin",
    value: function renderRebin() {
      return /*#__PURE__*/_react["default"].createElement(Rebin, {
        value: this.state.rebin,
        handleChange: this.handleRebin
      });
    }
  }, {
    key: "renderRescale",
    value: function renderRescale() {
      return /*#__PURE__*/_react["default"].createElement(Rescale, {
        value: this.state.rescale,
        handleChange: this.handleRescale
      });
    }
  }, {
    key: "renderCompose",
    value: function renderCompose() {
      return /*#__PURE__*/_react["default"].createElement(Compose, {
        value: this.state.compose,
        handleChange: this.handleCompose
      });
    }
  }, {
    key: "tidy",
    value: function tidy() {
      var stateCopy = Object.assign({}, this.state);
      // Rebin
      if (stateCopy.rebin.type == 'none') stateCopy.rebin = {
        type: 'none'
      };
      if (stateCopy.rebin.type == 'rect') stateCopy.rebin = getOnly(stateCopy.rebin, ['type', 'aggregation', 'width', 'height']);
      if (stateCopy.rebin.type == 'square') stateCopy.rebin = getOnly(stateCopy.rebin, ['type', 'aggregation', 'size']);
      if (stateCopy.rebin.type == 'voronoi') stateCopy.rebin = getOnly(stateCopy.rebin, ['type', 'aggregation', 'size', 'stroke']);
      // Rescale
      if (stateCopy.rescale.type != 'equidepth') stateCopy.rescale = getOnly(stateCopy.rescale, ['type']);
      // Compose
      if (stateCopy.compose.mix in ['none', 'mean', 'max', 'separate']) stateCopy.compose = getOnly(stateCopy.compose, ['mix']);
      if (stateCopy.compose.mix == 'invmean') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'threshold']);
      if (stateCopy.compose.mix == 'blend') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'mixing']);
      if (stateCopy.compose.mix == 'weaving') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'size']);
      if (stateCopy.compose.mix == 'glyph') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'template', 'width', 'height']);
      if (stateCopy.compose.mix == 'dotdensity') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'size']);
      if (stateCopy.compose.mix == 'time') stateCopy.compose = getOnly(stateCopy.compose, ['mix', 'interval']);
      return stateCopy;
    }
  }, {
    key: "render",
    value: function render() {
      window.spec = this.tidy();
      return /*#__PURE__*/_react["default"].createElement("form", {
        id: "editform"
      }, /*#__PURE__*/_react["default"].createElement("table", null, this.renderRebin(), this.renderRescale(), this.renderCompose()), /*#__PURE__*/_react["default"].createElement("div", {
        hidden: true
      }, JSON.stringify(this.tidy())));
    }
  }]);
}(_react["default"].Component);
function register_config_editor(id) {
  // Change this code to a toplevel function to configure the component
  (0, _es6ElementReady.elementReady)('#root_' + id).then(function () {
    _reactDom["default"].render(/*#__PURE__*/_react["default"].createElement(ConfigForm, null), document.getElementById('root_' + id));
  });

  // adding Configure button
  (0, _es6ElementReady.elementReady)('#mdm-form_' + id).then(function () {
    //console.log("Config button", $("#config-btn"));
    (0, _jquery["default"])('#config-btn_' + id).click(function () {
      var sty = (0, _jquery["default"])('#mdm-form_' + id).css('display');
      var newSty = sty == 'none' ? 'block' : 'none';
      var txt = newSty == 'none' ? 'Configure...' : 'Close props editor';
      (0, _jquery["default"])('#mdm-form_' + id).css('display', newSty);
      (0, _jquery["default"])('#config-btn_' + id).text(txt);
    });
  });
}