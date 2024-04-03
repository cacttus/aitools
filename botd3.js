
'use strict';



/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global global, define, System, Reflect, Promise */
var __extends;
var __assign;
var __rest;
var __decorate;
var __param;
var __esDecorate;
var __runInitializers;
var __propKey;
var __setFunctionName;
var __metadata;
var __awaiter;
var __generator;
var __exportStar;
var __values;
var __read;
var __spread;
var __spreadArrays;
var __spreadArray;
var __await;
var __asyncGenerator;
var __asyncDelegator;
var __asyncValues;
var __makeTemplateObject;
var __importStar;
var __importDefault;
var __classPrivateFieldGet;
var __classPrivateFieldSet;
var __classPrivateFieldIn;
var __createBinding;
(function (factory) {
    var root = typeof global === "object" ? global : typeof self === "object" ? self : typeof this === "object" ? this : {};
    if (typeof define === "function" && define.amd) {
        define("tslib", ["exports"], function (exports) { factory(createExporter(root, createExporter(exports))); });
    }
    else if (typeof module === "object" && typeof module.exports === "object") {
        factory(createExporter(root, createExporter(module.exports)));
    }
    else {
        factory(createExporter(root));
    }
    function createExporter(exports, previous) {
        if (exports !== root) {
            if (typeof Object.create === "function") {
                Object.defineProperty(exports, "__esModule", { value: true });
            }
            else {
                exports.__esModule = true;
            }
        }
        return function (id, v) { return exports[id] = previous ? previous(id, v) : v; };
    }
})()
(function (exporter) {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };

    __extends = function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };

    __assign = Object.assign || function (t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };

    __rest = function (s, e) {
        var t = {};
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
            t[p] = s[p];
        if (s != null && typeof Object.getOwnPropertySymbols === "function")
            for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
                if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                    t[p[i]] = s[p[i]];
            }
        return t;
    };

    __decorate = function (decorators, target, key, desc) {
        var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
        if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
        else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
        return c > 3 && r && Object.defineProperty(target, key, r), r;
    };

    __param = function (paramIndex, decorator) {
        return function (target, key) { decorator(target, key, paramIndex); }
    };

    __esDecorate = function (ctor, descriptorIn, decorators, contextIn, initializers, extraInitializers) {
        function accept(f) { if (f !== void 0 && typeof f !== "function") throw new TypeError("Function expected"); return f; }
        var kind = contextIn.kind, key = kind === "getter" ? "get" : kind === "setter" ? "set" : "value";
        var target = !descriptorIn && ctor ? contextIn["static"] ? ctor : ctor.prototype : null;
        var descriptor = descriptorIn || (target ? Object.getOwnPropertyDescriptor(target, contextIn.name) : {});
        var _, done = false;
        for (var i = decorators.length - 1; i >= 0; i--) {
            var context = {};
            for (var p in contextIn) context[p] = p === "access" ? {} : contextIn[p];
            for (var p in contextIn.access) context.access[p] = contextIn.access[p];
            context.addInitializer = function (f) { if (done) throw new TypeError("Cannot add initializers after decoration has completed"); extraInitializers.push(accept(f || null)); };
            var result = (0, decorators[i])(kind === "accessor" ? { get: descriptor.get, set: descriptor.set } : descriptor[key], context);
            if (kind === "accessor") {
                if (result === void 0) continue;
                if (result === null || typeof result !== "object") throw new TypeError("Object expected");
                if (_ = accept(result.get)) descriptor.get = _;
                if (_ = accept(result.set)) descriptor.set = _;
                if (_ = accept(result.init)) initializers.unshift(_);
            }
            else if (_ = accept(result)) {
                if (kind === "field") initializers.unshift(_);
                else descriptor[key] = _;
            }
        }
        if (target) Object.defineProperty(target, contextIn.name, descriptor);
        done = true;
    };

    __runInitializers = function (thisArg, initializers, value) {
        var useValue = arguments.length > 2;
        for (var i = 0; i < initializers.length; i++) {
            value = useValue ? initializers[i].call(thisArg, value) : initializers[i].call(thisArg);
        }
        return useValue ? value : void 0;
    };

    __propKey = function (x) {
        return typeof x === "symbol" ? x : "".concat(x);
    };

    __setFunctionName = function (f, name, prefix) {
        if (typeof name === "symbol") name = name.description ? "[".concat(name.description, "]") : "";
        return Object.defineProperty(f, "name", { configurable: true, value: prefix ? "".concat(prefix, " ", name) : name });
    };

    __metadata = function (metadataKey, metadataValue) {
        if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(metadataKey, metadataValue);
    };

    __awaiter = function (thisArg, _arguments, P, generator) {
        function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
        return new (P || (P = Promise))(function (resolve, reject) {
            function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
            function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
            function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
            step((generator = generator.apply(thisArg, _arguments || [])).next());
        });
    };

    __generator = function (thisArg, body) {
        var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
        return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
        function verb(n) { return function (v) { return step([n, v]); }; }
        function step(op) {
            if (f) throw new TypeError("Generator is already executing.");
            while (g && (g = 0, op[0] && (_ = 0)), _) try {
                if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
                if (y = 0, t) op = [op[0] & 2, t.value];
                switch (op[0]) {
                    case 0: case 1: t = op; break;
                    case 4: _.label++; return { value: op[1], done: false };
                    case 5: _.label++; y = op[1]; op = [0]; continue;
                    case 7: op = _.ops.pop(); _.trys.pop(); continue;
                    default:
                        if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                        if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                        if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                        if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                        if (t[2]) _.ops.pop();
                        _.trys.pop(); continue;
                }
                op = body.call(thisArg, _);
            } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
            if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
        }
    };

    __exportStar = function(m, o) {
        for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(o, p)) __createBinding(o, m, p);
    };

    __createBinding = Object.create ? (function(o, m, k, k2) {
        if (k2 === undefined) k2 = k;
        var desc = Object.getOwnPropertyDescriptor(m, k);
        if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
            desc = { enumerable: true, get: function() { return m[k]; } };
        }
        Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
        if (k2 === undefined) k2 = k;
        o[k2] = m[k];
    });

    __values = function (o) {
        var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
        if (m) return m.call(o);
        if (o && typeof o.length === "number") return {
            next: function () {
                if (o && i >= o.length) o = void 0;
                return { value: o && o[i++], done: !o };
            }
        };
        throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
    };

    __read = function (o, n) {
        var m = typeof Symbol === "function" && o[Symbol.iterator];
        if (!m) return o;
        var i = m.call(o), r, ar = [], e;
        try {
            while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
        }
        catch (error) { e = { error: error }; }
        finally {
            try {
                if (r && !r.done && (m = i["return"])) m.call(i);
            }
            finally { if (e) throw e.error; }
        }
        return ar;
    };

    /** @deprecated */
    __spread = function () {
        for (var ar = [], i = 0; i < arguments.length; i++)
            ar = ar.concat(__read(arguments[i]));
        return ar;
    };

    /** @deprecated */
    __spreadArrays = function () {
        for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
        for (var r = Array(s), k = 0, i = 0; i < il; i++)
            for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
                r[k] = a[j];
        return r;
    };

    __spreadArray = function (to, from, pack) {
        if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
            if (ar || !(i in from)) {
                if (!ar) ar = Array.prototype.slice.call(from, 0, i);
                ar[i] = from[i];
            }
        }
        return to.concat(ar || Array.prototype.slice.call(from));
    };

    __await = function (v) {
        return this instanceof __await ? (this.v = v, this) : new __await(v);
    };

    __asyncGenerator = function (thisArg, _arguments, generator) {
        if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
        var g = generator.apply(thisArg, _arguments || []), i, q = [];
        return i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i;
        function verb(n) { if (g[n]) i[n] = function (v) { return new Promise(function (a, b) { q.push([n, v, a, b]) > 1 || resume(n, v); }); }; }
        function resume(n, v) { try { step(g[n](v)); } catch (e) { settle(q[0][3], e); } }
        function step(r) { r.value instanceof __await ? Promise.resolve(r.value.v).then(fulfill, reject) : settle(q[0][2], r);  }
        function fulfill(value) { resume("next", value); }
        function reject(value) { resume("throw", value); }
        function settle(f, v) { if (f(v), q.shift(), q.length) resume(q[0][0], q[0][1]); }
    };

    __asyncDelegator = function (o) {
        var i, p;
        return i = {}, verb("next"), verb("throw", function (e) { throw e; }), verb("return"), i[Symbol.iterator] = function () { return this; }, i;
        function verb(n, f) { i[n] = o[n] ? function (v) { return (p = !p) ? { value: __await(o[n](v)), done: false } : f ? f(v) : v; } : f; }
    };

    __asyncValues = function (o) {
        if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
        var m = o[Symbol.asyncIterator], i;
        return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
        function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
        function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
    };

    __makeTemplateObject = function (cooked, raw) {
        if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
        return cooked;
    };

    var __setModuleDefault = Object.create ? (function(o, v) {
        Object.defineProperty(o, "default", { enumerable: true, value: v });
    }) : function(o, v) {
        o["default"] = v;
    };

    __importStar = function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
        __setModuleDefault(result, mod);
        return result;
    };

    __importDefault = function (mod) {
        return (mod && mod.__esModule) ? mod : { "default": mod };
    };

    __classPrivateFieldGet = function (receiver, state, kind, f) {
        if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
        if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
        return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
    };

    __classPrivateFieldSet = function (receiver, state, value, kind, f) {
        if (kind === "m") throw new TypeError("Private method is not writable");
        if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
        if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
        return (kind === "a" ? f.call(receiver, value) : f ? f.value = value : state.set(receiver, value)), value;
    };

    __classPrivateFieldIn = function (state, receiver) {
        if (receiver === null || (typeof receiver !== "object" && typeof receiver !== "function")) throw new TypeError("Cannot use 'in' operator on non-object");
        return typeof state === "function" ? receiver === state : state.has(receiver);
    };

    exporter("__extends", __extends);
    exporter("__assign", __assign);
    exporter("__rest", __rest);
    exporter("__decorate", __decorate);
    exporter("__param", __param);
    exporter("__esDecorate", __esDecorate);
    exporter("__runInitializers", __runInitializers);
    exporter("__propKey", __propKey);
    exporter("__setFunctionName", __setFunctionName);
    exporter("__metadata", __metadata);
    exporter("__awaiter", __awaiter);
    exporter("__generator", __generator);
    exporter("__exportStar", __exportStar);
    exporter("__createBinding", __createBinding);
    exporter("__values", __values);
    exporter("__read", __read);
    exporter("__spread", __spread);
    exporter("__spreadArrays", __spreadArrays);
    exporter("__spreadArray", __spreadArray);
    exporter("__await", __await);
    exporter("__asyncGenerator", __asyncGenerator);
    exporter("__asyncDelegator", __asyncDelegator);
    exporter("__asyncValues", __asyncValues);
    exporter("__makeTemplateObject", __makeTemplateObject);
    exporter("__importStar", __importStar);
    exporter("__importDefault", __importDefault);
    exporter("__classPrivateFieldGet", __classPrivateFieldGet);
    exporter("__classPrivateFieldSet", __classPrivateFieldSet);
    exporter("__classPrivateFieldIn", __classPrivateFieldIn);
})();

