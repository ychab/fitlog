const { src, dest, series } = require('gulp');

function sb_admin() {
  return src('./node_modules/startbootstrap-sb-admin/**/*')
    .pipe(dest('fitlog/static/sb-admin/'));
}

function vue() {
  return src('./node_modules/vue/**/*')
    .pipe(dest('fitlog/static/vue/'));
}

function vue_cookies() {
  return src('./node_modules/vue-cookies/**/*')
    .pipe(dest('fitlog/static/vue-cookies/'));
}

function axios() {
  return src('./node_modules/axios/**/*')
    .pipe(dest('fitlog/static/axios/'));
}

exports.sb_admin = sb_admin;
exports.vue = vue;
exports.vue_cookies = vue_cookies;
exports.axios = axios;
exports.default = series(sb_admin, vue, vue_cookies, axios);
