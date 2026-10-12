<template>
<nav class="main-nav navbar is-primary" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <span style="font-size: 2em"><emojize>Stattik :zap:</emojize></span>
    </a>
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">

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
      <a href= "/search" class="navbar-item">
        <span class="icon is-medium">
          <i class="fas fa-search fa-2x"></i>
        </span>
      </a>
      <a href= "https://github.com/stattikcms/stattik" class="navbar-item">
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