var version = "1.6.0";

/**
 * Enum for the source state.
 *
 * @readonly
 * @enum {number}
 */
var State;
(function (State) {
    State[State["Success"] = 0] = "Success";
    State[State["Undefined"] = -1] = "Undefined";
    State[State["NotFunction"] = -2] = "NotFunction";
    State[State["UnexpectedBehaviour"] = -3] = "UnexpectedBehaviour";
    State[State["Null"] = -4] = "Null";
})(State || (State = {}));
/**
 * Enum for types of bots.
 * Specific types of bots come first, followed by automation technologies.
 *
 * @readonly
 * @enum {string}
 */
exports.BotKind = void 0;
(function (BotKind) {
    BotKind["Awesomium"] = "awesomium";
    BotKind["Cef"] = "cef";
    BotKind["CefSharp"] = "cefsharp";
    BotKind["CoachJS"] = "coachjs";
    BotKind["Electron"] = "electron";
    BotKind["FMiner"] = "fminer";
    BotKind["Geb"] = "geb";
    BotKind["NightmareJS"] = "nightmarejs";
    BotKind["Phantomas"] = "phantomas";
    BotKind["PhantomJS"] = "phantomjs";
    BotKind["Rhino"] = "rhino";
    BotKind["Selenium"] = "selenium";
    BotKind["Sequentum"] = "sequentum";
    BotKind["SlimerJS"] = "slimerjs";
    BotKind["WebDriverIO"] = "webdriverio";
    BotKind["WebDriver"] = "webdriver";
    BotKind["HeadlessChrome"] = "headless_chrome";
    BotKind["Unknown"] = "unknown";
})(exports.BotKind || (exports.BotKind = {}));
/**
 * Bot detection error.
 */
