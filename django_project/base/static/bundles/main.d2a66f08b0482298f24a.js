/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./base/static/js/index.js":
/*!*********************************!*\
  !*** ./base/static/js/index.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

eval("__webpack_require__(/*! ../style/scss/style.scss */ \"./base/static/style/scss/style.scss\");\n\ndocument.addEventListener(\"DOMContentLoaded\", () => {\n  // Get all \"navbar-burger\" elements\n  const $navbarBurgers = Array.prototype.slice.call(\n    document.querySelectorAll(\".navbar-burger\"),\n    0\n  );\n\n  // Add a click event on each of them\n  $navbarBurgers.forEach((el) => {\n    el.addEventListener(\"click\", () => {\n      // Get the target from the \"data-target\" attribute\n      const target = el.dataset.target;\n      const $target = document.getElementById(target);\n\n      // Toggle the \"is-active\" class on both the \"navbar-burger\" and the \"navbar-menu\"\n      el.classList.toggle(\"is-active\");\n      $target.classList.toggle(\"is-active\");\n    });\n  });\n});\n\n\n//# sourceURL=webpack://qgis-plugins/./base/static/js/index.js?");

/***/ }),

/***/ "./base/static/style/scss/style.scss":
/*!*******************************************!*\
  !*** ./base/static/style/scss/style.scss ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://qgis-plugins/./base/static/style/scss/style.scss?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 	
/******/ 		        // webpack-livereload-plugin
/******/ 		        (function() {
/******/ 		          if (typeof window === "undefined") { return };
/******/ 		          var id = "webpack-livereload-plugin-script-73151229d325f893";
/******/ 		          if (document.getElementById(id)) { return; }
/******/ 		          var el = document.createElement("script");
/******/ 		          el.id = id;
/******/ 		          el.async = true;
/******/ 		          el.src = "//" + location.hostname + ":35729/livereload.js";
/******/ 		          document.getElementsByTagName("head")[0].appendChild(el);
/******/ 		          console.log("[Live Reload] enabled");
/******/ 		        }());
/******/ 		        // Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./base/static/js/index.js");
/******/ 	
/******/ })()
;