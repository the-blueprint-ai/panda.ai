<script>
import { mapGetters } from "vuex";
import {
  CardComponent,
  CardNumber,
  CardExpiry,
  CardCvv,
} from "@chargebee/chargebee-js-vue-wrapper";

export default {
  props: {
    modalId: String,
    country: String,
    subscriptionPeriod: String,
    planType: String,
  },
  data() {
    return {
      currentPage: 1,
      formFirstName: "",
      formLastName: "",
      formEmail: "",
      formAddress: "",
      formCity: "",
      formPostcode: "",
      formCountry: "",
      formNameOnCard: "",
      loading: false,
      token: "",
      error: "",
      classes: {
        focus: "focus",
        invalid: "invalid",
        empty: "empty",
        complete: "complete",
      },
      placeholder: {
        number: "4111 1111 1111 1111",
        cvv: "CVV",
        expiry: "MM / YY",
      },
      fonts: ['../assets/fonts/iosevka-regular.ttf'],
      styles: {
        base: {
          color: "#000000",
          fontWeight: "500",
          fontFamily: "Iosevka, Monaco",
          fontSize: "17px",

          ":focus": {
            color: "#424770",
          },

          "::placeholder": {
            color: "#ced4da",
          },

          ":focus::placeholder": {
            color: "#7b808c",
          },
        },

        invalid: {
          color: "#e41029",

          ":focus": {
            color: "#e44d5f",
          },
          "::placeholder": {
            color: "#FFCCA5",
          },
        },
      },
    };
  },
  mounted() {},
  created() {
    this.formFirstName = this.first_name;
    this.formLastName = this.last_name;
    this.formEmail = this.email;
    this.formNameOnCard = `${this.first_name} ${this.last_name}`;
  },
  computed: {
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
      email: "getStoreEmail",
      first_name: "getStoreFirstName",
      last_name: "getStoreLastName",
    }),
  },
  methods: {
    nextPage() {
      this.currentPage += 1;
    },
    previousPage() {
      this.currentPage -= 1;
    },
    goToPage(pageNumber) {
      this.currentPage = pageNumber;
    },
    tokenize() {
      this.loading = true;

      this.$refs.card
        .tokenize({})
        .then((data) => {
          this.loading = false;
          this.token = data.token;
          this.error = "";
        })
        .catch((error) => {
          this.loading = false;
          this.error = "Problem with your card details, please try again.";
          this.token = "";
        });
    },
    onSubmit(e) {
      e.preventDefault();
      this.$refs.cardComponent.tokenize().then((data) => {
        console.log("chargebee token", data.token);
      });
    },
    onChange(status) {
      let errors = {
        ...this.errors,
        [status.field]: status.error,
      };
      this.errors = errors;
      let { message } =
        Object.values(errors)
          .filter((message) => !!message)
          .pop() || {};
      this.errorMessage = message;
    },
    onFocus(event) {
      console.log(event.field, "focused");
    },
    onReady(el) {
      el.focus();
    },
  },
  components: {
    CardComponent,
    CardNumber,
    CardExpiry,
    CardCvv,
  },
};
</script>