var BotdError = /** @class */ (function (_super) {
    tslib.__extends(BotdError, _super);
    /**
     * Creates a new BotdError.
     *
     * @class
     */
    function BotdError(state, message) {
        var _this = _super.call(this, message) || this;
        _this.state = state;
        _this.name = 'BotdError';
        Object.setPrototypeOf(_this, BotdError.prototype);
        return _this;
    }
    return BotdError;
}(Error));
var BrowserEngineKind;
(function (BrowserEngineKind) {
    BrowserEngineKind["Unknown"] = "unknown";
    BrowserEngineKind["Chromium"] = "chromium";
    BrowserEngineKind["Gecko"] = "gecko";
    BrowserEngineKind["Webkit"] = "webkit";
})(BrowserEngineKind || (BrowserEngineKind = {}));
var BrowserKind;
(function (BrowserKind) {
    BrowserKind["Unknown"] = "unknown";
    BrowserKind["Chrome"] = "chrome";
    BrowserKind["Firefox"] = "firefox";
    BrowserKind["Opera"] = "opera";
    BrowserKind["Safari"] = "safari";
    BrowserKind["IE"] = "internet_explorer";
    BrowserKind["WeChat"] = "wechat";
})(BrowserKind || (BrowserKind = {}));

function detectAppVersion(_a) {
    var appVersion = _a.appVersion;
    if (appVersion.state !== State.Success)
        return false;
    if (/headless/i.test(appVersion.value))
        return exports.BotKind.HeadlessChrome;
    if (/electron/i.test(appVersion.value))
        return exports.BotKind.Electron;
    if (/slimerjs/i.test(appVersion.value))
        return exports.BotKind.SlimerJS;
}

function arrayIncludes(arr, value) {
    return arr.indexOf(value) !== -1;
}
function strIncludes(str, value) {
    return str.indexOf(value) !== -1;
}
function arrayFind(array, callback) {
    if ('find' in array)
        return array.find(callback);
    for (var i = 0; i < array.length; i++) {
        if (callback(array[i], i, array))
            return array[i];
    }
    return undefined;
}

function getObjectProps(obj) {
    return Object.getOwnPropertyNames(obj);
}
function includes(arr) {
    var keys = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        keys[_i - 1] = arguments[_i];
    }
    var _loop_1 = function (key) {
        if (typeof key === 'string') {
            if (arrayIncludes(arr, key))
                return { value: true };
        }
        else {
            var match = arrayFind(arr, function (value) { return key.test(value); });
            if (match != null)
                return { value: true };
        }
    };
    for (var _a = 0, keys_1 = keys; _a < keys_1.length; _a++) {
        var key = keys_1[_a];
        var state_1 = _loop_1(key);
        if (typeof state_1 === "object")
            return state_1.value;
    }
    return false;
}
function countTruthy(values) {
    return values.reduce(function (sum, value) { return sum + (value ? 1 : 0); }, 0);
}

