import Vue from "vue";
import Router from "vue-router";
import AppHeader from "./layout/AppHeader";
import AppFooter from "./layout/AppFooter";
import Components from "./views/Components.vue";
import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Profile from "./views/Profile.vue";
import GeoLocation from "./views/GeoLocation.vue";
import FileManager from "./views/FileManager";
import ProductList from "./views/ProductList";

Vue.use(Router);

export default new Router({
    linkExactActiveClass: "active",
    mode: 'history',
    routes: [
        {
            path: "/",
            name: "landing",
            components: {
                header: AppHeader,
                default: Landing,
                footer: AppFooter
            }
        },
        {
            path: "/geolocation",
            name: "geolocation",
            components: {
                header: AppHeader,
                default: GeoLocation,
                footer: AppFooter
            }
        },
        {
            path: "/components",
            name: "components",
            components: {
                header: AppHeader,
                default: Components,
                footer: AppFooter
            }
        },
        {
            path: "/login",
            name: "login",
            components: {
                header: AppHeader,
                default: Login,
                footer: AppFooter
            }
        },
        {
            path: "/register",
            name: "register",
            components: {
                header: AppHeader,
                default: Register,
                footer: AppFooter
            }
        },
        {
            path: "/profile",
            name: "profile",
            components: {
                header: AppHeader,
                default: Profile,
                footer: AppFooter
            }
        },
        {
            path: "/filemanager",
            name: "filemanager",
            components: {
                // header: AppHeader,
                default: FileManager,
                footer: AppFooter
            }
        },
            {
            path: "/productlist",
            name: "productlist",
            components: {
                // header: AppHeader,
                default: ProductList,
                // footer: AppFooter
            }
        }
    ],
    scrollBehavior: to => {
        if (to.hash) {
            return {selector: to.hash};
        } else {
            return {x: 0, y: 0};
        }
    }
});
