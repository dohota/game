// 想要使用必须先引入 defineStore；
import { defineStore } from 'pinia';
// 这里我们使用的是es6 的模块化规范进行导出的。

// defineStore 方法有两个参数，第一个参数是模块化名字（也就相当于身份证一样，不能重复）

// 第二个参数是选项，对象里面有三个属性，相比于vuex 少了一个 mutations.
const useMainStore = defineStore('main', {
    state(){  // 存放的就是模块的变量
        return {
        
        }
    },
    getters:{ // 相当于vue里面的计算属性，可以缓存数据

    },
    actions:{ // 可以通过actions 方法，改变 state 里面的值。
        
    }
})

export default{
    /**
     * Vue.use调用函数
     * @param {*} app 
     */
    install:function(app: any){
        app.config.globalProperties.$store = useMainStore();
    },
}