function detectDocumentAttributes(_a) {
    var documentElementKeys = _a.documentElementKeys;
    if (documentElementKeys.state !== State.Success)
        return false;
    if (includes(documentElementKeys.value, 'selenium', 'webdriver', 'driver')) {
        return exports.BotKind.Selenium;
    }
}

function detectErrorTrace(_a) {
    var errorTrace = _a.errorTrace;
    if (errorTrace.state !== State.Success)
        return false;
    if (/PhantomJS/i.test(errorTrace.value))
        return exports.BotKind.PhantomJS;
}

function getBrowserEngineKind() {
    var _a, _b;
    // Based on research in October 2020. Tested to detect Chromium 42-86.
    var w = window;
    var n = navigator;
    if (countTruthy([
        'webkitPersistentStorage' in n,
        'webkitTemporaryStorage' in n,
        n.vendor.indexOf('Google') === 0,
        'webkitResolveLocalFileSystemURL' in w,
        'BatteryManager' in w,
        'webkitMediaStream' in w,
        'webkitSpeechGrammar' in w,
    ]) >= 5) {
        return BrowserEngineKind.Chromium;
    }
    if (countTruthy([
        'ApplePayError' in w,
        'CSSPrimitiveValue' in w,
        'Counter' in w,
        n.vendor.indexOf('Apple') === 0,
        'getStorageUpdates' in n,
        'WebKitMediaKeys' in w,
    ]) >= 4) {
        return BrowserEngineKind.Webkit;
    }
    if (countTruthy([
        'buildID' in navigator,
        'MozAppearance' in ((_b = (_a = document.documentElement) === null || _a === void 0 ? void 0 : _a.style) !== null && _b !== void 0 ? _b : {}),
        'onmozfullscreenchange' in w,
        'mozInnerScreenX' in w,
        'CSSMozDocumentRule' in w,
        'CanvasCaptureMediaStream' in w,
    ]) >= 4) {
        return BrowserEngineKind.Gecko;
    }
    return BrowserEngineKind.Unknown;
}
function getBrowserKind() {
    var _a;
    var userAgent = (_a = navigator.userAgent) === null || _a === void 0 ? void 0 : _a.toLowerCase();
    if (strIncludes(userAgent, 'wechat')) {
        return BrowserKind.WeChat;
    }
    else if (strIncludes(userAgent, 'firefox')) {
        return BrowserKind.Firefox;
    }
    else if (strIncludes(userAgent, 'opera') || strIncludes(userAgent, 'opr')) {
        return BrowserKind.Opera;
    }
    else if (strIncludes(userAgent, 'chrome')) {
        return BrowserKind.Chrome;
    }
    else if (strIncludes(userAgent, 'safari')) {
        return BrowserKind.Safari;
    }
    else if (strIncludes(userAgent, 'trident') || strIncludes(userAgent, 'msie')) {
        return BrowserKind.IE;
    }
    else {
        return BrowserKind.Unknown;
    }
}
// Source: https://github.com/fingerprintjs/fingerprintjs/blob/master/src/utils/browser.ts#L223
function isAndroid() {
    var browserEngineKind = getBrowserEngineKind();
    var isItChromium = browserEngineKind === BrowserEngineKind.Chromium;
    var isItGecko = browserEngineKind === BrowserEngineKind.Gecko;
    // Only 2 browser engines are presented on Android.
    // Actually, there is also Android 4.1 browser, but it's not worth detecting it at the moment.
    if (!isItChromium && !isItGecko)
        return false;
    var w = window;
    // Chrome removes all words "Android" from `navigator` when desktop version is requested
    // Firefox keeps "Android" in `navigator.appVersion` when desktop version is requested
    return (countTruthy([
        'onorientationchange' in w,
        'orientation' in w,
        isItChromium && !('SharedWorker' in w),
        isItGecko && /android/i.test(navigator.appVersion),
    ]) >= 2);
}
function isDesktopSafari() {
    if (getBrowserEngineKind() !== BrowserEngineKind.Webkit) {
        return false;
    }
    var w = window;
    return (countTruthy([
        'safari' in w,
        !('DeviceMotionEvent' in w),
        !('ongestureend' in w),
        !('standalone' in navigator),
    ]) >= 3);
}
function getDocumentFocus() {
    if (document.hasFocus === undefined) {
        return false;
    }
    return document.hasFocus();
}
function isChromium86OrNewer() {
    // Checked in Chrome 85 vs Chrome 86 both on desktop and Android
    var w = window;
    return (countTruthy([
        !('MediaSettingsRange' in w),
        'RTCEncodedAudioFrame' in w,
        '' + w.Intl === '[object Intl]',
        '' + w.Reflect === '[object Reflect]',
    ]) >= 3);
}

