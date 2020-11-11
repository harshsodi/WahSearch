'use strict'
// Template version: 1.3.1
// see http://vuejs-templates.github.io/webpack for documentation.

const path = require('path')

const fs = require('fs');
const yaml = require('js-yaml');


try {
  let fileContents = fs.readFileSync('/opt/config.yml', 'utf8');
  let data = yaml.safeLoad(fileContents);

  module.exports = {
    dev: {

      // Paths
      assetsSubDirectory: 'static',
      assetsPublicPath: '/',
      proxyTable: {
        '/': { // 
          // Interface root address
          target: 'http://0.0.0.0:8090/', // Backend server address
          changeOrigin: true, // Turning on the proxy can also solve cross-domain problems
          pathRewrite: {
            '^/': '/' // Copy the remote address and try to be consistent
          },
        }
      },

      // Various Dev Server settings
      host: '0.0.0.0', // can be overwritten by process.env.HOST
      port: "8090", // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
      autoOpenBrowser: true,
      errorOverlay: true,
      notifyOnErrors: true,
      poll: false,


      /**
       * Source Maps
       */

      // https://webpack.js.org/configuration/devtool/#development
      devtool: 'cheap-module-eval-source-map',

      // If you have problems debugging vue-files in devtools,
      // set this to false - it *may* help
      // https://vue-loader.vuejs.org/en/options.html#cachebusting
      cacheBusting: true,

      cssSourceMap: true
    },

    build: {
      // Template for index.html
      index: path.resolve(__dirname, '../biguniverse/index.html'),

      // Paths
      assetsRoot: path.resolve(__dirname, '../biguniverse'),
      assetsSubDirectory: 'static',
      assetsPublicPath: './',

      /**
       * Source Maps
       */

      productionSourceMap: true,
      // https://webpack.js.org/configuration/devtool/#production
      devtool: '#source-map',

      // Gzip off by default as many popular static hosts such as
      // Surge or Netlify already gzip all static assets for you.
      // Before setting to `true`, make sure to:
      // npm install --save-dev compression-webpack-plugin
      productionGzip: false,
      productionGzipExtensions: ['js', 'css'],

      // Run the build command with an extra argument to
      // View the bundle analyzer report after build finishes:
      // `npm run build --report`
      // Set to `true` or `false` to always turn it on or off
      bundleAnalyzerReport: process.env.npm_config_report
    }
  }

} catch (e) {
  console.log(e);
}