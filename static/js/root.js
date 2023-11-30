// Home
const startComp = Vue.component("startComp", {
  // Delimiters
  delimiters: ["{[", "]}"],
  // Template
  template: `
    <div>
        <div v-if="loading">
            <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
        </div>
        <div v-else>
        <!-- Navigation bar with title, login and signup -->
            <div>
                <div>
                 <!-- Logo to be done -->
                </div>
                <div>
                    <router-link to="/signup">
                        <button>Signup</button>
                    </router-link>
                </div>
                <div>
                    <router-link to="/login">
                        <button>Login</button>
                    </router-link>
                </div>
            </div>
            <div>
            <!-- About -->
                <div>
                    <!-- Farmer info -->
                </div>
                <div>
                    <!-- Lab info -->
                </div>
                <div>
                    <!-- Market user info -->
                </div>
            </div>
        </div>
    </div>
    `,
  // Data
  data: function () {
    return {
      loading: false,
    };
  },
});

// Signup Component
const signupComp = Vue.component("signupComp", {
  // Delimiters
  delimiters: ["{[", "]}"],
  // Template
  template: `
    <div>
        <div v-if="loading">
            <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
        </div>
        <div v-else>
            <div>
                <router-link to="/farmer-signup">
                    <button>Farmer</button>
                </router-link>
            </div>
            <div>
                <router-link to="/market-buyer-signup">
                    <button>Buyer</button>
                </router-link>
            </div>
            <div>
                <router-link to="/lab-admin-signup">
                    <button>Laboratory</button>
                </router-link>
            </div>
        </div>
    </div>
    `,
  // DATA
  data: function () {
    return {
      loading: false,
    };
  },
});

// FARMER SIGNUP
const farmerSignupComp = Vue.component("farmerSignupComp", {
  // DELIMITERS
  delimiters: ["{[", "]}"],
  // TEMPLATE
  template: `
    <div>
        <div v-if="loading">
            <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
        </div>
        <div v-else>
            <div>
                <label for = "farmer-signup-name">Name</label>
                <input v-model = "name" type = "text" id = "farmer-signup-name" required>
            </div>
            <div>
                <label for = "farmer-signup-phone">Phone</label>
                <input v-model = "phone" type = "text" id = "farmer-signup-phone" required>
            </div>
            <div>
                <label for = "farmer-signup-email">E-mail</label>
                <input v-model = "email" type = "text" id = "farmer-signup-email">
            </div>
            <div>
                <label for = "farmer-signup-address">Address</label>
                <input v-model = "address" type = "text" id = "farmer-signup-address" required>
            </div>
            <div>
                <label for = "farmer-signup-password">Password</label>
                <input v-model = "password" type = "password" id = "farmer-signup-password" required>
            </div>
            <button @click = submit()>Signup</button>
            <br />
            <router-link to = "/login">
                <button>Login</button>
            </router-link>
            <p v-if = "phone_number_in_use">Phone number already in use.</p>
            <p v-if = "email_in_use">Email in use.</p>
            <p v-if = "invalid_email"<Invalid Email</p>
            <p v-if = "invalid_phone">Invalid phone number.</p>
            <p v-if = "invalid_name">Invalid name.</p>
            <p v-if = "invalid_password">Invalid password.</p>
        </div>
      </div>
    `,
  // DATA
  data: function () {
    return {
      phone_number_in_use: false,
      email_in_use: false,
      invalid_email: false,
      invalid_phone: false,
      invalid_name: false,
      invalid_password: false,
      loading: false,
      name: "",
      phone: "",
      email: "",
      address: "",
      password: "",
    };
  },
  methods: {
    // Phone and Email checks
    checkMail: function (mail) {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
        return true;
      } else {
        alert("invalid email address");
        return false;
      }
    },
    checkPhone: function (phone) {
      if (phone.length == 10 && !isNaN(phone)) {
        return true;
      }
      return false;
    },
    submit: function () {
      // Validation APIs
      const signup_validate_url =
        "http://" + window.location.host + "/signup-validate-api";
      const dashboard_url = "http://" + window.location.host + "/dashboard";

      // Checks
      if (!this.checkMail(this.email)) {
        this.invalid_email = true;
        if (this.email.length > 0) {
          return;
        }
      }
      if (!this.checkPhone(this.phone)) {
        this.invalid_phone = true;
        return;
      }
      if (this.password.length < 8) {
        this.invalid_password = true;
        return;
      }
      if (this.name.length < 8) {
        this.invalid_name = true;
        return;
      }
      fetch(signup_validate_url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          phone: this.phone,
          name: this.name,
          email: this.email,
          address: this.address,
        },
      })
        .then((response) => {
          if (!response.ok) {
            console.log("Response not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (
            data["valid_phone"] &&
            data["valid_email"] &&
            data["valid_address"] &&
            data["valid_name"]
          ) {
            fetch(signup_validate_url, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                name: this.name,
                address: this.address,
                phone: this.phone,
                password: this.password,
                email: this.email,
                role: "FARMER",
                context: "SIGNUP",
              }),
            })
              .then((response) => {
                console.log("Response not ok");
                return response.json();
              })
              .then((data) => {
                if (data["success"]) {
                  this.setCookie("auth-token", data["auth-token"], 12);
                  window.location.href = dashboard_url;
                }
              });
          }
        })
        .catch((error) => {
          console.log(error);
        });
      this.loading = false;
    },
    setCookie: function (cname, cvalue, exhours) {
      const d = new Date();
      d.setTime(d.getTime() + exhours * 60 * 60 * 1000);
      let expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
});

