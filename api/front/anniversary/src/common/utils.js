"use strict";
export const css3Supports = detectCssAnimationSupported();
export function detectCssAnimationSupported() {
    var _a = detectCssFeatureSupported("perspective"), supports3d = _a.supported, supported3dPrefix = _a.supportedPrefix;
    var _b = detectCssFeatureSupported("transform"), supportsTransform = _b.supported, supportedTransformPrefix = _b.supportedPrefix;
    return {
        supports3d: supports3d,
        supported3dPrefix: supported3dPrefix,
        supportsTransform: supportsTransform,
        supportedTransformPrefix: supportedTransformPrefix
    };
}

export function detectCssFeatureSupported(name) {
    var supportedPrefix;
    var supported = false;
    var prefixes = ["Webkit", "Moz", "ms", "O"];
    var div = document.createElement("div");
    if (div.style[name] !== undefined) {
        /*Browser supports CSS transform 3d without prefix*/
        supportedPrefix = "";
        supported = true;
    }
    else {
        name = name.substr(0, 1).toUpperCase() + name.substr(1);
        for (var i = 0; i < prefixes.length; ++i) {
            if (prefixes[i] + name in div.style) {
                supported = true;
                supportedPrefix = prefixes[i];
                break;
            }
        }
    }
    return {
        supported: supported,
        supportedPrefix: supportedPrefix
    };
}
export const transform7CSS3D = [
    getTransform3dCSS("-100%", -400, 40, -1, 0, "hidden"),
    getTransform3dCSS("0", -350, 45, -1, 1, "visible"),
    getTransform3dCSS("100%", -300, 45, 0, 1, "visible"),
    getTransform3dCSS("200%", -200, 40, 1, 1, "visible"),
    getTransform3dCSS("300%", 0, 0, 2, 1, "visible"),
    getTransform3dCSS("400%", -200, -40, 1, 1, "visible"),
    getTransform3dCSS("500%", -300, -45, 0, 1, "visible"),
    getTransform3dCSS("600%", -350, -45, -1, 1, "visible"),
    getTransform3dCSS("700%", -400, -40, -1, 0, "hidden")
];
export const transform7CSS2D = [
    getTransform2dCSS("-100%", 0.6, "100%", "50%", 0, "hidden"),
    getTransform2dCSS("0", 0.6, "100%", "50%", 1, "visible"),
    getTransform2dCSS("100%", 0.7, "100%", "50%", 1, "visible"),
    getTransform2dCSS("200%", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("300%", 1, "50%", "50%", 1, "visible"),
    getTransform2dCSS("400%", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("500%", 0.7, "0%", "50%", 1, "visible"),
    getTransform2dCSS("600%", 0.6, "0%", "50%", 1, "visible"),
    getTransform2dCSS("700%", 0.6, "0%", "50%", 0, "hidden")
];
export function getTransform7CSS() {
    if (css3Supports.supports3d) {
        return transform7CSS3D;
    }
    else {
        return transform7CSS2D;
    }
}

export const transform5CSS3D = [
    getTransform3dCSS("-100%", -400, 45, -1, 0, "hidden"),
    getTransform3dCSS("0", -300, 45, 0, 1, "visible"),
    getTransform3dCSS("100%", -200, 45, 1, 1, "visible"),
    getTransform3dCSS("200%", 0, 0, 2, 1, "visible"),
    getTransform3dCSS("300%", -200, -45, 1, 1, "visible"),
    getTransform3dCSS("400%", -300, -45, 0, 1, "visible"),
    getTransform3dCSS("500%", -400, -45, -1, 0, "hidden")
];
export const transform5CSS2D = [
    getTransform2dCSS("-100%", 0.6, "100%", "50%", 0, "hidden"),
    getTransform2dCSS("0", 0.7, "100%", "50%", 1, "visible"),
    getTransform2dCSS("100%", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("200%", 1, "50%", "50%", 1, "visible"),
    getTransform2dCSS("300%", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("400%", 0.7, "0%", "50%", 1, "visible"),
    getTransform2dCSS("500%", 0.6, "0%", "50%", 0, "hidden")
];
export function getTransform5CSS() {
    if (css3Supports.supports3d) {
        return transform5CSS3D;
    }
    else {
        return transform5CSS2D;
    }
}

export const transform3CSS3D = [
    getTransform3dCSS("-100%", -400, 45, 0, 0, "hidden"),
    getTransform3dCSS("0", -300, 45, 1, 1, "visible"),
    getTransform3dCSS("100%", 0, 0, 2, 1, "visible"),
    getTransform3dCSS("200%", -300, -45, 1, 1, "visible"),
    getTransform3dCSS("300%", -400, -45, 0, 0, "hidden")
];
export const transform3CSS2D = [
    getTransform2dCSS("-100%", 0.65, "100%", "50%", 0, "hidden"),
    getTransform2dCSS("0", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("100%", 1, "50%", "50%", 1, "visible"),
    getTransform2dCSS("200%", 0.8, "50%", "50%", 1, "visible"),
    getTransform2dCSS("300%", 0.65, "0%", "50%", 0, "hidden")
];
function getTransform3CSS() {
    if (css3Supports.supports3d) {
        return transform3CSS3D;
    }
    else {
        return transform3CSS2D;
    }
}

export const transform3dCSS = [
    getTransform3dCSS("-100%", -300, 45, 0, 0, "hidden"),
    getTransform3dCSS("0%", 0, 0, 2, 1, "visible"),
    getTransform3dCSS("100%", -300, -45, 0, 0, "hidden")
];
export const transform1CSS2D = [
    getTransform2dCSS("-100%", 0.65, "100%", "50%", 0, "hidden"),
    getTransform2dCSS("0", 1, "50%", "50%", 1, "visible"),
    getTransform2dCSS("100%", 0.65, "0%", "50%", 0, "hidden")
];
export function getTransform1CSS() {
    if (css3Supports.supports3d) {
        return transform3dCSS;
    }
    else {
        return transform1CSS2D;
    }
}

export function getTransform3dCSS(tx, ty, ry, zIndex, opacity, visibility) {
    var result = {};
    var value = "translateX(" + tx + ") translateZ(" + ty + "px) rotateY(" + ry + "deg)";
    ["-webkit-", "-moz-", "-o-", "-ms-", ""].forEach(function (prefix) {
        result[prefix + "transform"] = value;
    });
    result = Object.assign({}, result, { "z-index": zIndex, opacity: opacity, visibility: visibility });
    return result;
}

export function getTransform2dCSS(t, s, originX, originY, opacity, visibility) {
    var result = {};
    var value = "translate(" + t + ") scale(" + s + ")";
    ["-webkit-", "-moz-", "-o-", "-ms-", ""].forEach(function (prefix) {
        result[prefix + "transform"] = value;
        result[prefix + "transform-origin"] = originX + " " + originY;
    });
    result = Object.assign({}, result, { opacity: opacity, visibility: visibility });
    return result;
}

export function getElementWidth(el) {
    return el.offsetWidth;
}

export function getTansCSS(showCount) {
    switch (showCount) {
        case 1:
            return getTransform1CSS();
        case 3:
            return getTransform3CSS();
        case 5:
            return getTransform5CSS();
        case 7:
            return getTransform7CSS();
    }
    return [];
}

