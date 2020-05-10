const webpack = require('webpack');
// vue.config.js
module.exports = {
  lintOnSave: false,
  publicPath: '',
  devServer: {
    hot: true,
    hotOnly: true,
    disableHostCheck: false,
    historyApiFallback: true,
    // public: '0.0.0.0:8080',
    host:'0.0.0.0',
    // port:'8080',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
    },
    watchOptions: {
      poll: 1000,
      ignored: '/frontend/node_modules/'
    }
  },
  configureWebpack: {
    // Set up all the aliases we use in our app.
    plugins: [
      new webpack.optimize.LimitChunkCountPlugin({
        maxChunks: 6
      })
    ]
  },
  pwa: {
    name: 'GeoLocation',
    themeColor: '#172b4d',
    msTileColor: '#172b4d',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#172b4d'
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production'
  }
};