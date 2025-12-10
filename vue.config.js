module.exports = {
  lintOnSave: false,

  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/sccs/styles.scss";`,
      },
    },
  },

  publicPath: process.env.NODE_ENV === "production" ? "/" : "/",
  devServer: {
    port: 8082,
    // https: true,
  },
  pluginOptions: {
    i18n: {
      // locale: 'en',
      fallbackLocale: "en",
      localeDir: "locales",
      enableInSFC: false,
    },
  },
};