// USER SIGNUP COMPONENT
const marketBuyerSignupComp = Vue.component("marketBuyerSignupComp", {
  //DELIMITERS
  delimiters: ["{[", "]}"],
  // TEMPLATE
  template: `
    <div>
        <div v-if="loading">
            <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
        </div>
        <div v-else>
            <div>
                <label for = "user-signup-name">Name</label>
                <input v-model = "name" type = "text" id = "user-signup-name" required>
            </div>
            <div>
                <label for = "user-signup-phone">Phone</label>
                <input v-model = "phone" type = "text" id = "user-signup-phone" required>
            </div>
            <div>
                <label for = "user-signup-email">E-mail</label>
                <input v-model = "email" type = "text" id = "user-signup-email">
            </div>
            <div>
                <label for = "user-signup-address">Address</label>
                <input v-model = "address" type = "text" id = "user-signup-address" required>
            </div>
            <div>
                <label for = "user-signup-password">Password</label>
                <input v-model = "password" type = "password" id = "user-signup-password" required>
            </div>
            <button @click = submit()>Signup</button>
            <br />
            <router-link to = "/login">
                <button>Login</button>
            </router-link>
            <p v-if = "phone_number_in_use">Phone number already in use.</p>
            <p v-if = "email_in_use">Email in use.</p>
            <p v-if = "invalid_email"<Invalid Email</p>
            <p v-if = "invalid_phone">Invalid phone number.</p>
        </div>
      </div>
    `,
  // DATA
  data: function () {
    return {
      loading: false,
      phone_number_in_use: false,
      email_in_use: false,
      invalid_email: false,
      invalid_phone: false,
      name: "",
      phone: "",
      email: "",
      address: "",
      password: "",
    };
  },

  // METHODS
  methods: {
    // Phone and Email checks
    checkMail: function (mail) {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
        return true;
      } else {
        alert("invalid email address");
        return false;
      }
    },
    checkPhone: function (phone) {
      if (phone.length == 10 && !isNaN(phone)) {
        return true;
      }
      return false;
    },
    submit: function () {
      // Validation APIs
      const signup_validate_url =
        "http://" + window.location.host + "/signup-validate-api";
      const dashboard_url = "http://" + window.location.host + "/dashboard";

      // Checks
      if (!this.checkMail(this.email)) {
        this.invalid_email = true;
        if (this.email.length > 0) {
          return;
        }
      }
      if (!this.checkPhone(this.phone)) {
        this.invalid_phone = true;
        return;
      }
      if (this.password.length < 8) {
        this.invalid_password = true;
        return;
      }
      if (this.name.length < 8) {
        this.invalid_name = true;
        return;
      }
      fetch(signup_validate_url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          phone: this.phone,
          name: this.name,
          email: this.email,
          address: this.address,
        },
      })
        .then((response) => {
          if (!response.ok) {
            console.log("Response not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (
            data["valid_phone"] &&
            data["valid_email"] &&
            data["valid_address"] &&
            data["valid_name"]
          ) {
            fetch(signup_validate_url, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                name: this.name,
                address: this.address,
                phone: this.phone,
                password: this.password,
                email: this.email,
                role: "MARKET_BUYER",
                context: "SIGNUP",
              }),
            })
              .then((response) => {
                console.log("Response not ok");
                return response.json();
              })
              .then((data) => {
                if (data["success"]) {
                  this.setCookie("auth-token", data["auth-token"], 12);
                  window.location.href = dashboard_url;
                }
              });
          }
        })
        .catch((error) => {
          console.log(error);
        });
      this.loading = false;
    },
    setCookie: function (cname, cvalue, exhours) {
      const d = new Date();
      d.setTime(d.getTime() + exhours * 60 * 60 * 1000);
      let expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
});