function detectEvalLengthInconsistency(_a) {
    var evalLength = _a.evalLength;
    if (evalLength.state !== State.Success)
        return;
    var length = evalLength.value;
    var browser = getBrowserKind();
    var browserEngine = getBrowserEngineKind();
    return ((length === 37 && !arrayIncludes([BrowserEngineKind.Webkit, BrowserEngineKind.Gecko], browserEngine)) ||
        (length === 39 && !arrayIncludes([BrowserKind.IE], browser)) ||
        (length === 33 && !arrayIncludes([BrowserEngineKind.Chromium], browserEngine)));
}

function detectFunctionBind(_a) {
    var functionBind = _a.functionBind;
    if (functionBind.state === State.NotFunction)
        return exports.BotKind.PhantomJS;
}

function detectLanguagesLengthInconsistency(_a) {
    var languages = _a.languages;
    if (languages.state === State.Success && languages.value.length === 0) {
        return exports.BotKind.HeadlessChrome;
    }
}

function detectMimeTypesConsistent(_a) {
    var mimeTypesConsistent = _a.mimeTypesConsistent;
    if (mimeTypesConsistent.state === State.Success && !mimeTypesConsistent.value) {
        return exports.BotKind.Unknown;
    }
}

function detectNotificationPermissions(_a) {
    var notificationPermissions = _a.notificationPermissions;
    var browserKind = getBrowserKind();
    if (browserKind !== BrowserKind.Chrome)
        return false;
    if (notificationPermissions.state === State.Success && notificationPermissions.value) {
        return exports.BotKind.HeadlessChrome;
    }
}

function detectPluginsArray(_a) {
    var pluginsArray = _a.pluginsArray;
    if (pluginsArray.state === State.Success && !pluginsArray.value)
        return exports.BotKind.HeadlessChrome;
}

function detectPluginsLengthInconsistency(_a) {
    var pluginsLength = _a.pluginsLength;
    if (pluginsLength.state !== State.Success)
        return;
    var browserEngineKind = getBrowserEngineKind();
    // Chromium based android browsers and mobile webkit based browsers have 0 plugins length.
    if ((browserEngineKind === BrowserEngineKind.Chromium && isAndroid()) ||
        (browserEngineKind === BrowserEngineKind.Webkit && !isDesktopSafari()))
        return;
    if (pluginsLength.value === 0)
        return exports.BotKind.HeadlessChrome;
}

function detectProcess(_a) {
    var _b;
    var process = _a.process;
    if (process.state !== State.Success)
        return false;
    if (process.value.type === 'renderer' || ((_b = process.value.versions) === null || _b === void 0 ? void 0 : _b.electron) != null)
        return exports.BotKind.Electron;
}

function detectProductSub(_a) {
    var productSub = _a.productSub;
    if (productSub.state !== State.Success)
        return false;
    var browserKind = getBrowserKind();
    if ((browserKind === BrowserKind.Chrome ||
        browserKind === BrowserKind.Safari ||
        browserKind === BrowserKind.Opera ||
        browserKind === BrowserKind.WeChat) &&
        productSub.value !== '20030107')
        return exports.BotKind.Unknown;
}

function detectUserAgent(_a) {
    var userAgent = _a.userAgent;
    if (userAgent.state !== State.Success)
        return false;
    if (/PhantomJS/i.test(userAgent.value))
        return exports.BotKind.PhantomJS;
    if (/Headless/i.test(userAgent.value))
        return exports.BotKind.HeadlessChrome;
    if (/Electron/i.test(userAgent.value))
        return exports.BotKind.Electron;
    if (/slimerjs/i.test(userAgent.value))
        return exports.BotKind.SlimerJS;
}

function detectWebDriver(_a) {
    var webDriver = _a.webDriver;
    if (webDriver.state === State.Success && webDriver.value)
        return exports.BotKind.HeadlessChrome;
}

function detectWebGL(_a) {
    var webGL = _a.webGL;
    if (webGL.state === State.Success) {
        var _b = webGL.value, vendor = _b.vendor, renderer = _b.renderer;
        if (vendor == 'Brian Paul' && renderer == 'Mesa OffScreen') {
            return exports.BotKind.HeadlessChrome;
        }
    }
}

function detectWindowExternal(_a) {
    var windowExternal = _a.windowExternal;
    if (windowExternal.state !== State.Success)
        return false;
    if (/Sequentum/i.test(windowExternal.value))
        return exports.BotKind.Sequentum;
}

function detectWindowSize(_a) {
    var windowSize = _a.windowSize;
    if (windowSize.state !== State.Success)
        return false;
    var _b = windowSize.value, outerWidth = _b.outerWidth, outerHeight = _b.outerHeight;
    // When a page is opened in a new tab without focusing it right away, the window outer size is 0x0
    if (!getDocumentFocus())
        return;
    if (outerWidth === 0 && outerHeight === 0)
        return exports.BotKind.HeadlessChrome;
}

