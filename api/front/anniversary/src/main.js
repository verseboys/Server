// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import { Button,Row,Col,Input,Pagination,Modal,Checkbox, Icon,Alert} from 'ant-design-vue';
import './common/styles.less';

import "animate.css";



[ Button,
  Row,
  Col,
  Input,
  Pagination,
  Modal,
  Checkbox,
  Input.TextArea,
  Icon,
  Alert
].map(Comp => {
  Vue.component(Comp.name, Comp)
});


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
