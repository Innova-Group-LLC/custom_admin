<template>
  <div class="toolbar">
    <el-dropdown>
      <el-icon style="margin-right: 8px; margin-top: 1px">
        <setting />
      </el-icon>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>View</el-dropdown-item>
          <el-dropdown-item>Add</el-dropdown-item>
          <el-dropdown-item>Delete</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <span>Tom</span>
  </div>
</template>

<script>

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
    langs: {type: Object, required: true},
  },
}
</script>
