import Vue from 'vue'
import ElementUI from 'element-ui'
import lodash from 'lodash'
import c3 from 'c3'
import Trend from 'vuetrend'
import moment from 'moment-timezone'

import 'c3/c3.min.css'
import 'element-ui/lib/theme-default/index.css'
import './css/style.css'
import './css/forbes_logo.css'
import './css/loading_animation.css'
import './css/infinite.css'
import App from './App.vue'
import locale from 'element-ui/lib/locale/lang/en'

import VueMoment from 'vue-moment'
import VueResource from 'vue-resource'
import VueLodash from 'vue-lodash'


Vue.prototype.$c3 = c3

Vue.use(VueLodash, lodash)
Vue.use(ElementUI, { locale })
Vue.use(VueResource)
Vue.use(VueMoment, { moment })
Vue.use(Trend)
Vue.use(c3)


new Vue({
  el: '#app',
  render: h => h(App)
})