function detectDistinctiveProperties(_a) {
    var distinctiveProps = _a.distinctiveProps;
    if (distinctiveProps.state !== State.Success)
        return false;
    var value = distinctiveProps.value;
    var bot;
    for (bot in value)
        if (value[bot])
            return bot;
}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
var detectors = {
    detectAppVersion: detectAppVersion,
    detectDocumentAttributes: detectDocumentAttributes,
    detectErrorTrace: detectErrorTrace,
    detectEvalLengthInconsistency: detectEvalLengthInconsistency,
    detectFunctionBind: detectFunctionBind,
    detectLanguagesLengthInconsistency: detectLanguagesLengthInconsistency,
    detectNotificationPermissions: detectNotificationPermissions,
    detectPluginsArray: detectPluginsArray,
    detectPluginsLengthInconsistency: detectPluginsLengthInconsistency,
    detectProcess: detectProcess,
    detectUserAgent: detectUserAgent,
    detectWebDriver: detectWebDriver,
    detectWebGL: detectWebGL,
    detectWindowExternal: detectWindowExternal,
    detectWindowSize: detectWindowSize,
    detectMimeTypesConsistent: detectMimeTypesConsistent,
    detectProductSub: detectProductSub,
    detectDistinctiveProperties: detectDistinctiveProperties,
};

function getAppVersion() {
    var appVersion = navigator.appVersion;
    if (appVersion == undefined) {
        throw new BotdError(State.Undefined, 'navigator.appVersion is undefined');
    }
    return appVersion;
}

function getDocumentElementKeys() {
    if (document.documentElement === undefined) {
        throw new BotdError(State.Undefined, 'document.documentElement is undefined');
    }
    var documentElement = document.documentElement;
    if (typeof documentElement.getAttributeNames !== 'function') {
        throw new BotdError(State.NotFunction, 'document.documentElement.getAttributeNames is not a function');
    }
    return documentElement.getAttributeNames();
}

function getErrorTrace() {
    try {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        null[0]();
    }
    catch (error) {
        if (error instanceof Error && error['stack'] != null) {
            return error.stack.toString();
        }
    }
    throw new BotdError(State.UnexpectedBehaviour, 'errorTrace signal unexpected behaviour');
}

function getEvalLength() {
    return eval.toString().length;
}

function getFunctionBind() {
    if (Function.prototype.bind === undefined) {
        throw new BotdError(State.NotFunction, 'Function.prototype.bind is undefined');
    }
    return Function.prototype.bind.toString();
}

function getLanguages() {
    var n = navigator;
    var result = [];
    var language = n.language || n.userLanguage || n.browserLanguage || n.systemLanguage;
    if (language !== undefined) {
        result.push([language]);
    }
    if (Array.isArray(n.languages)) {
        var browserEngine = getBrowserEngineKind();
        // Starting from Chromium 86, there is only a single value in `navigator.language` in Incognito mode:
        // the value of `navigator.language`. Therefore, the value is ignored in this browser.
        if (!(browserEngine === BrowserEngineKind.Chromium && isChromium86OrNewer())) {
            result.push(n.languages);
        }
    }
    else if (typeof n.languages === 'string') {
        var languages = n.languages;
        if (languages) {
            result.push(languages.split(','));
        }
    }
    return result;
}

function areMimeTypesConsistent() {
    if (navigator.mimeTypes === undefined) {
        throw new BotdError(State.Undefined, 'navigator.mimeTypes is undefined');
    }
    var mimeTypes = navigator.mimeTypes;
    var isConsistent = Object.getPrototypeOf(mimeTypes) === MimeTypeArray.prototype;
    for (var i = 0; i < mimeTypes.length; i++) {
        isConsistent && (isConsistent = Object.getPrototypeOf(mimeTypes[i]) === MimeType.prototype);
    }
    return isConsistent;
}

function getNotificationPermissions() {
    return tslib.__awaiter(this, void 0, void 0, function () {
        var permissions, permissionStatus;
        return tslib.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (window.Notification === undefined) {
                        throw new BotdError(State.Undefined, 'window.Notification is undefined');
                    }
                    if (navigator.permissions === undefined) {
                        throw new BotdError(State.Undefined, 'navigator.permissions is undefined');
                    }
                    permissions = navigator.permissions;
                    if (typeof permissions.query !== 'function') {
                        throw new BotdError(State.NotFunction, 'navigator.permissions.query is not a function');
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, permissions.query({ name: 'notifications' })];
                case 2:
                    permissionStatus = _a.sent();
                    return [2 /*return*/, window.Notification.permission === 'denied' && permissionStatus.state === 'prompt'];
                case 3:
                    _a.sent();
                    throw new BotdError(State.UnexpectedBehaviour, 'notificationPermissions signal unexpected behaviour');
                case 4: return [2 /*return*/];
            }
        });
    });
}

function getPluginsArray() {
    if (navigator.plugins === undefined) {
        throw new BotdError(State.Undefined, 'navigator.plugins is undefined');
    }
    if (window.PluginArray === undefined) {
        throw new BotdError(State.Undefined, 'window.PluginArray is undefined');
    }
    return navigator.plugins instanceof PluginArray;
}

function getPluginsLength() {
    if (navigator.plugins === undefined) {
        throw new BotdError(State.Undefined, 'navigator.plugins is undefined');
    }
    if (navigator.plugins.length === undefined) {
        throw new BotdError(State.UnexpectedBehaviour, 'navigator.plugins.length is undefined');
    }
    return navigator.plugins.length;
}

function getProcess() {
    if (window.process === undefined) {
        throw new BotdError(State.Undefined, 'window.process is undefined');
    }
    return window.process;
}

