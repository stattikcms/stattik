const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  entry: './stattik_theme_bulma/assets/index.js',
  output: {
    path: path.resolve(__dirname, './stattik_theme_bulma/static'),
    filename: 'js/bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
            MiniCssExtractPlugin.loader,
            {
              loader: 'css-loader'
            },
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true,
                // options...
              }
            },
      ]},
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/bundle.css'
    }),
  ]
};