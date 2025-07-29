//注册一个Vue组件
Vue.component('captcha', {
    template: `
    <div class="captcha" style="display: flex;justify-content: space-between;align-items: center">
        <div class="captcha-input">
            <el-input type="text" name="captcha" v-model="value" required  :placeholder="placeholder" @keyup.enter.native="validate()"/>
        </div>
        <div class="captcha-img" @click="refresh()" style="cursor: pointer">
            <img :src="url" />
        </div>
    </div>
    `,
    props: {
        src: {
            type: String,
            required: true
        },
        placeholder: {
            type: String,
            default: 'Code'
        },
        msg: {
            type: String,
            default: 'Please enter the verification code'
        }
    },
    data() {
        return {
            url: this.src,
            value: ''
        }
    },
    methods: {
        refresh() {
            this.url = this.src + '?' + Math.random();
        },
        validate() {

            if (this.value.trim() === '') {
                this.$message.error(this.msg);
                return false;
            }

            loginApp.login();
        }
    },
    created() {
        window.validate = this.validate;
    }
})

Vue.component('captcha-msg', {
    data() {

        let msg = null
        if (window.messages && window.messages.length > 0) {
            msg = window.messages[0]
        }
        return {
            msg,
        }
    },
    template: `<el-alert style="margin-top: 5px" v-if="msg!==null" type="error" :closable="false" show-icon><span  v-text="msg.msg"></span></el-alert>`
})