function getProductSub() {
    var productSub = navigator.productSub;
    if (productSub === undefined) {
        throw new BotdError(State.Undefined, 'navigator.productSub is undefined');
    }
    return productSub;
}

function getRTT() {
    if (navigator.connection === undefined) {
        throw new BotdError(State.Undefined, 'navigator.connection is undefined');
    }
    if (navigator.connection.rtt === undefined) {
        throw new BotdError(State.Undefined, 'navigator.connection.rtt is undefined');
    }
    return navigator.connection.rtt;
}

function getUserAgent() {
    return navigator.userAgent;
}

function getWebDriver() {
    if (navigator.webdriver == undefined) {
        throw new BotdError(State.Undefined, 'navigator.webdriver is undefined');
    }
    return navigator.webdriver;
}

function getWebGL() {
    var canvasElement = document.createElement('canvas');
    if (typeof canvasElement.getContext !== 'function') {
        throw new BotdError(State.NotFunction, 'HTMLCanvasElement.getContext is not a function');
    }
    var webGLContext = canvasElement.getContext('webgl');
    if (webGLContext === null) {
        throw new BotdError(State.Null, 'WebGLRenderingContext is null');
    }
    if (typeof webGLContext.getParameter !== 'function') {
        throw new BotdError(State.NotFunction, 'WebGLRenderingContext.getParameter is not a function');
    }
    var vendor = webGLContext.getParameter(webGLContext.VENDOR);
    var renderer = webGLContext.getParameter(webGLContext.RENDERER);
    return { vendor: vendor, renderer: renderer };
}

function getWindowExternal() {
    if (window.external === undefined) {
        throw new BotdError(State.Undefined, 'window.external is undefined');
    }
    var external = window.external;
    if (typeof external.toString !== 'function') {
        throw new BotdError(State.NotFunction, 'window.external.toString is not a function');
    }
    return external.toString();
}

function getWindowSize() {
    return {
        outerWidth: window.outerWidth,
        outerHeight: window.outerHeight,
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
    };
}

function checkDistinctiveProperties() {
    var _a;
    // The order in the following list matters, because specific types of bots come first, followed by automation technologies.
    var distinctivePropsList = (_a = {},
        _a[exports.BotKind.Awesomium] = {
            window: ['awesomium'],
        },
        _a[exports.BotKind.Cef] = {
            window: ['RunPerfTest'],
        },
        _a[exports.BotKind.CefSharp] = {
            window: ['CefSharp'],
        },
        _a[exports.BotKind.CoachJS] = {
            window: ['emit'],
        },
        _a[exports.BotKind.FMiner] = {
            window: ['fmget_targets'],
        },
        _a[exports.BotKind.Geb] = {
            window: ['geb'],
        },
        _a[exports.BotKind.NightmareJS] = {
            window: ['__nightmare', 'nightmare'],
        },
        _a[exports.BotKind.Phantomas] = {
            window: ['__phantomas'],
        },
        _a[exports.BotKind.PhantomJS] = {
            window: ['callPhantom', '_phantom'],
        },
        _a[exports.BotKind.Rhino] = {
            window: ['spawn'],
        },
        _a[exports.BotKind.Selenium] = {
            window: ['_Selenium_IDE_Recorder', '_selenium', 'calledSelenium', /^([a-z]){3}_.*_(Array|Promise|Symbol)$/],
            document: ['__selenium_evaluate', 'selenium-evaluate', '__selenium_unwrapped'],
        },
        _a[exports.BotKind.WebDriverIO] = {
            window: ['wdioElectron'],
        },
        _a[exports.BotKind.WebDriver] = {
            window: [
                'webdriver',
                '__webdriverFunc',
                '__lastWatirAlert',
                '__lastWatirConfirm',
                '__lastWatirPrompt',
                '_WEBDRIVER_ELEM_CACHE',
                'ChromeDriverw',
            ],
            document: [
                '__webdriver_script_fn',
                '__driver_evaluate',
                '__webdriver_evaluate',
                '__fxdriver_evaluate',
                '__driver_unwrapped',
                '__webdriver_unwrapped',
                '__fxdriver_unwrapped',
                '__webdriver_script_fn',
                '__webdriver_script_func',
                '__webdriver_script_function',
                '$cdc_asdjflasutopfhvcZLmcf',
                '$cdc_asdjflasutopfhvcZLmcfl_',
                '$chrome_asyncScriptInfo',
                '__$webdriverAsyncExecutor',
            ],
        },
        _a[exports.BotKind.HeadlessChrome] = {
            window: ['domAutomation', 'domAutomationController'],
        },
        _a);
    var botName;
    var result = {};
    var windowProps = getObjectProps(window);
    var documentProps = [];
    if (window.document !== undefined)
        documentProps = getObjectProps(window.document);
    for (botName in distinctivePropsList) {
        var props = distinctivePropsList[botName];
        if (props !== undefined) {
            var windowContains = props.window === undefined ? false : includes.apply(void 0, tslib.__spreadArray([windowProps], props.window, false));
            var documentContains = props.document === undefined || !documentProps.length ? false : includes.apply(void 0, tslib.__spreadArray([documentProps], props.document, false));
            result[botName] = windowContains || documentContains;
        }
    }
    return result;
}

