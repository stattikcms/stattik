<component name="TopNav">
<template>
<nav class="main-nav navbar is-primary" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <span style="font-size: 2em"><emojize>KFields :zap:</emojize></span>
    </a>
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">

      <a href="/post" class="navbar-item">
        Blog
      </a>

      <a href="/project" class="navbar-item">
        Projects
      </a>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          More
        </a>

        <div class="navbar-dropdown">
          <a href="/about" class="navbar-item">
            About
          </a>
          <a href="/contact" class="navbar-item">
            Contact
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
      <a href= "https://github.com/kfields" class="navbar-item">
        <span class="icon is-medium">
          <i class="fab fa-github fa-2x"></i>
        </span>
      </a>
    </div>
  </div>
</nav>
</template>

</component>