// LAB ADMIN SIGNUP COMPONENT
const labSignupComp = Vue.component("labSignupComp", {
  delimiters: ["{[", "]}"],
  // TEMPLATE
  template: `
    <div>
        <div v-if="loading">
            <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
        </div>
        <div v-else>
            <div>
                <label for = "user-signup-name">Name</label>
                <input v-model="name" type = "text" id = "user-signup-name" required>
            </div>
            <div>
                <label for = "user-signup-phone">Phone</label>
                <input v-model="phone" type = "text" id = "user-signup-phone" required>
            </div>
            <div>
                <label for = "user-signup-email">E-mail</label>
                <input v-model="email" type = "text" id = "user-signup-email">
            </div>
            <div>
                <label for = "user-signup-address">Address</label>
                <input v-model = "address" type = "text" id = "user-signup-address" required>
            </div>
            <div>
                <label for = "user-signup-password">Password</label>
                <input v-model="password" type = "password" id = "user-signup-password" required>
            </div>
            <button @click = submit()>Signup</button>
            <br />
            <router-link to = "/login">
                <button>Login</button>
            </router-link>
            <p v-if = "phone_number_in_use">Phone number already in use.</p>
            <p v-if = "email_in_use">Email in use.</p>
            <p v-if = "invalid_email"<Invalid Email</p>
            <p v-if = "invalid_phone">Invalid phone number.</p>
        </div>
      </div>
    `,
  // DATA
  data: function () {
    return {
      loading: false,
      phone_number_in_use: false,
      email_in_use: false,
      invalid_email: false,
      invalid_phone: false,
      name: "",
      phone: "",
      email: "",
      address: "",
      password: "",
    };
  },

  // METHODS
  methods: {
    // Phone and Email checks
    checkMail: function (mail) {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
        return true;
      } else {
        alert("invalid email address");
        return false;
      }
    },
    checkPhone: function (phone) {
      if (phone.length == 10 && !isNaN(phone)) {
        return true;
      }
      return false;
    },
    submit: function () {
      // Validation APIs
      const signup_validate_url =
        "http://" + window.location.host + "/signup-validate-api";
      const dashboard_url = "http://" + window.location.host + "/dashboard";

      // Checks
      if (!this.checkMail(this.email)) {
        this.invalid_email = true;
        if (this.email.length > 0) {
          return;
        }
      }
      console.log("correct email");
      if (!this.checkPhone(this.phone)) {
        this.invalid_phone = true;
        return;
      }
      console.log("correct phone");
      if (this.password.length < 8) {
        this.invalid_password = true;
        return;
      }
      if (this.name.length < 5) {
        this.invalid_name = true;
        return;
      }
      fetch(signup_validate_url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          phone: this.phone,
          name: this.name,
          email: this.email,
          address: this.address,
        },
      })
        .then((response) => {
          if (!response.ok) {
            console.log("Response not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (
            data["valid_phone"] &&
            data["valid_email"] &&
            data["valid_address"] &&
            data["valid_name"]
          ) {
            fetch(signup_validate_url, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                name: this.name,
                address: this.address,
                phone: this.phone,
                password: this.password,
                email: this.email,
                role: "LAB_ADMIN",
                context: "SIGNUP",
              }),
            })
              .then((response) => {
                console.log("Response not ok");
                return response.json();
              })
              .then((data) => {
                console.log(data);
                if (data["success"]) {
                  console.log(data["auth-token"]);
                  this.setCookie("auth-token", data["auth-token"], 12);
                  window.location.href = dashboard_url;
                }
              });
          }
        })
        .catch((error) => {
          console.log(error);
        });
      this.loading = false;
    },
    setCookie: function (cname, cvalue, exhours) {
      const d = new Date();
      d.setTime(d.getTime() + exhours * 60 * 60 * 1000);
      let expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
});

