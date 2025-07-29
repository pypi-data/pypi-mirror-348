Vue.component('remember-me', {
    template: "#remember_me_template",
    data() {
        return {
            checked: false
        }
    },
    methods: {
        save() {
            localStorage.setItem("checked", this.checked)
            if (this.checked) {
                localStorage.setItem("username", this.$parent.username)
                localStorage.setItem("password", this.$parent.password)
            } else {
                localStorage.removeItem("username")
                localStorage.removeItem("password")
            }
        }
    },
    watch: {
        //监听checked
        checked(newVal, oldVal) {
            this.save()
        },
        //监听父级的username和password
        "$parent.username"(newVal, oldVal) {
            this.save()
        },
        "$parent.password"(newVal, oldVal) {
            this.save()
        }
    },
    mounted() {
        this.checked = localStorage.getItem("checked") === "true"
        if (this.checked) {
            this.$parent.username = localStorage.getItem("username")
            this.$parent.password = localStorage.getItem("password")
        }
    },
});