var sources = {
    userAgent: getUserAgent,
    appVersion: getAppVersion,
    rtt: getRTT,
    windowSize: getWindowSize,
    pluginsLength: getPluginsLength,
    pluginsArray: getPluginsArray,
    errorTrace: getErrorTrace,
    productSub: getProductSub,
    windowExternal: getWindowExternal,
    mimeTypesConsistent: areMimeTypesConsistent,
    evalLength: getEvalLength,
    webGL: getWebGL,
    webDriver: getWebDriver,
    languages: getLanguages,
    notificationPermissions: getNotificationPermissions,
    documentElementKeys: getDocumentElementKeys,
    functionBind: getFunctionBind,
    process: getProcess,
    distinctiveProps: checkDistinctiveProperties,
};

/**
 * Class representing a bot detector.
 *
 * @class
 * @implements {BotDetectorInterface}
 */
var BotDetector = /** @class */ (function () {
    function BotDetector() {
        this.components = undefined;
        this.detections = undefined;
    }
    BotDetector.prototype.getComponents = function () {
        return this.components;
    };
    BotDetector.prototype.getDetections = function () {
        return this.detections;
    };
    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    BotDetector.prototype.getSources = function () {
        return sources;
    };
    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    BotDetector.prototype.getDetectors = function () {
        return detectors;
    };
    /**
     * @inheritdoc
     */
    BotDetector.prototype.detect = function () {
        if (this.components === undefined) {
            throw new Error("BotDetector.detect can't be called before BotDetector.collect");
        }
        var components = this.components;
        var detectors = this.getDetectors();
        var detections = {};
        var finalDetection = {
            bot: false,
        };
        for (var detectorName in detectors) {
            var detector = detectors[detectorName];
            var detectorRes = detector(components);
            var detection = { bot: false };
            if (typeof detectorRes === 'string') {
                detection = { bot: true, botKind: detectorRes };
            }
            else if (detectorRes) {
                detection = { bot: true, botKind: exports.BotKind.Unknown };
            }
            detections[detectorName] = detection;
            if (detection.bot) {
                finalDetection = detection;
            }
        }
        this.detections = detections;
        return finalDetection;
    };
    /**
     * @inheritdoc
     */
    BotDetector.prototype.collect = function () {
        return tslib.__awaiter(this, void 0, void 0, function () {
            var sources, components, sourcesKeys;
            var _this = this;
            return tslib.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        sources = this.getSources();
                        components = {};
                        sourcesKeys = Object.keys(sources);
                        return [4 /*yield*/, Promise.all(sourcesKeys.map(function (sourceKey) { return tslib.__awaiter(_this, void 0, void 0, function () {
                                var res, _a, _b, error_1;
                                var _c;
                                return tslib.__generator(this, function (_d) {
                                    switch (_d.label) {
                                        case 0:
                                            res = sources[sourceKey];
                                            _d.label = 1;
                                        case 1:
                                            _d.trys.push([1, 3, , 4]);
                                            _a = components;
                                            _b = sourceKey;
                                            _c = {};
                                            return [4 /*yield*/, res()];
                                        case 2:
                                            _a[_b] = (_c.value = _d.sent(),
                                                _c.state = State.Success,
                                                _c);
                                            return [3 /*break*/, 4];
                                        case 3:
                                            error_1 = _d.sent();
                                            if (error_1 instanceof BotdError) {
                                                components[sourceKey] = {
                                                    state: error_1.state,
                                                    error: "".concat(error_1.name, ": ").concat(error_1.message),
                                                };
                                            }
                                            else {
                                                components[sourceKey] = {
                                                    state: State.UnexpectedBehaviour,
                                                    error: error_1 instanceof Error ? "".concat(error_1.name, ": ").concat(error_1.message) : String(error_1),
                                                };
                                            }
                                            return [3 /*break*/, 4];
                                        case 4: return [2 /*return*/];
                                    }
                                });
                            }); }))];
                    case 1:
                        _a.sent();
                        this.components = components;
                        return [2 /*return*/, this.components];
                }
            });
        });
    };
    return BotDetector;
}());

/**
 * Sends an unpersonalized AJAX request to collect installation statistics
 */
function monitor() {
    // The FingerprintJS CDN (https://github.com/fingerprintjs/cdn) replaces `window.__fpjs_d_m` with `true`
    if (window.__fpjs_d_m || Math.random() >= 0.001) {
        return;
    }
    try {
        var request = new XMLHttpRequest();
        request.open('get', "https://m1.openfpcdn.io/botd/v".concat(version, "/npm-monitoring"), true);
        request.send();
    }
    catch (error) {
        // console.error is ok here because it's an unexpected error handler
        // eslint-disable-next-line no-console
        console.error(error);
    }
}
function load(_a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.monitoring, monitoring = _c === void 0 ? true : _c;
    return tslib.__awaiter(this, void 0, void 0, function () {
        var detector;
        return tslib.__generator(this, function (_d) {
            switch (_d.label) {
                case 0:
                    if (monitoring) {
                        monitor();
                    }
                    detector = new BotDetector();
                    return [4 /*yield*/, detector.collect()];
                case 1:
                    _d.sent();
                    return [2 /*return*/, detector];
            }
        });
    });
}
var index = { load: load };
