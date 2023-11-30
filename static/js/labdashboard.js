// START COMPONENT
const startComp = Vue.component({
  // DELIMITER
  delimiters: ["{[", "]}"],

  // TEMPLATE
  template: `
  <div>
    <div>
      <div>
        <!-- Logo -->
      </div>
      <div>
        <router-link to="/lab-admin-signup">
            <button>Laboratory</button>
        </router-link>
          <router-link to="/lab-admin-signup">
              <button>Laboratory</button>
          </router-link>
      </div>
    <div>
      <h2>Your bookings</h2>
    </div>
    <div>
    </div>
  </div>
  `,

  // DATA
  data: function () {
    return {
      bookings: [],
    };
  },

  // DATA FROM APIs
  computed: {
    fill_bookings: function () {
      const bookings_url = "http://" + window.location.host + "/bookings-api";
      fetch(bookings_url, {
        method: "GET",
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          this.bookings = data;
        })
        .catch((error) => {
          console.log("error");
        });
    },
  },
});

// App routes
const routes = [
  {
    path: "/dashboard",
    component: startComp,
  },
];

// Router
const router = new VueRouter({
  routes: routes,
});

// FARMER DASHBOARD APP
app = new Vue({
  delimiters: ["{[", "]}"],
  el: "#app",
  router: router,
  data: {
    message: "Vue",
  },
});
