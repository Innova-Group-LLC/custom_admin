<template>
  <div v-if="!item.hidden">
    <template v-if="hasSubsections(item)">
      <app-link v-if="!onlyOneChild.meta.viewname.detail" :to="resolvePath(onlyOneChild.path)">
        <el-menu-item :index="onlyOneChild.meta.key" :class="{'submenu-title-noDropdown': !isNest}">
          <item :title="onlyOneChild.meta.title" />
        </el-menu-item>
      </app-link>
    </template>

    <el-submenu
      v-else
      ref="subMenu"
      :index="`menu_${item.meta.key}`" popper-append-to-body
    >
      <template slot="title">
        <item :icon="item.meta.icon" :title="item.meta.title" v-if="item.meta && item.meta.icon" />
        <item :title="item.meta.title" v-else-if="item.meta" />
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="`submenu_${child.meta.key}`"
        :is-nest="true"
        :item="child"
        :base-path="resolvePath(child.path)"
        class="nest-menu"
      />
    </el-submenu>
  </div>
</template>

<script>
import path from 'path'
import { isExternal } from '@/utils/validate'
import Item from './Item'
import AppLink from './Link'
import FixiOSBug from './FixiOSBug'

export default {
  name: 'SidebarItem',
  components: { Item, AppLink },
  mixins: [FixiOSBug],
  props: {
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    this.onlyOneChild = null
    return {}
  },
  methods: {
    hasSubsections(item) {
      return this.hasOneShowingChild(item.children, item) && (!this.onlyOneChild.children || this.onlyOneChild.noShowingChildren) && !item.alwaysShow
    },
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          // Temp set(will be used if only has one showing child)
          this.onlyOneChild = item
          return true
        }
      })

      // When there is only one child router, the child router is displayed by default
      if (showingChildren.length === 1) {
        return true
      }

      // Show parent if there are no child router to display
      if (showingChildren.length === 0) {
        this.onlyOneChild = { ... parent, path: '', noShowingChildren: true }
        return true
      }

      return false
    },
    resolvePath(routePath) {
      if (isExternal(routePath)) {
        return routePath
      }
      if (isExternal(this.basePath)) {
        return this.basePath
      }
      return path.resolve(this.basePath, routePath)
    }
  }
}
</script>