<template>
  <div
    class="modal fade"
    id="subscriptionModal"
    tabindex="-1"
    aria-labelledby="subscriptionModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header text-bg-light d-flex flex-column">
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
          <h1>🐼</h1>
          <h1 class="text-primary">{{ planType.toUpperCase() }} PLAN</h1>
          <p class="mt-n2">Add your account details</p>
          <div class="circle-nav">
            <span
              v-for="n in 3"
              :key="n"
              :class="['circle', { 'circle-active': currentPage === n }]"
              @click="goToPage(n)"
            ></span>
          </div>
        </div>
        <div class="modal-body text-primary">
          <h2 v-if="planType == 'free'" class="">
            <span v-if="country == 'uk'">£</span
            ><span v-if="country == 'usa'">$</span>{{ planType.toUpperCase() }}
          </h2>
          <h2 v-if="planType == 'bao'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">2.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">29.99 per year</span>
          </h2>
          <h2 v-if="planType == 'mei'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">5.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">59.99 per year</span>
          </h2>
          <h2 v-if="planType == 'da'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">14.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">149.99 per year</span>
          </h2>
          <div class="text-primary mb-4" v-if="planType == 'free'">
            <p class="lh-1">20 messages</p>
            <p class="lh-1 mt-n2">ALL Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'bao'">
            <p class="lh-1">100 messages a month</p>
            <p class="lh-1 mt-n2">3 Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'mei'">
            <p class="lh-1">300 messages a month</p>
            <p class="lh-1 mt-n2">5 Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'da'">
            <p class="lh-1">1,000 messages a month</p>
            <p class="lh-1 mt-n2">ALL Integrations</p>
          </div>
          <div class="divider"></div>
          <div
            v-if="currentPage == 1"
            class="modalContentPage1 d-inline-flex align-items-center"
            style="height: 250px"
          >
            <form>
              <div class="d-flex">
                <div class="form-floating mt-4 mb-3" style="width: 48%">
                  <input
                    type="text"
                    class="form-control"
                    id="firstName"
                    placeholder="Po"
                    v-model="formFirstName"
                  />
                  <label for="firstName">First Name</label>
                </div>
                <div class="form-floating mt-4 mb-3 ms-3" style="width: 48%">
                  <input
                    type="text"
                    class="form-control"
                    id="lastName"
                    placeholder="Ping"
                    v-model="formLastName"
                  />
                  <label for="lastName">Last Name</label>
                </div>
              </div>
              <div class="form-floating mb-3">
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  placeholder="Po.Ping@mypanda.ai"
                  v-model="formEmail"
                />
                <label for="email">Email</label>
              </div>
            </form>
          </div>
          <div
            v-if="currentPage == 2"
            class="modalContentPage2 d-inline-flex align-items-center"
            style="height: 250px"
          >
            <form>
              <div class="form-floating mt-4 mb-3">
                <input
                  type="text"
                  class="form-control"
                  id="address"
                  placeholder="Address"
                  v-model="formAddress"
                />
                <label for="email">Address</label>
              </div>
              <div class="d-flex">
                <div class="form-floating mb-3" style="width: 48%">
                  <input
                    type="text"
                    class="form-control"
                    id="city"
                    placeholder="City"
                    v-model="formCity"
                  />
                  <label for="firstName">City</label>
                </div>
                <div class="form-floating mb-3 ms-3" style="width: 48%">
                  <input
                    type="text"
                    class="form-control"
                    id="postcode"
                    placeholder="Postcode"
                    v-model="formPostcode"
                  />
                  <label for="lastName">Postcode</label>
                </div>
              </div>
              <div class="form-floating mb-3">
                <select
                  class="form-select"
                  aria-label="Country"
                  v-model="formCountry"
                >
                  <option value="uk">United Kingdom</option>
                  <option value="usa">United States of America</option>
                </select>
                <label for="country">Country</label>
              </div>
            </form>
          </div>
          <div
            v-if="currentPage == 3"
            class="modalContentPage3 d-inline-flex align-items-center justify-content-center"
            style="height: 250px; min-width: 100%"
          >
            <div class="ex1-fieldset" style="min-width: 80%">
              <div class="form-floating">
                <input
                  class="form-control mb-3"
                  id="nameOnCard"
                  :class="{ val: formNameOnCard }"
                  type="text"
                  placeholder="Kung Fu Panda"
                  v-model="formNameOnCard"
                />
                <label for="nameOnCard">Name on Card</label>
              </div>
              <div class="d-flex flex-column px-2 pt-3 pb-3"  style="border: 1px solid #ced4da; border-radius: 5px">
                <!-- Render card components in fields-mode -->
                <!-- Pass styles, classes, locale, placeholder, fonts as props -->
                <CardComponent
                  ref="card"
                  class="fieldset fields"
                  :classes="classes"
                  :placeholder="placeholder"
                  :styles="styles"
                >
                </CardComponent>
              </div>
              <div class="error text-danger mt-4" role="alert" v-if="error">{{ error }}</div>
              <div class="token" v-if="token">{{ token }}</div>
            </div>
          </div>
        </div>
        <div class="modal-footer text-bg-light">
          <button
            v-if="currentPage > 1"
            type="button"
            class="btn btn-outline-primary"
            @click="previousPage"
            style="width: 100px"
          >
            PREVIOUS
          </button>
          <button
            v-if="currentPage == 1"
            type="button"
            class="btn btn-secondary"
            @click="nextPage"
            style="width: 100px"
          >
            NEXT
          </button>
          <button
            v-if="currentPage == 2"
            type="button"
            class="btn btn-secondary"
            @click="nextPage"
            style="width: 100px"
          >
            NEXT
          </button>
          <button
            v-if="currentPage == 3"
            type="submit"
            :class="{ submit: loading }"
            class="btn btn-secondary"
            @click="tokenize"
            style="width: 100px"
          >
            PAY
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.circle-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;
}
.circle {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #ccc;
  margin: 0 5px;
}
.circle:hover {
  cursor: pointer;
}
.circle-active {
  background-color: #333;
}
.divider {
  height: 1px;
  width: 100%;
  background-color: #ccc;
}
</style>