// LOGIN COMPONENT
const loginComp = Vue.component("login", {
  // DELIMITERS
  delimiters: ["{[", "]}"],

  // TEMPLATE
  template: `
  <div>
    <div v-if="loading">
      <img src = "static/img/loader.gif" alt = "Page loading" width = "150" height = "150">
    </div>
    <div v-else>
      <div>
          <label for = "login-phone">Phone</label>
          <input v-model = "phone" type = "text" id = "login-phone" required>
      </div>
      <div>
          <label for = "login-password">Password</label>
          <input v-model = "password" type = "password" id = "login-password" required>
      </div>
      <button @click = submit()>Login</button>
      <p v-if = "phone_doesnot_exist">User doesn't exist</p>
      <p v-if = "wrong_password">Wrong password</p>
    </div>
  </div>
  `,
  // DATA
  data: function () {
    return {
      loading: false,
      phone: "",
      password: "",
      phone_doesnot_exist: false,
      wrong_password: false,
    };
  },

  // METHODS
  methods: {
    checkPhone: function (phone) {
      if (phone.length == 10 && !isNaN(phone)) {
        return true;
      }
      return false;
    },
    submit: function () {
      // API URLs
      const login_validate_url =
        "http://" + window.location.host + "/login-validate-api";
      const dashboard_url = "http://" + window.location.host + "/dashboard";

      // Check for valid phone number
      if (this.checkPhone(this.phone)) {
        this.loading = true;
        fetch(login_validate_url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            phone: this.phone,
          },
        })
          .then((response) => {
            if (!response.ok) {
              console.log("Response not ok");
            }
            return response.json();
          })
          .then((data) => {
            if (data["valid_phone"]) {
              fetch(login_validate_url, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  phone: this.phone,
                  password: this.password,
                  context: "LOGIN",
                }),
              })
                .then((response) => {
                  console.log("Response not ok");
                  return response.json();
                })
                .then((data) => {
                  if (data["success"]) {
                    this.setCookie("auth-token", data["auth-token"], 6);
                    window.location.href = dashboard_url;
                  }
                });
            }
          })
          .catch((error) => {
            console.log(error);
          });
        this.loading = false;
      }
    },
    setCookie: function (cname, cvalue, exhours) {
      const d = new Date();
      d.setTime(d.getTime() + exhours * 60 * 60 * 1000);
      let expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
});

// App routes
const routes = [
  {
    path: "/",
    component: startComp,
  },
  {
    path: "/signup",
    component: signupComp,
  },
  {
    path: "/market-buyer-signup",
    component: marketBuyerSignupComp,
  },
  {
    path: "/farmer-signup",
    component: farmerSignupComp,
  },
  {
    path: "/lab-admin-signup",
    component: labSignupComp,
  },
  {
    path: "/login",
    component: loginComp,
  },
  {
    path: "/*",
    componenet: startComp,
  },
];

// Router
const router = new VueRouter({
  routes: routes,
});

// App
app = new Vue({
  delimiters: ["{[", "]}"],
  el: "#app",
  router: router,
  data: {
    message: "Vue",
  },
});
