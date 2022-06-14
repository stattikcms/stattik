<component name="TopNav">
<template>
<nav class="main-nav navbar is-primary" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <!--<span style="font-size: 2em"><emoji /></span>-->
      <span style="font-size: 2em"><emojize>Markblocks :ice_cube:</emojize></span>
    </a>
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">

      <a href="/news" class="navbar-item">
        News
      </a>

      <a href="/docs" class="navbar-item">
        Docs
      </a>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          More
        </a>

        <div class="navbar-dropdown">
          <a class="navbar-item">
            About
          </a>
          <a class="navbar-item">
            Jobs
          </a>
          <a class="navbar-item">
            Contact
          </a>
          <hr class="navbar-divider" />
          <a class="navbar-item">
            Report an issue
          </a>
        </div>
      </div>
    </div>

    <div class="navbar-end">
      <a href="https://github.com/stattikcms/stattik" class="navbar-item">
        <span class="icon is-medium">
          <i class="fab fa-github fa-2x"></i>
        </span>
      </a>

    </div>
  </div>
</nav>
</template>

<!-- <script type="text/python">
Emoji = Vue.resolve('src/components/Emoji')

components = {
  'Emoji': Emoji,
}
</script> -->

</component>