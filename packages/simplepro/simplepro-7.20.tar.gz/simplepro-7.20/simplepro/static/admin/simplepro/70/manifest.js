function showManifest() {
    new Vue({
        data() {

            return {
                secretKey: getSecretKey(), domain: window.location.hostname, loading: false
            }
        }, methods: {
            async autoBind() {
                console.log('autoBind')
                this.loading = true
                //请求接口，判断是否有没有绑定域名的许可证
                let d = {
                    secretKey: this.secretKey, host: this.domain
                }
                try {
                    let res = await fetch('https://www.noondot.com/passport/automation', {
                        method: 'POST', body: JSON.stringify(d), headers: {
                            'Content-Type': 'application/json'  //如果写成contentType会报错
                        },
                    })
                    this.loading = false
                    let data = await res.json()
                    if (data.code !== "OK") {
                        //显示个错误提示
                        this.$message.error(data.msg)
                    } else {
                        //自动绑定成功
                        this.$message.success("自动绑定成功，2秒钟后自动刷新页面！")
                        setTimeout(() => {
                            window.location.reload()
                        }, 2000)
                    }

                } catch (e) {
                    console.warn(e)
                } finally {
                    this.loading = false
                }
            }
        }, el: '#app', template: `<div style="margin: 30px;">

<el-card>
    <div slot="header" class="clearfix">
        <span><i class="el-icon-error" style="color:red"></i> 授权提示</span>
    </div>
    <el-alert type="error">
        您的系统授权过期或者还没购买许可证，暂时无法使用，请联系前往<el-link href="//www.noondot.com/simplepro" target="_blank">https://www.noondot.com/simplepro</el-link>购买授权，谢谢您的支持与理解！
    </el-alert>
    <el-alert style="margin-top: 20px;font-size: 16px" type="success">
        <div>域名：<b>{{domain}}</b></div>
    </el-alert>
    <template v-if="secretKey">
        <el-alert style="margin-top: 20px;font-size: 16px" type="success">
            <div>SecretKey：{{secretKey}}</div>
            <div style="margin-top: 10px">您已经正确配置SecretKey，但是还没有绑定域名，请前往 <el-link href="https:////www.noondot.com" target="_blank">https://www.noondot.com</el-link> 绑定域名！</div>
            <div style="margin-top: 10px">
            点击头像->许可证管理->绑定域名
            </div>
            
            <div>
                如果您已经购买了许可证，可以点击按钮自动查询和绑定域名
                <el-button :disabled="loading" type="primary" @click="autoBind" v-loading="loading">自动绑定域名</el-button>
            </div>
        </el-alert>
    </template>
    <el-alert v-else style="margin-top: 20px;font-size: 16px" type="warning">
        <div>您还没有配置 SecretKey ，请在项目的 settings.py 任意处加入：</div>
        <div>SIMPLEPRO_SECRET_KEY = '您的账户秘钥'</div>
        <div>账户秘钥从<el-link href="//www.noondot.com" target="_blank">https://www.noondot.com</el-link>网站，登录后点击头像->许可证管理 处获取</div>
    </el-alert>
   
</el-card>
</div>`
    })
}

// showManifest();