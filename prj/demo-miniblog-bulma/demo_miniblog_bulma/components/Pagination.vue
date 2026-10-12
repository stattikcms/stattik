<template>
<nav class="pagination my-3" role="navigation" aria-label="pagination">
  <a v-if="self.paginator.page(self.number).has_previous()"
    href="{{self.paginator.page(self.number - 1).url}}"
    class="pagination-previous">
    Previous
  </a>
  <a v-if="self.paginator.page(self.number).has_next()"
    href="{{self.paginator.page(self.number + 1).url}}"
    class="pagination-next">
    Next page
  </a>
  <ul v-if="self.paginator.num_pages > 1" class="pagination-list">
    <li v-for="page in self.paginator.pages">
      <a href="{{page.url}}" class="pagination-link {{'is-current' if self.number == page.number else None}}" aria-label="Goto page 1">
        {{page.number}}
      </a>
    </li>
  </ul>
</nav>
</template>

<script type="text/python">
props = ['paginator', 'number']
</script>
