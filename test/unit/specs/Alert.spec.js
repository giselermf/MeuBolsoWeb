import Vue from 'vue'
import Hello from '@/components/Alert'

describe('Hello.vue', () => {
    it('should render correct contents', () => {
      console.log('hi there');
      const Constructor = Vue.extend(Hello)
      const vm = new Constructor().$mount()
      expect(vm.$el.querySelector('.hello h1').textContent)
        .to.equal('Welcome to Your Vue.js App')
    })
  })