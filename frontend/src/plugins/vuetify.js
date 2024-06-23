// plugins/vuetify.js or plugins/vuetify.ts
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { VNumberInput } from 'vuetify/labs/VNumberInput'

export default createVuetify({
  components: {
    VNumberInput,
    ...components
  },

  directives,
  icons: {
    iconfont: 'mdi',
    values: {
      ...aliases,
      mdi
    }
  }
})
