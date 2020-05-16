<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
<!--                <img src="img/brand/white.png" alt="logo">-->
                Geo-Maps
            </router-link>

            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="#">
                        <img src="img/brand/blue.png">
                    </a>
                </div>
                <div class="col-6 collapse-close">
                    <close-button @click="closeMenu"></close-button>
                </div>
            </div>

            <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
                <base-dropdown tag="li" class="nav-item">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <i class="ni ni-collection d-lg-none"></i>
                        <span class="nav-link-inner--text">Apps</span>
                    </a>
                                        <router-link to="/geolocation" class="dropdown-item">Geo Location</router-link>
<!--                    <router-link to="/profile" class="dropdown-item">Profile</router-link>-->
<!--                    <router-link to="/login" class="dropdown-item">Login</router-link>-->
<!--                    <router-link to="/register" class="dropdown-item">Register</router-link>-->
<!--                    <router-link to="/components" class="dropdown-item">Components</router-link>-->
                </base-dropdown>
            </ul>
            <ul class="navbar-nav align-items-lg-center ml-lg-auto">
<!--                <li class="nav-item">-->
<!--                    <a class="nav-link nav-link-icon" href="https://www.facebook.com/creativetim" target="_blank" rel="noopener"-->
<!--                       data-toggle="tooltip" title="Like us on Facebook">-->
<!--                        <i class="fa fa-facebook-square"></i>-->
<!--                        <span class="nav-link-inner&#45;&#45;text d-lg-none">Facebook</span>-->
<!--                    </a>-->
<!--                </li>-->
<!--                <li class="nav-item">-->
<!--                    <a class="nav-link nav-link-icon" href="https://www.instagram.com/creativetimofficial"-->
<!--                       target="_blank" rel="noopener" data-toggle="tooltip" title="Follow us on Instagram">-->
<!--                        <i class="fa fa-instagram"></i>-->
<!--                        <span class="nav-link-inner&#45;&#45;text d-lg-none">Instagram</span>-->
<!--                    </a>-->
<!--                </li>-->
<!--                <li class="nav-item">-->
<!--                    <a class="nav-link nav-link-icon" href="https://twitter.com/creativetim" target="_blank" rel="noopener"-->
<!--                       data-toggle="tooltip" title="Follow us on Twitter">-->
<!--                        <i class="fa fa-twitter-square"></i>-->
<!--                        <span class="nav-link-inner&#45;&#45;text d-lg-none">Twitter</span>-->
<!--                    </a>-->
<!--                </li>-->
                <li class="nav-item">
                    <a class="nav-link nav-link-icon" href="https://github.com/elvinos"
                       target="_blank" rel="noopener" data-toggle="tooltip" title="Star us on Github">
                        <i class="fa fa-github"></i>
                        <span class="nav-link-inner--text d-lg-none">Github</span>
                    </a>
                </li>
            </ul>
        </base-nav>
    </header>
</template>
<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";

export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown
  }
};
</script>
<style>
</style>
