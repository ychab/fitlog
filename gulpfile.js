const { src, dest, series } = require('gulp');

function sb_admin() {
  return src('./node_modules/startbootstrap-sb-admin/**/*')
    .pipe(dest('fitlog/static/sb-admin/'));
}

exports.sb_admin = sb_admin;
exports.default = series(sb_admin);
