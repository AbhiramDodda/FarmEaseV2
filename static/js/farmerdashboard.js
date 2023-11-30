// SOIL CARE COMPONENT
const soil_care = Vue.component("soil_care", {
  // DELIMITERS
  delimiters: ["{[", "]}"],

  // TEMPLATE
  template: `
  <div>
    <div>
      <ul>
        <li v-for="lab in labs_available">
          <div>
            <h3>{[ lab.name ]}</h3>
            <p>{[ lab.phone ]}</p>
            {[ lab.email ]}
            <p>{[ lab.address ]}</p>
          </div>
          <div>
            <button @click=book({[ lab.user_id ]})>Book</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
  `,
  // DATA
  data: function () {
    return {
      labs_available: [],
    };
  },

  // METHODS
  methods: {
    book: function (lab_id) {},
  },

  // MOUNTED
  mounted: function () {
    fetch("http://" + window.location.host + "/bookings-api", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.labs_available = data["labs"];
      });
  },
});

// START COMPONENT
const startComp = Vue.component("startComp", {
  // DELIMITER
  delimiters: ["{[", "]}"],

  // TEMPLATE
  template: `
  <div>
    <div>
      <h2>Your crops</h2>
      <div v-if="adding_crop">
        <div>
          <label for="crop_name">Crop</label>
          <select v-model="crop_name" id="crop_name">
            <option value="rice">Rice</option>
            <option value="wheat">Wheat</option>
            <option value="tomato">Tomato</option>
            <option value="brinjal">Brinjal</option>
          </select>
          <button @click = submit()>Add</button>
        </div>
      </div>
      <div>
        <ul>
          <li v-for="crop in crops">
            <div>
              {[ crop.crop_name ]}
              {[ crop.predicted_max_month ]}
            </div>
          </li>
        </ul>
      </div>
      <div>
        <button v-on:click="add_crop">Add Crop</button>
      </div>
    </div>
  </div>
  `,

  // DATA
  data: function () {
    return {
      crops: [],
      adding_crop: false,
      crop_name: "",
      crop_exists: false,
    };
  },

  // MOUNTED
  mounted: function () {
    fetch("http://" + window.location.host + "/crops-api", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.crops = data["crops"];
        console.log(data["crops"]);
      });
  },

  // METHODS
  methods: {
    add_crop: function () {
      this.adding_crop = true;
    },
    submit: function () {
      this.adding_crop = false;
      fetch("http://" + window.location.host + "/crops-api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          crop_name: this.crop_name,
        }),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data["crop_exists"]) {
            alert("Crop already exists");
          } else {
            this.get_crops();
          }
        });
    },
    get_crops: function () {
      fetch("http://" + window.location.host + "/crops-api", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          this.crops = data["crops"];
          console.log(data["crops"]);
        });
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
    path: "/soil-care",
    component: soil_care,
  },
];

// ROUTER
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
